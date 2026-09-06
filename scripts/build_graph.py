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
    build_graph.py --trend [split] dated evidence by leverage side, to test a hypothesis
    build_graph.py --provenance    what SELECTED the corpus: nodes by entry frame
    build_graph.py --as-of <date>  priced rows re-read in the dollars of a later date
"""
import json
import math
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FACULTY_ROOTS = {"exploration", "modeling", "goal-setting",
                 "planning-execution", "priors", "prior"}
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
# A date may be a year, a year-month, or a full day. Partial is honest where that is
# all the source supports -- an arXiv identifier fixes the month of v1 and no more --
# and a trend view can still order by it.
ISO_DATE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")

STRENGTH = {"direct": 3, "partial": 2, "incidental": 1}
# Symmetric relations are declared once, on the alphabetically-first technique id;
# the reverse is derived here, exactly as `addresses:` is.
SYMMETRIC = {"overlaps", "composes", "conflicts"}
ASYMMETRIC = {"subsumes": "subsumed_by", "supplies": "supplied_by"}
INTERACTIONS = SYMMETRIC | set(ASYMMETRIC)



# `cost:` bands — per-task inference spend in USD, upper bound inclusive. Declared once here
# and enforced against any evidence row whose `regime:` prices the run in $/task.
COST_BANDS = {"low": 1.0, "medium": 10.0, "high": 100.0, "extreme": float("inf")}
PRICE_RE = re.compile(r"\$\s*([0-9]+(?:\.[0-9]+)?)\s*(?:-per-task|/task)")


# A price is NOMINAL — the dollars of its row's `date:`. Three currencies age at three
# rates (data/deflators.yaml), and a row's currency is read off its `regime:` string.
GPU_CLASS = re.compile(r"\b(?:\d+x)?(A100|H100|B200|L4|RTX[ -]?(?:PRO[ -]?)?6000)\b", re.I)
HOURS = re.compile(r"(\d+(?:\.\d+)?)\s*h(?:ours?)?\b", re.I)


def row_currency(regime):
    """Which deflator series governs this row, or None if it names no price.

    A CAP is nominal by construction and is separated from a price actually paid: both
    match PRICE_RE, and deflating the first would be a category error.
    """
    s = str(regime or "")
    if PRICE_RE.search(s):
        return "fixed-cap" if "cap" in s.lower() else "api-usd-per-task"
    if GPU_CLASS.search(s) and HOURS.search(s):
        return "gpu-hour"
    return None


def deflators():
    """The dated price series. Absent file is not an error — every row then reads NOT BANKED."""
    p = ROOT / "data" / "deflators.yaml"
    doc = yaml.safe_load(p.read_text()) if p.exists() else {}
    return {s["id"]: s for s in (doc or {}).get("series", [])}


def price_band(usd_per_task):
    for band, upper in COST_BANDS.items():
        if usd_per_task <= upper:
            return band
    return "extreme"

def preconditions():
    """The closed token vocabulary a technique's `requires:` may cite."""
    doc = yaml.safe_load((ROOT / "data" / "preconditions.yaml").read_text())
    return {t["token"]: t for t in doc["tokens"]}


def quantity_errors(where, entry, token, field, required):
    """A number is only comparable with its unit, its vintage and its frame attached.

    `limit` on a profile and `demand` on a technique are the two sides of one
    comparison, so both are held to the same bar the evidence schema sets for a
    score: no unit, no compare; no source, no entry.
    """
    if entry.get(field) is None:
        return []
    errs = []
    if not token.get("unit"):
        return [f"{where}: {token['token']!r} has no unit, so it cannot carry a "
                f"{field!r} — give it a unit in data/preconditions.yaml or drop the number"]
    if entry.get("unit") != token["unit"]:
        errs.append(f"{where}: {field} on {token['token']!r} is in {entry.get('unit')!r} "
                    f"but the token's unit is {token['unit']!r}; two numbers on different "
                    f"axes must not be compared")
    if not isinstance(entry[field], (int, float)) or entry[field] <= 0:
        errs.append(f"{where}: {field} must be a positive number, got {entry[field]!r}")
    for f in required:
        if not entry.get(f):
            errs.append(f"{where}: {field} on {token['token']!r} needs {f!r} — a quantity "
                        f"without it cannot be read back")
    return errs


