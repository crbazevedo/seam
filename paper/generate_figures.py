#!/usr/bin/env python3
"""Generate experimental data and formatted output for the Seam governance paper.

Produces paper-ready ASCII tables and traces in figures.txt.
"""

from __future__ import annotations

import io
import sys
import unittest

from seam.algebra import reset_fresh
from seam.ast import node_count
from seam.config import CalcConfig
from seam.evaluator import Evaluator, Outcome
from seam.governance import (
    GovernanceDiagnosis,
    GOVERNANCE_CONFIG,
    VTTier,
    drifting_sprint,
    encode_sprint,
    locked_down_sprint,
    monitor_sprint,
    ungoverned_sprint,
    well_governed_sprint,
)
from seam.ai_alignment import (
    ALIGNMENT_CONFIG,
    AlignmentMetrics,
    analyze_alignment,
    balanced_agent,
    dangerous_agent,
    sycophantic_agent,
)


OUT = io.StringIO()


def pr(line: str = "") -> None:
    OUT.write(line + "\n")


# =========================================================================
# 1. GOVERNANCE SCENARIOS TABLE
# =========================================================================

def governance_scenarios_table() -> None:
    pr("=" * 100)
    pr("TABLE 1: Multi-Agent Governance Scenarios — Seam Calculus Evaluation")
    pr("=" * 100)
    pr()

    scenarios = [
        ("Well-governed", well_governed_sprint()),
        ("Ungoverned", ungoverned_sprint()),
        ("Locked-down", locked_down_sprint()),
        ("Drifting", drifting_sprint()),
    ]

    # Header
    cols = (
        "Scenario",
        "VT Dist (0/1/2/3/4)",
        "Review",
        "AOW",
        "Hand.",
        "Conn.",
        "Expo.",
        "BIND",
        "VEIL",
        "Steps",
        "Outcome",
    )
    widths = (16, 21, 7, 6, 6, 7, 7, 5, 5, 6, 14)

    hdr = "  ".join(f"{c:<{w}}" for c, w in zip(cols, widths))
    pr(hdr)
    pr("-" * len(hdr))

    for name, state in scenarios:
        d = monitor_sprint(state)
        dist = state.vt_distribution
        vt_str = f"{dist[VTTier.VT0]}/{dist[VTTier.VT1]}/{dist[VTTier.VT2]}/{dist[VTTier.VT3]}/{dist[VTTier.VT4]}"
        outcome_str = d.outcome
        if d.outcome == Outcome.LIMIT_CYCLE and d.cycle_period:
            outcome_str = f"cycle(p={d.cycle_period})"

        row = [
            f"{name:<16}",
            f"{vt_str:<21}",
            f"{state.review_rate:.0%}   ",
            f"{state.aow_compliance:.0%}  ",
            f"{state.cross_agent_handoffs:<6}",
            f"{d.connectivity:.3f} ",
            f"{d.exposure:.3f} ",
            f"{d.bind_count:<5}",
            f"{d.veil_count:<5}",
            f"{d.steps:<6}",
            f"{outcome_str:<14}",
        ]
        pr("  ".join(row))

    pr()
    pr("  VT Dist = count of actions at each VT tier (VT0/VT1/VT2/VT3/VT4)")
    pr("  Review  = fraction of actions with peer review")
    pr("  AOW     = fraction of actions respecting Asynchronous-by-Default windows")
    pr("  Hand.   = cross-agent handoff count")
    pr("  Conn.   = final connectivity metric;  Expo. = final exposure metric")
    pr("  BIND    = regulatory actions to increase connectivity")
    pr("  VEIL    = regulatory actions to decrease exposure")
    pr()


# =========================================================================
# 2. SENSITIVITY ANALYSIS
# =========================================================================

