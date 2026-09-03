#!/usr/bin/env python3
"""Grade a combination of techniques against a profile, before anyone builds it.

    grade_combination.py --profile arc-agi-3 --members technique.mcts,technique.dsl-search
    grade_combination.py --profile arc-agi-3 --cover        search minimal covers
    grade_combination.py --profile arc-agi-3 --members ... --emit bundles/name.md

Everything here is computed from the graph. The script adds no judgement of its
own: it reports what the declared edges already imply about a set of techniques
held together, which is the question a bundle answers and a table cannot.

Two results are worth more than the rest:

  * a member is REMOVABLE when every capability it covers is covered at least as
    strongly by another member — the overlap question, answered before the build;
  * a grade is PROVISIONAL when two members co-cover a capability with no declared
    interaction. An untyped pair means nobody has said whether the coverage adds,
    so the arithmetic below is not yet trustworthy. Type the pair, then re-grade.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_graph import (STRENGTH, build, load, preconditions,  # noqa: E402
                         screen, validate)

COST = {"low": 1, "medium": 2, "high": 3, "extreme": 4}
NAME = {3: "direct", 2: "partial", 1: "incidental", 0: "nothing"}


def interactions(nodes, members):
    """Declared interactions among the members, both directions."""
    out = []
    for nid in members:
        for x in nodes[nid].get("interacts", []):
            if x["technique"] in members:
                out.append((nid, x["rel"], x["technique"], x.get("scope"), x.get("note")))
    return out


def strength_of(nodes, tid, cap):
    for e in nodes[tid].get("addresses", []):
        if e["capability"] == cap:
            return STRENGTH[e["strength"]]
    return 0


def grade(nodes, tokens, profile, members):
    caps = [(c["capability"], c["criticality"]) for c in profile["requires_capabilities"]]
    levels = {s["token"]: s for s in profile.get("supplies", [])}
    inter = interactions(nodes, members)
    r = {"members": members, "coverage": [], "removable": [], "synergy": [],
         "conflicts": [], "untyped": [], "blocked": [], "charged": []}

    scr = screen(nodes, tokens, profile)
    bucket = {nid: b for b in scr for nid, *_ in scr[b]}
    for nid, blocked, charged, _ in [row for b in scr for row in scr[b]]:
        if nid in members and blocked:
            r["blocked"].append((nid, blocked))
        elif nid in members and charged:
            r["charged"].append((nid, charged))

    # a `supplies` edge inside the set fills a member's precondition from another
    # member, so the profile does not have to — the case where a combination is
    # genuinely worth more than the sum of its parts
    supplied = set()
    for src, rel, dst, scope, note in inter:
        if rel == "supplies":
            have = levels.get(scope, {}).get("level", "none")
            if have != "full":
                r["synergy"].append((src, dst, scope, have, note))
                supplied.add((dst, scope))
        elif rel == "conflicts":
            r["conflicts"].append((src, dst, scope, note))

    for cap, crit in caps:
        per = {m: strength_of(nodes, m, cap) for m in members}
        best = max(per.values(), default=0)
        holders = [m for m, s in per.items() if s == best and s > 0]
        r["coverage"].append((cap, crit, best, holders))
        co = sorted(m for m, s in per.items() if s >= 2)
        typed = {(min(a, c), max(a, c), sc) for a, _, c, sc, _ in inter}
        for i, a in enumerate(co):
            for b in co[i + 1:]:
                if (a, b, cap) not in typed:
                    r["untyped"].append((cap, a, b))

    # Removability is sequential, not per-member: two techniques covering one
    # capability at equal strength are each redundant given the other, and
    # reporting both as removable would invite dropping the pair and losing the
    # capability. Drop one, then re-ask. A member that SUPPLIES another's
    # precondition is never removable — the synergy is what it is there for.
    suppliers = {src for src, _, _, _, _ in r["synergy"]}
    kept = list(members)
    for m in members:
        if m in suppliers:
            continue
        others = [x for x in kept if x != m]
        covers = [cap for cap, _ in caps if strength_of(nodes, m, cap) > 0]
        if covers and all(
            any(strength_of(nodes, o, cap) >= strength_of(nodes, m, cap) for o in others)
            for cap in covers
        ):
            why = [(rel, other if src == m else src, sc)
                   for src, rel, other, sc, _ in inter
                   if m in (src, other) and rel in ("overlaps", "subsumes")]
            r["removable"].append((m, why))
            kept.remove(m)

    tok_union, shared = {}, []
    for m in members:
        for req in nodes[m].get("requires", []):
            tok_union.setdefault(req["token"], []).append(m)
    shared = {t: ms for t, ms in tok_union.items() if len(ms) > 1}
    r["tokens"] = tok_union
    r["shared_tokens"] = shared
    r["cost_tier"] = max((COST.get(nodes[m].get("cost"), 0) for m in members), default=0)

    # Only scored evidence counts toward the floor. An entry whose split is
    # `not-applicable` is a claim about standing or lineage, not a measurement,
    # and must not lift a combination's grade.
    floor = {}
    for cap, crit, best, holders in r["coverage"]:
        if len(holders) == 1:
            stars = [e.get("stars", 0) for e in nodes[holders[0]].get("evidence", [])
                     if e.get("split") != "not-applicable"]
            floor[holders[0]] = max(stars, default=0)
    r["evidence_floor"] = min(floor.values(), default=0)
    r["load_bearing"] = sorted(floor.items())
    return r


def report(r, nodes):
    L = [f"COMBINATION  {', '.join(m.split('.', 1)[1] for m in r['members'])}", ""]
    if r["blocked"]:
        L.append("INADMISSIBLE — a member needs something this deployment cannot supply")
        for nid, blocked in r["blocked"]:
            L.append(f"  {nid.split('.', 1)[1]}: {', '.join(t for t, _ in blocked)}")
        L.append("")
    if r["charged"]:
        L.append("CHARGED — admissible, at a price the deployment can see")
        for nid, ch in r["charged"]:
            L.append(f"  {nid.split('.', 1)[1]}: {', '.join(ch)} supplied only in part")
        L.append("")

    L.append("COVERAGE")
    for cap, crit, best, holders in r["coverage"]:
        who = ", ".join(h.split(".", 1)[1] for h in holders) or "-"
        L.append(f"  {NAME[best]:<11} {crit:<9} {cap:<42} {who}")
    missing = [c for c, crit, b, _ in r["coverage"] if crit == "required" and b == 0]
    L.append("")

    if r["synergy"]:
        L.append("SYNERGY — one member supplies what another needs")
        for src, dst, scope, have, note in r["synergy"]:
            L.append(f"  {src.split('.', 1)[1]} -> {dst.split('.', 1)[1]}: {scope} "
                     f"(profile supplies it '{have}')")
            if note:
                L.append(f"      {note.strip()}")
        L.append("")
    if r["conflicts"]:
        L.append("CONFLICT")
        for src, dst, scope, note in r["conflicts"]:
            L.append(f"  {src} X {dst} on {scope}: {note or ''}")
        L.append("")
    if r["removable"]:
        L.append("REMOVABLE — covers nothing another member does not cover as strongly")
        targets = {d for _, d, _, _, _ in r["synergy"]}
        for m, why in r["removable"]:
            tail = "; ".join(f"{rel} {o.split('.', 1)[1]} on {sc}" for rel, o, sc in why)
            if m in targets:
                tail += "; dropping it also makes the synergy above moot"
            L.append(f"  {m.split('.', 1)[1]}" + (f"  ({tail})" if tail else "  (untyped)"))
        L.append("")

    L.append(f"COST  {len(r['tokens'])} distinct preconditions across the set; "
             f"heaviest member tier {r['cost_tier']}/4")
    for t, ms in sorted(r["shared_tokens"].items()):
        L.append(f"  shared: {t} — {len(ms)} members (build once)")
    L.append(f"EVIDENCE FLOOR  {r['evidence_floor']} star(s) — the weakest SCORED evidence "
             f"among members that solely hold a capability (a 'not-applicable' split "
             f"does not count)")
    for m, s in r["load_bearing"]:
        note = f"{s} star(s)" if s else "no scored evidence"
        L.append(f"  {m.split('.', 1)[1]}: {note}, sole holder")
    L.append("")

    if r["untyped"]:
        L.append(f"PROVISIONAL — {len(r['untyped'])} co-covering pair(s) are untyped, so "
                 f"whether their coverage adds is undeclared:")
        for cap, a, b in r["untyped"]:
            L.append(f"  {cap}: {a.split('.', 1)[1]} ~ {b.split('.', 1)[1]}")
        L.append("  Type them in `interacts:` and re-grade before trusting this.")
    else:
        L.append("GRADE IS FIRM — every co-covering pair in this set is typed.")
    if missing:
        L.append(f"\nDOES NOT GIVE ({len(missing)} required capability(ies) uncovered):")
        L += [f"  {m}" for m in missing]
    return L


def covers(nodes, tokens, profile):
    """Smallest admissible sets covering the most `required` capabilities."""
    scr = screen(nodes, tokens, profile)
    pool = sorted(nid for b in ("clear", "charged") for nid, *_ in scr[b])
    req = [c["capability"] for c in profile["requires_capabilities"]
           if c["criticality"] == "required"]
    reachable = {c for c in req if any(strength_of(nodes, t, c) > 0 for t in pool)}
    best = []
    for n in range(1, len(pool) + 1):
        from itertools import combinations
        for combo in combinations(pool, n):
            got = {c for c in reachable if any(strength_of(nodes, t, c) > 0 for t in combo)}
            if got == reachable:
                best.append(combo)
        if best:
            break
    L = [f"MINIMAL ADMISSIBLE COVERS for profile.{profile['id'].split('.', 1)[1]}", "",
         f"  {len(reachable)} of {len(req)} required capabilities are reachable at all "
         f"from the {len(pool)} admissible techniques.",
         f"  unreachable: {', '.join(sorted(set(req) - reachable)) or 'none'}", ""]
    for combo in best:
        L.append("  " + " + ".join(c.split(".", 1)[1] for c in combo))
    return L


def emit_bundle(r, nodes, profile, path):
    covered = [(c, b, h) for c, crit, b, h in r["coverage"] if b > 0]
    missing = [c for c, crit, b, _ in r["coverage"] if crit == "required" and b == 0]
    lines = ["---", f"id: bundle.{Path(path).stem}", "kind: bundle",
             f"name: {Path(path).stem.replace('-', ' ').title()}", "satisfies:"]
    lines += [f"  - {c}" for c, _, _ in covered]
    lines.append("members:")
    for m in r["members"]:
        lb = [c for c, b, h in covered if h == [m]]
        lines.append(f"  - technique: {m}")
        lines.append(f"    load_bearing_for: [{', '.join(lb)}]")
    lines.append("minimality: argued")
    lines.append("does_not_give:")
    lines += [f"  - {c} — required by {profile['id']}, no member addresses it" for c in missing]
    for nid, ch in r["charged"]:
        lines.append(f"  - {nid.split('.', 1)[1]} at full strength: "
                     f"{', '.join(ch)} is supplied only in part")
    lines += ["---", "", f"# {Path(path).stem.replace('-', ' ').title()}", "",
              "*Drafted by `scripts/grade_combination.py` against "
              f"`{profile['id']}`. The frontmatter is derived; the prose below is not "
              "written yet — a bundle is not finished until someone argues the "
              "minimality claim.*", ""]
    Path(path).write_text("\n".join(lines) + "\n")
    return f"wrote {path}"


def main():
    args = sys.argv[1:]

    def opt(flag):
        return args[args.index(flag) + 1] if flag in args else None

    nodes, errors = load()
    tokens = preconditions()
    errors = validate(nodes, errors, tokens)
    if errors:
        print(f"{len(errors)} validation error(s) — fix before grading", file=sys.stderr)
        return 1
    build(nodes)
    pid = opt("--profile") or ""
    pid = pid if pid in nodes else f"profile.{pid}"
    if nodes.get(pid, {}).get("kind") != "profile":
        print(__doc__)
        return 1
    profile = nodes[pid]

    if "--cover" in args:
        print("\n".join(covers(nodes, tokens, profile)))
        return 0

    members = [m if m.startswith("technique.") else f"technique.{m}"
               for m in (opt("--members") or "").split(",") if m]
    unknown = [m for m in members if nodes.get(m, {}).get("kind") != "technique"]
    if not members or unknown:
        print(f"unknown member(s): {unknown}" if unknown else __doc__, file=sys.stderr)
        return 1
    r = grade(nodes, tokens, profile, members)
    print("\n".join(report(r, nodes)))
    if opt("--emit"):
        print("\n" + emit_bundle(r, nodes, profile, opt("--emit")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
