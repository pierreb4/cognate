#!/usr/bin/env python3
"""Parse the cognate corpus, validate it, emit data/graph.json.

Edges are declared once, on the technique (`addresses:`). The reverse edge onto
the capability is derived here, so the forward and reverse directions of the
pattern language cannot disagree.

    build_graph.py                 validate + emit + print the gap report
    build_graph.py --from <id>     forward:  requirement -> techniques / bundles
    build_graph.py --to <id>       reverse:  technique   -> capabilities it bears on
    build_graph.py --profile <id>  screen every technique against a deployment
    build_graph.py --pairs         list the untyped co-coverage pairs in full
"""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FACULTY_ROOTS = {"exploration", "modeling", "goal-setting",
                 "planning-execution", "priors", "prior"}
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)

STRENGTH = {"direct": 3, "partial": 2, "incidental": 1}
# Symmetric relations are declared once, on the alphabetically-first technique id;
# the reverse is derived here, exactly as `addresses:` is.
SYMMETRIC = {"overlaps", "composes", "conflicts"}
ASYMMETRIC = {"subsumes": "subsumed_by", "supplies": "supplied_by"}
INTERACTIONS = SYMMETRIC | set(ASYMMETRIC)


def preconditions():
    """The closed token vocabulary a technique's `requires:` may cite."""
    doc = yaml.safe_load((ROOT / "data" / "preconditions.yaml").read_text())
    return {t["token"]: t for t in doc["tokens"]}


def load():
    nodes, errors = {}, []
    for d in ("patterns", "techniques", "bundles", "profiles"):
        for path in sorted((ROOT / d).rglob("*.md")):
            m = FM.match(path.read_text())
            if not m:
                errors.append(f"{path.relative_to(ROOT)}: no frontmatter")
                continue
            try:
                fm = yaml.safe_load(m.group(1))
            except yaml.YAMLError as e:
                errors.append(f"{path.relative_to(ROOT)}: bad YAML: {e}")
                continue
            if not fm or "id" not in fm:
                errors.append(f"{path.relative_to(ROOT)}: missing id")
                continue
            if fm["id"] in nodes:
                errors.append(f"{path.relative_to(ROOT)}: duplicate id {fm['id']}")
                continue
            fm["_path"] = str(path.relative_to(ROOT))
            nodes[fm["id"]] = fm
    return nodes, errors


WARNINGS = []


