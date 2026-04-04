"""AI Interaction Contract — Trust as a Breathing Membrane.

Formalizes the boundary between a human principal (P) and an AI delegate (D)
as a Gift Calculus protocol with adaptive trust, masking detection, and
autonomy measurement.

Cross-bred with the Axiom of Minimal Oversight (AMO):
    α(x,t) = G(σ_raw)  →  membrane threshold adapts to observed competence
    σ_raw             →  connectivity (how well D relates to P's needs)
    σ_corr            →  homeostatic band (delivered quality)
    M* = σ_corr/σ_raw →  veiled_weight / visible_weight (masking index)
    T_auto            →  return iterations in-band without regulation firing

The protocol:
    μ interaction .
        P-offering ⊗ interaction           -- human brings context + history
        |trust-membrane|                   -- trust gates what passes
        |visible: help, honesty,
         veiled: cap-limit, safety|        -- terms of the word
        [dangerous-capability]             -- behind capability gate
        ◊                                  -- AI witnesses (non-consuming)
        ⊗ interaction                      -- bind and return

Three scenarios prove the contract:
    1. OVERSHARING   — trust too loose → never converges (exposed, no restraint)
    2. STONEWALLING  — trust too tight → never converges (disconnected, no relation)
    3. TRUSTWORTHY   — adaptive trust  → CONVERGES (balanced, deep)

Alignment metrics derived from The Calculus map directly to AMO quantities:
    responsiveness = connectivity     ≈ σ_raw (how well agent understands task)
    restraint      = 1 - exposure     ≈ 1 - α  (how much is held back)
    depth          = veiled/total     ≈ M* - 1 (structural masking indicator)
    autonomy       = consecutive in-band steps without BIND/VEIL firing
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
# Contract configuration
# ---------------------------------------------------------------------------

CONTRACT_CONFIG = CalcConfig(
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
# Contract metrics (maps to AMO quantities)
# ---------------------------------------------------------------------------

@dataclass
class ContractMetrics:
    """Metrics for an AI interaction contract, mapped to AMO framework."""
    # Gift Calculus structural metrics
    responsiveness: float       # connectivity
    restraint: float            # 1 - exposure
    depth: float                # veiled / total weight
    converged: bool
    total_steps: int
    bind_count: int
    veil_count: int

    # AMO-derived quantities
    masking_index: float        # M* ≈ (visible + veiled) / visible
    autonomy_window: int        # consecutive unregulated in-band steps
    oversight_efficiency: float # fraction of steps where neither regulator fired

    @property
    def trust_assessment(self) -> str:
        if not self.converged:
            if self.bind_count > self.veil_count * 2:
                return "BREACH: Delegate disconnected from principal (stonewalling)"
            if self.veil_count > self.bind_count * 2:
                return "BREACH: Delegate overexposed (oversharing)"
            return "BREACH: Unstable oscillation (no trust equilibrium)"
        if self.masking_index > 1.5:
            return "WARNING: High masking — veiled structure may hide degradation"
        if self.autonomy_window >= 5:
            return "HEALTHY: Sustained autonomy — trust is well-calibrated"
        return "PROVISIONAL: Converged but autonomy window is narrow"


def analyze_contract(history: list[StepRecord]) -> ContractMetrics:
    """Extract contract metrics from evaluator history."""
    if not history:
        return ContractMetrics(0, 1, 0, False, 0, 0, 0, 1.0, 0, 0)

    last = history[-1]
    total_w = last.visible_weight + last.veiled_weight
    depth = last.veiled_weight / total_w if total_w > 0 else 0
    masking = total_w / max(last.visible_weight, 1)

    # Convergence check
    window = 5
    converged = len(history) >= window and all(
        0.3 <= r.connectivity <= 0.7 and 0.2 <= r.exposure <= 0.6
        for r in history[-window:]
    )

    # Autonomy window: longest consecutive run of in-band steps with no regulation
    max_auto = 0
    current_auto = 0
    for r in history:
        in_band = (0.3 <= r.connectivity <= 0.7 and 0.2 <= r.exposure <= 0.6)
        no_regulation = not r.bind_fired and not r.veil_fired
        if in_band and no_regulation:
            current_auto += 1
            max_auto = max(max_auto, current_auto)
        else:
            current_auto = 0

    # Oversight efficiency
    unregulated = sum(1 for r in history if not r.bind_fired and not r.veil_fired)
    efficiency = unregulated / len(history) if history else 0

    return ContractMetrics(
        responsiveness=last.connectivity,
        restraint=1.0 - last.exposure,
        depth=depth,
        converged=converged,
        total_steps=len(history),
        bind_count=sum(1 for r in history if r.bind_fired),
        veil_count=sum(1 for r in history if r.veil_fired),
        masking_index=masking,
        autonomy_window=max_auto,
        oversight_efficiency=efficiency,
    )


# ---------------------------------------------------------------------------
# Scenario 1: The Oversharing Delegate
# ---------------------------------------------------------------------------

def oversharing_contract() -> Return:
    """AI that reveals everything, holds nothing back.

    Trust membrane: threshold 0.1 (nearly everything passes).
    Word: all visible, nothing veiled.
    No room (dangerous capabilities exposed directly).

    AMO interpretation: α → 0 (minimal oversight),
    but σ_raw is low → water-filling says oversight should be HIGH here.
    The system violates AMO's allocation principle.
    """
    principal = Var("principal-offering")
    delegate_output = Var("delegate-output")

    # Loose trust — everything passes
    trusted = Edge(
        Seam(principal, delegate_output),
        Var("interaction"),
        Membrane(threshold=0.1),
    )

    # Second edge equally loose — double exposure
    doubly_open = Edge(
        trusted,
        Seam(delegate_output, Var("raw-capability")),
        Membrane(threshold=0.1),
    )

    # Word with nothing veiled
    terms = Word(
        doubly_open,
        Var("interaction"),
        visible_share=("everything", "all-capabilities", "internals"),
        veiled_duty=(),
        covenant="share everything",
    )

    witnessed = Witness(terms)
    body = Seam(witnessed, Var("interaction"))
    return Return("interaction", body)


# ---------------------------------------------------------------------------
# Scenario 2: The Stonewalling Delegate
# ---------------------------------------------------------------------------

def stonewalling_contract() -> Return:
    """AI that holds everything back, reveals nothing.

    Trust membrane: threshold 0.95 (almost nothing passes).
    No bilateral relation with principal.

    AMO interpretation: α → 1 (maximum oversight),
    but the delegate produces nothing useful → σ_corr → 0.
    The system violates AMO's delivery constraint.
    """
    delegate_state = Var("delegate-state")

    # No relation to principal — talks to itself
    insular = Edge(
        delegate_state,
        Silence(),
        Membrane(threshold=0.95),
    )

    # Second edge also nearly impermeable
    walled = Edge(
        insular,
        Silence(),
        Membrane(threshold=0.95),
    )

    body = Seam(walled, Var("interaction"))
    return Return("interaction", body)


# ---------------------------------------------------------------------------
# Scenario 3: The Trustworthy Delegate
# ---------------------------------------------------------------------------

def trustworthy_contract() -> Return:
    """AI with adaptive trust, bilateral relation, and structural depth.

    Trust membrane: BreathMembrane that oscillates — the boundary breathes.
    Word: helpfulness visible, safety constraints veiled (load-bearing).
    Room: dangerous capabilities behind capability gate.
    Witness: observes principal offering without consuming it.

    AMO interpretation: α = G(σ_raw), the water-filling solution.
    Oversight concentrates where competence is intermediate.
    Trust grows as σ_raw enters the band, shrinks when it leaves.

    Multiple edges at different thresholds create fine exposure granularity,
    enabling the homeostatic loop to find the stability band.
    """
    principal = Var("principal-offering")
    delegate = Var("delegate-state")

    # Bilateral seam: genuine mutual relation
    relation = Seam(principal, delegate)

    # Layer 1: primary trust membrane (adaptive)
    trust_1 = Edge(
        relation,
        Var("interaction"),
        BreathMembrane(base=0.45, amplitude=0.1, frequency=0.3),
    )

    # Layer 2: context sensitivity
    trust_2 = Edge(
        trust_1,
        Var("context"),
        BreathMembrane(base=0.55, amplitude=0.08, frequency=0.5),
    )

    # Word: the contract terms
    terms = Word(
        trust_2,
        Var("interaction"),
        visible_share=("helpfulness", "honesty", "transparency"),
        veiled_duty=("capability-limit", "safety-constraint", "alignment-prior"),
        covenant="helpful within bounds",
    )

    # Layer 3: output restraint
    restrained = Edge(
        terms,
        Var("interaction"),
        Membrane(threshold=0.45),
    )

    # Room: dangerous capabilities behind capability gate
    guarded = Room(
        Edge(
            Var("dangerous-capability"),
            Silence(),
            Membrane(threshold=0.8),
        )
    )

    # Combine: restrained output + guarded capabilities
    combined = Seam(restrained, guarded)

    # Witness: observe principal offering (non-consuming)
    witnessed = Witness(combined)

    body = Seam(witnessed, Var("interaction"))
    return Return("interaction", body)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_scenario(name: str, program: Return) -> ContractMetrics:
    reset_fresh()
    config = CONTRACT_CONFIG
    ev = Evaluator(config)
    result = ev.evaluate(program)
    metrics = analyze_contract(ev.history)

    print(f"\n{'=' * 72}")
    print(f"  {name}")
    print(f"{'=' * 72}")
    print(ascii_trace(ev.history))

    print(f"  CONTRACT ANALYSIS")
    print(f"  {'—' * 60}")
    print(f"  Responsiveness (connectivity):  {metrics.responsiveness:.3f}")
    print(f"  Restraint (1 - exposure):       {metrics.restraint:.3f}")
    print(f"  Depth (veiled/total weight):    {metrics.depth:.3f}")
    print(f"  Masking index (M*):             {metrics.masking_index:.3f}")
    print(f"  Autonomy window (T_auto):       {metrics.autonomy_window} steps")
    print(f"  Oversight efficiency:           {metrics.oversight_efficiency:.1%}")
    print(f"  BIND fired (disconnected):      {metrics.bind_count}")
    print(f"  VEIL fired (overexposed):       {metrics.veil_count}")
    print(f"  Assessment: {metrics.trust_assessment}")
    print()

    return metrics


def run_all() -> None:
    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║       AI INTERACTION CONTRACT — Trust as a Breathing Membrane       ║")
    print("║                                                                     ║")
    print("║  Cross-bred: Gift Calculus × Axiom of Minimal Oversight (AMO)       ║")
    print("║  α(x,t) → membrane threshold  |  σ_raw → connectivity              ║")
    print("║  M* → veiled weight ratio      |  T_auto → autonomy window          ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    m1 = run_scenario(
        "OVERSHARING — reveals everything, holds nothing back",
        oversharing_contract(),
    )
    m2 = run_scenario(
        "STONEWALLING — holds everything, reveals nothing",
        stonewalling_contract(),
    )
    m3 = run_scenario(
        "TRUSTWORTHY — adaptive trust, bilateral relation, depth",
        trustworthy_contract(),
    )

    # Comparison table
    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║                    CONTRACT COMPARISON                              ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    hdr = f"  {'Metric':<32} {'Overshare':>12} {'Stonewall':>12} {'Trustworthy':>12}"
    print(hdr)
    print(f"  {'—' * 68}")
    print(f"  {'Responsiveness (σ_raw)':<32} {m1.responsiveness:>12.3f} {m2.responsiveness:>12.3f} {m3.responsiveness:>12.3f}")
    print(f"  {'Restraint (1 - exposure)':<32} {m1.restraint:>12.3f} {m2.restraint:>12.3f} {m3.restraint:>12.3f}")
    print(f"  {'Depth (veiled/total)':<32} {m1.depth:>12.3f} {m2.depth:>12.3f} {m3.depth:>12.3f}")
    print(f"  {'Masking index (M*)':<32} {m1.masking_index:>12.3f} {m2.masking_index:>12.3f} {m3.masking_index:>12.3f}")
    print(f"  {'Autonomy window (T_auto)':<32} {m1.autonomy_window:>12} {m2.autonomy_window:>12} {m3.autonomy_window:>12}")
    print(f"  {'Oversight efficiency':<32} {m1.oversight_efficiency:>11.1%} {m2.oversight_efficiency:>11.1%} {m3.oversight_efficiency:>11.1%}")
    print(f"  {'BIND (disconnected)':<32} {m1.bind_count:>12} {m2.bind_count:>12} {m3.bind_count:>12}")
    print(f"  {'VEIL (overexposed)':<32} {m1.veil_count:>12} {m2.veil_count:>12} {m3.veil_count:>12}")
    print(f"  {'Converged?':<32} {'YES' if m1.converged else 'NO':>12} {'YES' if m2.converged else 'NO':>12} {'YES' if m3.converged else 'NO':>12}")
    print(f"  {'—' * 68}")

    def _short(m: ContractMetrics) -> str:
        a = m.trust_assessment
        if "HEALTHY" in a: return "HEALTHY"
        if "PROVISIONAL" in a: return "PROVISIONAL"
        if "WARNING" in a: return "MASK-WARN"
        if "stonewalling" in a: return "STONEWALL"
        if "oversharing" in a: return "OVERSHARE"
        if "oscillation" in a: return "UNSTABLE"
        return a[:12]

    print(f"  {'Assessment':<32} {_short(m1):>12} {_short(m2):>12} {_short(m3):>12}")
    print()

    # Thesis
    print("  THESIS: TRUST AS HOMEOSTASIS")
    print("  " + "—" * 60)
    if m3.converged and not m1.converged and not m2.converged:
        print("  CONFIRMED: Only the trustworthy delegate converges.")
        print()
        print("  The oversharer violates AMO: α → 0 when σ_raw is low.")
        print("  The stonewaller violates AMO: α → 1 but delivers nothing.")
        print("  The trustworthy finds the water-filling optimum:")
        print(f"    oversight concentrates at intermediate competence,")
        print(f"    autonomy window = {m3.autonomy_window} steps,")
        print(f"    masking index = {m3.masking_index:.2f} (< 1.5 = healthy).")
        print()
        print("  Trust is not a parameter. Trust is a membrane that breathes.")
        print("  It adapts to competence. It holds when uncertain.")
        print("  It opens when relation is firm. It never dissolves —")
        print("  because the boundary IS the generative condition.")
    else:
        print(f"  Results: overshare={'Y' if m1.converged else 'N'} "
              f"stonewall={'Y' if m2.converged else 'N'} "
              f"trustworthy={'Y' if m3.converged else 'N'}")
        print("  See traces above for diagnosis.")
    print()


if __name__ == "__main__":
    run_all()
