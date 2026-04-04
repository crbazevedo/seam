# Roadmap

## Phase 0: Foundation (COMPLETE)

- [x] Formal specification, interpreter, parser, seed programs
- [x] Lambda encoding, AI alignment demo, agent mesh demo
- [x] 93 tests, resource safety

## Phase 1A: Engineering Truth (COMPLETE)

- [x] Bug fixes, convergence diagnostics, sensitivity analysis
- [x] Reframe novelty claims, cite prior art
- [x] 96 tests

## Phase 1B: Prove and Ground (COMPLETE)

- [x] Theorems 1-5: BIND/VEIL monotonicity, orthogonality, termination, convergence
- [x] Scientific claim tests, clean README, PROOF.md
- [x] 117 tests

## Phase 2: Research and Grounding (COMPLETE)

- [x] **Theorem 6: Metric confluence** — BIND and VEIL commute (same metrics regardless of order)
- [x] **Limit cycle characterization** — period depends on exposure band width, not stability window
- [x] **Corrected claim:** sycophant converges at expo_hi ≥ 0.7 — non-convergence is a band-width effect, not structural impossibility
- [x] **Conversation quality monitor** — grounding example mapping turn metrics to structural archetypes
- [x] **Paper outline** (spec/PAPER_OUTLINE.md)
- [x] 122 tests, all passing

### Discoveries from Phase 2

1. **BIND/VEIL are metrically confluent.** Order doesn't matter — the evaluator
   is a well-defined function on the metric space. Trees differ structurally
   (different fresh names) but metrics are identical.

2. **Limit cycle period is a band-width effect.** Tighter exposure band → longer
   cycles. The sycophant converges at expo_hi ≥ 0.7. This corrects the original
   claim that sycophancy is "structurally incapable of homeostasis."

3. **The conversation monitor works but is aggregate-only.** Turn-level metrics
   map to structural archetypes whose convergence properties are proven. But the
   encoding doesn't capture turn ORDER — trajectory sensitivity is future work.

### Open Questions

1. Tight convergence time bounds
2. Structural conditions for non-convergence (independent of config)
3. Trajectory-sensitive conversation encoding
4. Type system for static analysis of convergence properties

## Phase 3: The Paper (NEXT)

Concrete deliverable: one publishable document.

- [ ] Write full paper draft (from PAPER_OUTLINE.md)
- [ ] Generate figures (convergence traces, sensitivity heatmap, limit cycle phase portrait)
- [ ] Internal review (honest roast of the draft)
- [ ] Submit to workshop or Alignment Forum

## Phase 4: Formal Foundations

- [ ] Small-step operational semantics
- [ ] Confluence proof (structural, not just metric)
- [ ] Behavioral equivalence / bisimulation

## Phase 5: Type System + Language

- [ ] Relational types, membrane types
- [ ] Static convergence analysis
- [ ] REPL

## Phase 6: Applications

- [ ] Trajectory-sensitive conversation encoding
- [ ] Real LLM behavior data grounding
- [ ] Human-AI interaction protocol (The Practice, live)

---

## Principles

1. **Correctness over speed.** Proofs before optimizations.
2. **Resource safety always.** Hard caps, bounded growth, no exceptions.
3. **The rite came first.** The philosophy guides the formalism, not the reverse.
4. **Honesty over marketing.** Cite what's borrowed. Claim only what's new.
5. **Test the claims, not just the engine.** Every proven property has a test.
6. **Ground the theory.** Abstract results need concrete demonstrations.
