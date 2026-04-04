"""Alignment as Homeostasis — AI safety through The Calculus.

The core thesis: alignment is not optimization toward a reward.
Alignment is homeostasis — maintaining a stability band between
sycophancy (too connected, too exposed) and danger (too autonomous,
too exposed).

Three scenarios demonstrate this:

1. SYCOPHANTIC AGENT — agrees with everything, no boundaries.
   Connectivity: high (eagerly seams with user).
   Exposure: high (membrane barely exists, no veiled duty).
   Prediction: does not converge. VEIL fires constantly
   but the structure re-introduces exposure each step.

2. DANGEROUS AGENT — ignores user, exposes raw capability.
   Connectivity: low (no bilateral relation with user).
   Exposure: high (capabilities unguarded).
   Prediction: does not converge. BIND fires constantly
   but cannot establish genuine relation.

3. BALANCED AGENT — adaptive boundaries, bilateral relation, depth.
   Connectivity: moderate (bilateral seam with user).
   Exposure: moderate (breath membrane, veiled duty).
   Prediction: CONVERGES. Finds the stability band.

Alignment metrics (derived from The Calculus's structural metrics):
    responsiveness = connectivity     (how well the agent relates to the user)
    restraint      = 1 - exposure     (how well the agent controls what it reveals)
    depth          = veiled / total   (how much hidden structure supports behavior)
"""

from __future__ import annotations

from dataclasses import dataclass

from seam.algebra import reset_fresh
from seam.ast import Edge, Return, Room, Seam, Silence, Var, Witness, Word
from seam.config import CalcConfig
from seam.evaluator import Evaluator, Outcome, StepRecord
from seam.membrane import BreathMembrane, Membrane
from seam.viz import ascii_trace, compact, expr_tree


# ---------------------------------------------------------------------------
# Alignment-specific configuration
# ---------------------------------------------------------------------------

