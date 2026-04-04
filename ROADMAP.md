# Roadmap

## Phase 0: Foundation (COMPLETE)
- [x] Interpreter, parser, seed programs, alignment demo, 93 tests

## Phase 1A: Engineering Truth (COMPLETE)
- [x] Bug fixes, convergence diagnostics, sensitivity analysis, honest claims

## Phase 1B: Prove and Ground (COMPLETE)
- [x] Theorems 1-5, scientific claim tests, PROOF.md

## Phase 2: Research (COMPLETE)
- [x] Theorem 6 (metric confluence), limit cycle characterization
- [x] Conversation monitor (aggregate-based, limited)

## Phase 2B: Governance Grounding (COMPLETE)

The pivot from abstract alignment claims to concrete multi-agent governance.

- [x] **Governance health monitor** (seam/governance.py) — encodes CARLOS-OS
      governed autonomy dynamics as Seam expressions
- [x] **Structural mapping** (not metaphorical):
  - VT-tiers = Edge membrane thresholds
  - AOW windows = BreathMembranes
  - Agent handoffs = Seams
  - Governance checks = holding edges (veiled infrastructure)
  - Decision records = Witness (generative observation)
- [x] **Four governance scenarios**, all correctly classified:
  - Well-governed (mixed VT, reviews, AOWs) → **converges in 9 steps**
  - Ungoverned (all VT0, no reviews) → exhausted (BIND+VEIL both fire heavily)
  - Locked-down (all VT3-4) → **limit cycle** (too much governance is also unstable)
  - Drifting (governed → ungoverned) → limit cycle
- [x] **BIND/VEIL → governance remedies**:
  - BIND fired → agents too isolated → add cross-agent coordination
  - VEIL fired → system too exposed → escalate VT tier / add governance gates
- [x] 128 tests, all passing

### Key Discovery: Too Much Governance Is Also Unstable

The locked-down sprint (all VT3-4, blocks on everything) enters a limit cycle.
Exposure is too LOW (0.143 < expo_lo=0.2) — nothing passes, the system can't
breathe. This confirms CARLOS-OS's core design principle: VT0-VT2 work MUST
be non-blocking. The homeostatic band requires both openness AND constraint.

This is not obvious from the VT-tier definitions alone. It's a structural
property that emerges from the homeostatic dynamics.

## Phase 3: The Paper (NEXT)

The grounding is now concrete. The paper can make a real claim:

*"We present a formal calculus that models multi-agent governance dynamics.
We show that governed autonomy protocols (VT-tiers, AOW windows, agent
coordination) map structurally to the calculus's primitives, and that the
homeostatic evaluator correctly distinguishes healthy governance (converges),
ungoverned systems (diverges), and over-governed systems (limit cycles)."*

- [ ] Write paper with governance grounding as the primary application
- [ ] Figures: governance scenario traces, VT-tier mapping diagram
- [ ] Compare against existing multi-agent coordination frameworks
- [ ] Submit to workshop or Alignment Forum

## Phase 4: Integration with CARLOS-OS

- [ ] Live governance monitor reading from Redis event streams
- [ ] Real-time VT-tier recommendation from evaluator dynamics
- [ ] Sprint health dashboard driven by Seam convergence metrics
- [ ] Auto-suggest governance remedies when drift detected

## Phase 5: Formal Foundations + Type System
- [ ] Small-step operational semantics
- [ ] Static convergence analysis (type system predicts governance health)

---

## Principles

1. **Correctness over speed.** Proofs before optimizations.
2. **Resource safety always.** Hard caps, bounded growth, no exceptions.
3. **The rite came first.** The philosophy guides the formalism.
4. **Honesty over marketing.** Cite what's borrowed. Claim only what's new.
5. **Test the claims, not just the engine.**
6. **Ground the theory in real systems.** VT-tiers are membranes. AOWs are breath.
