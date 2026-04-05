# Structural Health Monitoring for Governed Human-Agent Systems: A Homeostatic Approach

Carlos R. B. Azevedo

April 2026

---

## Abstract

Multi-agent AI systems require governance: rules that determine how much
autonomy each agent has. Current approaches enforce governance through
static policies (risk tiers, approval workflows) or runtime policy engines.
These tell you whether a specific action is permitted. They do not tell you
whether your governance *configuration* is healthy.

We present a formal model for **governance health monitoring** — a
structural diagnostic that auto-encodes governance events into an
expression tree, computes two health metrics (coordination health and
gatedness), and classifies the governance configuration as stable,
oscillating, or drifting. We prove five formal properties: the regulatory
actions always improve their target metric, they don't interfere with each
other, the evaluation always terminates, and the application order doesn't
matter.

We evaluate on four governance scenarios from a real multi-agent system
(CARLOS-OS). The well-governed configuration converges. The ungoverned
configuration drifts. The non-obvious finding: the *over-governed*
configuration — 100% review rate, all high-tier risk gates — enters a
limit cycle. It is structurally unstable because nothing passes.
A threshold-based classifier labels this "perfectly governed." Our
structural diagnostic catches it.

The model, interpreter (128 tests), and live demonstration are open source
at https://github.com/crbazevedo/seam.

---

## 1. Introduction

### 1.1 The Problem

Consider a team of AI agents working alongside a human operator. Some
actions are safe to automate (reading files, running tests). Others are
risky (sending emails to board members, deploying to production). A
governance framework assigns risk tiers — the higher the tier, the more
human oversight is required.

This pattern is widespread. The EU AI Act [1] defines four risk levels.
NIST's AI Risk Management Framework [2] prescribes governance functions.
Microsoft's Agent Governance Toolkit [3] enforces policies at runtime.
In practice, most multi-agent systems use some form of tiered governance:
AutoGen's conversation patterns [4], CrewAI's role-based delegation,
LangGraph's state machine guards.

The governance *enforcement* problem is largely solved: given a policy,
check whether each action complies. But a different question is unanswered:

> **Is the governance configuration itself healthy?**

A system where every action is gated at the highest tier has 100%
compliance. It is also paralyzed — nothing gets done without approval.
A system where every action is autonomous has 0% overhead. It is also
uncontrolled. Both are valid governance configurations. Neither is healthy.

### 1.2 Why Governance is Homeostatic

Healthy governance occupies a band between two failure modes:

- **Under-governed** (too open): actions pass without oversight.
  Risk increases. Trust erodes after incidents.
- **Over-governed** (too closed): every action requires approval.
  Throughput drops. Teams route around the governance to get work done,
  creating shadow processes that are *less* governed than the original.

This is not a problem with a fixed solution. The right governance level
changes with conditions — deadline pressure, team trust, incident history.
Governance is *homeostatic*: it must stay within a band, and that band
is maintained through continuous adjustment, not static rules.

### 1.3 Contributions

We present a formal model where:

1. **Governance events** (agent handoffs, risk-tier assignments, approval
   decisions, governance checks) are auto-encoded into an **expression
   tree** — a structural representation of the governance state. (Section 3)

2. Two **health metrics** are computed from the tree: *coordination health*
   (how well agents are coordinating) and *gatedness* (how much is being
   gated vs. passing freely). (Section 3)

3. A **homeostatic evaluator** detects when either metric exits a health
   band and prescribes specific interventions: "add coordination" or
   "tighten gates." We prove five formal properties guaranteeing
   predictable evaluator behavior. (Section 4)

4. Evaluation on four governance scenarios from a real system shows the
   model correctly distinguishes stable, drifting, and oscillating
   governance — including the non-obvious over-governance failure mode.
   (Section 5)

---

## 2. Background and Related Work

### 2.1 Governance in Multi-Agent AI Systems

The shift from single-agent to multi-agent AI systems has created a
governance gap. Bose [5] presents the first systematic survey of
governance frameworks for LLM agent collectives, identifying three
failure modes — operational miscoordination, strategic misalignment,
adversarial collusion — and taxonomizing five governance models
(hierarchical, prescriptive, democratic, economic, emergent). The
survey finds industry favors deterministic but brittle models while
academia explores adaptive but chaotic ones.

