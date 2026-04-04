# Architecture

## Module Dependency Graph

```
config.py          ← no dependencies
    ↓
ast.py             ← config
    ↓
membrane.py        ← no dependencies (duck-typed, no inheritance)
    ↓
algebra.py         ← ast, config
    ↓
metrics.py         ← ast, config, membrane
rooms.py           ← ast, algebra
    ↓
evaluator.py       ← ast, algebra, config, membrane, metrics, rooms
    ↓
seed.py            ← ast, membrane
lambda_encoding.py ← ast, membrane
ai_alignment.py    ← ast, algebra, config, evaluator, membrane, viz
ai_agents.py       ← ast, algebra, config, evaluator, membrane, viz
    ↓
parser.py          ← ast, membrane
viz.py             ← ast, evaluator
main.py            ← everything
```

## Key Design Decisions

### 1. Immutable Expression Trees
All `Expr` nodes are frozen dataclasses. Evaluation produces new trees rather than mutating. This:
- Eliminates aliasing bugs
- Enables clean substitution
- Allows history to be stored without defensive copying
- Makes the homeostatic loop well-defined (each step is a pure function)

### 2. Metrics on Expressions, Not Global State
v1 had a global `Fabric` (union-find) that tracked connectivity. This was a semantic mismatch: the spec says `connectivity(e)`, not `connectivity(global_fabric)`.

v2 computes all metrics by walking the expression tree. Single-pass, iterative (no recursion overflow), capped at `max_nodes * 2` visits.

### 3. BIND/VEIL as Tree Transformations
The homeostatic actions modify the expression structure:
- BIND: inserts a `Seam` node bridging the most isolated sub-expression
- VEIL: wraps the most exposed `Seam` in an `Edge` with a tighter membrane

This is the core innovation: evaluation doesn't just reduce — it *regulates* the term itself.

### 4. Normalization Prevents Blowup
v1 grew expressions without bound (O(n^2) per iteration). v2 normalizes after every step:
- Flatten seam chains (associativity)
- Remove silence (identity)
- Sort children (commutativity → canonical form)
- Cap node count

### 5. Duck-Typed Membranes
Membrane types don't share a base class. They implement the same interface:
- `__call__(reach, state) → Flow`
- `tighten(amount) → Membrane`
This avoids the frozen-dataclass inheritance issues that Python's MRO creates.

### 6. Hard Resource Caps
Every loop, recursion, and growth path has a hard cap:
- `max_returns = 100` — μ-return iterations
- `max_nodes = 500` — expression tree size
- `max_depth = 50` — recursion/substitution depth
- All tree walks use iterative stacks, not recursion

These are non-negotiable. v1 exhausted system memory without them.

## File Sizes (approximate)

| File | Lines | Role |
|------|-------|------|
| ast.py | 180 | Expression types, visitor, node_count |
| algebra.py | 220 | Normalization, substitution, free_vars |
| evaluator.py | 430 | μ-return, BIND, VEIL, witness, rooms |
| metrics.py | 120 | connectivity, exposure, structural_weight |
| membrane.py | 100 | Flow enum, 4 membrane types |
| rooms.py | 40 | Capability-based access |
| parser.py | 284 | Tokenizer + recursive descent |
| seed.py | 180 | 5 programs (seed, practice, commons, crossing, duration) |
| lambda_encoding.py | 130 | Church numerals, S/K/I, Y combinator |
| ai_alignment.py | 300 | 3 alignment scenarios + analysis |
| ai_agents.py | 150 | 3 agent mesh scenarios |
| viz.py | 180 | ASCII traces, expression trees |
| config.py | 30 | CalcConfig dataclass |
| main.py | 100 | CLI entry point |
| **Total** | **~2,450** | |