def load():
    nodes, errors = {}, []
    for d in ("patterns", "techniques", "bundles", "profiles", "hypotheses"):
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


def validate_deflators(series, errors):
    """A deflator is a claim about the world and carries a source exactly as a row does."""
    seen = set()
    for s in series.values():
        where = f"data/deflators.yaml: {s.get('id')!r}"
        if not s.get("id") or not s.get("note"):
            errors.append(f"{where}: a series needs 'id' and 'note'")
        if s.get("applies_to") not in ("api-usd-per-task", "gpu-hour", "fixed-cap"):
            errors.append(f"{where}: applies_to must name a currency build_graph.py can read "
                          f"off a regime — api-usd-per-task, gpu-hour or fixed-cap; got "
                          f"{s.get('applies_to')!r}")
        if s.get("applies_to") in seen:
            errors.append(f"{where}: two series govern {s.get('applies_to')!r}; one currency, "
                          f"one series")
        seen.add(s.get("applies_to"))
        if s.get("status") not in ("banked", "unbanked", "contested"):
            errors.append(f"{where}: status must be 'banked', 'unbanked' or 'contested'")
        bases = {b.get("id"): b for b in (s.get("bases") or [])}
        pts = s.get("points") or []
        if s.get("status") == "unbanked" and pts:
            errors.append(f"{where}: an unbanked series holds no points — bank the primary "
                          f"or drop them")
        if s.get("status") == "contested" and len(bases) < 2:
            errors.append(f"{where}: 'contested' is a claim that the sources disagree — it "
                          f"needs at least two bases; one source is not a disagreement")
        for b in (s.get("bases") or []):
            for f in ("id", "source", "covers_from", "covers_to", "note"):
                if not b.get(f):
                    errors.append(f"{where}: basis {b.get('id')!r} needs {f!r} — a rate "
                                  f"without the span it was measured over cannot be "
                                  f"extrapolated honestly")
            mine = [pt for pt in pts if pt.get("basis") == b.get("id")]
            if s.get("deflates", True) and len({str(pt.get("as_of")) for pt in mine}) < 2:
                errors.append(f"{where}: basis {b.get('id')!r} deflates but holds fewer than "
                              f"two dated points; one point is a level, not a trend")
        for pt in pts:
            if pt.get("basis") not in bases:
                errors.append(f"{where}: point cites undeclared basis {pt.get('basis')!r}")
            for f in ("as_of", "value", "source"):
                if not pt.get(f):
                    errors.append(f"{where}: a point needs {f!r}")
            if not ISO_DATE.match(str(pt.get("as_of", ""))):
                errors.append(f"{where}: point as_of must be YYYY[-MM[-DD]], got "
                              f"{pt.get('as_of')!r}")
            if not isinstance(pt.get("value"), (int, float)) or pt.get("value", 0) <= 0:
                errors.append(f"{where}: point value must be a positive number, got "
                              f"{pt.get('value')!r}")
    return errors


def _months(d):
    parts = (str(d) + "-01")[:7].split("-")
    return int(parts[0]) * 12 + int(parts[1])


