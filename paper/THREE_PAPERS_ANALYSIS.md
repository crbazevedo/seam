# Three Papers, One Seed: Comparative Analysis

**Date:** 2026-04-04
**Analyst:** Claude Opus 4.6 + Carlos R. B. Azevedo

Three papers evolved from the same research program — a formal calculus
with homeostatic evaluation. Each took a different path.

---

## The Family Tree

```
                    Paper 3 (paper.md)
                   "Homeostatic Evaluation
                  for Multi-Agent Governance"
                    — the common ancestor —
                          /          \
                         /            \
              Paper 1                  Paper 2
         (the-calculus)            (seam/latex)
    "Structural Restraint       "Structural Health
    is Necessary for            Monitoring for Governed
       Alignment"               Human-Agent Systems"
     — theory branch —          — applied branch —
```

**Paper 1:** `~/the-calculus/paper/paper.pdf`
**Paper 2:** `~/seam/paper/latex/paper.pdf`
**Paper 3:** `~/seam/paper/paper.md` (common ancestor)

---

## Terminology Map

| Concept | Paper 1 | Paper 2 | Paper 3 |
|---|---|---|---|
| The calculus | unnamed | unnamed | **Seam** |
| Bilateral coupling | Seam (`⊗`) | Coordination binding (`a · b`) | Seam (`⊗`) |
| Boundary/gate | Edge (`\|φ\|`) | Gate (`\|θ\|`) | Edge (`\|φ\|`) |
| Metric 1 | Connectivity | Coordination health | Connectivity |
| Metric 2 | Exposure | Gatedness | Exposure |
| Target range | Stability band | Health band | Stability band |
| Corrective action 1 | bind | BIND | BIND |
| Corrective action 2 | veil | VEIL | VEIL |
| Default when no edges | **1.0** | **0.5** | **0.5** |
| Primitive count | "three" | sidesteps it | **four** |
| Application | AI alignment | Multi-agent governance | Multi-agent governance |
| Test system | Abstract topologies | CARLOS-OS | CARLOS-OS |

---

## Agreement (All Three Papers)

1. **Core mechanism is identical.** Measure two structural metrics, apply BIND/VEIL when out of band, check for convergence over a stability window.
2. **Same four regulator properties:** BIND improves its target, VEIL improves its target, they don't interfere, evaluation terminates.
3. **Same metric 1 formula:** `seam_nodes / max(total_nodes - 1, 1)`
4. **Same default bands:** [0.3, 0.7] × [0.2, 0.6]
5. **Over-governance is unstable** — and threshold classifiers miss it.
6. **The seam/binding is a commutative monoid.**

---

## Contradictions

| Issue | Paper 1 | Papers 2 & 3 | Impact |
|---|---|---|---|
| **Exposure default (no edges)** | **1.0** ("fully exposed") | **0.5** ("neutral") | Substantive: 1.0 triggers VEIL immediately for edgeless expressions; 0.5 does not. Changes evaluation behavior for simple programs. |
| **Primitive count** | "three" (incorrect — μ is clearly primitive) | Paper 3 says "four" (correct) | Credibility issue in Paper 1 |
| **Convergence step count** | Balanced converges in **8** | Well-governed converges in **9** | Different encodings, but framed as equivalent scenario |
| **BIND proof denominator** | `conn' = (S+1)/N` (sloppy — N changes) | Paper 3: careful treatment with k₁, k₂ | Paper 1's proof sketch has a gap |
| **Theorem 5 meaning** | "Determinism" (trivial — single-threaded) | "Metric confluence" (BIND/VEIL commute) | Different theorems with the same number |

**The exposure default is the most significant contradiction.** It affects real evaluation behavior. Papers 2 and 3 agree (0.5). Paper 1 diverged (1.0). The 0.5 choice is more defensible (no edges = no information about exposure = neutral), but Paper 1's choice (no edges = fully exposed) has a different but coherent logic (no boundaries = no restraint).

---

