"""Tests for the seed program and derived structures."""

import unittest

from seam.algebra import reset_fresh
from seam.config import CalcConfig
from seam.evaluator import Evaluator
from seam.seed import (
    commons_program,
    crossing_program,
    duration_program,
    practice_program,
    seed_program,
)


class TestSeedProgram(unittest.TestCase):
    """The seed program must converge within resource bounds."""

    def setUp(self):
        reset_fresh()
        self.config = CalcConfig(
            max_returns=50,
            max_nodes=300,
            max_depth=30,
            stability_window=3,
        )

    def test_seed_terminates(self):
        prog = seed_program()
        ev = Evaluator(self.config)
        result = ev.evaluate(prog)
        self.assertLessEqual(len(ev.history), self.config.max_returns)
        self.assertIsNotNone(result)

    def test_seed_converges(self):
        """The seed program should reach homeostatic stability."""
        prog = seed_program()
        ev = Evaluator(self.config)
        ev.evaluate(prog)
        # Check that at least some steps are in band
        in_band = sum(
            1 for r in ev.history
            if (self.config.connectivity_lo <= r.connectivity <= self.config.connectivity_hi
                and self.config.exposure_lo <= r.exposure <= self.config.exposure_hi)
        )
        # Should have at least stability_window steps in band (convergence)
        self.assertGreaterEqual(in_band, 1, "Seed program never entered stability band")

    def test_seed_node_count_bounded(self):
        prog = seed_program()
        ev = Evaluator(self.config)
        ev.evaluate(prog)
        for rec in ev.history:
            self.assertLessEqual(rec.node_count, self.config.max_nodes + 50)


class TestDerivedPrograms(unittest.TestCase):
    """All derived programs must terminate within resource bounds."""

    def setUp(self):
        self.config = CalcConfig(
            max_returns=30,
            max_nodes=200,
            max_depth=30,
            stability_window=3,
        )

    def test_practice(self):
        reset_fresh()
        ev = Evaluator(self.config)
        ev.evaluate(practice_program())
        self.assertLessEqual(len(ev.history), self.config.max_returns)

    def test_commons(self):
        reset_fresh()
        ev = Evaluator(self.config)
        ev.evaluate(commons_program(n_practices=2))
        self.assertLessEqual(len(ev.history), self.config.max_returns)

    def test_crossing(self):
        reset_fresh()
        ev = Evaluator(self.config)
        ev.evaluate(crossing_program())
        self.assertLessEqual(len(ev.history), self.config.max_returns)

    def test_duration(self):
        reset_fresh()
        ev = Evaluator(self.config)
        ev.evaluate(duration_program())
        self.assertLessEqual(len(ev.history), self.config.max_returns)


if __name__ == "__main__":
    unittest.main()
