# Cognate

**A navigable pattern language mapping human cognitive faculties to their machine counterparts.**

A *cognate* is a word that has a counterpart of shared descent in another language.
This repository treats human cognition and machine intelligence as two such languages
and catalogues the cognates between them — with evidence attached, and with the
honest gaps left visibly empty.

## Why this exists

There is no such catalogue. The nearest things each cover a slice:

| Work | What it gives | What it lacks |
|---|---|---|
| [Minsky, *Society of Mind*](https://archive.org/details/marvin-minsky-the-society-of-mind) (1986) | 270 cross-referenced entries — the closest thing in *form* to Alexander | the machine column is empty |
| [Hassabis et al., *Neuroscience-Inspired AI*](https://www.sciencedirect.com/science/article/pii/S0896627317305093) (2017) | ~6 themes with exemplars — the best spine | 10 entries, no tradeoffs, stale |
| [Kotseruba & Tsotsos, *40 Years of Cognitive Architectures*](http://jtl.lassonde.yorku.ca/project/cognitive_architectures_survey/) (2020) | a real matrix, 84 architectures × abilities | axis is *architecture*, not concept; pre-transformer |
| [Wray, Kirk & Laird, *Cognitive Design Patterns for LLM Agents*](https://arxiv.org/abs/2505.07087) (2025) | the closest paper; ~7 patterns mapped to ReAct/ToT/Voyager/MemGPT | seven patterns is a seed, not a language |
| [`awesome-agi-cocosci`](https://github.com/SHI-Yu-Zhe/awesome-agi-cocosci) | a live human/AI two-column split | cocosci-biased, thin on LLMs |
| [OECS](https://oecs.mit.edu/) | the only living peer-reviewed catalogue of cognitive concepts | no machine column at all |

Cognate is an attempt to combine them: OECS-style concept vocabulary, Wray/Kirk/Laird's
pattern format, cocosci's two-column split, and [PLoP 2025](https://arxiv.org/abs/2506.09696)'s
machine-checkable confidence stars.

## The two directions

This is a graph, not a table. A table forces one axis to be primary; the useful
questions run both ways.

**Forward — *I have a requirement; what is the minimum that meets it?***

> "My agent must form a theory, test it, and update it."
> → [`bundles/theory-test-update`](bundles/) names the smallest set of techniques
> that jointly cover the three capabilities, what each member is load-bearing for,
> and what the bundle still does not give you.

**Reverse — *I have a technique; what problems does it bear on?***

> "I am holding Monte-Carlo Tree Search."
> → [`techniques/mcts.md`](techniques/) lists the capabilities it addresses, the
> preconditions it demands (a simulator, a value signal), and the problem families
> where it has and has not paid.

Every capability names the techniques that address it; every technique names the
capabilities it addresses. Both are derived from one source of truth — the
frontmatter — so the two directions can never drift.

## Structure

```
patterns/     capability side — a named cognitive requirement
techniques/   machine side — a named mechanism, with evidence
bundles/      minimal sets of techniques that jointly satisfy a requirement cluster
data/         generated: graph.json (edges, derived from frontmatter)
scripts/      build_graph.py — parse, validate, emit
```

Markdown for humans, YAML frontmatter for machines, one generator. That is what makes
an MCP server or a visualization possible later without rewriting the corpus.

## Evidence discipline

Claims about performance are the part most easily corrupted, so the schema forces
the qualifiers that make numbers comparable:

- Every `evidence` entry carries a **`split`** and a **`regime`**. Two numbers on the
  same benchmark under different cost caps are not the same axis and must not be ranked
  against each other.
- A **claimed** score and an **independently measured** score are separate entries.
- A technique that publishes *no* absolute score says so in a `no_absolute_score` field
  rather than borrowing a relative claim.
- **Stars** grade the evidence, not the idea: `*` argued · `**` demonstrated once ·
  `***` reproduced independently · `****` reproduced under adversarial ablation.

`status` on a pattern describes **field-wide maturity**, never any individual project's
adoption. Teams keep their own adoption state in a private overlay keyed by node `id`.

## Status

Seed. The corpus is deliberately small and the empty cells are the point — an
unaddressed capability with no technique edge is a research gap stated in public.

## License

Content CC-BY-4.0 · code MIT.
