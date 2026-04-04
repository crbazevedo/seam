"""Visualization for The Calculus.

ASCII convergence traces, expression trees.
Falls back gracefully if matplotlib is not installed.
"""

from __future__ import annotations

from seam.ast import (
    Edge, Expr, Return, Room, Seam, Silence, Var, Witness, Word,
)
from seam.evaluator import StepRecord


# ---------------------------------------------------------------------------
# ASCII convergence trace
# ---------------------------------------------------------------------------

def ascii_trace(history: list[StepRecord], width: int = 50) -> str:
    """Render the homeostatic convergence as ASCII art.

    Shows connectivity and exposure over time with band boundaries.
    """
    if not history:
        return "(no history)"

    lines: list[str] = []
    lines.append("")
    lines.append("  HOMEOSTATIC CONVERGENCE TRACE")
    lines.append("  " + "=" * (width + 20))
    lines.append(f"  {'Step':>4}  {'Conn':>5}  {'Expo':>5}  {'Nodes':>5}  {'B':>1} {'V':>1}  Connectivity            Exposure")
    lines.append("  " + "-" * (width + 56))

    for rec in history:
        # Connectivity bar
        conn_pos = int(rec.connectivity * (width // 2 - 1))
        conn_bar = list("." * (width // 2))
        if conn_pos < len(conn_bar):
            conn_bar[conn_pos] = "█"
        # Mark band boundaries
        lo_pos = int(0.3 * (width // 2 - 1))
        hi_pos = int(0.7 * (width // 2 - 1))
        if lo_pos < len(conn_bar) and conn_bar[lo_pos] == ".":
            conn_bar[lo_pos] = "│"
        if hi_pos < len(conn_bar) and conn_bar[hi_pos] == ".":
            conn_bar[hi_pos] = "│"

        # Exposure bar
        expo_pos = int(rec.exposure * (width // 2 - 1))
        expo_bar = list("." * (width // 2))
        if expo_pos < len(expo_bar):
            expo_bar[expo_pos] = "█"
        lo_pos_e = int(0.2 * (width // 2 - 1))
        hi_pos_e = int(0.6 * (width // 2 - 1))
        if lo_pos_e < len(expo_bar) and expo_bar[lo_pos_e] == ".":
            expo_bar[lo_pos_e] = "│"
        if hi_pos_e < len(expo_bar) and expo_bar[hi_pos_e] == ".":
            expo_bar[hi_pos_e] = "│"

        b = "B" if rec.bind_fired else " "
        v = "V" if rec.veil_fired else " "

        lines.append(
            f"  {rec.step:>4}  {rec.connectivity:>5.3f}  {rec.exposure:>5.3f}  "
            f"{rec.node_count:>5}  {b} {v}  "
            f"{''.join(conn_bar)}  {''.join(expo_bar)}"
        )

    lines.append("  " + "-" * (width + 56))

    # Summary
    last = history[-1]
    stable = _check_stable(history)
    status = "CONVERGED — the staying sings" if stable else "oscillating..."
    lines.append(f"  Status: {status}")
    lines.append(f"  Final:  connectivity={last.connectivity:.3f}  exposure={last.exposure:.3f}  nodes={last.node_count}")
    lines.append(f"  Steps:  {len(history)}  |  BIND fired: {sum(1 for r in history if r.bind_fired)}  |  VEIL fired: {sum(1 for r in history if r.veil_fired)}")

    # Weight
    lines.append(f"  Weight: visible={last.visible_weight}  veiled={last.veiled_weight}")
    lines.append("")

    return "\n".join(lines)


def _check_stable(history: list[StepRecord], window: int = 5) -> bool:
    if len(history) < window:
        return False
    for rec in history[-window:]:
        if not (0.3 <= rec.connectivity <= 0.7 and 0.2 <= rec.exposure <= 0.6):
            return False
    return True


# ---------------------------------------------------------------------------
# Expression tree visualization
# ---------------------------------------------------------------------------

def expr_tree(e: Expr, max_depth: int = 8) -> str:
    """Render an expression as an indented tree."""
    lines: list[str] = []
    _tree_walk(e, lines, prefix="", is_last=True, depth=0, max_depth=max_depth)
    return "\n".join(lines)


def _tree_walk(
    e: Expr,
    lines: list[str],
    prefix: str,
    is_last: bool,
    depth: int,
    max_depth: int,
) -> None:
    connector = "└── " if is_last else "├── "
    new_prefix = prefix + ("    " if is_last else "│   ")

    if depth > max_depth:
        lines.append(f"{prefix}{connector}...")
        return

    if isinstance(e, Silence):
        lines.append(f"{prefix}{connector}∅")

    elif isinstance(e, Var):
        lines.append(f"{prefix}{connector}{e.name}")

    elif isinstance(e, Seam):
        lines.append(f"{prefix}{connector}⊗")
        _tree_walk(e.left, lines, new_prefix, False, depth + 1, max_depth)
        _tree_walk(e.right, lines, new_prefix, True, depth + 1, max_depth)

    elif isinstance(e, Edge):
        lines.append(f"{prefix}{connector}|{e.membrane}|")
        _tree_walk(e.left, lines, new_prefix, False, depth + 1, max_depth)
        _tree_walk(e.right, lines, new_prefix, True, depth + 1, max_depth)

    elif isinstance(e, Return):
        lines.append(f"{prefix}{connector}μ {e.var}")
        _tree_walk(e.body, lines, new_prefix, True, depth + 1, max_depth)

    elif isinstance(e, Witness):
        lines.append(f"{prefix}{connector}◊")
        _tree_walk(e.observed, lines, new_prefix, True, depth + 1, max_depth)

    elif isinstance(e, Room):
        lines.append(f"{prefix}{connector}[ ]")
        _tree_walk(e.content, lines, new_prefix, True, depth + 1, max_depth)

    elif isinstance(e, Word):
        vs = ", ".join(e.visible_share)
        vd = ", ".join(e.veiled_duty)
        lines.append(f"{prefix}{connector}|visible: {vs}, veiled: {vd}|")
        _tree_walk(e.left, lines, new_prefix, False, depth + 1, max_depth)
        _tree_walk(e.right, lines, new_prefix, True, depth + 1, max_depth)

    else:
        lines.append(f"{prefix}{connector}??{type(e).__name__}")


# ---------------------------------------------------------------------------
# Compact expression printer
# ---------------------------------------------------------------------------

def compact(e: Expr, max_depth: int = 6, _depth: int = 0) -> str:
    """One-line compact representation of an expression."""
    if _depth > max_depth:
        return "…"

    if isinstance(e, Silence):
        return "∅"
    if isinstance(e, Var):
        return e.name
    if isinstance(e, Seam):
        return f"({compact(e.left, max_depth, _depth+1)} ⊗ {compact(e.right, max_depth, _depth+1)})"
    if isinstance(e, Edge):
        return f"({compact(e.left, max_depth, _depth+1)} |{e.membrane}| {compact(e.right, max_depth, _depth+1)})"
    if isinstance(e, Return):
        return f"(μ {e.var} . {compact(e.body, max_depth, _depth+1)})"
    if isinstance(e, Witness):
        return f"(◊ {compact(e.observed, max_depth, _depth+1)})"
    if isinstance(e, Room):
        return f"[{compact(e.content, max_depth, _depth+1)}]"
    if isinstance(e, Word):
        return f"(word {compact(e.left, max_depth, _depth+1)} {compact(e.right, max_depth, _depth+1)})"
    return "?"