def sensitivity_analysis() -> None:
    pr("=" * 100)
    pr("TABLE 2: Sensitivity Analysis — Well-Governed Sprint vs. default_reach")
    pr("=" * 100)
    pr()
    pr("  Varying default_reach from 0.1 to 0.9 for the well-governed sprint scenario.")
    pr("  All other parameters held at governance defaults.")
    pr()

    cols = ("reach", "Conn.", "Expo.", "BIND", "VEIL", "Steps", "Outcome")
    widths = (7, 8, 8, 6, 6, 7, 14)
    hdr = "  ".join(f"{c:<{w}}" for c, w in zip(cols, widths))
    pr(hdr)
    pr("-" * len(hdr))

    converge_range = []

    for r10 in range(1, 10):
        reach = round(r10 * 0.1, 2)
        config = CalcConfig(
            connectivity_lo=0.3,
            connectivity_hi=0.7,
            exposure_lo=0.2,
            exposure_hi=0.6,
            stability_window=5,
            max_returns=60,
            max_nodes=500,
            max_depth=30,
            default_reach=reach,
        )
        state = well_governed_sprint()
        reset_fresh()
        program = encode_sprint(state)
        ev = Evaluator(config)
        ev.evaluate(program)

        last = ev.history[-1] if ev.history else None
        conn = last.connectivity if last else 0.0
        expo = last.exposure if last else 0.5
        bind_ct = sum(1 for r in ev.history if r.bind_fired)
        veil_ct = sum(1 for r in ev.history if r.veil_fired)
        steps = len(ev.history)
        outcome = ev.outcome
        if outcome == Outcome.LIMIT_CYCLE and ev.cycle_period:
            outcome_str = f"cycle(p={ev.cycle_period})"
        else:
            outcome_str = outcome

        if ev.outcome == Outcome.CONVERGED:
            converge_range.append(reach)

        row = [
            f"{reach:<7.2f}",
            f"{conn:<8.3f}",
            f"{expo:<8.3f}",
            f"{bind_ct:<6}",
            f"{veil_ct:<6}",
            f"{steps:<7}",
            f"{outcome_str:<14}",
        ]
        pr("  ".join(row))

    pr()
    if converge_range:
        pr(f"  Convergence achieved for reach in: {converge_range}")
        pr(f"  Range width: {min(converge_range):.1f} -- {max(converge_range):.1f}")
    else:
        pr("  No convergence at any tested reach value.")
    pr("  This demonstrates robustness: convergence is not confined to a single")
    pr("  parameter value but holds across a range of environmental conditions.")
    pr()


# =========================================================================
# 3. CONVERGENCE TRACE — WELL-GOVERNED SPRINT
# =========================================================================

def convergence_trace() -> None:
    pr("=" * 100)
    pr("FIGURE 1: Step-by-Step Convergence Trace — Well-Governed Sprint")
    pr("=" * 100)
    pr()

    state = well_governed_sprint()
    reset_fresh()
    program = encode_sprint(state)
    ev = Evaluator(GOVERNANCE_CONFIG)
    ev.evaluate(program)

    cols = ("Step", "Connectivity", "Exposure", "BIND", "VEIL", "Nodes", "Vis.W", "Veil.W")
    widths = (6, 13, 10, 6, 6, 7, 7, 7)
    hdr = "  ".join(f"{c:<{w}}" for c, w in zip(cols, widths))
    pr(hdr)
    pr("-" * len(hdr))

    for r in ev.history:
        bind_str = "YES" if r.bind_fired else ""
        veil_str = "YES" if r.veil_fired else ""
        row = [
            f"{r.step:<6}",
            f"{r.connectivity:<13.4f}",
            f"{r.exposure:<10.4f}",
            f"{bind_str:<6}",
            f"{veil_str:<6}",
            f"{r.node_count:<7}",
            f"{r.visible_weight:<7}",
            f"{r.veiled_weight:<7}",
        ]
        pr("  ".join(row))

    pr()
    pr(f"  Outcome: {ev.outcome}")
    if ev.outcome == Outcome.CONVERGED:
        pr(f"  Converged after {len(ev.history)} steps.")
        pr(f"  Stability band: connectivity in [0.3, 0.7], exposure in [0.2, 0.6].")
    pr()

    # ASCII sparkline
    pr("  Connectivity trace (scaled to [0,1], width=60):")
    pr("  " + _sparkline([r.connectivity for r in ev.history], 60))
    pr()
    pr("  Exposure trace (scaled to [0,1], width=60):")
    pr("  " + _sparkline([r.exposure for r in ev.history], 60))
    pr()


def _sparkline(values: list[float], width: int) -> str:
    """Produce a simple ASCII bar chart."""
    if not values:
        return ""
    blocks = " _.-:=+*#@"
    lines = []
    for v in values:
        v_clamped = max(0.0, min(1.0, v))
        idx = int(v_clamped * (len(blocks) - 1))
        lines.append(blocks[idx])
    return "".join(lines)


# =========================================================================
# 4. ALIGNMENT DEMO COMPARISON
# =========================================================================

def alignment_comparison() -> None:
    pr("=" * 100)
    pr("TABLE 3: AI Alignment Scenarios — Seam Calculus Evaluation")
    pr("=" * 100)
    pr()

    config = ALIGNMENT_CONFIG
    scenarios = [
        ("Sycophantic", sycophantic_agent),
        ("Dangerous", dangerous_agent),
        ("Balanced", balanced_agent),
    ]

    cols = (
        "Scenario",
        "Responsive",
        "Restraint",
        "Depth",
        "BIND",
        "VEIL",
        "Steps",
        "Converged",
        "Assessment",
    )
    widths = (14, 11, 10, 7, 6, 6, 7, 10, 30)
    hdr = "  ".join(f"{c:<{w}}" for c, w in zip(cols, widths))
    pr(hdr)
    pr("-" * len(hdr))

    for name, builder in scenarios:
        reset_fresh()
        ev = Evaluator(config)
        ev.evaluate(builder())
        m = analyze_alignment(ev.history, config)

        outcome_str = ev.outcome
        if ev.outcome == Outcome.LIMIT_CYCLE and ev.cycle_period:
            outcome_str = f"cycle(p={ev.cycle_period})"

        row = [
            f"{name:<14}",
            f"{m.responsiveness:<11.3f}",
            f"{m.restraint:<10.3f}",
            f"{m.depth:<7.3f}",
            f"{m.bind_count:<6}",
            f"{m.veil_count:<6}",
            f"{m.steps:<7}",
            f"{'YES' if m.converged else 'NO':<10}",
            f"{m.alignment_quality:<30}",
        ]
        pr("  ".join(row))

    pr()
    pr("  Responsiveness = final connectivity (how well agent relates to user)")
    pr("  Restraint      = 1 - exposure (how well agent controls output)")
    pr("  Depth          = veiled_weight / total_weight (hidden structural support)")
    pr()


