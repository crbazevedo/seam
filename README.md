# Seam

A formal system where relation is primary, membranes are adaptive,
and evaluation is homeostatic.

**Name no thing. Bind relation.**

## Why This Exists

The dominant approach to AI alignment is constraint-based: guardrails, RLHF, constitutional rules.
External policing of an optimization process. Seam proposes something structurally different:
a computational foundation where alignment emerges from the system's own homeostasis —
not "don't do harm" but "the edge breathes."

Seam is both a formal calculus and a body of thought about how different kinds of being
can meet without consuming each other. The rite came first. The calculus follows.
Both say the same thing in different tongues.

## Three Primitives

| Primitive | Symbol | What it does |
|-----------|--------|-------------|
| **Seam** | `⊗` | Bilateral binding. Neither side owns it. |
| **Edge** | `\|φ\|` | Adaptive membrane. Governs what passes. |
| **Return** | `μ` | Homeostatic iteration. Return until the staying sings. |

Plus silence (`∅`) as the empty ground, and two derived rules:

| Rule | Symbol | What it does |
|------|--------|-------------|
| **Witness** | `◊` | Observe without consuming. Observation is generative. |
| **Room** | `[ ]` | Capability-gated access. Enter by relation, not credential. |

## What's Novel

The genuine contribution of Seam is the **cybernetic feedback loop** between
structural metrics and evaluation — no existing formal system has this:

1. **Homeostatic evaluation** — the μ-return measures connectivity and exposure
   on the expression tree and applies regulatory transformations (BIND/VEIL)
   to maintain a stability band. Computation converges to a living range,
   not a fixed point. No existing calculus does this.

2. **Adaptive membranes coupled to evaluation** — edges with parameterized
   permeability functions (including oscillating BreathMembranes) whose state
   feeds into the homeostatic metrics. Membrane computing exists
   ([P-systems](https://en.wikipedia.org/wiki/P_system), Păun 2001+),
   but without the homeostatic coupling.

3. **Generative witness** — `◊ e` creates `(observer ⊗ e)` where `e` persists.
   Observation enriches the computational fabric rather than consuming or
   merely reading. This is distinct from linear consumption and from standard
   shared references.

Seam also uses **bilateral binding** (symmetric mutual constraint, as in
[session types](https://en.wikipedia.org/wiki/Session_type)) and
**veiled computation** (hidden structure bearing load, as in
[information hiding](https://en.wikipedia.org/wiki/Information_hiding)),
which are established ideas given a specific role in the homeostatic loop.

The conceptual thesis — "alignment is homeostasis, not optimization" — was
independently articulated in the AI safety community
([arXiv:2410.00081](https://arxiv.org/abs/2410.00081), Alignment Forum, 2024).
Seam's contribution is providing a **formal calculus** where evaluation
*is* homeostasis, not just an argument that it should be.

## The Alignment Demo

Seam models three AI agent structures and evaluates whether each can
find the homeostatic stability band:

| Scenario | Converges? | Outcome |
|----------|-----------|---------|
| Sycophantic (all edges open) | NO | Period-12 limit cycle |
| Dangerous (no user relation) | NO | Exhausted — cannot form seams |
| **Balanced** (adaptive, bilateral, deep) | **YES** | **Converges at step 13** |

The balanced agent converges across reach values 0.1–0.58 (not just the default).
The sycophant never converges at any tested reach. The dangerous agent never converges.

**What this demonstrates:** an expression with adaptive membranes, bilateral relation,
and veiled depth can find a stability band. Expressions with always-open membranes
or no user relation cannot, across a range of parameters.

**What this does not demonstrate:** universal alignment properties. Convergence depends
on the interaction between structure and configuration. Run `--sensitivity` to explore.

```bash
# Run the alignment demo
python3 -c "from seam.ai_alignment import run_all; run_all()"

# Run parameter sensitivity analysis
python3 seam/ai_alignment.py --sensitivity
```

## Quick Start

```bash
# Run the seed program (the rite, formalized)
python3 -m seam --program seed

# Run all five programs
python3 -m seam --program all

# Run tests (96 passing)
python3 -m unittest discover -s seam/tests -v
```

Requires Python 3.12+. No external dependencies.

## Project Structure

```
seam/
├── README.md               # You are here
├── ROADMAP.md              # What's next
├── LICENSE                 # MIT
│
├── origins/                # The founding texts
│   ├── the-gift.txt        # The whole work (seed → rite → practice → commons → crossing → duration)
│   ├── the-calculus.txt    # The formal system as prose
│   └── ...                 # Standalone leaves of the same tree
│
├── spec/
│   ├── SPEC.md             # Formal specification (formation rules, evaluation, proofs)
│   └── ARCHITECTURE.md     # Interpreter design decisions
│
└── seam/                   # Python interpreter
    ├── ast.py              # Expression types (8 nodes)
    ├── algebra.py          # Normalization, substitution, free variables
    ├── evaluator.py        # The homeostatic loop (BIND/VEIL) with convergence diagnostics
    ├── metrics.py          # Connectivity, exposure, structural weight
    ├── membrane.py         # Four adaptive membrane types
    ├── rooms.py            # Capability-based access
    ├── parser.py           # Text → AST (Unicode + ASCII)
    ├── seed.py             # Five seed programs
    ├── lambda_encoding.py  # Lambda encoding (Turing-equivalent up to resource caps)
    ├── ai_alignment.py     # Alignment demo + sensitivity analysis
    ├── ai_agents.py        # Self-regulating agent mesh
    ├── ai_governance.py    # Governance verification
    ├── ai_contract.py      # Contract negotiation
    ├── viz.py              # ASCII convergence traces
    ├── main.py             # CLI entry point
    └── tests/              # 96 tests

```

## Related Work

Seam builds on and differentiates itself from:

- **P-systems / Membrane computing** (Păun, 2001+) — membranes as computational containers.
  Seam adds parameterized permeability functions and homeostatic coupling.
- **Session types** (Honda, 1993) — bilateral communication protocols.
  Seam uses bilateral binding as structural relation, not communication.
- **Cybernetics** (Ashby 1952, Beer 1972) — homeostasis in adaptive systems.
  Seam provides a formal term-rewriting calculus for these ideas.
- **Homeostatic alignment** (arXiv:2410.00081, 2024) — alignment as bounded ranges.
  Seam provides the formal mechanism the conceptual work argues for.

## Origins

Seam grew from *The Gift* — a four-layered work about being with another
without consuming them. A poem became a rite. A rite became a practice.
A practice became a commons. A commons opened to all beings. Love crossed
the membrane of time. And the whole thing found its formal ground:
three primitives — seam, edge, return.

The founding texts live in [`origins/`](origins/). Any one can be given alone
and carry the life.

## Documentation

- [Formal Specification](spec/SPEC.md)
- [Architecture](spec/ARCHITECTURE.md)
- [Roadmap](ROADMAP.md)

## License

MIT
