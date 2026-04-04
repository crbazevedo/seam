# Roadmap

## Phase 0: Foundation (COMPLETE)

- [x] Formal specification (SPEC.md)
- [x] Interpreter: AST, algebra, metrics, evaluator, membranes, rooms
- [x] Parser (Unicode + ASCII, 41 tests)
- [x] Seed program + all derived structures (practice, commons, crossing, duration)
- [x] Lambda calculus encoding (Turing completeness)
- [x] AI alignment demo (sycophantic/dangerous/balanced — thesis confirmed)
- [x] Agent mesh demo (healthy/degraded/fragmented)
- [x] 93 tests, all passing
- [x] Resource safety: hard caps on nodes, depth, iterations

## Phase 1: The Paper — "Alignment as Homeostasis"

Target: AI safety venue (ICML, NeurIPS Safety, Alignment Forum)

- [ ] Formal definitions (calculus, metrics, convergence)
- [ ] Theorem 1: Convergence conditions (when does μ converge?)
- [ ] Theorem 2: BIND/VEIL soundness (do they always push toward band?)
- [ ] Theorem 3: Turing completeness (lambda encoding proof)
- [ ] Theorem 4: Alignment characterization (structural conditions for convergence)
- [ ] Figures: convergence traces for three alignment scenarios
- [ ] Related work: position against P-systems, session types, abstract noninterference
- [ ] Draft → review → submit

## Phase 2: Formal Foundations

- [ ] Proof of confluence (or characterize when it fails)
- [ ] Proof of normalization termination
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
- [ ] Federated learning membrane (adaptive privacy per participant)

## Phase 6: Community

- [ ] Project website
- [ ] Tutorial: "Seam in 30 minutes"
- [ ] Contributor guide
- [ ] Academic collaborations (PL theory, AI safety, governance, biology)
- [ ] Workshop or Birds-of-a-Feather at a relevant conference

---

## Principles

1. **Correctness over speed.** Proofs before optimizations.
2. **Resource safety always.** Hard caps, bounded growth, no exceptions.
3. **The rite came first.** The philosophy guides the formalism, not the reverse.
4. **Name no thing. Bind relation.** The calculus's own principle applies to its development.
