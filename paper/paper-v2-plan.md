# Paper v2 Plan: Governed Human-Agent Relationships

## Working Title

"Structural Health Monitoring for Governed Human-Agent Systems:
A Homeostatic Approach"

Alternative:
"When to Trust, When to Gate: Formal Governance for Human-Agent Teams"

## Target Audience

Primary: **SEAMS** (Software Engineering for Adaptive and Self-Managing Systems)
- Cross-disciplinary: SE + formal methods + adaptive systems
- Audience knows MAPE-K, self-adaptive architectures, runtime verification
- Accepts novel formal approaches with practical motivation
- 10-page format, values both formalism and evaluation

Secondary: **AAMAS** (Autonomous Agents and Multi-Agent Systems)
- Knows multi-agent coordination, trust, autonomy
- Larger community, more competitive
- Would reach the AutoGen/CrewAI/LangGraph audience

Tertiary: **CHI Late-Breaking Work** or **CSCW**
- If we frame around human-agent relationship quality
- Shorter format, values user-centered framing

## Why SEAMS is right

The paper's core claim is that governance health is a structural property
that can be formally monitored and regulated — this is exactly SEAMS's
scope. The MAPE-K loop (Monitor-Analyze-Plan-Execute over Knowledge) maps
directly to our evaluator: Monitor (metrics), Analyze (BIND/VEIL detection),
Plan (remedies), Execute (governance intervention), Knowledge (expression tree).

## Narrative Arc

The reader should follow this journey:

1. **The problem they recognize** — "I'm building a multi-agent system.
   How much autonomy should each agent have? I use risk tiers (VT0-VT4).
   But how do I know if my governance configuration is healthy?"

2. **Why existing tools don't answer it** — "Threshold checks (average VT,
   review rate) detect obvious problems but miss structural ones. A system
   with 100% review rate and all-VT4 looks 'perfectly governed' by every
   metric, but is actually paralyzed."

3. **What we propose** — "A formal model where governance events build an
   expression tree, two structural metrics are computed, and a homeostatic
   evaluator diagnoses health. Five proven properties guarantee the
   evaluator behaves predictably."

4. **How it works** — "Each governance event (VT assignment, agent handoff,
   governance check, approval) modifies the expression tree. Connectivity
   measures coordination. Exposure measures gatedness. When either exits
   a stability band, the evaluator fires regulatory actions with specific
   remedies."

5. **What we found** — "Four governance scenarios. Well-governed converges.
   Ungoverned diverges. Over-governed limit-cycles. Drifting oscillates.
   The over-governance result is non-obvious: threshold classifiers miss it."

6. **What this means for practice** — "A governance policy engine that
   auto-encodes events, computes structural health, and prescribes
   interventions. Not a predictor. A diagnostic — like a type checker
   for governance configurations."

## Figures Plan

### Figure 1: The Governance Health Problem
Two-panel figure:
- Left: A VT-tier spectrum (VT0 → VT4) with "too open" on left, "too closed" on right
- Right: The stability band — connectivity and exposure ranges where governance is healthy
- Caption: "Governance is homeostatic: too open (everything passes) and too closed (everything holds) are both unstable."

### Figure 2: From Events to Expression Tree
Four-step encoding diagram:
- Step 1: Raw governance event (agent handoff, VT2 action, governance check)
- Step 2: Mapped to Seam primitive (Seam node, Edge with threshold, holding Edge)
- Step 3: Expression tree after accumulation
- Step 4: Metrics computed (connectivity bar, exposure bar)
- Caption: "Each governance event modifies the expression tree. Metrics emerge from structure."

### Figure 3: Convergence Traces for Four Scenarios
Four small line plots (2x2 grid), each showing connectivity and exposure over evaluation steps:
- Well-governed: both metrics enter band by step 9
- Ungoverned: both oscillate, never settle
- Over-governed: exposure stuck below band
- Drifting: oscillation pattern
- Caption: "Only the well-governed configuration finds the stability band."

### Figure 4: BIND/VEIL Regulatory Cycle
Flow diagram:
- Measure → Is connectivity below band? → BIND (add coordination)
- Measure → Is exposure above band? → VEIL (tighten governance)
- Both in band for N steps? → CONVERGED
- Caption: "The evaluator's regulatory cycle. BIND increases connectivity (Theorem 1). VEIL decreases exposure (Theorem 2). They don't interfere (Theorem 3)."

### Figure 5: Baseline Comparison
Table comparing Seam vs. threshold classifier on the four scenarios.
Highlight the locked-down case where thresholds say "stable" but Seam says "limit cycle."

### Figure 6: Live Governance Dashboard (Screenshot)
Screenshot of the demo showing:
- Top bar gauges (connectivity, exposure, status badge)
- Expression tree preview
- Regulation log
- Agent coordination bars
- Caption: "The governance health monitor in action. Metrics are computed from the expression tree, not hardcoded."