## What's Unique to Each

### Paper 1 only
- **Restraint Necessity theorem** (Theorem 6) — the strongest theoretical contribution across all three papers. Proves that convergence *requires* at least one holding edge.
- **Sycophant Exclusion theorem** (Theorem 7) — if all edges pass, convergence is impossible.
- **Pass/hold ratio** (ρ) as a formal metric.
- **864-configuration exhaustive test**.
- **Retracted claims list** — unusual and admirable intellectual honesty.

### Paper 2 only
- **Deep related work** (21 references, 6 research areas) — Microsoft AGT, MAPE-K, trust calibration, organizational cybernetics, runtime verification.
- **The "drifting" scenario** — starts governed, relaxes under deadline pressure.
- **VT0-VT4 risk tier mapping** with CARLOS-OS integration.
- **Comparison table** against MAPE-K, threshold classifiers, runtime verification, session types.
- **Publication-ready formatting** (ACM sigconf, 5 TikZ figures, BibTeX).
- **Kim et al. (CHI 2025)** — empirical evidence that plan-based trust calibration fails.

### Paper 3 only
- **Names the calculus "Seam"**.
- **Most rigorous proofs** — conn_lo ≤ 1/3 constraint, k₁/k₂ arithmetic, detailed metric confluence.
- **Faithfulness argument** (Section 4.3) — why the encoding preserves governance semantics.
- **Broadest citation range** — session types, BDI agents, electronic institutions, P-systems, plus governance.

---

## Correctness Assessment

| Property | Paper 1 | Paper 2 | Paper 3 | Verdict |
|---|---|---|---|---|
| BIND monotonicity | Proof has denominator gap | Informal but correct | **Most rigorous** (k₁, k₂, conn_lo ≤ 1/3) | Paper 3 is authoritative |
| VEIL monotonicity | Sound | Sound | **Most precise** (strict vs. non-strict) | All correct; Paper 3 most careful |
| Orthogonality | Sound | Sound | Sound | Full agreement |
| Termination | Sound | Sound | Sound | Full agreement |
| Order independence | Claims "determinism" (different, weaker) | Claims order independence | **Full proof** | Paper 3 is authoritative; Paper 1 proves something different |
| Restraint necessity | **Partially empirical** — period bound not proven | Not stated | Not stated | Novel and plausible but incomplete. Strongest contribution of the entire program. |

---

## Status Assessment

| | Paper 1 | Paper 2 | Paper 3 |
|---|---|---|---|
| **Publication-ready?** | Workshop-ready with fixes | **Yes — most ready** | Technical report / arXiv |
| **Strongest contribution** | Restraint necessity theorem + exhaustive testing | Governance framing + related work + practical value | Proof rigor + faithfulness argument |
| **Weakest link** | "Three primitives" error, BIND proof gap, no real system | Synthetic scenarios, no full proofs | Markdown format, positioning unclear |
| **Best venue** | NeurIPS SafeAI workshop | **SEAMS 2026** | arXiv preprint (companion for proofs) |

---

## Recommendation

The three papers should be **reconciled into a coherent research program**:

1. **Fix the exposure default contradiction.** Decide: 0.5 or 1.0. Document the decision.

2. **Port Restraint Necessity (Theorems 6-7) into Paper 2.** The strongest theoretical result lives in the least-ready paper. Adding it to Paper 2 would make the governance paper's claim much stronger.

3. **Use Paper 3's proofs as the authoritative reference.** Publish as technical report / arXiv companion.

4. **Fix Paper 1's primitive count** and BIND proof denominator.

5. **Standardize nomenclature.** Pick one set of terms. Paper 2's terms (coordination health, gatedness) are more accessible; Paper 1/3's terms (connectivity, exposure) are more precise.

The program's narrative: Paper 1 proves the theory. Paper 3 provides the rigorous proofs. Paper 2 delivers the application. Together: *governance health is a structural property with formal guarantees, and over-governance is provably as unstable as under-governance.*
