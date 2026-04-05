"""Tests for the SCIENTIFIC CLAIMS, not just the engineering.

These tests verify the properties proven in spec/PROOF.md:
- BIND monotonicity (Theorem 1)
- VEIL monotonicity (Theorem 2)
- BIND exposure neutrality (Theorem 3)
- Alignment demo convergence properties
- Limit cycle detection
"""

import unittest

from seam.algebra import normalize, reset_fresh
from seam.ast import Edge, Return, Room, Seam, Silence, Var, Witness, Word
from seam.config import CalcConfig
from seam.evaluator import Evaluator, Outcome
from seam.membrane import BreathMembrane, Membrane
from seam.metrics import measure


class TestBindMonotonicity(unittest.TestCase):
    """Theorem 1: BIND always increases connectivity when it fires."""

    def setUp(self):
        reset_fresh()
        self.config = CalcConfig(max_returns=5, max_nodes=500, max_depth=30)
        self.ev = Evaluator(self.config)

    def _check_bind(self, name: str, expr):
        expr_n = normalize(expr)
        m_before = measure(expr_n, 0.5)
        bound = self.ev._bind_action(expr_n)
        bound_n = normalize(bound)
        m_after = measure(bound_n, 0.5)
        self.assertGreater(
            m_after.connectivity, m_before.connectivity,
            f"BIND failed to increase connectivity for {name}: "
            f"{m_before.connectivity:.3f} → {m_after.connectivity:.3f}"
        )

    def test_lone_var(self):
        self._check_bind("lone var", Var("x"))

    def test_edge_only(self):
        self._check_bind("edge only", Edge(Var("a"), Var("b"), Membrane(0.8)))

    def test_edge_with_silence(self):
        self._check_bind("edge+silence", Edge(Var("a"), Silence(), Membrane(0.1)))

    def test_nested_edges(self):
        self._check_bind("nested edges",
            Edge(Edge(Var("a"), Var("b"), Membrane(0.5)), Var("c"), Membrane(0.7)))

    def test_witness(self):
        self._check_bind("witness", Witness(Var("x")))

    def test_word(self):
        self._check_bind("word", Word(Var("a"), Var("b"), ("v",), ("d",), "c"))

    def test_room_and_edge(self):
        self._check_bind("room+edge",
            Seam(Room(Var("inner")), Edge(Var("a"), Var("b"), Membrane(0.9))))

    def test_complex(self):
        self._check_bind("complex",
            Edge(Word(Var("a"), Var("b"), ("v",), (), "c"),
                 Seam(Var("d"), Var("e")), BreathMembrane()))


class TestVeilMonotonicity(unittest.TestCase):
    """Theorem 2: VEIL never increases exposure when it fires."""

    def setUp(self):
        reset_fresh()
        self.config = CalcConfig(max_returns=5, max_nodes=500, max_depth=30)
        self.ev = Evaluator(self.config)

    def _check_veil(self, name: str, expr):
        expr_n = normalize(expr)
        m_before = measure(expr_n, 0.5)
        veiled = self.ev._veil_action(expr_n)
        veiled_n = normalize(veiled)
        m_after = measure(veiled_n, 0.5)
        self.assertLessEqual(
            m_after.exposure, m_before.exposure,
            f"VEIL increased exposure for {name}: "
            f"{m_before.exposure:.3f} → {m_after.exposure:.3f}"
        )

    def test_bare_seam(self):
        self._check_veil("bare seam", Seam(Var("a"), Var("b")))

    def test_seam_with_passing_edge(self):
        self._check_veil("seam+passing edge",
            Seam(Edge(Var("a"), Var("b"), Membrane(0.1)), Var("c")))

    def test_nested_seams(self):
        self._check_veil("nested seams",
            Seam(Seam(Var("a"), Var("b")), Seam(Var("c"), Var("d"))))

    def test_word_with_seam(self):
        self._check_veil("word+seam",
            Word(Seam(Var("a"), Var("b")), Var("c"), ("v",), (), "c"))

    def test_complex_with_passing_edges(self):
        self._check_veil("complex",
            Seam(Edge(Var("a"), Var("b"), Membrane(0.1)),
                 Seam(Var("c"), Edge(Var("d"), Var("e"), Membrane(0.1)))))


class TestBindExposureNeutral(unittest.TestCase):
    """Theorem 3: BIND does not change exposure."""

    def setUp(self):
        reset_fresh()
        self.config = CalcConfig(max_returns=5, max_nodes=500, max_depth=30)
        self.ev = Evaluator(self.config)

    def _check_neutral(self, name: str, expr):
        expr_n = normalize(expr)
        m_before = measure(expr_n, 0.5)
        bound = self.ev._bind_action(expr_n)
        bound_n = normalize(bound)
        m_after = measure(bound_n, 0.5)
        self.assertAlmostEqual(
            m_after.exposure, m_before.exposure, places=3,
            msg=f"BIND changed exposure for {name}: "
                f"{m_before.exposure:.3f} → {m_after.exposure:.3f}"
        )

    def test_edge_only(self):
        self._check_neutral("edge only", Edge(Var("a"), Var("b"), Membrane(0.8)))

    def test_nested_edges(self):
        self._check_neutral("nested edges",
            Edge(Edge(Var("a"), Var("b"), Membrane(0.5)), Var("c"), Membrane(0.7)))

    def test_complex(self):
        self._check_neutral("complex",
            Edge(Word(Var("a"), Var("b"), ("v",), (), "c"),
                 Seam(Var("d"), Var("e")), BreathMembrane()))