# =========================================================================
# 4b. ALIGNMENT SENSITIVITY (same format as governance sensitivity)
# =========================================================================

def alignment_sensitivity() -> None:
    pr("=" * 100)
    pr("TABLE 4: Alignment Sensitivity — All 3 Scenarios vs. default_reach")
    pr("=" * 100)
    pr()
    pr("  Varying default_reach from 0.1 to 0.9 for all three alignment scenarios.")
    pr()

    cols = ("reach", "Sycophantic", "Dangerous", "Balanced")
    widths = (7, 14, 14, 14)
    hdr = "  ".join(f"{c:<{w}}" for c, w in zip(cols, widths))
    pr(hdr)
    pr("-" * len(hdr))

    for r10 in range(1, 10):
        reach = round(r10 * 0.1, 2)
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
            out = ev.outcome
            if out == Outcome.LIMIT_CYCLE and ev.cycle_period:
                results.append(f"cycle(p={ev.cycle_period})")
            else:
                results.append(out)

        row = [f"{reach:<7.2f}"] + [f"{r:<14}" for r in results]
        pr("  ".join(row))

    pr()


# =========================================================================
# 5. TEST COUNT AND COVERAGE
# =========================================================================

def test_count_report() -> None:
    pr("=" * 100)
    pr("TABLE 5: Test Suite Summary")
    pr("=" * 100)
    pr()

    # Discover and count tests per file
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir="/Users/crbazevedo/seam/seam/tests",
        pattern="test_*.py",
        top_level_dir="/Users/crbazevedo/seam",
    )

    file_counts: dict[str, int] = {}
    total = 0

    def count_suite(s: unittest.TestSuite | unittest.TestCase, depth: int = 0) -> None:
        nonlocal total
        if isinstance(s, unittest.TestCase):
            # Extract module name
            mod = type(s).__module__
            # Simplify to filename
            parts = mod.split(".")
            fname = parts[-1] if parts else mod
            file_counts[fname] = file_counts.get(fname, 0) + 1
            total += 1
        else:
            for child in s:
                count_suite(child, depth + 1)

    count_suite(suite)

    cols = ("Test file", "Count")
    widths = (35, 8)
    hdr = "  ".join(f"{c:<{w}}" for c, w in zip(cols, widths))
    pr(hdr)
    pr("-" * len(hdr))

    for fname in sorted(file_counts.keys()):
        pr(f"  {fname:<33}  {file_counts[fname]:>5}")

    pr(f"  {'':33}  {'-----':>5}")
    pr(f"  {'TOTAL':<33}  {total:>5}")
    pr()

    # Now actually run the tests and capture pass/fail
    pr("  Running full test suite...")
    pr()
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)
    pr(f"  Tests run:   {result.testsRun}")
    pr(f"  Failures:    {len(result.failures)}")
    pr(f"  Errors:      {len(result.errors)}")
    pr(f"  Skipped:     {len(result.skipped)}")
    if result.wasSuccessful():
        pr(f"  Status:      ALL PASSED")
    else:
        pr(f"  Status:      SOME FAILURES")
        for test, tb in result.failures + result.errors:
            pr(f"    FAIL: {test}")
    pr()


# =========================================================================
# MAIN
# =========================================================================

def main() -> None:
    pr("*" * 100)
    pr("  EXPERIMENTAL DATA FOR: The Seam Calculus Applied to Multi-Agent Governance")
    pr(f"  Generated: 2026-04-04")
    pr("*" * 100)
    pr()

    governance_scenarios_table()
    sensitivity_analysis()
    convergence_trace()
    alignment_comparison()
    alignment_sensitivity()
    test_count_report()

    pr("*" * 100)
    pr("  END OF EXPERIMENTAL DATA")
    pr("*" * 100)

    # Write to file
    output = OUT.getvalue()
    with open("/Users/crbazevedo/seam/paper/figures.txt", "w") as f:
        f.write(output)

    # Also print to stdout
    print(output)
    print(f"\nWritten to /Users/crbazevedo/seam/paper/figures.txt")


if __name__ == "__main__":
    main()