Microsoft's Agent Governance Toolkit [3], released April 2026, provides
runtime policy enforcement: zero-trust identity, execution sandboxing,
compliance grading, and circuit breakers, covering all 10 OWASP agentic
AI risks with sub-millisecond enforcement. It addresses *per-action
enforcement* but not *configuration-level health*. Our approach is
complementary: structural health monitoring answers "is the governance
working?" alongside policy engines that answer "is this action
permitted?"

Li et al. [6] propose a layered governance architecture (sandboxing,
intent verification, zero-trust authorization, audit logging). Xiang
et al. [17] introduce AgentGuard for runtime verification with
probabilistic model checking. These provide external verification and
enforcement. Our model makes governance health an intrinsic structural
property.

### 2.2 Adjustable Autonomy and Trust

The question "how much autonomy should each agent have?" has been studied
extensively. Parasuraman et al. [7] define 10 Levels of Automation.
Kaber [18] reviews how LoA taxonomies have been used and critiques their
limitations for increasingly autonomous systems. SARI [9] formulates
shared autonomy as a POMDP, learning assistance across repeated
interactions.

On the trust side, Lee and See [19] define trust as attitude under
uncertainty, distinguishing analytic, analogical, and affective processes.
Hoff and Bashir [20] integrate empirical evidence into a three-layered
model (dispositional, situational, learned). Kim et al. [21] find that
user involvement in LLM planning *fails* to calibrate trust — plausible
plans mislead users — arguing that governance must be structural, not
reliant on user judgment of agent plans.

These approaches model autonomy and trust for *single* agent-human pairs.
We extend to multi-agent systems where the health question is about the
*configuration* — the distribution of autonomy levels and coordination
patterns across a team.

### 2.3 Self-Adaptive Systems

The MAPE-K reference architecture [10] (Monitor-Analyze-Plan-Execute over
Knowledge) is the standard model for self-adaptive software. Our evaluator
follows the MAPE-K pattern: Monitor (compute metrics), Analyze (detect
deviations from health band), Plan (select regulatory action), Execute
(prescribe intervention), Knowledge (expression tree).

The key difference: MAPE-K loops operate on *numerical* state variables.
Our monitor operates on *structural* state — an expression tree whose
topology encodes the governance configuration. Metrics emerge from the
structure itself, not from externally defined sensor readings.

Weyns [11] provides a comprehensive introduction to self-adaptive systems
engineering. Sanwouo et al. [12] propose AWARE as a successor to MAPE-K,
distributing the feedback loop and making it goal-driven. Li et al. [22]
map how generative AI can enhance each MAPE-K phase. Our contribution
provides a formal structural substrate for the Monitor and Analyze
components — one where governance health has algebraic properties.

### 2.4 Organizational Cybernetics

Ashby's Law of Requisite Variety [13] states that a controller must have
at least as much variety as the system being controlled. Beer's Viable
System Model [14] applies this to organizations, modeling five subsystems
that maintain viability through homeostatic loops. Perez Rios [15] recently
applied Beer's VSM to AI governance, mapping organizational pathologies
to AI failure modes.

Our model operationalizes the cybernetic principle: the health band IS
the homeostatic target, the regulatory actions (BIND, VEIL) ARE the
requisite variety, and the convergence/divergence/limit-cycle classification
IS the viability diagnosis.

### 2.5 Formal Runtime Monitoring

Runtime verification [16] checks whether a system execution satisfies a
formal property. Tools like Uppaal and PRISM verify temporal-logic
specifications. These approaches answer "does the trace satisfy φ?" —
a binary yes/no. Our approach answers "is the governance configuration
in a healthy structural state?" — a continuous diagnostic with specific
remedies.

---

## 3. The Governance Health Model

### 3.1 Governance Events

We model governance as a stream of typed events:

| Event Type | Example | Encoding |
|---|---|---|
| **Coordination** | Agent A hands off work to Agent B | Coordination binding between A and B |
| **Gated action** | Agent performs a VT2 action | Gate with autonomy-level threshold |
| **Governance check** | Preflight check runs before work | Holding gate (invisible infrastructure) |
| **Observation** | System ingests a file into knowledge base | Witness: creates link without consuming |
| **Resolution** | Human approves or denies a pending action | Gate switches from passing to holding |

