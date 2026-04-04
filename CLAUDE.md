# Seam — Development Context

## What this is

Seam is a formal calculus with three primitives (seam, edge, return) that models
relation-first computation with adaptive membranes and homeostatic evaluation.
It originated from a poetic/philosophical work called The Gift and was formalized
into a working interpreter with 96 tests.

## Running

```bash
python3 -m seam                    # Default: seed program
python3 -m seam --program all      # All five programs + lambda demo
python3 -m unittest discover -s seam/tests -v  # Tests
python3 -c "from seam.ai_alignment import run_all; run_all()"  # Alignment demo
python3 seam/ai_alignment.py --sensitivity  # Parameter sensitivity
```

## Architecture

- Pure Python 3.12+, no external dependencies
- Immutable AST (frozen dataclasses)
- Metrics computed by tree walks, not global state
- Hard resource caps: max_returns=100, max_nodes=500, max_depth=50
- All tree walks use iterative stacks, never recursion

## Key constraint

**Resource safety is non-negotiable.** Never introduce unbounded growth,
unbounded recursion, or operations that could exhaust memory/CPU.
Hard caps on everything. This is a design principle, not a temporary measure.

## The three primitives

- `⊗` (seam): bilateral binding — commutative monoid with silence as identity
- `|φ|` (edge): adaptive membrane — function from (reach, state) → {pass, hold}
- `μ` (return): homeostatic iteration — converges to stability band, not fixed point

## Module dependency order

config → ast → {algebra, metrics, membrane, rooms} → evaluator → {seed, lambda_encoding, ai_*} → {parser, viz, main}

## What's genuinely novel (established in Phase 1A review)

The core contribution is the **cybernetic feedback loop**: structural metrics
(connectivity, exposure) measured on the AST drive regulatory evaluation
(BIND/VEIL) which modifies membranes and structure, which changes the metrics.
No existing formal system has this.

Individual features (bilateral binding, information hiding, membranes) have
precedent. The integration and the homeostatic evaluation mechanism do not.

## Important: honest claims

- Lambda encoding is Turing-*equivalent* up to resource caps, not classically TC
- The alignment demo is robust (converges across 64% of reach range) but
  parameter-sensitive at boundaries
- CrossingMembrane is functionally identical to Membrane(0.3) — kept for
  semantic clarity
- Cite prior art: P-systems (Păun 2001), session types (Honda 1993),
  cybernetics (Ashby 1952), homeostatic alignment (arXiv:2410.00081)

## Convergence diagnostics (added Phase 1A)

The evaluator now classifies outcomes:
- `CONVERGED` — stability band held for window
- `LIMIT_CYCLE` — periodic behavior detected (with period)
- `DIVERGING` — node count monotonically growing
- `EXHAUSTED` — hit max_returns without any of the above
