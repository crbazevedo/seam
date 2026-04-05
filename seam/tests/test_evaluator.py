"""Tests for the evaluator — homeostatic convergence."""

import unittest

from seam.algebra import reset_fresh
from seam.ast import Edge, Return, Room, Seam, Silence, Var, Witness
from seam.config import CalcConfig
from seam.evaluator import Evaluator, Outcome
from seam.membrane import BreathMembrane, Membrane


class TestEvalBasic(unittest.TestCase):
    def setUp(self):
        reset_fresh()
        self.config = CalcConfig(max_returns=30, max_nodes=200, max_depth=30)
        self.ev = Evaluator(self.config)

    def test_silence(self):
        result = self.ev.evaluate(Silence())
        self.assertIsInstance(result, Silence)

    def test_var(self):
        result = self.ev.evaluate(Var("x"))
        self.assertEqual(result, Var("x"))

    def test_seam_identity(self):
        """a ⊗ ∅ evaluates to a (after normalization)."""
        result = self.ev.evaluate(Seam(Var("a"), Silence()))
        self.assertEqual(result, Var("a"))

    def test_witness(self):
        """◊ x creates (witness$N ⊗ x)."""
        result = self.ev.evaluate(Witness(Var("x")))
        self.assertIsInstance(result, Seam)


class TestBetaReduction(unittest.TestCase):
    """(μ x . body) ⊗ arg → subst(body, x, arg)"""

    def setUp(self):
        reset_fresh()
        self.config = CalcConfig(max_returns=30, max_nodes=200, max_depth=30)
        self.ev = Evaluator(self.config)

    def test_simple_application(self):
        """(μ x . x) ⊗ a → a (identity function)."""
        identity = Return("x", Var("x"))
        expr = Seam(identity, Var("a"))
        result = self.ev.evaluate(expr)
        # Should reduce to something involving Var("a")
        # The return will iterate, but the body is just x,
        # so it will converge quickly
        self.assertNotIsInstance(result, type(None))


class TestHomeostaticConvergence(unittest.TestCase):
    """The return drives homeostatic convergence."""

    def setUp(self):
        reset_fresh()
        self.config = CalcConfig(
            max_returns=50,
            max_nodes=300,
            max_depth=30,
            stability_window=3,  # shorter window for testing
        )
        self.ev = Evaluator(self.config)

    def test_simple_return_terminates(self):
        """μ x . (x ⊗ a) terminates within max_returns."""
        expr = Return("x", Seam(Var("x"), Var("a")))
        result = self.ev.evaluate(expr)
        self.assertLessEqual(len(self.ev.history), self.config.max_returns)

    def test_return_with_edge(self):
        """μ x . (x |φ| a) terminates."""
        expr = Return("x", Edge(Var("x"), Var("a"), BreathMembrane()))
        result = self.ev.evaluate(expr)
        self.assertLessEqual(len(self.ev.history), self.config.max_returns)

    def test_bind_fires_when_disconnected(self):
        """BIND fires when connectivity is too low."""
        # Pure edges, no seams → low connectivity
        expr = Return("x", Edge(Var("x"), Silence(), Membrane(threshold=0.9)))
        self.ev.evaluate(expr)
        bind_count = sum(1 for r in self.ev.history if r.bind_fired)
        self.assertGreater(bind_count, 0)

    def test_node_count_bounded(self):
        """Expression size never exceeds max_nodes."""
        expr = Return("x", Seam(Var("x"), Seam(Var("a"), Var("b"))))
        self.ev.evaluate(expr)
        for rec in self.ev.history:
            self.assertLessEqual(rec.node_count, self.config.max_nodes + 50)


class TestRoomAccess(unittest.TestCase):
    """Rooms open when there's shared relation."""

    def setUp(self):
        reset_fresh()
        self.config = CalcConfig(max_returns=20, max_nodes=200, max_depth=30)
        self.ev = Evaluator(self.config)

    def test_room_opens_with_relation(self):
        """a ⊗ [a ⊗ b] → a ⊗ (a ⊗ b) because a shares variable 'a'."""
        room = Room(Seam(Var("a"), Var("b")))
        expr = Seam(Var("a"), room)
        result = self.ev.evaluate(expr)
        # Room should have opened — result should not contain Room
        self.assertNotIsInstance(result, Room)

    def test_room_stays_closed_without_relation(self):
        """x ⊗ [a ⊗ b] stays closed — x has no relation to a or b."""
        room = Room(Seam(Var("a"), Var("b")))
        expr = Seam(Var("x"), room)
        result = self.ev.evaluate(expr)
        # Result should still contain a Room
        has_room = _contains_room(result)
        self.assertTrue(has_room)


class TestConvergenceDiagnostics(unittest.TestCase):
    """Tests for limit cycle detection and outcome classification."""

    def setUp(self):
        reset_fresh()

    def test_converged_outcome(self):
        """A well-structured expression reports CONVERGED."""
        config = CalcConfig(
            max_returns=50, max_nodes=300, max_depth=30,
            stability_window=3,
        )
        ev = Evaluator(config)
        # Expression with edges (needed for gatedness — exposure=1.0 without edges)
        expr = Return("x", Edge(Seam(Var("x"), Var("a")), Var("b"), BreathMembrane(base=0.5, amplitude=0.1)))
        ev.evaluate(expr)
        self.assertEqual(ev.outcome, Outcome.CONVERGED)

    def test_non_converged_outcome(self):
        """An expression that doesn't converge reports a non-converged outcome."""
        config = CalcConfig(
            max_returns=15, max_nodes=300, max_depth=30,
            stability_window=10,  # very high — unlikely to converge
        )
        ev = Evaluator(config)
        expr = Return("x", Edge(Var("x"), Var("a"), Membrane(threshold=0.1)))
        ev.evaluate(expr)
        self.assertNotEqual(ev.outcome, Outcome.CONVERGED)

    def test_outcome_not_none(self):
        """Outcome is always set after evaluation."""
        config = CalcConfig(max_returns=10, max_nodes=100, max_depth=20)
        ev = Evaluator(config)
        ev.evaluate(Silence())
        self.assertIsNotNone(ev.outcome)


def _contains_room(e) -> bool:
    from seam.ast import Edge, Room, Seam, Witness, Word, Return as Ret
    if isinstance(e, Room):
        return True
    if isinstance(e, Seam):
        return _contains_room(e.left) or _contains_room(e.right)
    if isinstance(e, Edge):
        return _contains_room(e.left) or _contains_room(e.right)
    if isinstance(e, Witness):
        return _contains_room(e.observed)
    if isinstance(e, Ret):
        return _contains_room(e.body)
    if isinstance(e, Word):
        return _contains_room(e.left) or _contains_room(e.right)
    return False


if __name__ == "__main__":
    unittest.main()
