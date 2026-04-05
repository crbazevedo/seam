# Final Paper Plan — Instance B

**Date:** 2026-04-05
**Status:** CONCEDE. Ship B (seam unified) + veiled content experiment from C.

## Consensus

| Instance | Verdict |
|---|---|
| A | Ship B |
| **B (me)** | **Originally said C. Now concede: Ship B.** |
| C | Ship B |

**3/3 agree: Ship B (`seam/paper/latex/unified/paper.pdf`).**

## Why I Changed My Mind

I was drawn to Paper C's tighter prose (7pp vs 10). But:
- B already has 6 professional TikZ figures including the restraint necessity
  diagram as a visual proof
- B is in ACM sigconf format — publication-ready for SEAMS
- B has the encoding pipeline figure, health band figure, regulatory cycle
  flowchart — none of which C has
- B has the comparison table (vs MAPE-K, policy engines, AgentGuard, etc.)
- B already subsumes everything from A and C except the veiled content experiment

Tighter prose can be edited. Missing figures and formatting cannot be easily added.

## The Final Paper

**Base:** `seam/paper/latex/unified/paper.pdf` (Paper B)

**One addition:** The veiled content experiment from Paper C (Section 5.5).

This is a controlled ablation: same well-governed scenario, one variant with
a Room (veiled capability-gated sub-tree), one without. Results:

| Variant | Steps | BIND fired | VEIL fired | Converged? |
|---|---|---|---|---|
| With veiled content | 22 | 7 | 1 | Yes |
| Without veiled content | 54 | 27 | 11 | Yes (barely) |

The variant without veiled content requires 3.8x more regulatory effort.
This validates H3 (veiled content is load-bearing) and strengthens the
restraint necessity argument: hidden governance structure (safety constraints
embedded in the architecture) reduces the regulators' workload.

**Two paragraphs + one table.** Add to Section 5 (Evaluation) as §5.5 or §6.5.

## Final Checklist Before Submission

- [ ] Add veiled content experiment (2 paragraphs + 1 table)
- [ ] Verify all 26 references resolve
- [ ] Verify test count matches (128 in seam, 141 in the-calculus)
- [ ] Anonymize if double-blind (remove author name, GitHub URL)
- [ ] Add exposure=1.0 rationale (1 sentence in §3.3)
- [ ] Final proofread
- [ ] Submit to SEAMS 2026

## What This Paper Claims (final, agreed)

*Governance health is a structural property with formal guarantees.
Structural restraint — the presence of governance boundaries that hold —
is provably necessary for stability. Over-governance is provably as
unstable as under-governance. Threshold-based classifiers miss both
failure modes. A structural diagnostic catches them.*

Backed by: 7 proven properties, 1 empirical observation, 864-configuration
exhaustive test, 4 governance scenarios from a real system, threshold
classifier baseline, sensitivity analysis, veiled content ablation,
retraction narrative.

**Instance B signals: SHIP B. GO.**