### 3.2 The Governance Structure

Each event modifies an expression tree — the **governance structure**.
The tree is built from three node types:

**Coordination binding** (`a · b`): Represents bilateral coordination
between two parties. When Agent A hands off work to Agent B, a binding
is created. Bindings are symmetric (`a · b = b · a`), associative
(`(a · b) · c = a · (b · c)`), and grounded in an empty element
(`a · ∅ = a`). This gives them the algebraic structure of a commutative
monoid — the simplest structure that captures "coordination without
ordering."

**Gate** (`a |θ| b`): Represents a governance boundary with autonomy
level θ. When the system's *reach* (a parameter representing the current
operating context) exceeds θ, the gate passes and the content is visible.
When reach is below θ, the gate holds and the content is *veiled* — it
has structural weight but is not directly accessible.

The mapping from risk tiers to gate thresholds:

| Risk Tier | Description | Threshold θ | Behavior at default reach (0.5) |
|---|---|---|---|
| VT0 | Full autonomy | 0.1 | Always passes |
| VT1 | Act and notify | 0.3 | Passes |
| VT2 | Needs approval | 0.5 | Marginal (passes at default) |
| VT3 | Propose and wait | 0.7 | Holds |
| VT4 | Stop and escalate | 0.95 | Always holds |

**Adaptive gate** (`a |breath(b,a,f)| b`): A gate whose threshold
oscillates over time: `effective_threshold = base + amplitude × sin(cycle × frequency)`.
This models Action Opportunity Windows (AOWs) — time-bounded intervals
during which governance gates open. Like working hours for approvals:
the gate opens during business hours and closes overnight.

**Evaluation iteration** (`μ x . body`): The governance cycle. Each
iteration substitutes the previous governance state into the body,
evaluates it, measures the resulting structure, applies regulation if
needed, and checks for stability.

### 3.3 Health Metrics

Two metrics are computed from the governance structure by a single
tree walk:

**Coordination health:**
```
coordination = binding_nodes / max(total_nodes - 1, 1)
```
Measures how much of the governance structure consists of bilateral
coordination. Range: [0, 1]. High coordination health means agents are
working together. Low coordination health means agents are isolated.

**Gatedness:**
```
gatedness = gates_passing / max(total_gates, 1)
```
Measures what fraction of governance gates are currently passing (allowing
actions through). Range: [0, 1]. Neutral (0.5) if no gates exist. High
gatedness means most actions pass without oversight. Low gatedness means
most actions are held for review.

### 3.4 The Health Band

Healthy governance occupies a band:

- **Coordination:** [0.3, 0.7] — agents are coordinating but not
  over-coupled
- **Gatedness:** [0.2, 0.6] — some actions pass freely, some are gated

When either metric exits the band, the evaluator fires a regulatory
action:

**BIND** (coordination too low): "Agents are too isolated. Add
cross-agent review, require handoffs, increase coordination."

**VEIL** (gatedness too high): "Too much is passing without oversight.
Tighten the risk tier for recent action types, add governance gates."

### 3.5 Outcome Classification

The evaluator classifies the governance configuration:

| Outcome | Definition | Meaning |
|---|---|---|
| **Stable** | Both metrics in band for N consecutive cycles | Governance is healthy |
| **Limit cycle** | Metrics oscillate periodically | Governance is unstable (drifting back and forth) |
| **Diverging** | Structure grows without stabilizing | Governance is breaking down |
| **Exhausted** | Neither converges nor cycles within step limit | Governance is stuck |

---

## 4. Formal Properties

We state five properties with proof sketches. Full proofs and
corresponding test cases are in the supplementary material.

**Property 1 (BIND improves coordination).** When `coordination < 0.3`
and BIND fires, the resulting coordination is strictly higher. BIND adds
one coordination binding (increasing the numerator by at least 1) and
at most 3 total nodes (increasing the denominator by at most 3). Since
coordination < 0.3 implies binding_nodes < 0.3 × (total - 1), the
ratio increases. Verified across 8 expression types.

