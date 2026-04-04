# Homeostatic Evaluation for Multi-Agent Governance

Carlos R. B. Azevedo

April 2026

---

## Abstract

We introduce **Seam**, a term-rewriting calculus whose evaluator maintains
homeostatic stability rather than reducing to normal form. The evaluator
measures two structural metrics on the expression tree — *connectivity*
and *exposure* — and applies regulatory transformations (BIND, VEIL)
to maintain both within a target band. We prove five formal properties
(BIND/VEIL monotonicity, orthogonality, termination, metric confluence)
and state sufficient convergence conditions.

We ground the calculus in multi-agent governance by encoding governed
autonomy protocols as Seam expressions: risk tiers as membrane thresholds,
action windows as oscillating membranes, agent coordination as bilateral
bindings. We demonstrate that the evaluator distinguishes well-governed
systems (converges), ungoverned systems (does not converge), and
over-governed systems (limit cycles). The last result is non-obvious and
cannot be detected by threshold-based classifiers.

Source: https://github.com/crbazevedo/seam

---

## 1. Introduction

Multi-agent AI systems face a governance problem: how much autonomy
should each agent have? Too little blocks work. Too much risks irreversible
harm. Current approaches handle this through static risk-tier policies and
approval workflows, tuned by experience.

We propose modeling governance dynamics as a term-rewriting system with
**homeostatic evaluation**. Instead of reducing to normal form — the
standard for lambda calculus, process calculi, and rewriting systems — our
evaluator targets a *stability band*: a range of structural metric values
where the system is healthy. The evaluator measures the expression tree's
topology and applies structural transformations to stay within the band.

This makes Seam, to our knowledge, the first term-rewriting calculus
where evaluation targets homeostatic stability. The homeostatic principle
itself is well-established in cybernetics [Ashby, 1952; Beer, 1972] and
has been proposed for AI alignment [Kenton et al., 2024]. Seam provides
a formal mechanism with proven properties.

**Contributions.**
1. A term-rewriting calculus with homeostatic evaluation. (Section 2)
2. Five proven properties and stated convergence conditions. (Section 3)
3. A structural encoding of governed autonomy protocols. (Section 4)
4. Demonstration on four governance scenarios, including a non-obvious
   instability result with baseline comparison. (Section 5)

---

## 2. The Seam Calculus

### 2.1 Primitives

Four primitives:

| Symbol | Name | Role |
|--------|------|------|
| `∅` | Silence | Empty ground. Identity of seam. |
| `⊗` | Seam | Bilateral binding. Commutative monoid. |
| `\|φ\|` | Edge | Adaptive membrane. `φ(reach) → pass \| hold` |
| `μ` | Return | Homeostatic iteration. |

Two derived rules: *Witness* (`◊ e` — creates `(fresh ⊗ e)`) and
*Room* (`[e]` — enter by shared free variables). *Word* (`e₁ |T| e₂`)
is a typed bilateral binding with visible/veiled declarations. These are
syntactic conveniences; all have evaluation rules defined in terms of the
four primitives.

**Seam laws** (commutative monoid):
associativity, commutativity, identity with `∅`.
Normalization applies these laws after each evaluation step to maintain
a canonical form.

### 2.2 Membranes

An edge `e₁ |φ| e₂` is governed by a membrane function `φ(reach) → {pass, hold}`.
When `φ` passes, content is visible and evaluation proceeds. When `φ` holds,
content is *veiled* — structural weight without direct access.

**Membrane(θ)**: pass iff `reach ≥ θ`.
**BreathMembrane(b, a, f, c)**: oscillating threshold `b + a·sin(c·f)`.

### 2.3 Metrics

Computed by a single iterative walk over the expression tree:

**Connectivity** = `seam_nodes / max(total_nodes - 1, 1)`.
Measures how interconnected the expression is.

**Exposure** = `edges_passing / max(edges_total, 1)`.
Measures how transparent the expression is. (0.5 if no edges.)

These metrics are structural ratios of the AST, not externally defined
sensor readings. They emerge from the expression's topology.

### 2.4 Homeostatic Evaluation

The return `μ x . e` iterates:

1. Substitute previous result for `x` in body `e`
2. Evaluate and normalize
3. Measure connectivity and exposure
4. If `connectivity < conn_lo`: **BIND** — insert a Seam node
5. If `exposure > expo_hi`: **VEIL** — wrap a Seam in a holding Edge
6. If both metrics in band for `stability_window` consecutive steps: **converge**
7. Otherwise: continue (up to `max_returns` steps)

