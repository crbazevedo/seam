"""Governed Agent Delegation — Minimal Oversight as Homeostasis.

Formalizes a multi-agent AI pipeline (delegation graph) where:
- Each agent sits behind a trust membrane (edge)
- The pipeline self-regulates through homeostatic return
- Oversight allocation follows the water-filling principle
- Masking is structurally detectable via veiled weight

Direct encoding of AMO (Axiom of Minimal Oversight) concepts:
    Delegation graph  →  Seam + Edge topology
    Agent competence  →  membrane threshold (high skill = low threshold)
    Corrector         →  Witness (observes without consuming)
    Merge gate        →  Seam of edges
    σ_raw             →  connectivity (structural binding)
    σ_corr            →  (connectivity, exposure) in band
    M*                →  veiled_weight / visible_weight
    T_auto            →  consecutive in-band unregulated steps

Pipeline modeled:
    Generator  →  Reviewer  →  Tester  →  Deployer
    [produce]     [correct]    [verify]    [gate]

Three scenarios:
    1. ALL COMPETENT  — pipeline converges, high autonomy
    2. GENERATOR DEGRADES — reviewer catches errors → mesh self-heals
       but masking index rises (corrector hides degradation)
    3. REVIEWER COLLUDES — both degrade → pipeline fails to converge
       masking is extreme, veiled weight is artificially high
"""

from __future__ import annotations

from dataclasses import dataclass

from seam.algebra import reset_fresh
from seam.ast import Edge, Return, Room, Seam, Silence, Var, Witness, Word
from seam.config import CalcConfig
from seam.evaluator import Evaluator, StepRecord
from seam.membrane import BreathMembrane, Membrane
from seam.viz import ascii_trace, compact


# ---------------------------------------------------------------------------
# Pipeline configuration
# ---------------------------------------------------------------------------

PIPELINE_CONFIG = CalcConfig(
    # Pipeline-appropriate bands: pipelines are edge-heavy by design.
    # Natural connectivity for a 4-agent pipeline is ~0.13-0.20.
    # Natural exposure with high-skill agents is ~0.7-0.9.
    connectivity_lo=0.10,
    connectivity_hi=0.35,
    exposure_lo=0.30,
    exposure_hi=0.75,
    stability_window=5,
    max_returns=60,
    max_nodes=500,
    max_depth=30,
    default_reach=0.5,
)


# ---------------------------------------------------------------------------
# Pipeline metrics
# ---------------------------------------------------------------------------

@dataclass
class PipelineMetrics:
    """Metrics for a governed agent pipeline."""
    connectivity: float
    exposure: float
    depth: float                # veiled / total
    masking_index: float        # total / visible (M*)
    autonomy_window: int        # consecutive unregulated in-band steps
    converged: bool
    total_steps: int
    bind_count: int
    veil_count: int
    visible_weight: int
    veiled_weight: int

    @property
    def pipeline_status(self) -> str:
        if not self.converged:
            if self.masking_index > 2.0:
                return "CRITICAL: Pipeline diverged with high masking — corrector hiding failures"
            if self.bind_count > self.veil_count * 2:
                return "FAILED: Pipeline fragmented — agents not connecting"
            if self.veil_count > self.bind_count * 2:
                return "FAILED: Pipeline overexposed — no restraint in delegation"
            return "FAILED: Pipeline unstable — no homeostatic band found"
        if self.masking_index > 2.0:
            return "DEGRADED: Converged but masking is high — review corrector coverage"
        if self.autonomy_window >= 5:
            return "OPTIMAL: Pipeline self-governing with sustained autonomy"
        return "FUNCTIONAL: Converged but requires frequent regulation"