def validate(nodes, errors, tokens):
    def resolves(ref):
        return ref in nodes or ref in FACULTY_ROOTS

    def strength_on(tid, cap):
        for e in nodes.get(tid, {}).get("addresses", []):
            if e.get("capability") == cap:
                return e.get("strength")
        return None

    declared = set()
    for nid, n in nodes.items():
        where = n["_path"]
        for ref in n.get("part_of", []) + n.get("completed_by", []):
            if not resolves(ref):
                errors.append(f"{where}: unresolved reference {ref!r}")

        if n.get("kind") == "technique":
            for e in n.get("addresses", []):
                if not resolves(e.get("capability", "")):
                    errors.append(f"{where}: addresses unknown capability {e.get('capability')!r}")
            for r in n.get("requires", []):
                if not isinstance(r, dict) or "token" not in r:
                    errors.append(f"{where}: requires entry is prose, not a token: {r!r}")
                elif r["token"] not in tokens:
                    errors.append(f"{where}: unknown precondition token {r['token']!r} "
                                  f"(add it to data/preconditions.yaml or reuse one)")

            for x in n.get("interacts", []):
                other, rel, on = x.get("technique"), x.get("rel"), x.get("scope")
                if rel not in INTERACTIONS:
                    errors.append(f"{where}: unknown interaction {rel!r}")
                    continue
                if other == nid or nodes.get(other, {}).get("kind") != "technique":
                    errors.append(f"{where}: interacts target {other!r} is not another technique")
                    continue
                key = (min(nid, other), max(nid, other), rel, on)
                if key in declared:
                    errors.append(f"{where}: interaction {rel} with {other} on {on} declared twice")
                declared.add(key)
                if rel in SYMMETRIC and nid > other:
                    errors.append(f"{where}: symmetric '{rel}' must be declared on {other} "
                                  f"(the alphabetically-first id); the reverse is derived")
                if rel == "supplies":
                    if on not in tokens:
                        errors.append(f"{where}: supplies must name a precondition token, got {on!r}")
                    elif on not in [r.get("token") for r in nodes[other].get("requires", [])]:
                        errors.append(f"{where}: {other} does not require {on!r}, so it cannot be supplied")
                elif rel != "conflicts":
                    mine, theirs = strength_on(nid, on), strength_on(other, on)
                    if mine is None or theirs is None:
                        errors.append(f"{where}: '{rel}' on {on!r} but "
                                      f"{'this node' if mine is None else other} does not address it")
                    elif rel == "subsumes" and STRENGTH[mine] <= STRENGTH[theirs]:
                        errors.append(f"{where}: subsumes {other} on {on} but its strength "
                                      f"'{mine}' is not greater than '{theirs}'")
                if rel == "composes" and not x.get("evidence"):
                    errors.append(f"{where}: 'composes' claims the combination adds coverage — "
                                  f"cite a source measuring it, or use 'overlaps'")

            no_abs = n.get("no_absolute_score", False)
            kinds = set()
            for ev in n.get("evidence", []):
                kinds.add(ev.get("kind"))
                for field in ("split", "regime", "source", "stars"):
                    if not ev.get(field):
                        errors.append(f"{where}: evidence missing {field!r}: {ev.get('claim')!r}")
                stars = ev.get("stars", 0)
                if not isinstance(stars, int) or not 1 <= stars <= 4:
                    errors.append(f"{where}: stars must be 1-4, got {stars!r}")
                elif stars > 2 and ev.get("kind") != "measured":
                    errors.append(f"{where}: stars>2 requires kind 'measured': {ev.get('claim')!r}")
                if not ev.get("date"):
                    WARNINGS.append(f"{where}: evidence has no date (needed for trend views): {ev.get('claim')!r}")
                if no_abs and "%" in str(ev.get("claim", "")):
                    errors.append(f"{where}: no_absolute_score set but claim carries a %")
            # rule 4 lint: a caveat that disputes a claim needs the claim on the record
            caveats = " ".join(n.get("caveats", [])).lower()
            if ("claim" in caveats or "unsupported" in caveats) and "claimed" not in kinds:
                errors.append(f"{where}: caveats dispute a claim, but no evidence entry of kind 'claimed'")

        if n.get("kind") == "profile":
            seen = set()
            for s in n.get("supplies", []):
                tok, level = s.get("token"), s.get("level")
                if tok not in tokens:
                    errors.append(f"{where}: unknown precondition token {tok!r}")
                elif tok in seen:
                    errors.append(f"{where}: token {tok!r} declared twice")
                seen.add(tok)
                if level not in ("full", "partial", "none"):
                    errors.append(f"{where}: {tok}: level must be full/partial/none, got {level!r}")
                if s.get("binding") not in ("competition", "project"):
                    errors.append(f"{where}: {tok}: binding must be 'competition' or 'project'")
                if tokens.get(tok, {}).get("kind") == "assumption":
                    errors.append(f"{where}: {tok!r} is an assumption — it can be checked, "
                                  f"not supplied; drop it from `supplies:`")
            for tok, spec in tokens.items():
                if spec["kind"] != "assumption" and tok not in seen:
                    WARNINGS.append(f"{where}: no position on {tok!r} — the screen will "
                                    f"treat it as unavailable")
            for c in n.get("requires_capabilities", []):
                if not resolves(c.get("capability", "")):
                    errors.append(f"{where}: requires unknown capability {c.get('capability')!r}")
                if c.get("criticality") not in ("required", "useful"):
                    errors.append(f"{where}: {c.get('capability')}: criticality must be "
                                  f"'required' or 'useful'")

        if n.get("kind") == "bundle":
            for ref in n.get("satisfies", []):
                if not resolves(ref):
                    errors.append(f"{where}: satisfies unknown capability {ref!r}")
            for m in n.get("members", []):
                if not resolves(m.get("technique", "")):
                    errors.append(f"{where}: unknown member {m.get('technique')!r}")
                for ref in m.get("load_bearing_for", []):
                    if not resolves(ref):
                        errors.append(f"{where}: load_bearing_for unknown {ref!r}")
            if n.get("minimality") == "tested" and not n.get("ablation_source"):
                errors.append(f"{where}: minimality 'tested' requires an ablation_source")
    return errors