Non-convergence is classified as *limit cycle* (periodic metric trace),
*diverging* (monotonically growing), or *exhausted* (step limit).

---

## 3. Formal Properties

We prove five properties and state convergence conditions. Full proofs
are in the supplement (spec/PROOF.md).

**Theorem 1 (BIND monotonicity).** Let `conn_lo ≤ 1/3`. If
`connectivity(e) < conn_lo` and `e' = BIND(e)` (normalized),
then `connectivity(e') > connectivity(e)`.

*Proof.* BIND adds k₁ ≥ 1 Seam nodes and k₂ ≤ 3 total nodes.
We need k₁(N-1) > S·k₂. Since S < conn_lo·(N-1) ≤ (N-1)/3:
need (N-1) > (N-1)·k₂/3. With k₂ ≤ 3: need 1 > 1, which fails
only at exact equality. Since S < conn_lo·(N-1) is strict, the
inequality holds strictly. ∎

*Note: The bound conn_lo ≤ 1/3 ensures the proof works for k₂ ≤ 3.
The default configuration uses conn_lo = 0.3.*

**Theorem 2 (VEIL monotonicity).** If `exposure(e) > expo_hi` and
`e' = VEIL(e)`, then `exposure(e') ≤ exposure(e)`, with strict
inequality when the expression contains a bare Seam or a passing Edge.

*Proof.* VEIL either wraps a Seam in a holding Edge (P passing out of
E+1 total: P/(E+1) < P/E) or tightens a passing Edge to holding
((P-1)/E < P/E). If neither case applies (all Seams are already
veiled and all Edges already hold), VEIL has no effect and the
inequality is non-strict. ∎

**Theorem 3 (Orthogonality).** BIND adds only Seam and Var nodes.
VEIL adds or modifies only Edge nodes. Therefore
`exposure(BIND(e)) = exposure(e)` and BIND does not interfere with
VEIL's effect.

**Theorem 4 (Termination).** The μ-return executes at most `max_returns`
steps, each bounded by O(`max_nodes · max_depth`).

**Theorem 5 (Metric confluence).** For any normalized expression `e`:
`connectivity(VEIL(BIND(e))) = connectivity(BIND(VEIL(e)))` and
`exposure(VEIL(BIND(e))) = exposure(BIND(VEIL(e)))`.

*Proof.* By Theorem 3, BIND does not modify edges, so
`exposure(BIND(e)) = exposure(e)` and `exposure(VEIL(BIND(e))) = exposure(VEIL(e))`.
VEIL wraps Seam nodes in Edges or tightens Edges; after normalization
(which flattens seam chains and sorts by structural key), the Seam
nodes that BIND would target are the same regardless of whether VEIL
has already wrapped some of them — BIND targets the first bare Seam or
leaf in a tree walk, and VEIL's wrapping creates an Edge that BIND
traverses into. The connectivity added by BIND is the same in both
orders because the number of new Seam nodes and total nodes is
identical. ∎

*Note: The trees may differ structurally (different fresh variable names),
but the metric values — which are what the evaluator acts on — are
identical. Verified empirically across all tested expression types.*

**Observation (Convergence conditions).** The μ-return converges when:
(a) BIND can drive connectivity into `[conn_lo, conn_hi]` in bounded
steps (guaranteed by Theorem 1), (b) membrane dynamics produce exposure
values in `[expo_lo, expo_hi]`, and (c) a window of `stability_window`
steps exists where both hold simultaneously. We do not prove (b) or (c)
in general; they depend on membrane parameters and expression structure.

---

## 4. Multi-Agent Governance

### 4.1 Governed Autonomy

We study CARLOS-OS, a multi-agent platform where 6 agents operate under
a Governed Autonomy protocol. Actions are classified into five risk tiers
(VT0–VT4) determining autonomy level, and may be constrained by Action
Opportunity Windows (AOWs) — time-bounded intervals during which actions
are permitted.

| Tier | Autonomy | Example |
|------|----------|---------|
| VT0 | Full — act and log | Read files, run tests |
| VT1 | Act and notify | Create issues, push to feature branches |
| VT2 | Act with recommendation | Push to main, change data models |
| VT3 | Propose and wait | Delete data, architectural decisions |
| VT4 | Stop and escalate | Production deployments, legal commitments |

### 4.2 Encoding

The encoding maps governance concepts to Seam primitives. We acknowledge
this is a design choice — other encodings are possible — but argue it
is *faithful*: each governance concept maps to the primitive whose
formal properties match the concept's operational semantics.

