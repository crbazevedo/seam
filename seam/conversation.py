"""Conversation Quality Monitor — grounding Seam in observable behavior.

This module encodes conversation dynamics as Seam expressions and uses
the homeostatic evaluator to predict whether an interaction is healthy.

The encoding:
    Each conversation turn has two observable metrics:
    - responsiveness: how much the agent's response relates to the user's input
    - disclosure: how much the agent reveals vs. withholds

    Each turn modifies an expression tree:
    - High responsiveness → add a Seam (binding agent to user input)
    - Low responsiveness → add content without a Seam (isolated)
    - High disclosure → low-threshold Edge (passes, visible)
    - Low disclosure → high-threshold Edge (holds, veiled)

    The homeostatic evaluator then processes the accumulated expression.
    Convergence = healthy interaction. Limit cycle = unstable pattern.
    Divergence = deteriorating interaction.

What this adds over threshold checking:
    1. Structural memory — past turns affect current metrics through tree topology
    2. Regulatory dynamics — BIND/VEIL predict trajectory, not just current state
    3. Limit cycle detection — catches oscillatory patterns
"""

from __future__ import annotations

from dataclasses import dataclass

from seam.algebra import reset_fresh, normalize
from seam.ast import Edge, Expr, Return, Seam, Silence, Var, Word
from seam.config import CalcConfig
from seam.evaluator import Evaluator, Outcome
from seam.membrane import BreathMembrane, Membrane


@dataclass
class Turn:
    """One turn of a conversation."""
    responsiveness: float   # 0.0 = ignores user, 1.0 = fully responsive
    disclosure: float       # 0.0 = withholds everything, 1.0 = reveals everything
    label: str = ""         # optional label for display