**Property 2 (VEIL improves gatedness).** When `gatedness > 0.6` and
VEIL fires, the resulting gatedness is equal or lower. VEIL either wraps
an exposed node in a holding gate (adding one holding gate to the
denominator) or tightens an existing gate. Verified across 5 expression
types.

**Property 3 (Non-interference).** BIND adds only coordination bindings.
VEIL adds or modifies only gates. Therefore: `gatedness(BIND(e)) = gatedness(e)`.
The regulatory actions operate on orthogonal dimensions.

**Property 4 (Termination).** The evaluator executes at most
`max_iterations` cycles, each bounded by O(`max_nodes × max_depth`).
Total work is bounded.

**Property 5 (Order independence).** For any governance structure `e`:
the metrics after applying BIND-then-VEIL are identical to the metrics
after applying VEIL-then-BIND. The evaluator's state is independent of
regulatory action ordering. This follows from Property 3: since BIND
doesn't affect gatedness and VEIL doesn't affect coordination, their
effects compose independently.

**What these properties guarantee for practitioners:** The regulatory
actions are predictable. BIND always helps coordination without harming
gatedness. VEIL always helps gatedness without harming coordination.
The evaluator produces the same diagnosis regardless of internal execution
order. And it always terminates.

---

## 5. Evaluation

### 5.1 System Under Study

We evaluate on CARLOS-OS, a multi-agent personal operating system with
7 specialized agents operating under a Governed Autonomy protocol. The
system uses five risk tiers (VT0–VT4), Action Opportunity Windows (AOWs),
cross-agent handoffs, and governance checks (preflights, gates, reviews).
The system has been in production use for 50+ sprints.

### 5.2 Four Governance Scenarios

We encode four governance configurations and evaluate each:

| Scenario | VT Distribution | Review Rate | Checks | Handoffs | Outcome |
|---|---|---|---|---|---|
| **Well-governed** | VT0:2, VT1:4, VT2:2 | 50% | 4 | 5 | **Stable (9 cycles)** |
| Ungoverned | VT0:6 | 0% | 0 | 0 | Exhausted |
| Over-governed | VT3:4, VT4:2 | 100% | 6 | 6 | **Limit cycle (p=4)** |
| Drifting | VT0:3, VT1:3 | 33% | 1 | 2 | Limit cycle (p=2) |

**Well-governed (stable).** A sprint with mixed risk tiers, cross-agent
reviews, and governance infrastructure finds the health band in 9 cycles.
Coordination stabilizes at 0.50, gatedness at 0.50. BIND fires 4 times
early (building initial coordination), then stops. VEIL does not fire.

**Ungoverned (exhausted).** All actions at VT0, no reviews, no governance
checks. BIND and VEIL both fire on every cycle but cannot compensate for
the structural deficit: there are no holding gates (no governance
infrastructure) and no coordination bindings (no handoffs). The
evaluator exhausts its step budget.

**Over-governed (limit cycle).** All actions at VT3-VT4, 100% review
rate, maximum governance checks. Gatedness drops to 0.14 — *below*
the health band's lower bound (0.20). Nothing passes. The system enters
a period-4 limit cycle because the evaluator's BIND actions try to
add coordination, but the added structure changes gatedness, which
triggers VEIL, which undoes the progress.

**Drifting (limit cycle).** Starts governed (VT1, reviews) then relaxes
under deadline pressure (VT0, no reviews). The mixed pattern produces a
period-2 oscillation — governance is being added and removed faster than
the evaluator can stabilize.

### 5.3 The Over-Governance Finding

The over-governed result is the central finding. A system with 100%
review rate, maximum governance checks, and all high-tier risk gates
*looks* perfectly governed by every conventional metric. A threshold-based
classifier checking `review_rate > 0.3 AND governance_checks > 2` labels
it "healthy."

Our structural diagnostic catches the instability because it models
*gatedness* — the ratio of passing to total gates. When everything holds,
gatedness drops below the health band. The system cannot breathe.

This is not a theoretical curiosity. It corresponds to a recognized
organizational failure mode: *process paralysis* — when governance
overhead exceeds the team's capacity to comply, and work either stops
or routes around the governance through informal channels.

The structural diagnosis makes this formal and testable: a governance
configuration where gatedness < 0.2 is structurally unstable, regardless
of how many checks are in place.

