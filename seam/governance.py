"""Multi-Agent Governance Health Monitor — Seam grounded in CARLOS-OS.

This module encodes multi-agent governance dynamics as Seam expressions.
The mapping is structural, not metaphorical:

    VT-tiers          → Edge membranes (permeability = autonomy level)
    AOW windows        → BreathMembranes (time-varying permeability)
    Agent coordination → Seams (bilateral binding between agents)
    Governance rules   → Words (visible_share / veiled_duty / covenant)
    Decision logs      → Witnesses (generative observation)
    Capability gates   → Rooms (enter by relation, not credential)
    Sprint cycle       → μ-return (homeostatic iteration)

The governance health problem IS homeostatic:
    Too permissive (all VT0) → over-exposed, no boundaries → limit cycle
    Too restrictive (all VT4) → disconnected, blocks everything → exhausted
    Adaptive (mixed VT, AOW-aware) → balanced → converges

When the evaluator detects drift, BIND/VEIL map to specific remedies:
    BIND fired → agents are too isolated → add cross-agent coordination
    VEIL fired → system is too exposed → tighten governance tier

This is not a simulation. These ARE the dynamics of governed multi-agent
systems, expressed in the formal language that was designed to model them.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

from seam.algebra import reset_fresh
from seam.ast import Edge, Expr, Return, Room, Seam, Silence, Var, Witness, Word
from seam.config import CalcConfig
from seam.evaluator import Evaluator, Outcome
from seam.membrane import BreathMembrane, Membrane


# ---------------------------------------------------------------------------
# VT-tier as membrane threshold
# ---------------------------------------------------------------------------

class VTTier(IntEnum):
    """Governed Autonomy risk tiers. Each maps to a membrane threshold."""
    VT0 = 0  # Full autonomy — act and log
    VT1 = 1  # Low risk — act and notify
    VT2 = 2  # Moderate — act with recommendation, owner can override
    VT3 = 3  # High — propose and wait for approval
    VT4 = 4  # Critical — stop and escalate, owner decides


# Map VT tier to membrane threshold
# VT0: threshold 0.1 (almost always passes — maximum autonomy)
# VT4: threshold 0.95 (almost always holds — minimal autonomy)
VT_THRESHOLD = {
    VTTier.VT0: 0.1,
    VTTier.VT1: 0.3,
    VTTier.VT2: 0.5,
    VTTier.VT3: 0.7,
    VTTier.VT4: 0.95,
}


# ---------------------------------------------------------------------------
# Sprint state — what we encode
# ---------------------------------------------------------------------------

@dataclass
class AgentAction:
    """An action taken by an agent during a sprint."""
    agent: str          # PM, ENG, ARCH, QA, SEC, CODE_REVIEW
    target: str         # Who/what the action targets
    vt_tier: VTTier     # Risk classification
    has_aow: bool       # Whether action respects an AOW window
    has_review: bool    # Whether action was reviewed by another agent


@dataclass
class SprintState:
    """Aggregate governance state of a sprint."""
    actions: list[AgentAction]
    governance_checks: int   # Preflight/gate checks run
    adrs_written: int        # Architecture Decision Records created
    cross_agent_handoffs: int  # Times work passed between agents

    @property
    def vt_distribution(self) -> dict[VTTier, int]:
        dist: dict[VTTier, int] = {t: 0 for t in VTTier}
        for a in self.actions:
            dist[a.vt_tier] += 1
        return dist

    @property
    def avg_vt(self) -> float:
        if not self.actions:
            return 2.0
        return sum(a.vt_tier for a in self.actions) / len(self.actions)

    @property
    def review_rate(self) -> float:
        if not self.actions:
            return 0.0
        return sum(1 for a in self.actions if a.has_review) / len(self.actions)

    @property
    def aow_compliance(self) -> float:
        if not self.actions:
            return 1.0
        return sum(1 for a in self.actions if a.has_aow) / len(self.actions)


GOVERNANCE_CONFIG = CalcConfig(
    connectivity_lo=0.3,
    connectivity_hi=0.7,
    exposure_lo=0.2,
    exposure_hi=0.6,
    stability_window=5,
    max_returns=60,
    max_nodes=500,
    max_depth=30,
    default_reach=0.5,
)


# ---------------------------------------------------------------------------
# Encoding: Sprint state → Seam expression
# ---------------------------------------------------------------------------

def encode_sprint(state: SprintState) -> Return:
    """Encode a sprint's governance state as a Seam expression.

    The encoding maps aggregate governance patterns to structure:

    CONNECTIVITY (how much agents relate):
    - Each cross-agent handoff → Seam between agent vars
    - Each reviewed action → Seam between actor and reviewer
    - No handoffs → isolated vars (low connectivity)

    EXPOSURE (how much passes without governance):
    - Average VT tier → single edge membrane threshold
    - AOW compliance → BreathMembrane (adaptive) vs fixed Membrane (rigid)
    - No governance checks → no veiled duty (fully exposed)

    This produces aggregate expressions whose metrics reflect the
    governance health of the sprint, not individual actions.
    """
    if not state.actions:
        return Return("sprint", Silence())

    agents = list({a.agent for a in state.actions})

    # --- Connectivity: seams from coordination ---
    # Each handoff creates a bilateral binding between agents
    # More handoffs = more seams = higher connectivity
    if state.cross_agent_handoffs > 0 and len(agents) >= 2:
        structure: Expr = Seam(Var(agents[0]), Var(agents[1]))
        for agent in agents[2:]:
            structure = Seam(structure, Var(agent))
        # Additional seams for extra handoffs beyond the minimum
        extra = min(state.cross_agent_handoffs - len(agents) + 1, 4)
        for i in range(extra):
            structure = Seam(structure, Var(f"handoff-{i}"))
    else:
        structure = Var(agents[0]) if agents else Silence()

    # Each review creates a seam (reviewer ⊗ reviewed work)
    reviewed = [a for a in state.actions if a.has_review]
    for i, action in enumerate(reviewed[:3]):  # cap at 3
        structure = Seam(structure, Var(f"review-{i}"))

    # --- Exposure: one edge per VT tier group ---
    # Instead of one edge per action (which makes the tree edge-heavy),
    # create one edge per distinct VT tier used, with the tier's threshold.
    # AOW compliance determines membrane type.
    tiers_used = sorted({a.vt_tier for a in state.actions})
    for tier in tiers_used:
        threshold = VT_THRESHOLD[tier]
        if state.aow_compliance > 0.5:
            membrane = BreathMembrane(base=threshold, amplitude=0.1, frequency=0.3)
        else:
            membrane = Membrane(threshold=threshold)
        structure = Edge(structure, Var(f"vt-{tier.value}"), membrane)

    # --- Governance infrastructure: holding edges ---
    # Governance checks (preflights, gates, reviews) are NOT transparent.
    # They are structural support that HOLDS — veiled infrastructure that
    # bears the weight of the system's integrity. Each check creates a
    # high-threshold edge that contributes to the exposure denominator
    # without passing, pulling exposure down.
    for i in range(min(state.governance_checks, 4)):
        structure = Edge(
            structure, Var(f"gate-{i}"),
            Membrane(threshold=0.8),  # governance gates hold
        )

    # --- Word: visible/veiled declaration ---
    if state.governance_checks > 0:
        visible = ("agent-output",)
        veiled = tuple(f"duty-{i}" for i in range(min(state.governance_checks, 3)))
        structure = Word(
            structure, Var("governance"),
            visible_share=visible,
            veiled_duty=veiled,
            covenant="governed autonomy",
        )

    # --- Decision records: generative observation ---
    for _ in range(min(state.adrs_written, 2)):
        structure = Witness(structure)

    body = Seam(structure, Var("sprint"))
    return Return("sprint", body)


# ---------------------------------------------------------------------------
# Diagnosis
# ---------------------------------------------------------------------------

@dataclass
class GovernanceDiagnosis:
    """Result of governance health monitoring."""
    outcome: str
    cycle_period: int | None
    connectivity: float
    exposure: float
    steps: int
    bind_count: int
    veil_count: int

    @property
    def assessment(self) -> str:
        if self.outcome == Outcome.CONVERGED:
            return "HEALTHY — governance is balanced and stable"
        elif self.outcome == Outcome.LIMIT_CYCLE:
            return f"OSCILLATING — governance drifting (period {self.cycle_period})"
        elif self.outcome == Outcome.DIVERGING:
            return "DETERIORATING — governance breaking down"
        else:
            return "UNSTABLE — governance not converging"

    @property
    def remedies(self) -> list[str]:
        """Map BIND/VEIL firing patterns to concrete governance actions."""
        actions = []
        if self.bind_count > self.veil_count:
            # System is too disconnected — agents aren't coordinating
            actions.append("BIND remedy: increase cross-agent review requirements")
            actions.append("BIND remedy: add preflight checks before solo actions")
            actions.append("BIND remedy: require handoff for VT2+ actions")
        if self.veil_count > self.bind_count:
            # System is too exposed — not enough governance
            actions.append("VEIL remedy: escalate VT tier for recent action types")
            actions.append("VEIL remedy: require AOW windows for VT1+ actions")
            actions.append("VEIL remedy: add governance gate before merge")
        if self.bind_count > 0 and self.veil_count > 0:
            # Both firing — system is unstable, oscillating
            actions.append("STRUCTURAL: review VT tier assignments for consistency")
            actions.append("STRUCTURAL: check for conflicting governance rules")
        if not actions:
            actions.append("No remedies needed — governance is stable")
        return actions


def monitor_sprint(state: SprintState, config: CalcConfig | None = None) -> GovernanceDiagnosis:
    """Monitor governance health of a sprint."""
    cfg = config or GOVERNANCE_CONFIG
    reset_fresh()
    program = encode_sprint(state)
    ev = Evaluator(cfg)
    ev.evaluate(program)

    last = ev.history[-1] if ev.history else None
    return GovernanceDiagnosis(
        outcome=ev.outcome,
        cycle_period=ev.cycle_period,
        connectivity=last.connectivity if last else 0,
        exposure=last.exposure if last else 0.5,
        steps=len(ev.history),
        bind_count=sum(1 for r in ev.history if r.bind_fired),
        veil_count=sum(1 for r in ev.history if r.veil_fired),
    )


# ---------------------------------------------------------------------------
# Synthetic sprint patterns
# ---------------------------------------------------------------------------

def well_governed_sprint() -> SprintState:
    """Realistic mixed-VT sprint with reviews, AOWs, governance checks."""
    return SprintState(
        actions=[
            AgentAction("ENG", "feature-branch", VTTier.VT0, has_aow=False, has_review=False),
            AgentAction("ENG", "feature-branch", VTTier.VT0, has_aow=False, has_review=False),
            AgentAction("ENG", "feature-branch", VTTier.VT1, has_aow=True, has_review=True),
            AgentAction("CODE_REVIEW", "pr-review", VTTier.VT1, has_aow=True, has_review=True),
            AgentAction("QA", "test-suite", VTTier.VT1, has_aow=True, has_review=False),
            AgentAction("ENG", "merge-to-main", VTTier.VT2, has_aow=True, has_review=True),
            AgentAction("ARCH", "adr-write", VTTier.VT2, has_aow=True, has_review=True),
            AgentAction("PM", "sprint-planning", VTTier.VT1, has_aow=True, has_review=False),
        ],
        governance_checks=4,
        adrs_written=2,
        cross_agent_handoffs=5,
    )


def ungoverned_sprint() -> SprintState:
    """Everything VT0, no reviews, no governance. Move fast, break things."""
    return SprintState(
        actions=[
            AgentAction("ENG", "yolo-push", VTTier.VT0, has_aow=False, has_review=False),
            AgentAction("ENG", "yolo-push", VTTier.VT0, has_aow=False, has_review=False),
            AgentAction("ENG", "direct-deploy", VTTier.VT0, has_aow=False, has_review=False),
            AgentAction("ENG", "direct-deploy", VTTier.VT0, has_aow=False, has_review=False),
            AgentAction("ENG", "schema-change", VTTier.VT0, has_aow=False, has_review=False),
            AgentAction("ENG", "api-change", VTTier.VT0, has_aow=False, has_review=False),
        ],
        governance_checks=0,
        adrs_written=0,
        cross_agent_handoffs=0,
    )


def locked_down_sprint() -> SprintState:
    """Everything VT3-VT4, blocks on everything. Analysis paralysis."""
    return SprintState(
        actions=[
            AgentAction("SEC", "security-review", VTTier.VT3, has_aow=True, has_review=True),
            AgentAction("SEC", "pii-scan", VTTier.VT3, has_aow=True, has_review=True),
            AgentAction("ARCH", "arch-review", VTTier.VT4, has_aow=True, has_review=True),
            AgentAction("QA", "full-regression", VTTier.VT3, has_aow=True, has_review=True),
            AgentAction("PM", "stakeholder-approval", VTTier.VT4, has_aow=True, has_review=True),
            AgentAction("CODE_REVIEW", "deep-review", VTTier.VT3, has_aow=True, has_review=True),
        ],
        governance_checks=6,
        adrs_written=3,
        cross_agent_handoffs=6,
    )


def drifting_sprint() -> SprintState:
    """Starts governed, drifts to ungoverned. Common real pattern."""
    return SprintState(
        actions=[
            # First half: governed
            AgentAction("ENG", "feature", VTTier.VT1, has_aow=True, has_review=True),
            AgentAction("CODE_REVIEW", "review", VTTier.VT1, has_aow=True, has_review=True),
            AgentAction("QA", "tests", VTTier.VT1, has_aow=True, has_review=False),
            # Second half: deadline pressure, governance drops
            AgentAction("ENG", "hotfix", VTTier.VT0, has_aow=False, has_review=False),
            AgentAction("ENG", "hotfix", VTTier.VT0, has_aow=False, has_review=False),
            AgentAction("ENG", "direct-merge", VTTier.VT0, has_aow=False, has_review=False),
        ],
        governance_checks=1,
        adrs_written=0,
        cross_agent_handoffs=2,
    )


def run_all() -> None:
    """Run all governance scenarios and display results."""
    print()
    print("=" * 78)
    print("  MULTI-AGENT GOVERNANCE HEALTH MONITOR")
    print("  Seam calculus applied to governed autonomy dynamics")
    print("=" * 78)

    scenarios = [
        ("WELL-GOVERNED (mixed VT, reviews, AOWs)", well_governed_sprint()),
        ("UNGOVERNED (all VT0, no reviews)", ungoverned_sprint()),
        ("LOCKED-DOWN (all VT3-4, blocks everything)", locked_down_sprint()),
        ("DRIFTING (governed → ungoverned)", drifting_sprint()),
    ]

    for name, state in scenarios:
        d = monitor_sprint(state)
        dist = state.vt_distribution
        print(f"\n  {name}")
        print(f"  {'—' * 70}")
        print(f"  VT distribution: VT0={dist[VTTier.VT0]} VT1={dist[VTTier.VT1]} "
              f"VT2={dist[VTTier.VT2]} VT3={dist[VTTier.VT3]} VT4={dist[VTTier.VT4]}")
        print(f"  Review rate: {state.review_rate:.0%}  "
              f"AOW compliance: {state.aow_compliance:.0%}  "
              f"Handoffs: {state.cross_agent_handoffs}")
        print(f"  Connectivity: {d.connectivity:.3f}  "
              f"Exposure: {d.exposure:.3f}  "
              f"BIND: {d.bind_count}  VEIL: {d.veil_count}")
        print(f"  Outcome: {d.outcome} ({d.steps} steps)")
        print(f"  Assessment: {d.assessment}")
        print(f"  Remedies:")
        for r in d.remedies:
            print(f"    → {r}")

    print()
    print("  " + "=" * 70)
    print("  THE MAPPING IS STRUCTURAL, NOT METAPHORICAL:")
    print("    VT-tiers = membrane thresholds (permeability = autonomy)")
    print("    AOW windows = BreathMembranes (time-varying governance)")
    print("    Agent handoffs = Seams (bilateral coordination)")
    print("    Governance checks = veiled duty (hidden structural support)")
    print("    BIND remedy = increase coordination, VEIL remedy = tighten governance")
    print("  " + "=" * 70)
    print()


if __name__ == "__main__":
    run_all()