def value_at(s, basis, date):
    """Log-linear read of one basis at `date`, with a flag when it leaves the span the
    primary measured. Two points a year apart ARE a rate, so reading between and beyond
    them is the arithmetic the source states — but past `covers_to` it is extrapolation
    and the view says so rather than printing a bare number."""
    pts = sorted([pt for pt in (s.get("points") or []) if pt.get("basis") == basis],
                 key=lambda pt: _months(pt["as_of"]))
    if len(pts) < 2:
        return None
    x = _months(date)
    lo, hi = pts[0], pts[-1]
    for a, b in zip(pts, pts[1:]):
        if _months(a["as_of"]) <= x <= _months(b["as_of"]):
            lo, hi = a, b
            break
    xa, xb = _months(lo["as_of"]), _months(hi["as_of"])
    ya, yb = math.log(lo["value"]), math.log(hi["value"])
    val = math.exp(ya + (yb - ya) * ((x - xa) / (xb - xa))) if xb != xa else lo["value"]
    b = next((bb for bb in (s.get("bases") or []) if bb.get("id") == basis), {})
    outside = not (_months(b.get("covers_from", "1900-01")) <= x
                   <= _months(b.get("covers_to", "2999-12")))
    return val, outside


def as_of_report(nodes, series, target):
    """Every priced row re-read in the dollars of `target`, or the reason it cannot be.

    The view never edits a row. It prints the nominal price beside the deflated one so the
    two can never be confused, and where the sources disagree it prints their RANGE — a
    point estimate would hide the disagreement, which is the most important thing the
    deflators found.
    """
    by_currency = {s.get("applies_to"): s for s in series.values()}
    L = [f"AS OF  {target}    priced rows in the dollars of that date", "",
         "  Nothing here is written back: a row stays in the dollars of its own date.", ""]
    n_rows = n_shown = 0
    for n in sorted(nodes.values(), key=lambda n: n.get("name", "")):
        if n.get("kind") != "technique":
            continue
        lines = []
        for ev in n.get("evidence", []):
            cur = row_currency(ev.get("regime"))
            if not cur:
                continue
            n_rows += 1
            m = PRICE_RE.search(str(ev.get("regime", "")))
            usd = float(m.group(1)) if m else None
            nominal = f"${usd:g}/task" if usd else str(ev.get("regime"))[:22]
            s = by_currency.get(cur)
            date = str(ev.get("date", "?"))
            if s is None:
                verdict = [f"no series governs {cur}"]
            elif not s.get("deflates", True):
                why = ("a cap is a rule, not a price" if s.get("status") != "contested"
                       else f"CONTESTED — {s['id']} found no single index to deflate by")
                verdict = [f"not deflated: {why}"]
            else:
                factors = []
                for b in (s.get("bases") or []):
                    a, z = value_at(s, b["id"], date), value_at(s, b["id"], target)
                    if a and z:
                        factors.append((z[0] / a[0], b["id"], a[1] or z[1]))
                if not factors:
                    verdict = [f"NOT BANKED — {s['id']} holds no usable points"]
                else:
                    n_shown += 1
                    lo, hi = min(f[0] for f in factors), max(f[0] for f in factors)
                    ex = " EXTRAPOLATED past the primaries' data" if any(f[2] for f in factors) else ""
                    tag = "CONTESTED " if s.get("status") == "contested" else ""
                    verdict = [f"{tag}x{lo:.3g}–x{hi:.3g} across {len(factors)} sourced "
                               f"rate(s){ex}"]
                    if usd:
                        b1, b2 = price_band(usd * lo), price_band(usd * hi)
                        band = b1 if b1 == b2 else f"{b1}..{b2}"
                        verdict.append(f"      = ${usd * lo:.3g}–${usd * hi:.3g}/task, band "
                                       f"{band}  (label says {n.get('cost')})")
            lines.append(f"    {date:<11}{cur:<18}{nominal:<24}{verdict[0]}")
            lines += verdict[1:]
        if lines:
            L.append(f"  {n['name']}  [cost: {n.get('cost')}]")
            L += lines
            L.append("")
    L += [f"  {n_rows} priced row(s); {n_shown} re-priced. A range is not a forecast: it is "
          f"what the",
          "  sourced primaries disagree between. See data/deflators.yaml for who they are."]
    return L


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
                else:
                    errors += quantity_errors(where, r, tokens[r["token"]], "demand",
                                              ("measured_on", "source"))

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

            if n.get("leverage") not in ("knowledge", "computation", "both"):
                errors.append(f"{where}: leverage must be 'knowledge' (bounded by authored "
                              f"content), 'computation' (improves with compute alone) or "
                              f"'both'; got {n.get('leverage')!r}")
            # `cost:` is the per-task inference price band (SCHEMA.md). A label is an estimate
            # until a row prices the run in $/task; then it must equal the band of the dearest one.
            cost = n.get("cost")
            if cost not in COST_BANDS:
                errors.append(f"{where}: cost must be one of {list(COST_BANDS)}; got {cost!r}")
            priced = [(float(m.group(1)), ev) for ev in n.get("evidence", [])
                      for m in [PRICE_RE.search(str(ev.get("regime", "")))] if m]
            if priced and cost in COST_BANDS:
                usd, ev = max(priced, key=lambda pe: pe[0])
                band = price_band(usd)
                if band != cost:
                    errors.append(f"{where}: cost '{cost}' but the dearest priced row is "
                                  f"${usd:g}/task, band '{band}': {str(ev.get('claim'))[:60]!r}")
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
                for tb in ev.get("requires_beyond", []):
                    if tb not in tokens:
                        errors.append(f"{where}: requires_beyond names unknown token {tb!r}")
                    elif tb in [r.get("token") for r in n.get("requires", [])]:
                        errors.append(f"{where}: requires_beyond {tb!r} is already in this "
                                      f"technique's requires — 'beyond' means beyond")
                src = str(ev.get("source", ""))
                if re.match(r"^https?://[^/]+/?$", src):
                    WARNINGS.append(f"{where}: source {src} is a bare domain, not a citation "
                                    f"of the result: {ev.get('claim')!r}")
                if ev.get("date") and not ISO_DATE.match(str(ev["date"])):
                    errors.append(f"{where}: date {ev['date']!r} must be YYYY, YYYY-MM or "
                                  f"YYYY-MM-DD")
                if not ev.get("date") and ev.get("split") != "not-applicable":
                    WARNINGS.append(f"{where}: evidence has no date (needed for trend views): {ev.get('claim')!r}")
                if no_abs and "%" in str(ev.get("claim", "")):
                    errors.append(f"{where}: no_absolute_score set but claim carries a %")
            # rule 4 lint: a caveat that disputes a claim needs the claim on the record
            caveats = " ".join(n.get("caveats", [])).lower()
            if ("claim" in caveats or "unsupported" in caveats) and "claimed" not in kinds:
                errors.append(f"{where}: caveats dispute a claim, but no evidence entry of kind 'claimed'")

        if n.get("kind") == "hypothesis":
            for f in ("claim", "source", "date", "status", "stars"):
                if not n.get(f):
                    errors.append(f"{where}: hypothesis needs {f!r}")
            if n.get("status") not in ("argued", "supported", "contested", "refuted"):
                errors.append(f"{where}: status must be argued/supported/contested/refuted")
            if n.get("stars", 0) > 2 and n.get("status") == "argued":
                errors.append(f"{where}: an argued hypothesis may not exceed 2 stars")
            if not n.get("predicts"):
                errors.append(f"{where}: a hypothesis with no `predicts` cannot be checked "
                              f"against the corpus, which is the only reason to hold one")
            for ref in n.get("bears_on", []):
                if ref != "all" and not resolves(ref):
                    errors.append(f"{where}: bears_on unknown {ref!r}")

        if n.get("kind") == "capability":
            arrival = n.get("arrival", "engineered")
            if arrival not in ("engineered", "emergent-claimed", "emergent-demonstrated",
                               "contested"):
                errors.append(f"{where}: arrival must be engineered / emergent-claimed / "
                              f"emergent-demonstrated / contested, got {arrival!r}")
            if arrival != "engineered":
                if not n.get("emerges_from"):
                    errors.append(f"{where}: arrival {arrival!r} must name `emerges_from` — "
                                  f"emergence with no carrier is not a falsifiable claim")
                for f in ("arrival_source", "arrival_date"):
                    if not n.get(f):
                        errors.append(f"{where}: arrival {arrival!r} needs {f!r}")
                for ref in n.get("emerges_from", []):
                    if nodes.get(ref, {}).get("kind") != "technique":
                        errors.append(f"{where}: emerges_from {ref!r} is not a technique")

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
                if tok in tokens:
                    errors += quantity_errors(where, s, tokens[tok], "limit",
                                              ("as_of", "checked", "source"))
                for h in s.get("history", []):
                    for f in ("as_of", "source", "note"):
                        if not h.get(f):
                            errors.append(f"{where}: {tok}: a superseded quantity needs "
                                          f"{f!r} — that is the whole point of keeping it")
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
        arrival = n.get("arrival", "engineered")
        tail = "" if arrival == "engineered" else \
            f"  [{arrival} from {', '.join(n.get('emerges_from', []))}]"
        if not hits:
            lines.append(f"  EMPTY     {nid}  ({n.get('status')})  — no technique addresses "
                         f"this{tail or '; arrival is engineered, so this is a build, not a wait'}")
        elif not direct:
            lines.append(f"  INDIRECT  {nid}  ({n.get('status')})  — {len(hits)} edge(s), none 'direct'{tail}")
    return lines


