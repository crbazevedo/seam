# Seam — Development Context

## What this is

Seam is a term-rewriting calculus with a cybernetic evaluator: structural metrics
(connectivity, exposure) drive regulatory transformations (BIND, VEIL) that
maintain a stability band. Four primitives (silence, seam, edge, return) plus
two derived rules (witness, room).

## Running

```bash
python3 -m seam                    # Default: seed program
python3 -m seam --program all      # All five programs + lambda demo
python3 -m unittest discover -s seam/tests -v  # 117 tests
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

**Resource safety is non-negotiable.** Hard caps on everything. No unbounded
growth, no unbounded recursion.

## Module dependency order

config → ast → {algebra, metrics, membrane, rooms} → evaluator → {seed, lambda_encoding, ai_*} → {parser, viz, main}

## Proven properties (spec/PROOF.md)

- Theorem 1: BIND always increases connectivity when it fires
- Theorem 2: VEIL never increases exposure when it fires
- Theorem 3: BIND does not affect exposure (orthogonal dimensions)
- Theorem 4: μ-return always terminates
- Theorem 5: Sufficient conditions for convergence (stated, not fully proven)

## What's genuinely novel

The cybernetic feedback loop: structural metrics → regulatory evaluation →
structural modification → repeat. No existing formal system has this.
Individual features have precedent (cite P-systems, session types, cybernetics).

## Honest limitations

- Lambda encoding is bounded, not classically Turing-complete
- Alignment demo is robust but parameter-sensitive at boundaries
- The mapping from Seam expressions to real AI behavior is interpretive
- CrossingMembrane is functionally identical to Membrane(0.3)
- "Name no thing" is aspirational — the implementation uses named variables
