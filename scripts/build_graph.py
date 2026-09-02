#!/usr/bin/env python3
"""Parse the cognate corpus, validate it, emit data/graph.json.

Edges are declared once, on the technique (`addresses:`). The reverse edge onto
the capability is derived here, so the forward and reverse directions of the
pattern language cannot disagree.

    build_graph.py                 validate + emit + print the gap report
    build_graph.py --from <id>     forward:  requirement -> techniques / bundles
    build_graph.py --to <id>       reverse:  technique   -> capabilities it bears on
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


def load():
    nodes, errors = {}, []
    for d in ("patterns", "techniques", "bundles"):
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


def validate(nodes, errors):
    def resolves(ref):
        return ref in nodes or ref in FACULTY_ROOTS

    for nid, n in nodes.items():
        where = n["_path"]
        for ref in n.get("part_of", []) + n.get("completed_by", []):
            if not resolves(ref):
                errors.append(f"{where}: unresolved reference {ref!r}")

        if n.get("kind") == "technique":
            for e in n.get("addresses", []):
                if not resolves(e.get("capability", "")):
                    errors.append(f"{where}: addresses unknown capability {e.get('capability')!r}")
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
                if no_abs and "%" in str(ev.get("claim", "")):
                    errors.append(f"{where}: no_absolute_score set but claim carries a %")
            # rule 4 lint: a caveat that disputes a claim needs the claim on the record
            caveats = " ".join(n.get("caveats", [])).lower()
            if ("claim" in caveats or "unsupported" in caveats) and "claimed" not in kinds:
                errors.append(f"{where}: caveats dispute a claim, but no evidence entry of kind 'claimed'")

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


def main():
    nodes, errors = load()
    errors = validate(nodes, errors)
    edges, addressed = build(nodes)

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
    if errors:
        print(f"\n{len(errors)} validation error(s):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print("\nvalidation: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