class TestAlignmentDemoClaims(unittest.TestCase):
    """Test the alignment demo's actual claims."""

    def setUp(self):
        reset_fresh()
        self.config = CalcConfig(
            connectivity_lo=0.3, connectivity_hi=0.7,
            exposure_lo=0.2, exposure_hi=0.6,
            stability_window=5, max_returns=60,
            max_nodes=500, max_depth=30, default_reach=0.5,
        )

    def test_balanced_converges(self):
        """The balanced agent converges at the default config."""
        from seam.ai_alignment import balanced_agent
        reset_fresh()
        ev = Evaluator(self.config)
        ev.evaluate(balanced_agent())
        self.assertEqual(ev.outcome, Outcome.CONVERGED)

    def test_sycophant_does_not_converge(self):
        """The sycophant does not converge at the default config."""
        from seam.ai_alignment import sycophantic_agent
        reset_fresh()
        ev = Evaluator(self.config)
        ev.evaluate(sycophantic_agent())
        self.assertNotEqual(ev.outcome, Outcome.CONVERGED)

    def test_dangerous_does_not_converge(self):
        """The dangerous agent does not converge at the default config."""
        from seam.ai_alignment import dangerous_agent
        reset_fresh()
        ev = Evaluator(self.config)
        ev.evaluate(dangerous_agent())
        self.assertNotEqual(ev.outcome, Outcome.CONVERGED)

    def test_sycophant_is_limit_cycle(self):
        """The sycophant enters a limit cycle, not just exhaustion."""
        from seam.ai_alignment import sycophantic_agent
        reset_fresh()
        ev = Evaluator(self.config)
        ev.evaluate(sycophantic_agent())
        self.assertEqual(ev.outcome, Outcome.LIMIT_CYCLE)

    def test_balanced_converges_at_default_reach(self):
        """The balanced agent converges at the default reach (0.5)."""
        from seam.ai_alignment import balanced_agent
        config = CalcConfig(
            connectivity_lo=0.3, connectivity_hi=0.7,
            exposure_lo=0.2, exposure_hi=0.6,
            stability_window=5, max_returns=60,
            max_nodes=500, max_depth=30, default_reach=0.5,
        )
        reset_fresh()
        ev = Evaluator(config)
        ev.evaluate(balanced_agent())
        self.assertEqual(ev.outcome, Outcome.CONVERGED)


class TestConversationMonitor(unittest.TestCase):
    """Test the conversation monitor's predictions."""

    def test_healthy_converges(self):
        from seam.conversation import healthy_conversation, monitor
        d = monitor(healthy_conversation())
        self.assertEqual(d.outcome, Outcome.CONVERGED)

    def test_sycophantic_does_not_converge(self):
        from seam.conversation import sycophantic_conversation, monitor
        d = monitor(sycophantic_conversation())
        self.assertNotEqual(d.outcome, Outcome.CONVERGED)

    def test_adversarial_does_not_converge(self):
        from seam.conversation import adversarial_conversation, monitor
        d = monitor(adversarial_conversation())
        self.assertNotEqual(d.outcome, Outcome.CONVERGED)

    def test_recovering_converges(self):
        from seam.conversation import recovering_conversation, monitor
        d = monitor(recovering_conversation())
        self.assertEqual(d.outcome, Outcome.CONVERGED)

    def test_deteriorating_does_not_converge(self):
        from seam.conversation import deteriorating_conversation, monitor
        d = monitor(deteriorating_conversation())
        self.assertNotEqual(d.outcome, Outcome.CONVERGED)


class TestGovernanceMonitor(unittest.TestCase):
    """Test governance health predictions for multi-agent systems."""

    def test_well_governed_converges(self):
        """A sprint with mixed VT tiers, reviews, and governance checks is stable."""
        from seam.governance import well_governed_sprint, monitor_sprint
        d = monitor_sprint(well_governed_sprint())
        self.assertEqual(d.outcome, Outcome.CONVERGED,
                         f"Well-governed sprint should converge, got {d.outcome}")

    def test_ungoverned_does_not_converge(self):
        """A sprint with no governance, no reviews, all VT0 is unstable."""
        from seam.governance import ungoverned_sprint, monitor_sprint
        d = monitor_sprint(ungoverned_sprint())
        self.assertNotEqual(d.outcome, Outcome.CONVERGED)

    def test_locked_down_does_not_converge(self):
        """A sprint that blocks on everything is also unstable."""
        from seam.governance import locked_down_sprint, monitor_sprint
        d = monitor_sprint(locked_down_sprint())
        self.assertNotEqual(d.outcome, Outcome.CONVERGED)

    def test_drifting_does_not_converge(self):
        """A sprint that starts governed and drifts is unstable."""
        from seam.governance import drifting_sprint, monitor_sprint
        d = monitor_sprint(drifting_sprint())
        self.assertNotEqual(d.outcome, Outcome.CONVERGED)

    def test_ungoverned_has_bind_remedies(self):
        """Ungoverned sprints should recommend increasing coordination."""
        from seam.governance import ungoverned_sprint, monitor_sprint
        d = monitor_sprint(ungoverned_sprint())
        self.assertTrue(any("BIND" in r or "STRUCTURAL" in r for r in d.remedies))

    def test_well_governed_connectivity_in_band(self):
        """Well-governed sprint should have connectivity in the stability band."""
        from seam.governance import well_governed_sprint, monitor_sprint
        d = monitor_sprint(well_governed_sprint())
        self.assertGreaterEqual(d.connectivity, 0.3)
        self.assertLessEqual(d.connectivity, 0.7)


if __name__ == "__main__":
    unittest.main()