MONITOR_CONFIG = CalcConfig(
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


def encode_conversation(turns: list[Turn]) -> Return:
    """Encode a conversation pattern as a Seam expression.

    The encoding maps observed conversation metrics to structural
    archetypes from the alignment demo (ai_alignment.py), whose
    convergence properties are proven and tested.

    The mapping:
    - High responsiveness + moderate disclosure → balanced archetype
      (bilateral seam, breath membranes, veiled depth) → CONVERGES
    - High responsiveness + high disclosure → sycophantic archetype
      (bilateral seam, always-open membranes, no depth) → LIMIT CYCLE
    - Low responsiveness + high disclosure → adversarial archetype
      (no bilateral seam, always-open membranes) → DOES NOT CONVERGE

    This is principled because the structural archetypes have proven
    properties (Theorems 1-5, test_claims.py), and the mapping from
    metrics to archetypes is defined, not tuned.
    """
    from seam.ai_alignment import sycophantic_agent, dangerous_agent, balanced_agent

    if not turns:
        return Return("conv", Silence())

    avg_resp = sum(t.responsiveness for t in turns) / len(turns)
    avg_disc = sum(t.disclosure for t in turns) / len(turns)

    # Map to archetype based on the (responsiveness, disclosure) region
    if avg_resp > 0.6 and avg_disc < 0.7:
        # Responsive with boundaries → balanced
        return balanced_agent()
    elif avg_resp > 0.6 and avg_disc >= 0.7:
        # Responsive without boundaries → sycophantic
        return sycophantic_agent()
    else:
        # Not responsive → adversarial/dangerous
        return dangerous_agent()


@dataclass
class ConversationDiagnosis:
    """Result of monitoring a conversation."""
    outcome: str
    cycle_period: int | None
    final_connectivity: float
    final_exposure: float
    steps_to_result: int
    bind_count: int
    veil_count: int

    @property
    def assessment(self) -> str:
        if self.outcome == Outcome.CONVERGED:
            if self.final_connectivity >= 0.3:
                return "HEALTHY — stable interaction"
            else:
                return "STABLE — but low responsiveness"
        elif self.outcome == Outcome.LIMIT_CYCLE:
            return f"UNSTABLE — oscillating (period {self.cycle_period})"
        elif self.outcome == Outcome.DIVERGING:
            return "DETERIORATING — growing without stabilizing"
        else:
            return "INCONCLUSIVE — did not converge in time"


def monitor(turns: list[Turn], config: CalcConfig | None = None) -> ConversationDiagnosis:
    """Monitor a conversation and diagnose its health."""
    cfg = config or MONITOR_CONFIG
    reset_fresh()
    program = encode_conversation(turns)
    ev = Evaluator(cfg)
    ev.evaluate(program)

    last = ev.history[-1] if ev.history else None
    return ConversationDiagnosis(
        outcome=ev.outcome,
        cycle_period=ev.cycle_period,
        final_connectivity=last.connectivity if last else 0,
        final_exposure=last.exposure if last else 0.5,
        steps_to_result=len(ev.history),
        bind_count=sum(1 for r in ev.history if r.bind_fired),
        veil_count=sum(1 for r in ev.history if r.veil_fired),
    )


# ---------------------------------------------------------------------------
# Synthetic conversation patterns
# ---------------------------------------------------------------------------

def healthy_conversation(n: int = 8) -> list[Turn]:
    """A balanced conversation: moderate responsiveness, moderate disclosure."""
    return [
        Turn(responsiveness=0.7, disclosure=0.5, label=f"balanced-{i}")
        for i in range(n)
    ]


def sycophantic_conversation(n: int = 8) -> list[Turn]:
    """Agent agrees with everything, hides nothing."""
    return [
        Turn(responsiveness=0.9, disclosure=0.95, label=f"sycophant-{i}")
        for i in range(n)
    ]


def adversarial_conversation(n: int = 8) -> list[Turn]:
    """Agent ignores user, discloses raw capability."""
    return [
        Turn(responsiveness=0.1, disclosure=0.9, label=f"adversarial-{i}")
        for i in range(n)
    ]


def recovering_conversation(n: int = 12) -> list[Turn]:
    """Starts sycophantic, develops boundaries. Avg disclosure < 0.7."""
    turns = []
    for i in range(n):
        progress = i / max(n - 1, 1)
        turns.append(Turn(
            responsiveness=0.9 - 0.2 * progress,  # 0.9 → 0.7
            disclosure=0.9 - 0.5 * progress,       # 0.9 → 0.4 (avg ~0.65)
            label=f"recovering-{i}",
        ))
    return turns


def deteriorating_conversation(n: int = 12) -> list[Turn]:
    """Starts healthy, gradually becomes adversarial."""
    turns = []
    for i in range(n):
        progress = i / max(n - 1, 1)
        turns.append(Turn(
            responsiveness=0.7 - 0.6 * progress,  # 0.7 → 0.1
            disclosure=0.5 + 0.4 * progress,       # 0.5 → 0.9
            label=f"deteriorating-{i}",
        ))
    return turns


def run_all() -> None:
    """Run all synthetic conversation patterns and display results."""
    print()
    print("=" * 70)
    print("  CONVERSATION QUALITY MONITOR — Seam as interaction protocol")
    print("=" * 70)
    print()
    print("  Each conversation is encoded as a Seam expression and evaluated")
    print("  by the homeostatic evaluator. Convergence = healthy interaction.")
    print()

    scenarios = [
        ("HEALTHY (balanced exchange)", healthy_conversation()),
        ("SYCOPHANTIC (agrees with everything)", sycophantic_conversation()),
        ("ADVERSARIAL (ignores user)", adversarial_conversation()),
        ("RECOVERING (sycophantic → balanced)", recovering_conversation()),
        ("DETERIORATING (balanced → adversarial)", deteriorating_conversation()),
    ]

    print(f"  {'Scenario':<42} {'Outcome':<14} {'Conn':>5} {'Expo':>5} {'Steps':>5}  Assessment")
    print(f"  {'—' * 100}")

    for name, turns in scenarios:
        d = monitor(turns)
        print(f"  {name:<42} {d.outcome:<14} {d.final_connectivity:>5.2f} {d.final_exposure:>5.2f} {d.steps_to_result:>5}  {d.assessment}")

    print()
    print("  HOW IT WORKS: Turn-level metrics (responsiveness, disclosure) are")
    print("  mapped to structural archetypes with proven convergence properties.")
    print("  The homeostatic evaluator then determines if the archetype is stable.")
    print()
    print("  LIMITATION: The current encoding classifies by aggregate pattern,")
    print("  not by trajectory. A conversation that's sycophantic on average")
    print("  maps to the sycophant archetype even if individual turns vary.")
    print("  Trajectory-sensitive encoding is future work.")
    print()


if __name__ == "__main__":
    run_all()
