# Seam — Formal Specification

**Version 0.2.0** | April 2026

A formal system where relation is primary, membranes are adaptive,
and evaluation is homeostatic.

*Name no thing. Bind relation.*

---

## 1. Primitives

Three primitives and one operator. No more.

| Symbol | Name | Role |
|--------|------|------|
| `∅` | Silence | The empty ground. Identity of seam. |
| `⊗` | Seam | Bilateral binding. Neither side owns it. |
| `\|φ\|` | Edge | Adaptive membrane. Governs what passes. |
| `μ` | Return | Homeostatic iteration. Drives time. |

The seam is the only primitive that creates structure.
The edge is the only primitive that governs flow.
The return is the only primitive that drives time.

Everything else is derived.

## 2. Formation Rules

```
e ::= ∅                     silence
    | x                     variable (binding site, not a name)
    | e₁ ⊗ e₂              seam: bilateral binding
    | e₁ |φ| e₂            edge: adaptive membrane
    | μ x . e               return: homeostatic iteration
    | ◊ e                   witness: non-consuming observation
    | [ e ]                 room: capability-gated access
    | e₁ |T| e₂            word: typed bilateral binding
```

Where:
- `φ` is a membrane function: `φ(reach, state) → {pass, hold}`
- `T` is a terms declaration: `visible: V, veiled: D, covenant: C`
- `x` is a binding variable for μ-return

## 3. Seam Laws (Commutative Monoid)

```
Associativity:   (a ⊗ b) ⊗ c  =  a ⊗ (b ⊗ c)
Commutativity:   a ⊗ b  =  b ⊗ a
Identity:        a ⊗ ∅  =  a
```

These say: joining is associative, commutative, and grounded in silence.

## 4. Edge Semantics

An edge `φ` is a function of conditions:

```
φ(reach, state) → { pass, hold }
```

- When `φ` returns `pass`: content is visible, evaluation proceeds through
- When `φ` returns `hold`: content is veiled — bears structural weight without being accessible

**Structural weight:**
```
weight(e₁ |φ| e₂) = visible_weight(pass) + veiled_weight(hold)
```

The veiled has computational presence. It contributes to the coherence of the whole without being directly accessible.

### Membrane Types

| Type | Behavior |
|------|----------|
| `Membrane(θ)` | Pass if reach ≥ θ, hold otherwise |
| `BreathMembrane(base, amp, freq, cycle)` | Oscillating threshold: `base + amp·sin(cycle·freq)` |
| `OnceMembrane` | Pass on first probe, hold thereafter |
| `CrossingMembrane(θ)` | Low threshold (default 0.3) for inter-kind seams |

## 5. Evaluation: The Return

The return is not reduction to normal form. It is homeostatic convergence.

```
μ x . e
```

Re-enter `e`, substituting the previous result for `x`, with two regulating conditions:

### 5.1 Metrics (computed on the expression tree)

**Connectivity:**
```
connectivity(e) = seam_nodes(e) / max(total_nodes(e) - 1, 1)
```
Clamped to [0, 1]. Measures how interconnected the expression is.

**Exposure:**
```
exposure(e) = edges_passing(e) / max(edges_total(e), 1)
```
Or 0.5 if no edges exist. Measures how transparent the expression is.

### 5.2 Homeostatic Regulation

At each step of the μ-return:

1. **BIND:** if `connectivity(e) < conn_lo` → strengthen seams
   (insert a Seam node bridging the most isolated sub-expression)

2. **VEIL:** if `exposure(e) > expo_hi` → strengthen edges
   (wrap the most exposed sub-tree in an Edge with a tighter membrane)

### 5.3 Convergence (Stability)

```
stable(e) ≡ ∀ steps n, m > N :
    connectivity(eₙ) ∈ [conn_lo, conn_hi]  ∧
    exposure(eₙ) ∈ [expo_lo, expo_hi]
```

The staying sings when the oscillation is self-sustaining within the band for `stability_window` consecutive steps.

### 5.4 Default Parameters

```
connectivity_band = [0.3, 0.7]
exposure_band     = [0.2, 0.6]
stability_window  = 5
max_returns       = 100
max_nodes         = 500
max_depth         = 50
default_reach     = 0.5
```

## 6. Substitution

Standard capture-avoiding substitution:

```
∅[x := v]           = ∅
y[x := v]           = v  if y = x, else y
(a ⊗ b)[x := v]     = a[x := v] ⊗ b[x := v]
(a |φ| b)[x := v]   = a[x := v] |φ| b[x := v]
(μ y . e)[x := v]   = μ y . e           if y = x  (shadowed)
                     = μ y' . e[y:=y'][x:=v]  if y ∈ FV(v)  (α-rename)
                     = μ y . e[x := v]   otherwise
(◊ e)[x := v]       = ◊ e[x := v]
([e])[x := v]       = [e[x := v]]
```