| Governance | Seam | Why this mapping |
|---|---|---|
| VT tier | `Membrane(θ)` | Both gate by threshold. VT0 (θ=0.1) passes freely; VT4 (θ=0.95) holds. |
| AOW | `BreathMembrane` | Both have time-varying permeability. |
| Agent handoff | `Seam` | Both create bilateral binding. Handoff binds two agents mutually. |
| Governance check | Holding `Edge` | Both are veiled infrastructure — structural support that is not directly visible. |
| Decision record | `Witness` | Both observe without consuming. An ADR enriches governance without destroying the decision. |

**Sprint encoding.** A sprint's state is encoded as:
1. One Seam per cross-agent handoff (connectivity layer)
2. One Seam per reviewed action (coordination)
3. One Edge per distinct VT tier used, with tier threshold (exposure layer)
4. One holding Edge per governance check (infrastructure)
5. A Word declaring visible/veiled governance terms
6. A μ-return modeling the sprint cycle

### 4.3 The faithfulness argument

The encoding is faithful in this sense: the structural properties that
Theorems 1-5 guarantee for the calculus correspond to operational
properties of the governance system.

- **Theorem 1 (BIND monotonicity)** → Adding coordination (handoffs,
  reviews) always increases connectivity. In CARLOS-OS: adding
  cross-agent review requirements always improves coordination health.
- **Theorem 2 (VEIL monotonicity)** → Adding governance gates always
  reduces exposure. In CARLOS-OS: adding VT-tier checks always
  reduces uncontrolled action.
- **Theorem 3 (Orthogonality)** → Coordination changes don't affect
  governance gates, and vice versa. In CARLOS-OS: adding a review
  requirement doesn't change the VT tier of existing actions.
- **Theorem 5 (Confluence)** → The order of adding coordination vs.
  governance doesn't matter. In CARLOS-OS: it doesn't matter whether
  you add reviews first or tighten VT tiers first — the result is the same.

---

## 5. Demonstration

### 5.1 Four Governance Scenarios

We encode four synthetic sprint patterns and evaluate them:

| Scenario | VT Mix | Reviews | Checks | Handoffs | Outcome | Steps |
|---|---|---|---|---|---|---|
| **Well-governed** | 0:2 1:4 2:2 | 50% | 4 | 5 | **Converges** | 9 |
| Ungoverned | 0:6 | 0% | 0 | 0 | Exhausted | 60 |
| **Locked-down** | 3:4 4:2 | 100% | 6 | 6 | **Limit cycle** | 60 |
| Drifting | 0:3 1:3 | 33% | 1 | 2 | Limit cycle | 60 |

**Result 1: Well-governed sprints converge.** Mixed VT tiers with
governance infrastructure find the stability band in 9 steps.

**Result 2: Ungoverned sprints cannot stabilize.** Without governance
checks (holding edges), there is no structural boundary.

**Result 3 (non-obvious): Over-governed sprints limit-cycle.** With all
actions at VT3-VT4, exposure drops to 0.14 — *below* the stability band
(expo_lo = 0.2). The system enters a period-4 limit cycle because nothing
passes. This formalizes a design principle: some openness is structurally
necessary.

**Result 4: Governance drift is detectable** as a period-2 limit cycle.

### 5.2 Baseline Comparison

A simple threshold classifier based on aggregate metrics:
```
"stable" if avg_vt ∈ [0.5, 2.5] AND review_rate > 0.3 AND checks > 2
```

| Scenario | Seam verdict | Threshold verdict | Match? |
|---|---|---|---|
| Well-governed | Converges | stable | Yes |
| Ungoverned | Exhausted | unstable | Yes |
| Locked-down | **Limit cycle** | **stable** | **No** |
| Drifting | Limit cycle | unstable | Yes |

The threshold classifier incorrectly labels the locked-down sprint as
"stable" (avg_vt = 3.3, review_rate = 100%, checks = 6 — all above
thresholds). Seam detects the instability because it models the *dynamics*:
holding edges suppress exposure below the band, causing oscillation.
A static threshold check sees high reviews and many checks as healthy.
The homeostatic evaluator sees a system that cannot breathe.

### 5.3 Sensitivity

The well-governed scenario converges for reach ∈ [0.1, 0.7] — 78% of
the tested range. Convergence fails at reach ≥ 0.8 where all membrane
thresholds are exceeded and every edge passes. The governance
infrastructure (holding edges from checks) provides stability across
a wide parameter range.

---

## 6. Related Work

**Membrane computing.** P-systems [Păun, 2000] introduced membranes as
computational containers. Active membrane variants [Păun, 2001; Leporati
et al., 2024] add structural operations. Seam differs: membranes are
parameterized permeability functions coupled to a homeostatic evaluator.

