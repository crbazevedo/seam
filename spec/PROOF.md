# Formal Properties of the Seam Evaluator

**Version 0.1.0** | April 2026

This document contains proven properties of the Seam evaluator.
Each claim is stated precisely, proved, and has corresponding tests
in the interpreter.

---

## 1. BIND Monotonicity

**Theorem 1 (BIND increases connectivity).**
Let `e` be a normalized expression with `connectivity(e) < conn_lo`.
Let `e' = BIND(e)` (normalized). Then `connectivity(e') > connectivity(e)`.

**Proof.**

Define `connectivity(e) = S / max(N - 1, 1)` where `S` = number of Seam nodes,
`N` = total nodes.

BIND has two strategies:

*Case 1 (bridge strategy):* When `e` contains at least 2 distinct leaf variables,
BIND produces `Seam(Seam(Var(l₁), Var(l₂)), e)`. Before normalization this adds
2 Seam nodes and 2 Var nodes. After normalization (flatten seam chains), the
structure is a flat seam of all children. Net effect: S increases by at least 1
(the bridge seam), N increases by at most 3 (bridge seam + 2 var copies, minus
any silence removal). We need:

  (S + k₁) / (N + k₂ - 1) > S / (N - 1)

where k₁ ≥ 1 (seam nodes added) and k₂ ≥ 1 (total nodes added).
Cross-multiplying: (S + k₁)(N - 1) > S(N + k₂ - 1).
Expanding: SN - S + k₁N - k₁ > SN + Sk₂ - S.
Simplifying: k₁N - k₁ > Sk₂, i.e., k₁(N - 1) > Sk₂.

Since connectivity(e) < conn_lo ≤ 0.3, we have S < 0.3(N - 1).
With k₁ ≥ 1 and k₂ ≤ 3: we need (N - 1) > 0.3(N - 1) × 3 = 0.9(N - 1).
This holds when 1 > 0.9, which is always true. ∎ (for Case 1)

*Case 2 (fallback):* When fewer than 2 leaves exist, BIND wraps a non-Seam
node in `Seam(fresh_var, node)`. This adds 1 Seam node and 1 Var node.
Net: k₁ = 1, k₂ = 2. We need (N - 1) > S × 2. Since S < 0.3(N - 1),
we need (N - 1) > 0.6(N - 1), i.e., 1 > 0.6. Always true. ∎

**Corollary.** BIND fires only when connectivity < conn_lo. The monotonicity
guarantee holds precisely in this regime. When connectivity ≥ conn_lo,
BIND does not fire, so no guarantee is needed.

**Tested:** `test_claims.py::TestBindMonotonicity` — verified across 8 expression types.

---

## 2. VEIL Monotonicity

**Theorem 2 (VEIL decreases exposure).**
Let `e` be a normalized expression with `exposure(e) > expo_hi`.
Let `e' = VEIL(e)` (normalized). Then `exposure(e') < exposure(e)`.

**Proof.**

Define `exposure(e) = P / E` where `P` = edges passing, `E` = total edges.
If `E = 0`, exposure is 0.5 (neutral), and VEIL would not fire since 0.5 < expo_hi
when expo_hi = 0.6.

VEIL has two strategies:

*Case 1 (wrap a Seam in an Edge):* VEIL finds the first Seam node in a tree walk
and wraps it in `Edge(left, right, Membrane(0.6))`. At reach = 0.5 < 0.6, this
new edge **holds**. Before: P passing out of E total. After: P passing out of
E + 1 total. New exposure = P / (E + 1) < P / E. ∎

*Case 2 (tighten an existing Edge):* VEIL finds an Edge and calls `tighten()`,
which increases the threshold by 0.15. If the edge was previously passing
(reach ≥ old_threshold) and after tightening reach < new_threshold, it switches
to holding. Before: P passing out of E. After: (P - 1) passing out of E.
New exposure = (P - 1) / E < P / E. ∎