def build(nodes):
    edges, addressed = [], {}
    for nid, n in nodes.items():
        if n.get("kind") == "technique":
            for e in n.get("addresses", []):
                cap = e["capability"]
                edges.append({"from": nid, "to": cap, "rel": "addresses",
                              "strength": e.get("strength"), "note": e.get("note")})
                addressed.setdefault(cap, []).append((nid, e.get("strength")))
            for r in n.get("requires", []):
                edges.append({"from": nid, "to": f"precondition.{r['token']}", "rel": "requires",
                              "note": r.get("note")})
            for x in n.get("interacts", []):
                rel, other = x["rel"], x["technique"]
                edges.append({"from": nid, "to": other, "rel": "interacts",
                              "interaction": rel, "scope": x.get("scope"), "note": x.get("note"),
                              "evidence": x.get("evidence")})
                edges.append({"from": other, "to": nid, "rel": "interacts", "derived": True,
                              "interaction": ASYMMETRIC.get(rel, rel), "scope": x.get("scope"),
                              "note": x.get("note"), "evidence": x.get("evidence")})
        for ref in n.get("part_of", []):
            edges.append({"from": nid, "to": ref, "rel": "part_of"})
        for ref in n.get("completed_by", []):
            edges.append({"from": nid, "to": ref, "rel": "completed_by"})
        if n.get("kind") == "bundle":
            for ref in n.get("satisfies", []):
                edges.append({"from": nid, "to": ref, "rel": "satisfies"})
            for m in n.get("members", []):
                edges.append({"from": nid, "to": m["technique"], "rel": "member"})
    return edges, addressed


def gap_report(nodes, addressed):
    lines = []
    for nid, n in sorted(nodes.items()):
        if n.get("kind") != "capability":
            continue
        hits = addressed.get(nid, [])
        direct = [t for t, s in hits if s == "direct"]
        if not hits:
            lines.append(f"  EMPTY     {nid}  ({n.get('status')})  — no technique addresses this")
        elif not direct:
            lines.append(f"  INDIRECT  {nid}  ({n.get('status')})  — {len(hits)} edge(s), none 'direct'")
    return lines


def screen(nodes, tokens, profile):
    """Which techniques this deployment could hold at all, and at what price.

    A technique is BLOCKED by any precondition the profile supplies at `none`,
    CHARGED where it is supplied only in part, and CLEAR otherwise. Assumption
    tokens never block — they are reported for checking, which is all an
    assumption can be. The screen is about admissibility, never about quality.
    """
    levels = {s["token"]: s for s in profile.get("supplies", [])}
    out = {"clear": [], "charged": [], "blocked": []}
    for nid, n in sorted(nodes.items()):
        if n.get("kind") != "technique":
            continue
        blocked, charged, checks = [], [], []
        for r in n.get("requires", []):
            tok = r["token"]
            if tokens[tok]["kind"] == "assumption":
                checks.append(tok)
                continue
            s = levels.get(tok, {"level": "none", "binding": "project"})
            if s["level"] == "none":
                blocked.append((tok, s.get("binding")))
            elif s["level"] == "partial":
                charged.append(tok)
        row = (nid, blocked, charged, checks)
        out["blocked" if blocked else "charged" if charged else "clear"].append(row)
    return out


def screen_report(nodes, tokens, addressed, profile):
    res = screen(nodes, tokens, profile)
    lines = [f"PROFILE  {profile['id']}  —  {profile.get('name')}", ""]
    for bucket, label in (("clear", "CLEAR    every precondition supplied in full"),
                          ("charged", "CHARGED  admissible, but something is supplied only in part"),
                          ("blocked", "BLOCKED  a precondition is not available at all")):
        lines.append(f"{label}  ({len(res[bucket])})")
        for nid, blocked, charged, checks in res[bucket]:
            name = nid.split(".", 1)[1]
            if blocked:
                by = ", ".join(f"{t} [{b}]" for t, b in blocked)
                lines.append(f"  {name:<34} needs {by}")
            elif charged:
                lines.append(f"  {name:<34} partial: {', '.join(charged)}")
            else:
                lines.append(f"  {name:<34}")
            if checks:
                lines.append(f"  {'':<34} assumes {', '.join(checks)} — check, cannot supply")
        lines.append("")

    admissible = {nid for b in ("clear", "charged") for nid, *_ in res[b]}
    lines.append("COVERAGE of this profile's stated requirements, admissible techniques only")
    for c in profile.get("requires_capabilities", []):
        cap = c["capability"]
        hits = [(t, s) for t, s in addressed.get(cap, []) if t in admissible]
        best = max((STRENGTH.get(s, 0) for _, s in hits), default=0)
        mark = {3: "direct", 2: "partial", 1: "incidental", 0: "NOTHING"}[best]
        lost = [t for t, _ in addressed.get(cap, []) if t not in admissible]
        tail = f"  (blocked here: {len(lost)})" if lost else ""
        lines.append(f"  {mark:<11} {c['criticality']:<9} {cap}{tail}")
    unmet = [c["capability"] for c in profile.get("requires_capabilities", [])
             if c["criticality"] == "required"
             and not any(t in admissible for t, _ in addressed.get(c["capability"], []))]
    lines += ["", f"{len(unmet)} required capability(ies) with no admissible technique at all:"]
    lines += [f"  {u}" for u in unmet] or ["  none"]
    return lines