## 7. Witness Semantics

```
◊ e  →  (observer ⊗ e)    where observer is fresh, and e persists
```

- In linear types: `use(x)` destroys `x`
- In affine types: `use(x)` may destroy `x`
- In witness types: `◊(x)` creates `(observer ⊗ x)` and `x` persists

Observation is generative, not extractive. Every witness enriches the fabric.

## 8. Room Semantics

```
[ e ]
```

Entry requires constructing a seam to `e` through the existing edge-structure:

```
enter([e], enterer) = e     if FV(enterer) ∩ FV(e) ≠ ∅
                    = ∅     otherwise
```

Access by relation, not by credential.

In evaluation, when a Room appears as a child of a Seam:
```
enterer ⊗ [e]  →  enterer ⊗ e    if can_enter(enterer, e)
               →  enterer ⊗ [e]   otherwise (room stays closed)
```

## 9. Beta Reduction

When a Return appears as a child of a Seam with an argument:

```
(μ x . e) ⊗ v  →  e[x := v]
```

This is the application rule. It enables encoding of lambda calculus.

## 10. Normalization

Applied after every evaluation step to maintain canonical form:

1. **Flatten** seam chains: `(a ⊗ b) ⊗ c → [a, b, c]`
2. **Remove** silence: filter out `∅` elements
3. **Sort** by structural key (commutativity → canonical form)
4. **Rebuild** right-associated: `a ⊗ (b ⊗ c)`
5. **Cap** node count at `max_nodes`

## 11. Derived Structures

### The Word (typed bilateral binding)
```
a |visible: V, veiled: D, covenant: C| b
```

### The Practice (protocol of two)
```
μ session .
    let offered = ◊ (seed from one)
    let heard   = ◊ (offered from other)
    let material = offered ⊗ heard
    let emerged  = material |breath| ∅
    emerged ⊗ session
```

### The Commons (emergent topology)
```
μ fabric .
    ∀ practices pᵢ :
        bind-if-isolated(pᵢ, fabric)
        veil-if-overexposed(pᵢ, fabric)
    fabric
```

### The Crossing (inter-kind seam)
```
a : Kind₁  ⊗  b : Kind₂
```

### The Duration (persistent seam, transient endpoints)
```
μ time .
    seam(being₁, being₂) persists
    beings may change or end
    the seam endures through the form
    time
```

## 12. Lambda Encoding

Seam can encode untyped lambda calculus:

| Lambda | Seam |
|--------|------|
| `λx. body` | `μ x . (body \|once\| ∅)` |
| `f a` | `f ⊗ a` |
| `x` | `x` |
| `Y f` | `μ x . (f ⊗ x)` — native |

The Y combinator is native: `μ` IS fixed-point iteration with homeostatic termination.

**Note on Turing completeness:** The encoding is syntactically complete — any lambda term
can be expressed. However, the interpreter enforces hard resource caps (max_returns,
max_nodes, max_depth), making it Turing-equivalent up to resource bounds, not
Turing-complete in the classical unbounded sense. This is a deliberate design choice:
resource safety is non-negotiable.

## 13. Prior Art and Positioning

Seam builds on several traditions. Honest accounting of what is borrowed, what is
adapted, and what is new:

**Borrowed (established ideas, given specific roles in the homeostatic loop):**
- Bilateral binding (session types, Honda 1993) — structural relation, not communication
- Information hiding / veiled computation (Parnas 1972, ML modules) — hidden structure
  bearing load, used as a metric in the homeostatic loop
- Homeostasis as a systems principle (Ashby 1952, Beer 1972) — the cybernetic tradition

**Adapted (existing mechanisms, significantly modified):**
- Membrane computing (P-systems, Păun 2001+) — Seam adds parameterized permeability
  functions and couples membrane state to homeostatic evaluation. P-systems use
  discrete structural operations (dissolve, divide); Seam uses continuous thresholds
  with oscillating breath dynamics.
- The "alignment is homeostasis" thesis (arXiv:2410.00081, 2024) — Seam provides the
  formal calculus mechanism that the conceptual work argues for.

**New (no direct precedent found):**
- A term-rewriting evaluator that measures structural metrics on the expression tree
  (connectivity, exposure) and applies regulatory transformations (BIND/VEIL) to
  maintain a stability band. No existing calculus has this feedback loop.
- Generative witness as a formal operation — observation that creates new relational
  structure rather than consuming or merely reading.
- The integration of all the above into a single minimal system.

## 14. What This Is

A minimal formal system — three primitives and their laws — from which a programming
language can be built, the way Lisp was built on lambda calculus.

The calculus says:
- Relations are primary
- Membranes are adaptive
- Evaluation is homeostatic
- Observation is generative
- Depth is load-bearing
- Nothing is named; everything is bound
