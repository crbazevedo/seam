# Seam

A formal system where relation is primary, membranes are adaptive,
and evaluation is homeostatic.

## What This Is

Seam is a term-rewriting calculus with a **cybernetic evaluator**: structural
metrics computed on the expression tree drive regulatory transformations that
maintain a stability band. No existing formal system has this feedback loop.

The evaluator doesn't reduce to normal form. It **regulates toward homeostasis** —
measuring connectivity (how related the parts are) and exposure (how transparent
the structure is), then applying BIND (insert relations) or VEIL (strengthen
boundaries) to stay within a target band. Convergence is stability, not stillness.

## Primitives

Four primitives, two derived rules:

| | Symbol | Name | Role |
|-|--------|------|------|
| primitive | `∅` | Silence | Empty ground. Identity of seam. |
| primitive | `⊗` | Seam | Bilateral binding. Commutative monoid. |
| primitive | `\|φ\|` | Edge | Adaptive membrane. `φ(reach) → pass \| hold` |
| primitive | `μ` | Return | Homeostatic iteration with BIND/VEIL regulation. |
| derived | `◊` | Witness | Generative observation. `◊e → (observer ⊗ e)`, `e` persists. |
| derived | `[ ]` | Room | Capability-gated access. Enter by relation, not credential. |

Plus `Word` (typed bilateral binding with visible/veiled declarations).

## What's Novel

The genuine contribution is the **feedback loop between structural metrics
and evaluation**. See [spec/PROOF.md](spec/PROOF.md) for formal proofs.

| Property | Status | Reference |
|----------|--------|-----------|
| BIND always increases connectivity | **Proven** | Theorem 1 |
| VEIL never increases exposure | **Proven** | Theorem 2 |
| BIND does not affect exposure | **Proven** | Theorem 3 |
| μ-return always terminates | **Proven** | Theorem 4 |
| Sufficient conditions for convergence | **Stated** | Theorem 5 |
| Not a PID controller | **Argued** | Section 5 |

Individual features (bilateral binding, information hiding, membranes) have
precedent. The integration and the homeostatic evaluation mechanism do not.
See [Prior Art](spec/SPEC.md#13-prior-art-and-positioning) for honest accounting.

## Multi-Agent Governance Monitor

The primary application: monitoring governance health in multi-agent systems.
The mapping from [CARLOS-OS governed autonomy](https://github.com/crbazevedo/carlos-os)
to Seam is structural, not metaphorical:

| Governance Concept | Seam Primitive | Why |
|---|---|---|
| VT-tier (risk level) | Edge membrane threshold | Tier permeability = autonomy level |
| AOW (action window) | BreathMembrane | Time-varying permeability window |
| Agent handoff | Seam | Bilateral coordination binding |
| Governance check | Holding edge | Veiled infrastructure bearing load |
| Decision record | Witness | Generative observation |

**Results on four governance scenarios:**

| Scenario | Outcome | Discovery |
|----------|---------|-----------|
| **Well-governed** (mixed VT, reviews) | **Converges (9 steps)** | Balanced governance is stable |
| Ungoverned (all VT0, no reviews) | Exhausted | No governance = can't stabilize |
| **Locked-down** (all VT3-4) | **Limit cycle** | **Too much governance is also unstable** |
| Drifting (governed → ungoverned) | Limit cycle | Governance drift is detectable |

The locked-down result is non-obvious: a system that gates everything can't
breathe. The homeostatic band requires both openness AND constraint.

```bash
python3 -c "from seam.governance import run_all; run_all()"
```

## Alignment Demo

Three abstract agent structures also evaluated:

```bash
python3 -c "from seam.ai_alignment import run_all; run_all()"
python3 seam/ai_alignment.py --sensitivity
```

## Quick Start

```bash
python3 -m seam --program seed            # The rite, formalized
python3 -m seam --program all             # All five programs
python3 -m unittest discover -s seam/tests -v   # 117 tests
```

Python 3.12+. No external dependencies.

## Project Structure

```
seam/
├── spec/
│   ├── SPEC.md             # Formal specification
│   ├── PROOF.md            # Proven properties (Theorems 1-5)
│   └── ARCHITECTURE.md     # Interpreter design
│
├── seam/                   # Python interpreter (~3,700 LOC)
│   ├── ast.py              # 8 expression types
│   ├── evaluator.py        # Homeostatic loop (BIND/VEIL) + convergence diagnostics
│   ├── metrics.py          # Connectivity, exposure, structural weight
│   ├── membrane.py         # 4 membrane types (threshold, breath, once, crossing)
│   ├── algebra.py          # Normalization (monoid laws), substitution
│   ├── parser.py           # Text → AST (Unicode + ASCII)
│   ├── ai_alignment.py     # Alignment demo + sensitivity analysis
│   └── tests/              # 117 tests (engine + scientific claims)
│
├── origins/                # The founding texts (where Seam came from)
│
├── ROADMAP.md
└── LICENSE                 # MIT
```

## Related Work

- **P-systems** (Păun, 2001+) — membrane computing. Seam adds parameterized permeability + homeostatic coupling.
- **Session types** (Honda, 1993) — bilateral protocols. Seam uses bilateral binding as structural relation.
- **Cybernetics** (Ashby, 1952) — homeostasis. Seam provides a formal term-rewriting calculus.
- **Homeostatic alignment** ([arXiv:2410.00081](https://arxiv.org/abs/2410.00081)) — conceptual thesis. Seam provides the formal mechanism.

## Origins

Seam grew from *The Gift*, a work about being with another without consuming them.
The founding texts live in [`origins/`](origins/).

## License

MIT