def screen(nodes, tokens, profile):
    """Which techniques this deployment could hold at all, and at what price.

    A technique is BLOCKED by any precondition the profile supplies at `none`,
    CHARGED where it is supplied only in part, and CLEAR otherwise. Assumption
    tokens never block — they are reported for checking, which is all an
    assumption can be. The screen is about admissibility, never about quality.
    """
    levels = {s["token"]: s for s in profile.get("supplies", [])}
    own = set(profile.get("own_splits", []))
    out = {"clear": [], "charged": [], "over_budget": [], "blocked": []}
    for nid, n in sorted(nodes.items()):
        if n.get("kind") != "technique":
            continue
        blocked, charged, checks, over = [], [], [], []
        for r in n.get("requires", []):
            tok = r["token"]
            if tokens[tok]["kind"] == "assumption":
                checks.append(tok)
                continue
            s = levels.get(tok, {"level": "none", "binding": "project"})
            # Quantity beats level: a precondition the deployment supplies, in an amount
            # smaller than the mechanism is published to need, is not "partial" — it is
            # a refutation with arithmetic behind it.
            if s.get("limit") and r.get("demand") and s.get("unit") == r.get("unit"):
                if r["demand"] > s["limit"]:
                    over.append((tok, r["demand"], s["limit"], r.get("measured_on"),
                                 r["measured_on"] in own if r.get("measured_on") else False,
                                 s.get("as_of"), s.get("checked")))
                    continue
            if s["level"] == "none":
                blocked.append((tok, s.get("binding")))
            elif s["level"] == "partial":
                charged.append(tok)
        unreachable = []
        for ev in n.get("evidence", []):
            missing = [t for t in ev.get("requires_beyond", [])
                       if levels.get(t, {"level": "none"})["level"] == "none"]
            if missing:
                unreachable.append((ev.get("claim", "")[:52], missing))
        row = (nid, blocked, charged, checks, over, unreachable)
        out["blocked" if blocked else "over_budget" if over
            else "charged" if charged else "clear"].append(row)
    return out


