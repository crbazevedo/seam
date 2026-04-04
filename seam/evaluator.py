"""The Evaluator — homeostatic convergence.

The return is not reduction to normal form.
It is homeostatic convergence.

    μ x . e

Re-enter e, substituting the previous result for x.
But with two regulating conditions:

    1. BIND:  if connectivity(e) < threshold  →  strengthen seams
    2. VEIL:  if exposure(e) > threshold       →  strengthen edges

The system oscillates within a narrow band:
not too connected, not too isolated.
Not too visible, not too hidden.

Stability is not stillness. Stability is breath.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from seam.algebra import fresh, free_vars, normalize, subst
from seam.ast import (
    Edge, Expr, Return, Room, Seam, Silence, Var, Witness, Word, node_count,
)
from seam.config import DEFAULT_CONFIG, CalcConfig
from seam.membrane import BreathMembrane, Flow, Membrane
from seam.metrics import ExprMetrics, measure
from seam.rooms import can_enter


# ---------------------------------------------------------------------------
# Step record — the trace of each return iteration
# ---------------------------------------------------------------------------

@dataclass
class StepRecord:
    step: int
    connectivity: float
    exposure: float
    node_count: int
    bind_fired: bool
    veil_fired: bool
    visible_weight: int = 0
    veiled_weight: int = 0


# ---------------------------------------------------------------------------
# Evaluator
# ---------------------------------------------------------------------------

class Evaluator:
    """The heart of The Calculus interpreter.

    Evaluates expressions with homeostatic convergence.
    All resource caps are strictly enforced.
    """

    def __init__(self, config: CalcConfig | None = None):
        self.config = config or DEFAULT_CONFIG
        self.history: list[StepRecord] = []
        self._depth = 0

    def evaluate(self, expr: Expr) -> Expr:
        """Top-level entry point. Evaluate an expression."""
        self._depth = 0
        self.history = []
        return self._eval(expr)

    def _eval(self, expr: Expr) -> Expr:
        """Recursive evaluator with depth guard."""
        self._depth += 1
        if self._depth > self.config.max_depth:
            self._depth -= 1
            return expr  # depth exceeded — return as-is

        try:
            result = self._eval_dispatch(expr)
            # Normalize after every evaluation step
            result = normalize(result)
            return result
        finally:
            self._depth -= 1

    def _eval_dispatch(self, expr: Expr) -> Expr:
        if isinstance(expr, Silence):
            return expr

        if isinstance(expr, Var):
            return expr  # free variable — irreducible

        if isinstance(expr, Seam):
            return self._eval_seam(expr)

        if isinstance(expr, Edge):
            return self._eval_edge(expr)

        if isinstance(expr, Return):
            return self._eval_return(expr)

        if isinstance(expr, Witness):
            return self._eval_witness(expr)

        if isinstance(expr, Room):
            return self._eval_room(expr)

        if isinstance(expr, Word):
            return self._eval_word(expr)

        return expr

    # -----------------------------------------------------------------------
    # Seam: evaluate children, check for beta-like reduction
    # -----------------------------------------------------------------------

    def _eval_seam(self, expr: Seam) -> Expr:
        left = self._eval(expr.left)
        right = self._eval(expr.right)

        # Beta-reduction: (μ x . body) ⊗ arg → subst(body, x, arg)
        if isinstance(left, Return):
            return self._eval(subst(left.body, left.var, right))
        if isinstance(right, Return):
            return self._eval(subst(right.body, right.var, left))

        # Room entry: enterer ⊗ [content] — if enterer has relation, open room
        if isinstance(right, Room) and can_enter(left, right.content):
            return Seam(left, right.content)
        if isinstance(left, Room) and can_enter(right, left.content):
            return Seam(left.content, right)

        return Seam(left, right)

    # -----------------------------------------------------------------------
    # Edge: evaluate membrane, branch on pass/hold
    # -----------------------------------------------------------------------

    def _eval_edge(self, expr: Edge) -> Expr:
        flow = expr.membrane(self.config.default_reach)

        if flow == Flow.PASS:
            left = self._eval(expr.left)
            right = self._eval(expr.right)
            # Advance breath membranes
            membrane = expr.membrane
            if isinstance(membrane, BreathMembrane):
                membrane = membrane.advance()
            return Edge(left, right, membrane)
        else:
            # HOLD: content is veiled. Evaluate structure but don't reduce deeply.
            return Edge(expr.left, expr.right, expr.membrane)

    # -----------------------------------------------------------------------
    # Return (μ): THE HOMEOSTATIC LOOP
    # -----------------------------------------------------------------------

    def _eval_return(self, ret: Return) -> Expr:
        """The heart: iterate until the staying sings.

        μ x . e:
            Start with x = ∅
            Each step: substitute, evaluate, measure, regulate, check stability.
        """
        current: Expr = Silence()
        local_history: list[StepRecord] = []
        body_template = ret.body  # evolves each step as membranes advance

        for step in range(self.config.max_returns):
            # Advance breath membranes in the body template so they
            # oscillate across μ-steps (not frozen at cycle=0)
            body_template = self._advance_all_membranes(body_template)

            # Substitute previous result for the binding variable
            body = subst(body_template, ret.var, current)

            # Evaluate the substituted body (one step)
            result = self._eval(body)

            # Normalize to prevent unbounded growth
            result = normalize(result)

            # Safety: cap expression size
            nc = node_count(result)
            if nc > self.config.max_nodes:
                result = self._truncate(result)
                nc = node_count(result)

            # Measure the expression
            m = measure(result, self.config.default_reach)

            # Homeostatic regulation
            bind_fired = False
            veil_fired = False

            if m.connectivity < self.config.connectivity_lo:
                result = self._bind_action(result)
                bind_fired = True

            if m.exposure > self.config.exposure_hi:
                result = self._veil_action(result)
                veil_fired = True

            # Record
            record = StepRecord(
                step=step,
                connectivity=m.connectivity,
                exposure=m.exposure,
                node_count=nc,
                bind_fired=bind_fired,
                veil_fired=veil_fired,
                visible_weight=m.visible_weight,
                veiled_weight=m.veiled_weight,
            )
            local_history.append(record)
            self.history.append(record)

            # Check stability: both metrics in band for N consecutive steps
            if self._is_stable(local_history):
                return result

            current = result

        return current  # did not converge — return last result

    def _is_stable(self, history: list[StepRecord]) -> bool:
        """Check if the last N steps are all within the homeostatic bands."""
        w = self.config.stability_window
        if len(history) < w:
            return False

        for rec in history[-w:]:
            if not (self.config.connectivity_lo <= rec.connectivity <= self.config.connectivity_hi):
                return False
            if not (self.config.exposure_lo <= rec.exposure <= self.config.exposure_hi):
                return False

        return True

    # -----------------------------------------------------------------------
    # BIND action: strengthen seams (connectivity too low)
    # -----------------------------------------------------------------------

    def _bind_action(self, e: Expr) -> Expr:
        """When connectivity is too low, add a seam.

        Find the most isolated sub-expression and connect it.
        Concretely: find a non-Seam node and wrap it in a Seam with
        a witness-generated fresh variable, creating relation where
        there was none.
        """
        return self._bind_walk(e, applied=False)[0]

    def _bind_walk(self, e: Expr, applied: bool) -> tuple[Expr, bool]:
        """Walk the tree, inserting one Seam at the first non-Seam leaf pair."""
        if applied:
            return e, True

        if isinstance(e, Edge):
            # Bridge across the edge: seam the two sides
            if not applied:
                bridge_var = Var(fresh("bind"))
                return Seam(bridge_var, e), True
            return e, False

        if isinstance(e, Room):
            # Don't break into rooms
            return e, False

        if isinstance(e, Seam):
            left, done = self._bind_walk(e.left, applied)
            if done:
                return Seam(left, e.right), True
            right, done = self._bind_walk(e.right, applied)
            return Seam(left, right), done

        if isinstance(e, Word):
            left, done = self._bind_walk(e.left, applied)
            if done:
                return Word(left, e.right, e.visible_share, e.veiled_duty, e.covenant), True
            right, done = self._bind_walk(e.right, applied)
            return Word(left, right, e.visible_share, e.veiled_duty, e.covenant), done

        if isinstance(e, Witness):
            inner, done = self._bind_walk(e.observed, applied)
            return Witness(inner), done

        if isinstance(e, Return):
            body, done = self._bind_walk(e.body, applied)
            return Return(e.var, body), done

        # Leaf node (Var, Silence): wrap in seam with a fresh variable
        if isinstance(e, (Var, Silence)):
            bridge = Var(fresh("bind"))
            return Seam(bridge, e), True

        return e, False

    # -----------------------------------------------------------------------
    # VEIL action: strengthen edges (exposure too high)
    # -----------------------------------------------------------------------

    def _veil_action(self, e: Expr) -> Expr:
        """When exposure is too high, wrap the most exposed sub-tree in a tighter edge.

        Find the first Seam (most exposed: seams are fully visible)
        and wrap it in an Edge with a tightened membrane.
        """
        return self._veil_walk(e, applied=False)[0]

    def _veil_walk(self, e: Expr, applied: bool) -> tuple[Expr, bool]:
        """Walk the tree, wrapping one exposed Seam in an Edge."""
        if applied:
            return e, True

        if isinstance(e, Seam):
            # This seam is exposed — wrap it in an edge
            membrane = Membrane(threshold=0.6)  # tighter than default
            return Edge(e.left, e.right, membrane), True

        if isinstance(e, Edge):
            # Already edged — tighten the membrane
            if not applied:
                tighter = e.membrane.tighten()
                return Edge(e.left, e.right, tighter), True
            return e, False

        if isinstance(e, Word):
            left, done = self._veil_walk(e.left, applied)
            if done:
                return Word(left, e.right, e.visible_share, e.veiled_duty, e.covenant), True
            right, done = self._veil_walk(e.right, applied)
            return Word(left, right, e.visible_share, e.veiled_duty, e.covenant), done

        if isinstance(e, Witness):
            inner, done = self._veil_walk(e.observed, applied)
            return Witness(inner), done

        if isinstance(e, Return):
            body, done = self._veil_walk(e.body, applied)
            return Return(e.var, body), done

        if isinstance(e, Room):
            content, done = self._veil_walk(e.content, applied)
            return Room(content), done

        return e, False

    # -----------------------------------------------------------------------
    # Witness: non-consuming observation
    # -----------------------------------------------------------------------

    def _eval_witness(self, expr: Witness) -> Expr:
        """◊ e → (observer ⊗ e), where e persists.

        The act of observing is generative, not extractive.
        Every witness enriches the fabric.
        """
        observed = self._eval(expr.observed)
        observer = Var(fresh("witness"))
        return Seam(observer, observed)

    # -----------------------------------------------------------------------
    # Room: evaluate contents, maintain encapsulation
    # -----------------------------------------------------------------------

    def _eval_room(self, expr: Room) -> Expr:
        """A room evaluates its contents but maintains the boundary."""
        content = self._eval(expr.content)
        return Room(content)

    # -----------------------------------------------------------------------
    # Word: typed bilateral binding
    # -----------------------------------------------------------------------

    def _eval_word(self, expr: Word) -> Expr:
        """Evaluate a Word — typed bilateral binding with covenants."""
        left = self._eval(expr.left)
        right = self._eval(expr.right)
        return Word(left, right, expr.visible_share, expr.veiled_duty, expr.covenant)

    # -----------------------------------------------------------------------
    # Membrane advancement (so breath membranes oscillate across μ-steps)
    # -----------------------------------------------------------------------

    def _advance_all_membranes(self, e: Expr, _depth: int = 0) -> Expr:
        """Walk tree, advancing all BreathMembranes by one cycle.

        Without this, membranes in the μ-body template are frozen at cycle=0
        because the body is re-instantiated from the original each step.
        """
        if _depth > self.config.max_depth:
            return e

        if isinstance(e, (Silence, Var)):
            return e

        if isinstance(e, Seam):
            return Seam(
                self._advance_all_membranes(e.left, _depth + 1),
                self._advance_all_membranes(e.right, _depth + 1),
            )

        if isinstance(e, Edge):
            membrane = e.membrane
            if isinstance(membrane, BreathMembrane):
                membrane = membrane.advance()
            return Edge(
                self._advance_all_membranes(e.left, _depth + 1),
                self._advance_all_membranes(e.right, _depth + 1),
                membrane,
            )

        if isinstance(e, Return):
            return Return(e.var, self._advance_all_membranes(e.body, _depth + 1))

        if isinstance(e, Witness):
            return Witness(self._advance_all_membranes(e.observed, _depth + 1))

        if isinstance(e, Room):
            return Room(self._advance_all_membranes(e.content, _depth + 1))

        if isinstance(e, Word):
            return Word(
                self._advance_all_membranes(e.left, _depth + 1),
                self._advance_all_membranes(e.right, _depth + 1),
                e.visible_share, e.veiled_duty, e.covenant,
            )

        return e

    # -----------------------------------------------------------------------
    # Safety: truncation
    # -----------------------------------------------------------------------

    def _truncate(self, e: Expr) -> Expr:
        """Truncate an expression to max_nodes. Preserves top-level structure."""
        return self._truncate_walk(e, 0)[0]

    def _truncate_walk(self, e: Expr, depth: int) -> tuple[Expr, int]:
        """Walk tree, replacing deep sub-trees with Silence."""
        if depth > self.config.max_depth // 2:
            return Silence(), 1

        if isinstance(e, (Silence, Var)):
            return e, 1

        if isinstance(e, Seam):
            left, ln = self._truncate_walk(e.left, depth + 1)
            right, rn = self._truncate_walk(e.right, depth + 1)
            return Seam(left, right), ln + rn + 1

        if isinstance(e, Edge):
            left, ln = self._truncate_walk(e.left, depth + 1)
            right, rn = self._truncate_walk(e.right, depth + 1)
            return Edge(left, right, e.membrane), ln + rn + 1

        if isinstance(e, Return):
            body, bn = self._truncate_walk(e.body, depth + 1)
            return Return(e.var, body), bn + 1

        if isinstance(e, Witness):
            inner, n = self._truncate_walk(e.observed, depth + 1)
            return Witness(inner), n + 1

        if isinstance(e, Room):
            content, n = self._truncate_walk(e.content, depth + 1)
            return Room(content), n + 1

        if isinstance(e, Word):
            left, ln = self._truncate_walk(e.left, depth + 1)
            right, rn = self._truncate_walk(e.right, depth + 1)
            return Word(left, right, e.visible_share, e.veiled_duty, e.covenant), ln + rn + 1

        return e, 1