def unclassified_pairs(nodes, addressed):
    """Technique pairs that co-cover a capability with no interaction declared.

    Until a pair is typed, a combination holding both cannot be graded: the
    grader has no way to tell added coverage from a duplicate. Load-bearing
    pairs only — two 'incidental' edges are not a combination anyone would build.
    """
    typed = set()
    for n in nodes.values():
        for x in n.get("interacts", []):
            typed.add((min(n["id"], x["technique"]), max(n["id"], x["technique"]), x.get("scope")))
    out = {}
    for cap, hits in addressed.items():
        strong = sorted(t for t, s in hits if STRENGTH.get(s, 0) >= 2)
        for i, a in enumerate(strong):
            for b in strong[i + 1:]:
                if (a, b, cap) not in typed:
                    out.setdefault(cap, []).append((a, b))
    return out


def pair_report(pairs, verbose):
    total = sum(len(v) for v in pairs.values())
    lines = [f"\nuntyped co-coverage ({total} load-bearing pair(s) not gradable):"]
    if not total:
        return lines + ["  none"]
    for cap, ps in sorted(pairs.items()):
        if verbose:
            lines += [f"  {cap}: {a.split('.', 1)[1]} ~ {b.split('.', 1)[1]}" for a, b in ps]
        else:
            members = sorted({t for p in ps for t in p})
            lines.append(f"  {cap}: {len(ps)} pair(s) over {len(members)} techniques")
    if not verbose:
        lines.append("  (--pairs to list them)")
    return lines


def main():
    nodes, errors = load()
    tokens = preconditions()
    errors = validate(nodes, errors, tokens)
    edges, addressed = build(nodes)
    nodes.update({f"precondition.{t}": {"id": f"precondition.{t}", "kind": "precondition",
                                        "name": t, "precondition_kind": v["kind"],
                                        "note": v["note"], "_path": "data/preconditions.yaml"}
                  for t, v in tokens.items()})

    if len(sys.argv) > 2 and sys.argv[1] == "--profile":
        pid = sys.argv[2]
        pid = pid if pid in nodes else f"profile.{pid}"
        if nodes.get(pid, {}).get("kind") != "profile":
            print(f"no such profile: {sys.argv[2]}", file=sys.stderr)
            return 1
        if errors:
            print(f"{len(errors)} validation error(s) — fix before trusting a screen",
                  file=sys.stderr)
            return 1
        print("\n".join(screen_report(nodes, tokens, addressed, nodes[pid])))
        return 0
    if len(sys.argv) > 2 and sys.argv[1] == "--from":
        cap = sys.argv[2]
        print(f"FORWARD  {cap}")
        for t, s in addressed.get(cap, []) or [("(nothing addresses this)", "")]:
            print(f"  <- {t} [{s}]")
        for nid, n in nodes.items():
            if n.get("kind") == "bundle" and cap in n.get("satisfies", []):
                print(f"  bundle: {nid} ({n.get('minimality')})")
        return 0
    if len(sys.argv) > 2 and sys.argv[1] == "--to":
        tid = sys.argv[2]
        print(f"REVERSE  {tid}")
        for e in edges:
            if e["from"] == tid and e["rel"] == "addresses":
                print(f"  -> {e['to']} [{e['strength']}] {e['note'] or ''}")
        req = [e for e in edges if e["from"] == tid and e["rel"] == "requires"]
        if req:
            print("  requires:")
            for e in req:
                tok = e["to"].split(".", 1)[1]
                print(f"    {tok} [{nodes[e['to']]['precondition_kind']}] — {e['note']}")
        inter = [e for e in edges if e["from"] == tid and e["rel"] == "interacts"]
        if inter:
            print("  interacts:")
            for e in inter:
                mark = " (derived)" if e.get("derived") else ""
                print(f"    {e['interaction']} {e['to']} on {e['scope']}{mark}")
        return 0

    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "graph.json").write_text(json.dumps(
        {"nodes": [{k: v for k, v in n.items()} for n in nodes.values()], "edges": edges},
        indent=2, default=str) + "\n")

    kinds = {}
    for n in nodes.values():
        kinds[n.get("kind")] = kinds.get(n.get("kind"), 0) + 1
    print(f"nodes: {kinds}  edges: {len(edges)}")
    gaps = gap_report(nodes, addressed)
    print(f"\ngap report ({len(gaps)} unmet):")
    print("\n".join(gaps) if gaps else "  none")
    print("\n".join(pair_report(unclassified_pairs(nodes, addressed),
                                "--pairs" in sys.argv)))
    if WARNINGS:
        print(f"\n{len(WARNINGS)} warning(s) (non-blocking):")
        for w in WARNINGS:
            print(f"  {w}")
    if errors:
        print(f"\n{len(errors)} validation error(s):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print("\nvalidation: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