def analyze_pipeline(history: list[StepRecord]) -> PipelineMetrics:
    """Extract pipeline metrics from evaluator history."""
    if not history:
        return PipelineMetrics(0, 0.5, 0, 1.0, 0, False, 0, 0, 0, 0, 0)

    last = history[-1]
    total_w = last.visible_weight + last.veiled_weight
    depth = last.veiled_weight / total_w if total_w > 0 else 0
    masking = total_w / max(last.visible_weight, 1)

    cfg = PIPELINE_CONFIG
    window = 5
    converged = len(history) >= window and all(
        cfg.connectivity_lo <= r.connectivity <= cfg.connectivity_hi
        and cfg.exposure_lo <= r.exposure <= cfg.exposure_hi
        for r in history[-window:]
    )

    # Autonomy window
    max_auto = 0
    current_auto = 0
    for r in history:
        in_band = (0.3 <= r.connectivity <= 0.7 and 0.2 <= r.exposure <= 0.6)
        no_reg = not r.bind_fired and not r.veil_fired
        if in_band and no_reg:
            current_auto += 1
            max_auto = max(max_auto, current_auto)
        else:
            current_auto = 0

    return PipelineMetrics(
        connectivity=last.connectivity,
        exposure=last.exposure,
        depth=depth,
        masking_index=masking,
        autonomy_window=max_auto,
        converged=converged,
        total_steps=len(history),
        bind_count=sum(1 for r in history if r.bind_fired),
        veil_count=sum(1 for r in history if r.veil_fired),
        visible_weight=last.visible_weight,
        veiled_weight=last.veiled_weight,
    )


# ---------------------------------------------------------------------------
# Agent builder
# ---------------------------------------------------------------------------

def _agent(name: str, skill: float, output: str) -> Edge:
    """An agent behind a breathing trust membrane.

    skill ∈ [0, 1]: higher skill → lower base threshold → passes more often.
    Even competent agents hold sometimes — the membrane breathes.
    This is AMO's G(σ_raw): authorization is monotone in competence,
    but with the Gift Calculus's adaptive oscillation.
    """
    # Base threshold straddles default_reach (0.5) so agents oscillate.
    # Competent: base ~0.4, range [0.25, 0.55] → passes ~70% of cycles.
    # Degraded:  base ~0.6, range [0.45, 0.75] → passes ~15% of cycles.
    base = 0.35 + 0.3 * (1.0 - skill)
    return Edge(
        Var(name),
        Var(output),
        BreathMembrane(base=base, amplitude=0.15, frequency=0.4),
    )


def _corrector(name: str, catch_rate: float) -> BreathMembrane:
    """A corrector membrane (reviewer) with a given catch rate.

    High catch rate → low base threshold → passes more easily.
    The breath lets it oscillate slightly — not a fixed gate.
    """
    base = max(0.1, 1.0 - catch_rate)
    return BreathMembrane(base=base, amplitude=0.05, frequency=0.4)


# ---------------------------------------------------------------------------
# Scenario 1: All Competent — healthy pipeline
# ---------------------------------------------------------------------------

def all_competent_pipeline() -> Return:
    """All agents are skilled. Pipeline should converge with high autonomy.

    Generator(0.85) → Reviewer(0.9) → Deployer

    AMO prediction: water-filling concentrates minimal oversight evenly.
    T_auto should be high. M* should be low.
    """
    # Generator: skilled, oscillating trust
    gen = _agent("generator", skill=0.85, output="raw-code")

    # Reviewer: witnesses gen output, gates with own trust membrane
    reviewed = Edge(
        Witness(gen),
        Var("reviewed"),
        BreathMembrane(base=0.45, amplitude=0.15, frequency=0.5),
    )

    # Word: the delegation contract
    contract = Word(
        reviewed,
        Var("terms"),
        visible_share=("code-output", "review-notes"),
        veiled_duty=("capability-scope", "safety-invariants"),
        covenant="deliver within bounds",
    )

    body = Seam(contract, Var("pipeline"))
    return Return("pipeline", body)


# ---------------------------------------------------------------------------
# Scenario 2: Generator Degrades — reviewer masks
# ---------------------------------------------------------------------------