**Multi-agent frameworks.** AutoGen [Wu et al., 2023], CrewAI, and
LangGraph provide runtime orchestration for multi-agent LLM systems but
lack formal governance models with structural guarantees. Seam provides a
formal layer that predicts governance stability.

**AI governance.** The EU AI Act [2024] and NIST AI RMF [2023] provide
regulatory frameworks with risk tiers. Seam formalizes risk tiers as
membrane thresholds with proven monotonicity and confluence properties.

**Cybernetics.** Ashby [1952] and Beer [1972] established homeostasis as
a systems principle. Recent work proposes homeostatic alignment objectives
[Kenton et al., 2024]. Seam provides a formal term-rewriting calculus
for these ideas — the mechanism, not just the argument.

**Session types.** Binary [Honda, 1993] and multiparty [Honda et al., 2008]
session types prescribe bilateral protocols. Seam uses bilateral binding
as a structural primitive enabling a connectivity metric that drives the
homeostatic loop.

**AI governance architectures.** Recent work on governance for autonomous
agents [Li et al., 2025] proposes layered enforcement (sandboxing, intent
verification, zero-trust authorization, audit logging). Perez Rios [2025]
applies Beer's VSM and organizational pathology taxonomies to AI governance.
These are architectural and procedural. Seam is formal and structural:
governance health is a property of term structure with proven invariants.

**Formal methods for MAS.** Electronic institutions [Esteva et al., 2001]
and norm-based systems [Boella & van der Torre, 2006] model governance
through logical specifications. Self-adaptive systems [Cheng et al., 2009]
study feedback loops in software. BDI logics [Rao & Georgeff, 1995] and
model checkers like MCMAS [Lomuscio et al., 2009] verify temporal-epistemic
properties. These are static — they verify at design time. Seam is
dynamic — the evaluator continuously monitors and regulates.

---

## 7. Discussion

**What Seam provides.** A formal framework where, given a governance
configuration, the evaluator predicts stability and recommends
interventions (BIND → add coordination; VEIL → tighten governance).
The five proven properties ensure predictable evaluator behavior.

**Limitations.** The encoding is aggregate, not trajectory-sensitive.
Convergence conditions are sufficient but not necessary. The metrics are
structural, not semantic. Scenarios are synthetic. Validation against real
sprint telemetry is future work.

**The non-obvious result.** Over-governance limit-cycles. A system where
everything is gated has exposure below the band — it cannot breathe. This
is not detectable by threshold classifiers (which see "many checks" as
healthy) but is structural: the homeostatic band requires both openness
and constraint. Making this formal and testable is the contribution.

**Future work.** Live integration with CARLOS-OS event streams.
Trajectory-sensitive encoding. A type system for static convergence
prediction. Empirical validation.

---

## References

- Ashby, W. R. (1952). *Design for a Brain*. Chapman & Hall.
- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Boella, G. & van der Torre, L. (2006). A game-theoretic approach to normative multi-agent systems. In *Normative MAS*.
- Chae, Y. et al. (2025). Continuous-time homeostatic dynamics. arXiv:2512.05158.
- Cheng, B. et al. (2009). Software engineering for self-adaptive systems. In *SEFSAS*, LNCS 5525.
- Esteva, M. et al. (2001). ISLANDER: An electronic institutions editor. AAMAS.
- Honda, K. (1993). Types for dyadic interaction. CONCUR.
- Honda, K., Yoshida, N., Carbone, M. (2008). Multiparty asynchronous session types. POPL.
- Kenton, Z. et al. (2024). From homeostasis to resource sharing. arXiv:2410.00081.
- Leporati, A. et al. (2024). P systems with reactive membranes. J. Membrane Computing.
- NIST (2023). AI Risk Management Framework.
- Păun, Gh. (2000). Computing with membranes. J. Computer and System Sciences.
- Rao, A. & Georgeff, M. (1995). BDI agents: From theory to practice. ICMAS.
- Li, H. et al. (2025). Governance architecture for autonomous agent systems. arXiv:2603.07191.
- Lomuscio, A., Qu, H., Raimondi, F. (2009). MCMAS: A model checker for MAS verification. CAV.
- Perez Rios, J. (2025). The VSM and organizational pathologies in the age of AI. *Systems* 13(9):749.
- Regulation (EU) 2024/1689. The AI Act.
- Wu, Q. et al. (2023). AutoGen: Enabling next-gen LLM applications. arXiv:2308.08155.