def screen_report(nodes, tokens, addressed, profile):
    res = screen(nodes, tokens, profile)
    lines = [f"PROFILE  {profile['id']}  —  {profile.get('name')}", ""]
    for bucket, label in (
            ("clear", "CLEAR       every precondition supplied in full"),
            ("charged", "CHARGED     admissible, but something is supplied only in part"),
            ("over_budget", "OVER BUDGET the deployment supplies this, in less than the "
                            "published cost"),
            ("blocked", "BLOCKED     a precondition is not available at all")):
        lines.append(f"{label}  ({len(res[bucket])})")
        for nid, blocked, charged, checks, over, unreachable in res[bucket]:
            name = nid.split(".", 1)[1]
            if blocked:
                by = ", ".join(f"{t} [{b}]" for t, b in blocked)
                lines.append(f"  {name:<34} needs {by}")
            elif over:
                for tok, demand, limit, frame, on_frame, as_of, checked in over:
                    lines.append(f"  {name:<34} {tok}: needs {demand}, budget {limit} "
                                 f"({demand / limit:.2f}x over)")
                    lines.append(f"  {'':<34}   budget as of {as_of}, checked {checked}")
                    lines.append(f"  {'':<34}   cost measured on {frame}" +
                                 ("" if on_frame else " — NOT this deployment, so the "
                                                      "arithmetic is indicative, not a verdict"))
            elif charged:
                lines.append(f"  {name:<34} partial: {', '.join(charged)}")
            else:
                lines.append(f"  {name:<34}")
            if checks:
                lines.append(f"  {'':<34} assumes {', '.join(checks)} — check, cannot supply")
            if unreachable:
                n_ev = len(nodes[nid].get("evidence", []))
                toks = sorted({t for _, ts in unreachable for t in ts})
                lines.append(f"  {'':<34} the MECHANISM is admissible, but {len(unreachable)} "
                             f"of {n_ev} published result(s) are not: they needed "
                             f"{', '.join(toks)}")
        lines.append("")

    cross = {}
    for b in res:
        for nid, *_ in res[b]:
            lev = nodes[nid].get("leverage", "?")
            cross.setdefault(lev, {}).setdefault(b, []).append(nid.split(".", 1)[1])
    lines.append("LEVERAGE  which side of the bitter lesson this deployment can reach")
    for lev in ("knowledge", "both", "computation"):
        row = cross.get(lev, {})
        counts = ", ".join(f"{len(v)} {k}" for k, v in sorted(row.items()))
        lines.append(f"  {lev:<12}{counts}")
    lines.append("")

    quantified = sum(1 for b in res for *_, over, _ in res[b] if over)
    have_demand = sum(1 for nid, n in nodes.items() if n.get("kind") == "technique"
                      and any(r.get("demand") for r in n.get("requires", [])))
    total = sum(1 for n in nodes.values() if n.get("kind") == "technique")
    lines.append(f"QUANTIFIED  {have_demand} of {total} techniques publish a cost in a unit "
                 f"this profile can screen against; {quantified} exceed a stated budget.")
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
    # A technique refuted only by arithmetic, only just, and on someone else's frame is
    # not the same as one that cannot run here at all. It does not count as coverage, and
    # it is not silently dropped either: it is named, with the margin that decides it.
    over = {nid: over for nid, _, _, _, over, _ in res["over_budget"]}
    contingent = []
    for c in profile.get("requires_capabilities", []):
        cap = c["capability"]
        have = max((STRENGTH.get(s, 0) for t, s in addressed.get(cap, [])
                    if t in admissible), default=0)
        for t, s in addressed.get(cap, []):
            if t in over and STRENGTH.get(s, 0) > have:
                tok, demand, limit, frame, on_frame, *_ = over[t][0]
                now = {3: "direct", 2: "partial", 1: "incidental", 0: "nothing"}[have]
                contingent.append(f"  {cap}: {now} -> {s} if {t.split('.', 1)[1]} qualifies, "
                                  f"held out by {demand} vs {limit} on {tok}, measured on "
                                  f"{'this deployment' if on_frame else frame}")
    if contingent:
        lines += ["", "CONTINGENT ON A BUDGET QUESTION — coverage that turns on a number, "
                      "not on a capability:"] + contingent

    unmet = [c["capability"] for c in profile.get("requires_capabilities", [])
             if c["criticality"] == "required"
             and not any(t in admissible for t, _ in addressed.get(c["capability"], []))
             and not any(t in over for t, _ in addressed.get(c["capability"], []))]
    lines += ["", f"{len(unmet)} required capability(ies) with no admissible technique at all:"]
    lines += [f"  {u}" for u in unmet] or ["  none"]
    return lines