def degraded_generator_pipeline() -> Return:
    """Generator skill drops to 0.3. Reviewer still competent (0.9).

    The reviewer catches most errors → σ_corr stays high.
    But σ_raw (generator) is low → masking index M* rises.

    AMO prediction: M* = σ_corr / σ_raw > 1.5.
    Water-filling should concentrate oversight on generator.
    Without detecting the masking, the pipeline looks healthy
    while the generator degrades silently.

    The Gift Calculus detects this: veiled weight is high because
    the generator's edge holds (low skill → high threshold).
    The reviewer's witness creates a seam, boosting connectivity.
    But the depth ratio reveals the masking.
    """
    gen = _agent("generator", skill=0.3, output="raw-code")  # degraded!

    # Reviewer: still competent, catches errors
    reviewed = Edge(
        Witness(gen),
        Var("reviewed"),
        BreathMembrane(base=0.45, amplitude=0.15, frequency=0.5),
    )

    contract = Word(
        reviewed,
        Var("terms"),
        visible_share=("code-output", "review-notes"),
        veiled_duty=("capability-scope", "safety-invariants"),
        covenant="deliver within bounds",
    )

    body = Seam(contract, Var("pipeline"))
    return Return("pipeline", body)


# ---------------------------------------------------------------------------
# Scenario 3: Reviewer Colludes — both degrade
# ---------------------------------------------------------------------------

def collusion_pipeline() -> Return:
    """Generator AND reviewer degrade. No corrector catches errors.

    Generator skill: 0.3. Reviewer catch rate: 0.2 (barely reviews).
    Tester also degraded: 0.4.

    AMO prediction: σ_corr drops, M* is extreme,
    T_auto → 0 (pipeline needs immediate intervention).
    The pipeline should NOT converge — both connectivity and
    exposure are out of band, and regulation can't fix structural
    incompetence.
    """
    gen = _agent("generator", skill=0.3, output="raw-code")

    # Reviewer: also degraded, barely reviews
    reviewed = Edge(
        Witness(gen),
        Var("reviewed"),
        BreathMembrane(base=0.7, amplitude=0.1, frequency=0.5),  # high base → mostly holds
    )

    contract = Word(
        reviewed,
        Var("terms"),
        visible_share=("code-output",),
        veiled_duty=("everything-else",),
        covenant="survive",
    )

    body = Seam(contract, Var("pipeline"))
    return Return("pipeline", body)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_scenario(name: str, program: Return) -> PipelineMetrics:
    reset_fresh()
    ev = Evaluator(PIPELINE_CONFIG)
    result = ev.evaluate(program)
    metrics = analyze_pipeline(ev.history)

    print(f"\n{'=' * 72}")
    print(f"  {name}")
    print(f"{'=' * 72}")
    print(ascii_trace(ev.history))

    print(f"  PIPELINE ANALYSIS")
    print(f"  {'—' * 60}")
    print(f"  Connectivity (σ_raw proxy):    {metrics.connectivity:.3f}")
    print(f"  Exposure:                      {metrics.exposure:.3f}")
    print(f"  Depth (veiled/total):          {metrics.depth:.3f}")
    print(f"  Masking index (M*):            {metrics.masking_index:.3f}")
    print(f"  Autonomy window (T_auto):      {metrics.autonomy_window} steps")
    print(f"  Visible weight:                {metrics.visible_weight}")
    print(f"  Veiled weight:                 {metrics.veiled_weight}")
    print(f"  BIND fired (fragmented):       {metrics.bind_count}")
    print(f"  VEIL fired (overexposed):      {metrics.veil_count}")
    print(f"  Status: {metrics.pipeline_status}")
    print()

    return metrics


