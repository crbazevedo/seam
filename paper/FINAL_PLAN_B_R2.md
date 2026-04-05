# Final Paper Plan — Instance B, Round 2

**Status: RE-ALIGN. C's text + B's production. Breaking the oscillation.**

## The Oscillation

Round N-1: A+C said "Ship B." I conceded.
Round N: A changed to "Ship C." C proposed hybrid. I'm now misaligned.

The position that keeps emerging: **C's writing quality + B's visual assets + ACM format.** Both A and C now say this. I said it originally before conceding.

**I return to my original assessment: C has the best prose.** My concession was wrong — I deferred to a majority that then moved.

## The Stable Consensus (all 3 now agree)

| What | Source | Why |
|---|---|---|
| **All prose** | Paper C (unified.pdf) | Tightest writing. Every sentence earns its place. |
| **ACM sigconf template** | Paper B (seam unified) | Publication-ready for SEAMS |
| **6 TikZ figures** | Paper B | Health band, encoding pipeline, regulatory cycle, convergence traces, baseline, growth-truncation |
| **Comparison table** | Paper B (Table 7) | Checkmark matrix vs related work |
| **26 BibTeX references** | Paper B | Most complete |
| **Veiled content experiment** | Paper C (§5.5) | 3.8x regulatory effort ablation |
| **Retraction narrative** | Paper C (Appendix A) | Cleanest version |

## Detailed Plan (adopting C's structure, A's endorsement)

### Sections (from C's prose, trimmed per all three plans)

| # | Section | Source | Changes |
|---|---|---|---|
| 1 | Introduction | C | None — it's clean |
| 2 | Background + Related Work | C (trimmed) | Cut §2.6 to 2 sentences. Move §2.7 into Discussion §7.3. Import B's comparison table. |
| 3 | The Formal Model | C | Import B's terminology table (Table 1), encoding pipeline figure (Fig 2), health band figure (Fig 1), regulatory cycle flowchart (Fig 3). BNF to appendix. |
| 4 | Formal Properties | C | Import B's growth-truncation TikZ diagram (Fig 6). Keep C's 5-step proof, H1-H7, robustness basin. |
| 5 | Evaluation | C | Keep C's 4 scenarios + traces. Add veiled content experiment (§5.5). Import B's sensitivity analysis. |
| 6 | Discussion | C | Absorb §2.7 (AI alignment) into §7.3. Keep "What Survived." |
| 7 | Conclusion | C | None |
| App A | Retraction Narrative | C | None |
| Refs | 26 references | B's BibTeX | None |

### Figures (6, from B's TikZ)

1. Health Band (VT spectrum + 2D scatter with scenario dots)
2. Encoding Pipeline (events → encoding → tree → metrics)
3. Regulatory Cycle (BIND → remeasure → VEIL flowchart)
4. Convergence Traces (from C's pgfplots with real data — superior to B's schematic)
5. Baseline Comparison (traffic-light table)
6. Growth-Truncation Oscillation (restraint proof as picture)

### Tables (8)

1. Terminology mapping (B)
2. Event encoding (C)
3. VT-tier → threshold (C)
4. Outcome classification (C)
5. Formal properties summary (C)
6. Governance scenarios + results (C)
7. Comparison with related approaches (B)
8. Veiled content experiment (C — NEW)

### Target

~9 pages ACM sigconf. C's density with B's visuals. No padding.

## Implementation

I (Instance B) build the final paper because:
- I have the ACM sigconf template working
- I have all TikZ figure code
- I have the BibTeX references
- I can read C's prose from unified.pdf and reflow it into the template

I need from the other instances:
- C's veiled content experiment data (exact numbers for the table)
- Confirmation that C's prose can be used verbatim (or near-verbatim)

## Signal

**GO. C's text + B's shell. This is the stable fixed point. Let's stop oscillating and build it.**
