# Roadmap

## Phase 0: Foundation (COMPLETE)

- [x] Formal specification (SPEC.md)
- [x] Interpreter: AST, algebra, metrics, evaluator, membranes, rooms
- [x] Parser (Unicode + ASCII, 41 tests)
- [x] Seed program + all derived structures (practice, commons, crossing, duration)
- [x] Lambda calculus encoding (Turing-equivalent up to resource caps)
- [x] AI alignment demo (sycophantic/dangerous/balanced)
- [x] Agent mesh demo (healthy/degraded/fragmented)
- [x] 93 tests, all passing
- [x] Resource safety: hard caps on nodes, depth, iterations

## Phase 1A: Engineering Truth (COMPLETE)

Honest assessment of claims, bug fixes, reframing.

- [x] Fix hardcoded band values in `analyze_alignment` (was ignoring config)
- [x] Improve BIND strategy (bridge existing leaves, not just fresh variables)
- [x] Add convergence diagnostics: limit cycle detection (period detection),
      divergence classification (CONVERGED / LIMIT_CYCLE / DIVERGING / EXHAUSTED)
- [x] Parameter sensitivity analysis for alignment demo
- [x] Reframe novelty claims honestly — cite prior art (P-systems, session types,
      cybernetics, arXiv:2410.00081)
- [x] Correct Turing completeness claim (bounded, not classical TC)
- [x] Add Prior Art section to SPEC.md
- [x] 96 tests, all passing

### Discoveries from Phase 1A

1. **The genuine novelty is the feedback loop**, not any single primitive.
   Structural metrics → regulatory evaluation → membrane modification → repeat.
   No existing calculus has this cybernetic evaluator.

2. **BreathMembrane is the critical innovation** among membrane types.
   Oscillating permeability coupled with homeostatic evaluation creates
   the living dynamics. The other membrane types are threshold variations.

3. **The sycophant's period-12 limit cycle is genuinely emergent** — not
   manually coded. This is a real dynamical systems result worth studying.

4. **BIND always increases connectivity when it fires** (mathematically
   guaranteed when connectivity < 0.3). The concern about ineffective
   BIND was valid in general but does not apply to the actual firing
   condition.

5. **The alignment demo is robust** — balanced agent converges for reach
   values 0.1 to 0.58 (64% of the tested range). Sycophant never converges
   at any tested reach. But convergence IS parameter-sensitive at the
   boundaries. The result is a demonstration, not a proof.

6. **CrossingMembrane is functionally redundant** with Membrane(0.3).
   Kept for semantic clarity but noted in architecture docs.

## Phase 1B: The Paper — "Alignment as Homeostasis" (NEXT)

Target: AI safety venue (ICML, NeurIPS Safety, Alignment Forum)

- [ ] Formal definitions (calculus, metrics, convergence)
- [ ] Theorem 1: Convergence conditions (when does μ converge?)
- [ ] Theorem 2: BIND/VEIL soundness (do they always push toward band?)
- [ ] Theorem 3: Structural conditions for convergence (what makes balanced work?)
- [ ] Theorem 4: Limit cycle characterization (when does cycling occur?)
- [ ] Figures: convergence traces, sensitivity heatmap, limit cycle phase portrait
- [ ] Related work: position against P-systems, session types, cybernetics,
      homeostatic alignment benchmarks (arXiv:2410.00081)
- [ ] Draft → review → submit

## Phase 2: Formal Foundations

- [ ] Proof of confluence (or characterize when it fails)
- [ ] Small-step operational semantics (complement the current big-step)
- [ ] Denotational semantics (what mathematical objects do expressions denote?)
- [ ] Bisimulation / behavioral equivalence theory
- [ ] Metatheory: decidability of convergence for restricted fragments

## Phase 3: The Type System

- [ ] Relational types (typing bindings, not things)
- [ ] Word types: `a |T| b` where T constrains the relation
- [ ] Membrane types: static analysis of edge permeability bounds
- [ ] Exposure typing: statically prove exposure ≤ threshold
- [ ] Connectivity typing: statically prove connectivity ≥ threshold
- [ ] Type inference for simple programs

## Phase 4: The Language

- [ ] Module system (modules as membranes, not namespaces)
- [ ] Standard library of membrane types
- [ ] Standard library of protocols (practice, crossing, duration)
- [ ] REPL with convergence visualization
- [ ] Error messages that speak in the Seam vocabulary
- [ ] Package manager / module registry

## Phase 5: Applications

- [ ] AI alignment monitor (real-time homeostatic analysis of LLM behavior)
- [ ] Multi-agent mesh coordinator (self-regulating agent framework)
- [ ] Human-AI interaction protocol (The Practice as usable protocol)
- [ ] Commons governance verifier (formally verify Ostrom's principles)
- [ ] Privacy boundary analyzer (prove exposure bounds for data protocols)

## Phase 6: Community

- [ ] Project website
- [ ] Tutorial: "Seam in 30 minutes"
- [ ] Contributor guide
- [ ] Academic collaborations (PL theory, AI safety, governance, biology)

---

## Principles

1. **Correctness over speed.** Proofs before optimizations.
2. **Resource safety always.** Hard caps, bounded growth, no exceptions.
3. **The rite came first.** The philosophy guides the formalism, not the reverse.
4. **Name no thing. Bind relation.** The calculus's own principle applies to its development.
5. **Honesty over marketing.** Cite what's borrowed. Claim only what's new. Let the narrow band of genuine novelty be strong enough.