## Tables Plan

### Table 1: Governance Event Encoding
| Event | Seam Operation | Effect on Metrics |
|---|---|---|
| Agent handoff | Seam(agent₁, agent₂) | Connectivity ↑ |
| VT-gated action | Edge(threshold) | Exposure ↑ if passes |
| Governance check | Edge(0.8) [holds] | Exposure ↓ |
| Auto-ingestion | Witness(observer, data) | Connectivity ↑ |
| Item resolved | Edge(0.8) [holds] | Exposure ↓ |

### Table 2: Formal Properties
| Property | Statement | Status |
|---|---|---|
| BIND monotonicity | BIND increases connectivity when it fires | Proven |
| VEIL monotonicity | VEIL never increases exposure | Proven |
| Orthogonality | BIND doesn't affect exposure, VEIL doesn't affect connectivity | Proven |
| Termination | Evaluator always terminates in bounded steps | Proven |
| Metric confluence | BIND/VEIL order doesn't matter for metrics | Proven |

### Table 3: Governance Scenarios
| Scenario | VT Mix | Coordination | Checks | Outcome |
|---|---|---|---|---|
| Well-governed | Mixed | High | Several | Converges |
| Ungoverned | All VT0 | None | None | Diverges |
| Over-governed | All VT3-4 | High | Many | Limit cycle |
| Drifting | Mixed→VT0 | Declining | Few | Oscillates |

### Table 4: Comparison with Related Approaches
| Approach | Monitors | Formal | Structural | Prescribes |
|---|---|---|---|---|
| MAPE-K | Yes | Partial | No | Yes |
| Threshold classifier | Yes | No | No | No |
| Runtime verification | Yes | Yes | No | No |
| Session types | No | Yes | Yes | No |
| **Seam** | **Yes** | **Yes** | **Yes** | **Yes** |

## Nomenclature

Avoid jargon from the calculus tradition. Use accessible terms:

| Formal term | Paper term |
|---|---|
| Expression tree | Governance structure |
| Seam node | Coordination binding |
| Edge node | Governance gate |
| Holding edge | Veiled infrastructure |
| Membrane threshold | Autonomy level |
| BreathMembrane | Adaptive gate |
| Connectivity metric | Coordination health |
| Exposure metric | Gatedness |
| BIND regulatory action | Coordination remedy |
| VEIL regulatory action | Gatedness remedy |
| μ-return | Governance cycle |
| Stability band | Health band |
| Convergence | Stable governance |
| Limit cycle | Oscillating governance |

## Section Outline

1. **Introduction** (1.5 pages)
   - The autonomy-control tension in human-agent teams
   - Why governance is homeostatic (too open and too closed are both unstable)
   - What we contribute: structural health monitoring with formal guarantees

2. **Background and Related Work** (1.5 pages)
   - Adjustable autonomy and trust calibration
   - Self-adaptive systems (MAPE-K)
   - Multi-agent governance frameworks (AutoGen, etc.)
   - Organizational cybernetics (Beer's VSM)
   - Formal runtime monitoring

3. **The Governance Health Model** (2 pages)
   - Governance events → governance structure (expression tree)
   - Coordination health (connectivity) and gatedness (exposure)
   - The health band: why both too high and too low are unstable
   - The regulatory cycle: BIND (add coordination) and VEIL (tighten gates)

4. **Formal Properties** (1 page)
   - Five properties with proof sketches
   - What they guarantee for practitioners

5. **Evaluation** (2 pages)
   - Four governance scenarios (Table 3)
   - Convergence traces (Figure 3)
   - Baseline comparison (Figure 5)
   - Sensitivity analysis
   - Live demonstration (Figure 6)

6. **Discussion** (1 page)
   - What practitioners gain
   - Limitations (aggregate encoding, sufficient conditions, synthetic data)
   - The over-governance discovery

7. **Conclusion and Future Work** (0.5 pages)
   - Trajectory-sensitive encoding
   - Live integration with real event streams
   - Type system for static governance analysis

## Key Differences from Paper v1

| Aspect | v1 | v2 |
|---|---|---|
| Title | "Homeostatic Evaluation for Multi-Agent Governance" | "Structural Health Monitoring for Governed Human-Agent Systems" |
| Framing | Calculus-first (here's a formal system, here's an application) | Problem-first (here's a governance problem, here's a solution) |
| Language | Term-rewriting, commutative monoid, membrane computing | Governance structure, coordination health, autonomy level |
| Audience | PL/formal methods researchers | Software engineers building multi-agent systems |
| Entry point | "We introduce Seam..." | "How do you know if your governance is healthy?" |
| Figures | Tables of theorems | Encoding diagrams, convergence traces, dashboard screenshot |
| Related work | P-systems, session types | MAPE-K, adjustable autonomy, trust calibration |