def trend(nodes, want=None):
    """Dated evidence ordered in time, tagged by which side of the bitter lesson it sits on.

    The point is that this is a QUERY over the register's own rows, not a citation of
    an essay. Undated rows are listed separately rather than dropped silently — a trend
    computed over an unknown fraction of the evidence is not a trend.
    """
    rows, undated = [], []
    for n in nodes.values():
        if n.get("kind") != "technique":
            continue
        for ev in n.get("evidence", []):
            split = ev.get("split")
            if split == "not-applicable" or (want and want not in str(split)):
                continue
            r = (str(ev.get("date")), split, n.get("leverage"), n["name"], ev.get("claim", ""),
                 ev.get("kind"), ev.get("stars"))
            (rows if ev.get("date") else undated).append(r)
    L = [f"TREND  {want or 'all splits'}", ""]
    for date, split, lev, name, claim, kind, stars in sorted(rows):
        L.append(f"  {date:<11}{str(lev):<12}{str(split):<30}{'*' * (stars or 0):<5}{kind}")
        L.append(f"  {'':<11}{name} — {claim[:74]}")
    if undated:
        L += ["", f"  {len(undated)} undated row(s) EXCLUDED — a trend over an unknown "
                  f"fraction of the evidence is not a trend:"]
        L += [f"    {r[3]} — {r[4][:66]}" for r in undated]
    return L


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