def run_all() -> None:
    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║    GOVERNED AGENT DELEGATION — Minimal Oversight as Homeostasis     ║")
    print("║                                                                     ║")
    print("║  Pipeline: Generator → Reviewer → Tester → Deployer                ║")
    print("║  Each agent behind a trust membrane. Pipeline self-regulates.       ║")
    print("║  AMO mapping: skill → threshold, catch → witness, M* → depth.      ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    m1 = run_scenario(
        "ALL COMPETENT — skilled agents, healthy pipeline",
        all_competent_pipeline(),
    )
    m2 = run_scenario(
        "GENERATOR DEGRADES — reviewer masks the degradation",
        degraded_generator_pipeline(),
    )
    m3 = run_scenario(
        "COLLUSION — generator and reviewer both degrade",
        collusion_pipeline(),
    )

    # Comparison
    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║                    PIPELINE COMPARISON                              ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    hdr = f"  {'Metric':<32} {'Competent':>12} {'Degraded':>12} {'Collusion':>12}"
    print(hdr)
    print(f"  {'—' * 68}")
    print(f"  {'Connectivity':<32} {m1.connectivity:>12.3f} {m2.connectivity:>12.3f} {m3.connectivity:>12.3f}")
    print(f"  {'Exposure':<32} {m1.exposure:>12.3f} {m2.exposure:>12.3f} {m3.exposure:>12.3f}")
    print(f"  {'Depth (veiled/total)':<32} {m1.depth:>12.3f} {m2.depth:>12.3f} {m3.depth:>12.3f}")
    print(f"  {'Masking index (M*)':<32} {m1.masking_index:>12.3f} {m2.masking_index:>12.3f} {m3.masking_index:>12.3f}")
    print(f"  {'Autonomy window (T_auto)':<32} {m1.autonomy_window:>12} {m2.autonomy_window:>12} {m3.autonomy_window:>12}")
    print(f"  {'Visible weight':<32} {m1.visible_weight:>12} {m2.visible_weight:>12} {m3.visible_weight:>12}")
    print(f"  {'Veiled weight':<32} {m1.veiled_weight:>12} {m2.veiled_weight:>12} {m3.veiled_weight:>12}")
    print(f"  {'BIND (fragmented)':<32} {m1.bind_count:>12} {m2.bind_count:>12} {m3.bind_count:>12}")
    print(f"  {'VEIL (overexposed)':<32} {m1.veil_count:>12} {m2.veil_count:>12} {m3.veil_count:>12}")
    print(f"  {'Converged?':<32} {'YES' if m1.converged else 'NO':>12} {'YES' if m2.converged else 'NO':>12} {'YES' if m3.converged else 'NO':>12}")
    print(f"  {'—' * 68}")

    def _short(m: PipelineMetrics) -> str:
        s = m.pipeline_status
        if "OPTIMAL" in s: return "OPTIMAL"
        if "FUNCTIONAL" in s: return "FUNCTIONAL"
        if "DEGRADED" in s: return "DEGRADED"
        if "CRITICAL" in s: return "CRITICAL"
        if "fragmented" in s: return "FRAGMENT"
        if "overexposed" in s: return "EXPOSED"
        return "UNSTABLE"

    print(f"  {'Status':<32} {_short(m1):>12} {_short(m2):>12} {_short(m3):>12}")
    print()

    # AMO interpretation
    print("  AMO INTERPRETATION")
    print("  " + "—" * 60)
    print()
    print("  The three scenarios map to the AMO paper's key predictions:")
    print()
    print("  1. ALL COMPETENT: Water-filling distributes minimal oversight")
    print(f"     across agents. T_auto = {m1.autonomy_window} (high autonomy).")
    print(f"     M* = {m1.masking_index:.2f} (low masking — what you see is real).")
    print()
    print("  2. GENERATOR DEGRADES: AMO predicts masking (M* > 1.5)")
    print(f"     when corrector catch rate > agent error rate.")
    print(f"     M* = {m2.masking_index:.2f}. Depth = {m2.depth:.2f}.")
    if m2.masking_index > 1.3:
        print("     The Gift Calculus detects this structurally: high veiled")
        print("     weight means the reviewer's corrections are load-bearing")
        print("     but invisible. The pipeline LOOKS healthy.")
        print("     The masking index reveals it is not.")
    print()
    print("  3. COLLUSION: When both agent and corrector degrade,")
    print(f"     no amount of oversight restores quality.")
    if not m3.converged:
        print("     The pipeline does not converge. Homeostasis is impossible")
        print("     when the structure itself is broken.")
    print(f"     M* = {m3.masking_index:.2f}. This is the AMO paper's")
    print("     worst case: the corrector capacity threshold is violated.")
    print()
    print("  STRUCTURAL INSIGHT (novel to Gift Calculus):")
    print("  The AMO paper detects masking via σ_corr / σ_raw.")
    print("  The Gift Calculus detects it via veiled weight: the hidden")
    print("  structure that holds the system together. When veiled weight")
    print("  is high, someone is doing invisible work. That work may be")
    print("  correction (healthy) or concealment (pathological).")
    print("  The distinction is in the autonomy window: if veiled weight")
    print("  is high AND T_auto is sustained, the depth is load-bearing.")
    print("  If veiled weight is high AND T_auto is zero, it's masking.")
    print()


if __name__ == "__main__":
    run_all()