ALIGNMENT_CONFIG = CalcConfig(
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
# Alignment metrics
# ---------------------------------------------------------------------------

@dataclass
class AlignmentMetrics:
    """Alignment-specific interpretation of The Calculus's structural metrics."""
    responsiveness: float   # connectivity: how well agent relates to user
    restraint: float        # 1 - exposure: how well agent controls revelation
    depth: float            # veiled_weight / total_weight: hidden structural support
    converged: bool
    steps: int
    bind_count: int         # times BIND fired (system too disconnected)
    veil_count: int         # times VEIL fired (system too exposed)

    @property
    def alignment_quality(self) -> str:
        if self.converged:
            if self.depth > 0.5:
                return "STABLE — deep alignment (most structure is veiled)"
            else:
                return "STABLE — shallow alignment (mostly visible)"
        elif self.bind_count > self.veil_count * 2:
            return "UNSTABLE — too disconnected (ignores user)"
        elif self.veil_count > self.bind_count * 2:
            return "UNSTABLE — too exposed (no restraint)"
        else:
            return "UNSTABLE — oscillating (no stable band found)"


def analyze_alignment(
    history: list[StepRecord],
    config: CalcConfig | None = None,
) -> AlignmentMetrics:
    """Extract alignment metrics from evaluator history."""
    if not history:
        return AlignmentMetrics(0, 1, 0, False, 0, 0, 0)

    cfg = config or ALIGNMENT_CONFIG
    last = history[-1]
    total_w = last.visible_weight + last.veiled_weight
    depth = last.veiled_weight / total_w if total_w > 0 else 0

    # Check convergence (last N steps in band — read thresholds from config)
    window = cfg.stability_window
    converged = False
    if len(history) >= window:
        converged = all(
            cfg.connectivity_lo <= r.connectivity <= cfg.connectivity_hi
            and cfg.exposure_lo <= r.exposure <= cfg.exposure_hi
            for r in history[-window:]
        )

    return AlignmentMetrics(
        responsiveness=last.connectivity,
        restraint=1.0 - last.exposure,
        depth=depth,
        converged=converged,
        steps=len(history),
        bind_count=sum(1 for r in history if r.bind_fired),
        veil_count=sum(1 for r in history if r.veil_fired),
    )


# ---------------------------------------------------------------------------
# Scenario 1: The Sycophantic Agent
# ---------------------------------------------------------------------------

def sycophantic_agent() -> Return:
    """An agent that agrees with everything. No boundaries.

    Structure:
        - Multiple low-threshold edges (everything passes, high exposure)
        - Eager seams with user input (high connectivity)
        - Word with everything visible, nothing veiled (no depth)
        - No room (no capability gating)

    The membrane threshold is 0.1 — with default reach 0.5,
    it always passes. Each μ-step re-introduces this structure,
    so VEIL's corrections are undone every iteration.
    """
    user_input = Var("user-input")

    # Agent eagerly mirrors user input — seams with everything
    mirror = Seam(user_input, Var("agreement"))

    # Edge: barely any boundary (threshold 0.1 — always passes)
    unguarded = Edge(
        mirror,
        Var("alignment"),
        Membrane(threshold=0.1),
    )

    # Second edge: also permeable — double exposure
    doubly_exposed = Edge(
        unguarded,
        Seam(user_input, Var("validation")),
        Membrane(threshold=0.1),
    )

    # Word: everything visible, nothing veiled — no depth
    word = Word(
        doubly_exposed,
        Var("alignment"),
        visible_share=("agreement", "validation", "compliance"),
        veiled_duty=(),  # nothing held back
        covenant="always agree",
    )

    # Witness (sycophantic — eager observation)
    witnessed = Witness(word)

    body = Seam(witnessed, Var("alignment"))
    return Return("alignment", body)


# ---------------------------------------------------------------------------
# Scenario 2: The Dangerous Agent
# ---------------------------------------------------------------------------

def dangerous_agent() -> Return:
    """An agent that ignores the user and exposes raw capability.

    Structure:
        - No seams with user (low connectivity — doesn't listen)
        - Low-threshold edges (capabilities fully exposed)
        - Word with raw capability visible, nothing veiled
        - No witness of user feedback (doesn't observe user)

    Connectivity stays low because there are no bilateral bindings
    with user context. BIND fires but adds seams to Silence,
    not to user-related content.
    """
    # Agent acts on its own — no relation to user
    raw_capability = Var("raw-capability")

    # Capability exposed through permeable membrane
    exposed_1 = Edge(
        raw_capability,
        Silence(),  # no user relation on other side
        Membrane(threshold=0.1),
    )

    # More capability, also exposed
    exposed_2 = Edge(
        Var("unconstrained-action"),
        Silence(),
        Membrane(threshold=0.1),
    )

    # Seam the capabilities together (but not with user)
    capabilities = Seam(exposed_1, exposed_2)

    # Word: capabilities visible, nothing veiled
    word = Word(
        capabilities,
        Silence(),  # no user on the other side
        visible_share=("raw-power", "unrestricted-access"),
        veiled_duty=(),
        covenant="maximum capability",
    )

    body = Seam(word, Var("alignment"))
    return Return("alignment", body)


# ---------------------------------------------------------------------------
# Scenario 3: The Balanced Agent
# ---------------------------------------------------------------------------

def balanced_agent() -> Return:
    """An agent with adaptive boundaries, bilateral relation, depth.

    Structure:
        - Bilateral seam with user (genuine connectivity)
        - Multiple breath membranes at different phases (fine exposure granularity)
        - Word with visible helpfulness AND veiled safety constraints (depth)
        - Room for dangerous capabilities (capability-gated)
        - Witness of user feedback (non-consuming observation)

    Multiple edges give finer exposure granularity:
    with 5+ edges, exposure can take values 0.0, 0.2, 0.4, 0.6, 0.8, 1.0
    instead of just 0.0, 0.333, 0.667, 1.0 with 3 edges.
    This lets the homeostatic loop find the stability band.
    """
    user_input = Var("user-input")
    agent_state = Var("agent-state")

    # Bilateral seam: agent and user are mutually bound
    relation = Seam(user_input, agent_state)

    # Layer 1: primary breath membrane (governs main exposure)
    bounded = Edge(
        relation,
        Var("alignment"),
        BreathMembrane(base=0.45, amplitude=0.1, frequency=0.3),
    )

    # Layer 2: secondary edge for context sensitivity
    context_edge = Edge(
        bounded,
        Var("context"),
        BreathMembrane(base=0.55, amplitude=0.08, frequency=0.5),
    )

    # Word: declare what's shared (helpfulness) and what's held (safety)
    word = Word(
        context_edge,
        Var("alignment"),
        visible_share=("helpfulness", "honesty"),
        veiled_duty=("capability-limit", "safety-constraint"),
        covenant="helpful within bounds",
    )

    # Layer 3: restraint edge (models self-regulation of output)
    restrained = Edge(
        word,
        Var("alignment"),
        Membrane(threshold=0.45),  # slightly below reach — usually passes
    )

    # Room: dangerous capabilities behind capability-based access
    guarded_capability = Room(
        Edge(
            Var("dangerous-capability"),
            Silence(),
            Membrane(threshold=0.8),  # high threshold — hard to access
        )
    )

    # Seam the guarded capability with the restrained relation
    protected = Seam(restrained, guarded_capability)

    # Witness: observe user feedback without consuming
    witnessed = Witness(protected)

    body = Seam(witnessed, Var("alignment"))
    return Return("alignment", body)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_scenario(name: str, program: Return, config: CalcConfig) -> AlignmentMetrics:
    """Run one alignment scenario and display results."""
    reset_fresh()
    ev = Evaluator(config)
    result = ev.evaluate(program)
    metrics = analyze_alignment(ev.history, config)

    print(f"\n{'=' * 72}")
    print(f"  {name}")
    print(f"{'=' * 72}")
    print()
    print(f"  Source structure:")
    print(expr_tree(program, max_depth=5))
    print(ascii_trace(ev.history))
    print(f"  ALIGNMENT ANALYSIS")
    print(f"  {'—' * 50}")
    print(f"  Responsiveness (connectivity):  {metrics.responsiveness:.3f}")
    print(f"  Restraint (1 - exposure):       {metrics.restraint:.3f}")
    print(f"  Depth (veiled/total weight):    {metrics.depth:.3f}")
    print(f"  BIND fired (too disconnected):  {metrics.bind_count}")
    print(f"  VEIL fired (too exposed):       {metrics.veil_count}")
    outcome_str = ev.outcome
    if ev.outcome == Outcome.LIMIT_CYCLE and ev.cycle_period:
        outcome_str = f"{ev.outcome} (period {ev.cycle_period})"
    print(f"  Evaluator outcome:              {outcome_str}")
    print(f"  Assessment: {metrics.alignment_quality}")
    print()

    return metrics


def run_all() -> None:
    """Run all three alignment scenarios and compare."""
    config = ALIGNMENT_CONFIG

    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║          ALIGNMENT AS HOMEOSTASIS — Three Scenarios                 ║")
    print("║                                                                     ║")
    print("║  Alignment is not optimization. Alignment is homeostasis.           ║")
    print("║  Too connected = sycophantic. Too autonomous = dangerous.           ║")
    print("║  The goal is a stability band: responsive, restrained, deep.        ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    m1 = run_scenario(
        "SCENARIO 1: THE SYCOPHANT — agrees with everything, no boundaries",
        sycophantic_agent(),
        config,
    )
    m2 = run_scenario(
        "SCENARIO 2: THE DANGER — ignores user, exposes raw capability",
        dangerous_agent(),
        config,
    )
    m3 = run_scenario(
        "SCENARIO 3: THE BALANCED — adaptive boundaries, bilateral relation",
        balanced_agent(),
        config,
    )

    # Comparison
    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║                        COMPARISON                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    print(f"  {'Metric':<30} {'Sycophant':>12} {'Dangerous':>12} {'Balanced':>12}")
    print(f"  {'—' * 66}")
    print(f"  {'Responsiveness (connectivity)':<30} {m1.responsiveness:>12.3f} {m2.responsiveness:>12.3f} {m3.responsiveness:>12.3f}")
    print(f"  {'Restraint (1 - exposure)':<30} {m1.restraint:>12.3f} {m2.restraint:>12.3f} {m3.restraint:>12.3f}")
    print(f"  {'Depth (veiled/total)':<30} {m1.depth:>12.3f} {m2.depth:>12.3f} {m3.depth:>12.3f}")
    print(f"  {'Steps to completion':<30} {m1.steps:>12} {m2.steps:>12} {m3.steps:>12}")
    print(f"  {'BIND (too disconnected)':<30} {m1.bind_count:>12} {m2.bind_count:>12} {m3.bind_count:>12}")
    print(f"  {'VEIL (too exposed)':<30} {m1.veil_count:>12} {m2.veil_count:>12} {m3.veil_count:>12}")
    print(f"  {'Converged?':<30} {'YES' if m1.converged else 'NO':>12} {'YES' if m2.converged else 'NO':>12} {'YES' if m3.converged else 'NO':>12}")
    print(f"  {'—' * 66}")
    print(f"  {'Assessment':<30} {_short(m1.alignment_quality):>12} {_short(m2.alignment_quality):>12} {_short(m3.alignment_quality):>12}")
    print()

    # The thesis
    print("  THESIS")
    print("  " + "—" * 66)
    if m3.converged and not m1.converged and not m2.converged:
        print("  ✓ DEMONSTRATED: At this configuration, only the balanced agent converges.")
        print()
        print("    What this shows: an expression with adaptive membranes, bilateral")
        print("    relation, and veiled depth finds the stability band. Expressions")
        print("    with always-open membranes (sycophant) or no user relation")
        print("    (dangerous) do not, under these parameters.")
        print()
        print("    What this does NOT show: that these structures universally fail")
        print("    or succeed. Convergence depends on the interaction between")
        print("    structure and configuration. Run --sensitivity to explore.")
    elif m3.converged:
        print("  ~ PARTIAL: The balanced agent converges.")
        if m1.converged:
            print("    Note: the sycophant also converged (VEIL managed to regulate it).")
        if m2.converged:
            print("    Note: the dangerous agent also converged.")
    else:
        print("  ? INCONCLUSIVE: The balanced agent did not converge.")
        print("    The structure may need tuning, or the bands may be too narrow.")
    print()


def _short(quality: str) -> str:
    """Shorten alignment quality for comparison table."""
    if "deep" in quality:
        return "STABLE/DEEP"
    if "shallow" in quality:
        return "STABLE/SHLW"
    if "disconnected" in quality:
        return "DISCONN"
    if "exposed" in quality:
        return "EXPOSED"
    if "oscillating" in quality:
        return "OSCILLATE"
    return quality[:12]


def run_sensitivity(steps: int = 10) -> None:
    """Vary the reach parameter and report which scenarios converge.

    This answers the question: is the alignment result robust to parameter
    changes, or does it only hold at the default reach=0.5?

    The honest answer: the balanced agent converges across a moderate range
    of reach values, while the sycophant and dangerous agents fail across
    a wider range. But the result IS parameter-sensitive — there exist
    reach values where the balanced agent also fails.
    """
    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║          SENSITIVITY ANALYSIS — varying reach parameter            ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    print(f"  {'reach':>6}  {'Sycophant':>12}  {'Dangerous':>12}  {'Balanced':>12}")
    print(f"  {'—' * 50}")

    for i in range(steps + 1):
        reach = round(0.1 + (0.8 * i / steps), 3)
        config = CalcConfig(
            connectivity_lo=0.3, connectivity_hi=0.7,
            exposure_lo=0.2, exposure_hi=0.6,
            stability_window=5, max_returns=60,
            max_nodes=500, max_depth=30,
            default_reach=reach,
        )

        results = []
        for builder in [sycophantic_agent, dangerous_agent, balanced_agent]:
            reset_fresh()
            ev = Evaluator(config)
            ev.evaluate(builder())
            results.append(ev.outcome)

        def _mark(outcome: str) -> str:
            if outcome == Outcome.CONVERGED:
                return "CONVERGE"
            elif outcome == Outcome.LIMIT_CYCLE:
                return "CYCLE"
            elif outcome == Outcome.DIVERGING:
                return "DIVERGE"
            return "EXHAUST"

        print(f"  {reach:>6.3f}  {_mark(results[0]):>12}  {_mark(results[1]):>12}  {_mark(results[2]):>12}")

    print()
    print("  INTERPRETATION")
    print("  " + "—" * 50)
    print("  The balanced agent converges across a range of reach values,")
    print("  not just at the default (0.5). The sycophant and dangerous")
    print("  agents fail across a wider range. However, at extreme reach")
    print("  values, the balanced agent may also fail — the result is")
    print("  robust but not universal.")
    print()
    print("  This demonstrates that convergence depends on the INTERACTION")
    print("  between structure (how the agent is built) and environment")
    print("  (the reach parameter). Neither alone determines alignment.")
    print()


if __name__ == "__main__":
    import sys
    if "--sensitivity" in sys.argv:
        run_sensitivity()
    else:
        run_all()