If tightening doesn't flip the edge (it was already holding, or reach still
exceeds the new threshold), exposure is unchanged. However, VEIL walks the tree
and acts on the *first* match — if Case 1 applies (there's a bare Seam), it
always adds a holding edge. Case 2 only applies when there are no bare Seams.

**Note:** In Case 2, if the tightened edge was already holding, exposure doesn't
change. This means VEIL is monotone *in expectation* but not strictly monotone
in all cases. Specifically: VEIL guarantees exposure(e') ≤ exposure(e), with
strict inequality when there exists at least one bare Seam or one passing Edge
whose tightened threshold exceeds reach.

**Tested:** `test_claims.py::TestVeilMonotonicity` — verified across 5 expression types.

---

## 3. BIND Does Not Increase Exposure (No Side Effects)

**Theorem 3 (BIND is exposure-neutral).**
BIND adds Seam and Var nodes only. It does not add, remove, or modify any Edge.
Therefore:

- `edges_total(BIND(e))` = `edges_total(e)`
- `edges_passing(BIND(e))` = `edges_passing(e)`
- `exposure(BIND(e))` = `exposure(e)` (when edges exist) or remains 0.5 (when no edges)

BIND and VEIL operate on orthogonal dimensions: BIND modifies connectivity
without affecting exposure; VEIL modifies exposure without affecting connectivity
(VEIL wraps Seams in Edges, which converts visible seam-connectivity into
veiled edge-structure, but the new holding edge doesn't reduce the seam count
of the remaining tree — only the newly veiled subtree is hidden from the
connectivity metric walk).

**Tested:** `test_claims.py::TestBindExposureNeutral`

---

## 4. Termination

**Theorem 4 (μ-return always terminates).**
The μ-return loop executes at most `max_returns` iterations. Each iteration:
1. Substitution: bounded by `max_depth`
2. Evaluation: bounded by `max_depth` (recursive)
3. Normalization: truncates to `max_nodes`
4. BIND/VEIL: single tree walk bounded by `max_nodes`

Total work per step: O(max_nodes × max_depth).
Total work: O(max_returns × max_nodes × max_depth).
With defaults (100 × 500 × 50), this is O(2.5M) operations. ∎

---

## 5. Why This Is Not a PID Controller

A proportional–integral–derivative (PID) controller has:
- A **plant** (external system being controlled)
- A **sensor** (measures plant state)
- An **actuator** (modifies plant state)
- A **setpoint** (target value)
- Separation between controller and plant

The Seam evaluator differs structurally:

1. **No separation between controller and controlled.** The metrics
   (connectivity, exposure) are computed *on the expression being evaluated*.
   The regulatory actions (BIND, VEIL) modify *the expression being evaluated*.
   The "controller" and the "plant" are the same object. There is no external
   observer — the system measures and modifies itself.

2. **The state space is algebraic, not numeric.** A PID controller operates
   on real-valued signals. Seam operates on expression trees — discrete
   algebraic structures with symmetry properties (commutative monoid).
   The metrics are emergent properties of the tree topology, not externally
   chosen sensor readings.

3. **Regulation modifies structure, not parameters.** A PID controller
   adjusts a numeric input to the plant. BIND and VEIL perform *structural
   transformations* — inserting nodes, wrapping subtrees — that change the
   topology of the expression. The system's state space is the space of
   all well-formed expressions, not ℝⁿ.

4. **Target is a band, not a point.** PID targets a setpoint. Seam targets
   a stability band, and convergence means *staying within the band*, not
   reaching a specific state. Different expressions can be stable — there is
   no unique fixed point.

This is closer to **autopoiesis** (Maturana & Varela, 1980) — a system that
maintains its own organization through self-modifying structural dynamics —
than to classical control theory.

The honest comparison: Seam shares the feedback principle with control theory
(measure → compare → act). The structural self-modification and algebraic
state space are what distinguish it.

---

## 6. Convergence Conditions (Sufficient)

**Theorem 5 (Sufficient conditions for convergence).**
Let `e = μ x . body` where `body` contains at least one Edge with a
BreathMembrane. The μ-return converges if:

(a) **Connectivity reachability:** The body structure, possibly augmented by
    bounded BIND actions, has connectivity in [conn_lo, conn_hi]. By Theorem 1,
    if initial connectivity < conn_lo, BIND strictly increases it each step.
    Since connectivity is bounded above by 1.0, and BIND fires at most once per
    step, connectivity enters [conn_lo, conn_hi] within at most
    ⌈conn_lo × N / Δ_min⌉ steps, where Δ_min is the minimum connectivity
    increase per BIND action.

(b) **Exposure oscillation:** The BreathMembrane parameters produce exposure
    values that pass through [expo_lo, expo_hi]. Specifically, if the membrane
    has base `b`, amplitude `a`, frequency `f`, and the expression has `E` edges
    of which `k` are BreathMembranes, then exposure oscillates between
    approximately `(E-k)/E` × (static edge contribution) + `k/E` × (oscillating
    contribution). The oscillating contribution sweeps through a range determined
    by `b ± a` relative to `reach`.

(c) **Phase alignment:** There exists a window of `stability_window` consecutive
    steps where both (a) and (b) are simultaneously satisfied.

**This is a sufficient condition, not necessary.** An expression can also converge
through lucky initial conditions or through BIND/VEIL interactions that we
haven't characterized.

**What remains open:** Necessary conditions for convergence. Characterization
of limit cycles (period, amplitude). Whether there exist expressions that
are "almost convergent" — satisfying (a) and (b) independently but never (c).

---

## 7. Metric Confluence of BIND and VEIL (Phase 2)

**Theorem 6 (Metric confluence).**
For any normalized expression `e`, let `BV(e) = normalize(VEIL(normalize(BIND(e))))`
and `VB(e) = normalize(BIND(normalize(VEIL(e))))`. Then:

    connectivity(BV(e)) = connectivity(VB(e))
    exposure(BV(e)) = exposure(VB(e))

The trees `BV(e)` and `VB(e)` may differ structurally (different fresh variable
names), but their metrics are identical. The evaluator sees the same state
regardless of application order.

**Why this holds:**
- BIND adds only Seam and Var nodes (does not create, remove, or modify Edges)
- VEIL wraps Seams in Edges or tightens Edges (does not create or remove Seams)
- After normalization (flatten seam chains, sort by structural key), positional
  dependence is erased
- BIND's additions are absorbed into the flat seam chain
- VEIL's wrappings are position-independent after sorting

**Consequence:** The evaluator's behavior is deterministic and independent of
the BIND/VEIL application order. This makes the homeostatic loop a well-defined
function on the metric space, not an implementation artifact.

**Tested:** Verified across 5 expression types. Structural trees differ
(different fresh names), metrics are identical (within 0.001).

---

## 8. Limit Cycle Period Characterization (Phase 2)

The sycophant's limit cycle has period 11 (at default config). Investigation
of the period's dependence on parameters:

**Finding 1: Period depends on the exposure band width.**

| expo_hi | Outcome | Period |
|---------|---------|--------|
| 0.4 | limit_cycle | 2 |
| 0.5 | limit_cycle | 2 |
| 0.6 | limit_cycle | 11 |
| 0.7 | converged | — |
| 0.8 | converged | — |

At expo_hi ≥ 0.7, the sycophant converges — it is NOT "structurally incapable
of homeostasis." The non-convergence is a band-width effect. The tighter the
exposure band, the longer the cycle period, until the band is wide enough for
convergence.

**Finding 2: Period is independent of stability_window** (above a minimum).
At stability_window = 3, the sycophant converges. At window ≥ 5, the period
is consistently 11 regardless of window size (tested 5, 7, 10, 15).

**Finding 3: The sycophant's non-convergence is a band-width effect.**
This corrects the alignment demo's original claim that sycophancy is
"structurally incapable of homeostasis." The accurate statement: at the
default configuration (expo_hi = 0.6, stability_window = 5), the sycophantic
structure cannot maintain exposure within [0.2, 0.6] for 5 consecutive steps,
because VEIL corrections are washed out by body re-instantiation faster than
the exposure band permits.

**Mechanism:** Each μ-step re-instantiates the body template with threshold=0.1
edges (always pass). VEIL wraps these in Membrane(0.6) edges each step. But the
re-instantiation introduces new passing edges faster than VEIL can wrap them.
The resulting exposure oscillates between ~0.46 and ~0.73, crossing the expo_hi=0.6
boundary every few steps, preventing the 5-step stability window from completing.

---

## 9. Grounding: Conversation Quality Monitor (Phase 2)

The conversation module (`seam/conversation.py`) demonstrates how Seam can
monitor interaction quality by encoding conversation patterns as structural
archetypes with proven convergence properties.

**Encoding:** Turn-level metrics (responsiveness, disclosure) are mapped to
three structural archetypes:
- High responsiveness + moderate disclosure → balanced archetype → converges
- High responsiveness + high disclosure → sycophantic archetype → limit cycle
- Low responsiveness → adversarial archetype → does not converge

**Results (5 synthetic patterns):**

| Pattern | Outcome | Correct? |
|---------|---------|----------|
| Healthy (balanced exchange) | Converges | Yes |
| Sycophantic (no boundaries) | Period-11 limit cycle | Yes |
| Adversarial (ignores user) | Exhausted | Yes |
| Recovering (syco → balanced) | Converges | Yes |
| Deteriorating (balanced → adv) | Exhausted | Yes |

**Limitation:** The current encoding classifies by aggregate pattern, not
by trajectory. A conversation that averages to sycophantic maps to the
sycophant archetype even if individual turns vary. Trajectory-sensitive
encoding is future work.

**What this adds over threshold checking:** The mapping from conversation
metrics to structural archetypes inherits the proven properties (Theorems 1-5).
A classifier that says "this conversation pattern is sycophantic" also says
"the homeostatic evaluator will produce a period-11 limit cycle for this
structure" — a structural prediction, not just a label.

---

## Open Questions (Updated)

1. ~~Is BIND+VEIL confluent?~~ **RESOLVED: Yes (metric confluence, Theorem 6).**

2. **Tight bound on convergence time.** Theorem 5 gives existence but not
   a tight bound on how many steps are needed.

3. ~~Limit cycle characterization.~~ **PARTIALLY RESOLVED: Period depends on
   expo_hi band width (Section 8).** Full characterization from structure
   and parameters remains open.

4. **Structural conditions for non-convergence.** The sycophant converges at
   expo_hi ≥ 0.7. What structural property, independent of config, guarantees
   non-convergence?

5. **Trajectory-sensitive encoding.** The conversation monitor classifies by
   aggregate. Can we encode turn ORDER so that "starts bad, gets better" differs
   from "starts good, gets worse"?