def provenance(nodes):
    """Report the corpus by entry frame — the register's own selection effect.

    A pattern language is curated, not sampled, so its composition is evidence about
    its authors before it is evidence about the field. This report is what lets a
    distributional reading (see hypotheses/) state its own frame instead of assuming
    it does not have one. Nodes are grouped by `provenance.frame`, the instrument that
    put them in view; a frame holding most of the corpus is the corpus's blind spot.
    """
    import collections
    by = collections.defaultdict(list)
    for n in nodes.values():
        if n.get("kind") not in ("technique", "capability"):
            continue
        pr = n.get("provenance") or {}
        by[pr.get("frame", "UNDECLARED")].append((n["kind"], n.get("name", n["id"]), pr))
    total = sum(len(v) for v in by.values())
    L = ["PROVENANCE  — what selected the corpus", ""]
    for frame, rows in sorted(by.items(), key=lambda kv: -len(kv[1])):
        k = collections.Counter(r[0] for r in rows)
        dates = sorted({r[2].get("entered") for r in rows if r[2].get("entered")})
        span = dates[0] if len(dates) < 2 else f"{dates[0]}..{dates[-1]}"
        L.append(f"  {len(rows):>3}/{total}  {100*len(rows)//total:>3}%  {frame}"
                 f"   [{k['technique']} technique, {k['capability']} capability]  {span}")
        note = rows[0][2].get("note")
        if note:
            L.append(f"           {note}")
        L.append("")
    top = max(by.items(), key=lambda kv: len(kv[1]))
    L += [f"  DOMINANT FRAME: {top[0]} holds {100*len(top[1])//total}% of the corpus.",
          "  A distributional claim over these nodes measures this frame first.", ""]
    return L


def main():
    nodes, errors = load()
    tokens = preconditions()
    series = deflators()
    errors = validate(nodes, errors, tokens)
    errors = validate_deflators(series, errors)
    edges, addressed = build(nodes)
    nodes.update({f"precondition.{t}": {"id": f"precondition.{t}", "kind": "precondition",
                                        "name": t, "precondition_kind": v["kind"],
                                        "note": v["note"], "_path": "data/preconditions.yaml"}
                  for t, v in tokens.items()})

    if len(sys.argv) > 1 and sys.argv[1] == "--provenance":
        print("\n".join(provenance(nodes)))
        return
    if len(sys.argv) > 2 and sys.argv[1] == "--as-of":
        print("\n".join(as_of_report(nodes, series, sys.argv[2])))
        return 0
    if len(sys.argv) > 1 and sys.argv[1] == "--trend":
        print("\n".join(trend(nodes, sys.argv[2] if len(sys.argv) > 2 else None)))
        return 0
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