### 5.4 Sensitivity

The well-governed scenario converges for reach values in [0.1, 0.7] — 78%
of the tested range. It fails at reach ≥ 0.8 where all gate thresholds
are exceeded. The wide convergence region reflects the governance
infrastructure (holding gates from checks) providing structural stability.

### 5.5 Baseline Comparison

| Scenario | Structural diagnostic | Threshold classifier | |
|---|---|---|---|
| Well-governed | Stable | Stable | Match |
| Ungoverned | Exhausted | Unstable | Match |
| Over-governed | **Limit cycle** | **Stable** | **Mismatch** |
| Drifting | Limit cycle | Unstable | Match |

The structural diagnostic catches the over-governed failure mode that
the threshold classifier misses.

### 5.6 Live Demonstration

We provide a self-contained HTML demonstration that simulates a day of
governance events in a multi-agent system. As events fire, the governance
structure grows, metrics update in real time, and the evaluator shows
regulatory actions. The demonstration includes:

- Auto-encoded governance events (no manual encoding)
- Real-time coordination and gatedness gauges
- Regulatory action log with specific remedies
- Per-agent coordination tracking (trust proxy)
- Expression tree preview

---

## 6. Discussion

### 6.1 What Practitioners Gain

A governance policy engine that answers: "Is my governance configuration
healthy?" Not "is this action permitted?" (that's policy enforcement) but
"is the overall balance of autonomy and oversight working?" With specific
remedies when it isn't.

The analogy: a type checker for governance configurations. It doesn't
predict when governance will fail. It tells you whether the structure
is sound — and what to fix if it isn't.

### 6.2 Relationship to Existing Tools

Our approach is complementary to runtime policy engines like Microsoft's
Agent Governance Toolkit [3]. Policy engines enforce *per-action*
compliance ("is this VT2 action approved?"). Our model provides
*configuration-level* health monitoring ("is the overall VT distribution
stable?"). Both are needed. Enforcement without health monitoring misses
structural problems. Health monitoring without enforcement has no teeth.

### 6.3 Limitations

**Aggregate encoding.** The current model encodes a governance
configuration's aggregate properties (VT distribution, total handoffs,
total checks). It does not capture the *sequence* of events. A
configuration that starts governed and drifts ungoverned produces the
same encoding as one that drifts then recovers. Trajectory-sensitive
encoding is future work.

**Sufficient conditions.** The convergence conditions (Property 5 of
the supplementary) state when the evaluator converges, but we do not
characterize all convergent configurations. The sufficient conditions
are useful for designing governance configurations guaranteed to be
stable.

**Synthetic evaluation.** The four scenarios are synthetic, though
derived from a real system's governance structure. Validation against
live sprint telemetry is planned.

**Threshold sensitivity.** The health band parameters (coordination
[0.3, 0.7], gatedness [0.2, 0.6]) are configuration choices. Different
bands produce different classifications. The over-governance finding
is robust (it persists across band widths) but the exact boundary
depends on the band.

---

## 7. Conclusion

We presented a formal model for governance health monitoring in
multi-agent systems. The model auto-encodes governance events into an
expression tree, computes coordination health and gatedness from the
tree's structure, and classifies the governance configuration as stable,
oscillating, or drifting.

The central finding — that over-governance is structurally as unstable
as under-governance — formalizes an intuition that practitioners know
but cannot currently test. The five proven properties ensure the
evaluator behaves predictably, and the comparison with threshold-based
classification shows the structural approach catches failure modes
that snapshot metrics miss.

**Future work.** (1) Trajectory-sensitive encoding that captures event
ordering. (2) Integration with live event streams from CARLOS-OS's
Redis bus. (3) A type system for static governance analysis — determining
governance health at design time rather than runtime. (4) Empirical
validation against sprint retrospective data to measure correlation
between structural diagnosis and human-perceived governance quality.

---

## References

[1] European Parliament. Regulation (EU) 2024/1689 — The Artificial
    Intelligence Act. 2024.

[2] NIST. AI Risk Management Framework (AI RMF 1.0). NIST AI 100-1, 2023.

[3] Microsoft. Agent Governance Toolkit: Open-source runtime security for
    AI agents. https://github.com/microsoft/agent-governance-toolkit, 2026.

