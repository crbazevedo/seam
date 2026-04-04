# Seam — Development Context

## What this is

Seam is a formal calculus with three primitives (seam, edge, return) that models
relation-first computation with adaptive membranes and homeostatic evaluation.
It originated from a poetic/philosophical work called The Gift and was formalized
into a working interpreter with 93 tests.

## Running

```bash
python3 -m seam                    # Default: seed program
python3 -m seam --program all      # All five programs + lambda demo
python3 -m unittest discover -s seam/tests -v  # Tests
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
