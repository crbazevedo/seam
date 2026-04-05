"""Structural metrics for expressions.

Metrics operate on the AST — not on a global side-channel.
This fixes the v1 semantic mismatch where connectivity(e) and
exposure(e) were measured on an external Fabric rather than
on the expression being evaluated.

connectivity(e): how interconnected is the expression?
    = seam_nodes / max(total_nodes - 1, 1), clamped to [0, 1]

exposure(e): how transparent is the expression?
    = edges_passing / max(edges_total, 1), or 0.5 if no edges

structural_weight(e): what is visible vs. veiled?
    = (visible_weight, veiled_weight) — nodes accessible vs. behind held edges
"""

from __future__ import annotations

from dataclasses import dataclass

from seam.ast import (
    Edge, Expr, Return, Room, Seam, Silence, Var, Witness, Word,
)
from seam.config import DEFAULT_CONFIG
from seam.membrane import Flow


@dataclass
class ExprMetrics:
    """All metrics computed in a single tree walk."""
    total_nodes: int = 0
    seam_nodes: int = 0
    edge_nodes: int = 0
    edges_passing: int = 0
    edges_holding: int = 0
    var_nodes: int = 0
    witness_nodes: int = 0
    room_nodes: int = 0
    visible_weight: int = 0
    veiled_weight: int = 0

    @property
    def connectivity(self) -> float:
        if self.total_nodes <= 1:
            return 0.0
        return min(self.seam_nodes / max(self.total_nodes - 1, 1), 1.0)

    @property
    def exposure(self) -> float:
        if self.edge_nodes == 0:
            return 1.0  # no gates = no restraint = fully exposed
        return self.edges_passing / self.edge_nodes


def measure(e: Expr, reach: float | None = None) -> ExprMetrics:
    """Single-pass iterative tree walk computing all metrics.

    The `reach` parameter is probed against every Edge membrane to
    determine whether it passes or holds, affecting exposure.
    """
    if reach is None:
        reach = DEFAULT_CONFIG.default_reach

    m = ExprMetrics()
    # Stack: (expr, is_veiled) — veiled tracks if we're behind a holding edge
    stack: list[tuple[Expr, bool]] = [(e, False)]
    cap = DEFAULT_CONFIG.max_nodes * 2

    while stack and m.total_nodes < cap:
        node, veiled = stack.pop()
        m.total_nodes += 1

        if veiled:
            m.veiled_weight += 1
        else:
            m.visible_weight += 1

        if isinstance(node, Silence):
            continue

        elif isinstance(node, Var):
            m.var_nodes += 1

        elif isinstance(node, Seam):
            m.seam_nodes += 1
            stack.append((node.left, veiled))
            stack.append((node.right, veiled))

        elif isinstance(node, Edge):
            m.edge_nodes += 1
            flow = node.membrane(reach)
            if flow == Flow.PASS:
                m.edges_passing += 1
                stack.append((node.left, veiled))
                stack.append((node.right, veiled))
            else:
                m.edges_holding += 1
                # Children are veiled — they have structural weight but aren't visible
                stack.append((node.left, True))
                stack.append((node.right, True))

        elif isinstance(node, Return):
            stack.append((node.body, veiled))

        elif isinstance(node, Witness):
            m.witness_nodes += 1
            stack.append((node.observed, veiled))

        elif isinstance(node, Room):
            m.room_nodes += 1
            # Room contents are veiled until entered
            stack.append((node.content, True))

        elif isinstance(node, Word):
            m.edge_nodes += 1  # Word is a typed edge
            # visible_share passes, veiled_duty holds
            if node.visible_share:
                m.edges_passing += 1
                stack.append((node.left, veiled))
                stack.append((node.right, veiled))
            else:
                m.edges_holding += 1
                stack.append((node.left, True))
                stack.append((node.right, True))

    return m


def connectivity(e: Expr, reach: float | None = None) -> float:
    return measure(e, reach).connectivity


def exposure(e: Expr, reach: float | None = None) -> float:
    return measure(e, reach).exposure


def structural_weight(e: Expr, reach: float | None = None) -> tuple[int, int]:
    m = measure(e, reach)
    return (m.visible_weight, m.veiled_weight)