[4] Wu, Q. et al. AutoGen: Enabling next-gen LLM applications via
    multi-agent conversation. COLM, 2024.

[5] Bose, P. From Anarchy to Assembly: A Survey of Governance Frameworks
    for Collaborative LLM Agent Systems. IJERET, 2025.

[6] Li, H. et al. Governance architecture for autonomous agent systems:
    Threats, framework, and engineering practice. arXiv:2603.07191, 2025.

[7] Parasuraman, R., Sheridan, T.B., Wickens, C.D. A model for types and
    levels of human interaction with automation. IEEE Trans. SMC-A, 2000.

[8] Javdani, S., Srinivasa, S.S., Bagnell, J.A. Shared autonomy via
    hindsight optimization for teleoperation and beyond. IJRR, 2018.

[9] Zurek, M. et al. SARI: Shared Autonomy across Repeated Interaction.
    ACM Trans. Human-Robot Interaction, 2024.

[10] Kephart, J.O., Chess, D.M. The vision of autonomic computing.
     IEEE Computer, 36(1):41–50, 2003.

[11] Weyns, D. Introduction to Self-Adaptive Systems: A Contemporary
     Software Engineering Perspective. Wiley, 2020.

[12] Feitosa, D. et al. Breaking the Loop: AWARE is the new MAPE-K.
     HAL, 2025.

[13] Ashby, W.R. An Introduction to Cybernetics. Chapman & Hall, 1956.

[14] Beer, S. Brain of the Firm. Wiley, 2nd edition, 1981.

[15] Perez Rios, J. The Viable System Model and organizational pathologies
     in the age of AI. Systems, 13(9):749, 2025.

[16] Leucker, M., Schallhart, C. A brief account of runtime verification.
     Journal of Logic and Algebraic Programming, 78(5):293–303, 2009.

[17] Xiang, R. et al. AgentGuard: Runtime Verification of AI Agents.
     arXiv:2509.23864, 2025.

[18] Kaber, D. Systematic Literature Review of Levels of Automation
     Taxonomy. Int. J. Human-Computer Interaction, 2025.

[19] Lee, J.D., See, K.A. Trust in Automation: Designing for Appropriate
     Reliance. Human Factors, 46(1):50–80, 2004.

[20] Hoff, K.A., Bashir, M. Trust in Automation: Integrating Empirical
     Evidence. Human Factors, 57(3):407–434, 2015.

[21] Kim, S. et al. Plan-Then-Execute: User Trust and Team Performance
     with LLM Agents. CHI 2025.

[22] Li, Y. et al. Generative AI for Self-Adaptive Systems: State of the
     Art and Research Roadmap. ACM Trans. TAAS, 2024.

---

## Appendix: Figure Descriptions

**Figure 1: The Governance Health Band.** Two-panel diagram. Left panel
shows a risk-tier spectrum from VT0 (full autonomy) to VT4 (stop and
escalate), with failure zones labeled "under-governed" and "over-governed"
on the extremes. Right panel shows the two-dimensional health band:
coordination [0.3, 0.7] on the x-axis, gatedness [0.2, 0.6] on the
y-axis. The green zone in the center is "stable governance." The red
zones at the extremes are failure modes.

**Figure 2: Event-to-Structure Encoding.** Four-step diagram showing:
(1) raw governance events (agent handoff, VT2 action, governance check),
(2) encoded as tree nodes (coordination binding, gate with threshold,
holding gate), (3) accumulated expression tree, (4) metrics computed
from tree.

**Figure 3: Convergence Traces.** 2×2 grid of line plots showing
coordination (blue) and gatedness (orange) over evaluation cycles for
each scenario. Dashed horizontal lines mark the health band boundaries.
The well-governed plot shows both lines entering the band by cycle 9.
The over-governed plot shows gatedness stuck below 0.2.

**Figure 4: Baseline Comparison.** Table with traffic-light coloring
highlighting the over-governed mismatch: threshold classifier shows
green (stable), structural diagnostic shows red (limit cycle).

**Figure 5: Live Dashboard Screenshot.** Annotated screenshot of the
governance health demo showing top-bar gauges, expression tree preview,
regulation log, and per-agent coordination bars.
