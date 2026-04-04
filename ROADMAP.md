# Roadmap

## Phase 0: Foundation (COMPLETE)

- [x] Formal specification (SPEC.md)
- [x] Interpreter: AST, algebra, metrics, evaluator, membranes, rooms
- [x] Parser (Unicode + ASCII, 41 tests)
- [x] Seed program + all derived structures
- [x] Lambda encoding (Turing-equivalent up to resource caps)
- [x] AI alignment demo + agent mesh demo
- [x] 93 tests, all passing
- [x] Resource safety: hard caps on nodes, depth, iterations

## Phase 1A: Engineering Truth (COMPLETE)

- [x] Fix hardcoded band values, improve BIND strategy
- [x] Add convergence diagnostics (limit cycle, divergence, exhaustion)
- [x] Parameter sensitivity analysis
- [x] Reframe novelty claims, cite prior art
- [x] 96 tests

## Phase 1B: Prove and Ground (COMPLETE)

Addressed the three root causes from the honest review: no proofs,
no grounding, identity crisis.

- [x] **Theorem 1: BIND monotonicity** — proven and tested (8 expression types)
- [x] **Theorem 2: VEIL monotonicity** — proven and tested (5 expression types)
- [x] **Theorem 3: BIND exposure neutrality** — proven and tested
- [x] **Theorem 4: Termination** — proven (O(max_returns × max_nodes × max_depth))
- [x] **Theorem 5: Sufficient convergence conditions** — stated
- [x] **Section 5: Not a PID controller** — autopoietic argument
- [x] Scientific claim tests: BIND/VEIL monotonicity, alignment demo properties,
      sycophant limit cycle detection, balanced robustness across reach values
- [x] Fixed primitive count (4 + 2 derived, not "three")
- [x] Clean README (technical focus, no stale data, poetry in origins/)
- [x] spec/PROOF.md with all formal arguments
- [x] 117 tests, all passing

### Discoveries from Phase 1B

1. **BIND monotonicity is provable** — not just empirically observed. The
   algebraic argument holds for all expressions when connectivity < conn_lo.

2. **BIND and VEIL operate on orthogonal dimensions.** BIND modifies only
   connectivity; VEIL modifies only exposure. No side effects between them.
   This is a clean separation that makes the system easier to reason about.

3. **The autopoietic distinction matters.** Seam is not a PID controller
   because the controller and the controlled system are the same expression.
   Metrics are emergent structural properties, not external sensor readings.
   The state space is algebraic (expression trees), not numeric (ℝⁿ).

4. **The sycophant limit cycle is confirmed** as a test-verified phenomenon,
   not just an observation.

### Open Questions (from PROOF.md)

1. Is BIND+VEIL confluent? (Does evaluation order matter?)
2. Tight convergence time bounds
3. Predicting limit cycle period from structure + parameters
4. Structural predicates that guarantee non-convergence

## Phase 2: The Paper — "Homeostatic Evaluation" (NEXT)

Target: workshop paper at ICML, NeurIPS Safety, or Alignment Forum post.

Scope reduced to what's actually achievable:

- [ ] Prove or disprove BIND/VEIL confluence (open question 1)
- [ ] Characterize limit cycle periods (open question 3)
- [ ] One grounding example: encode a simple observable behavior as a Seam
      expression and show the homeostatic dynamics match
- [ ] Write the paper: formal definitions, Theorems 1-5, figures, related work
- [ ] Submit

## Phase 3: Formal Foundations

- [ ] Small-step operational semantics
- [ ] Confluence proof or counterexample
- [ ] Denotational semantics
- [ ] Behavioral equivalence

## Phase 4: Type System + Language

- [ ] Relational types
- [ ] Membrane types (static permeability analysis)
- [ ] REPL

## Phase 5: Applications

- [ ] AI alignment monitor for real LLM behavior
- [ ] Human-AI interaction protocol (The Practice)

---

## Principles

1. **Correctness over speed.** Proofs before optimizations.
2. **Resource safety always.** Hard caps, bounded growth, no exceptions.
3. **The rite came first.** The philosophy guides the formalism, not the reverse.
4. **Honesty over marketing.** Cite what's borrowed. Claim only what's new.
5. **Test the claims, not just the engine.** Every proven property has a test.
