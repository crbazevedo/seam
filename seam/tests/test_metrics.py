"""Tests for structural metrics."""

import unittest

from seam.ast import Edge, Room, Seam, Silence, Var, Witness
from seam.membrane import Membrane
from seam.metrics import connectivity, exposure, measure, structural_weight


class TestConnectivity(unittest.TestCase):
    def test_silence(self):
        """Silence has 0 connectivity."""
        self.assertEqual(connectivity(Silence()), 0.0)

    def test_single_var(self):
        """A single var has 0 connectivity."""
        self.assertEqual(connectivity(Var("x")), 0.0)

    def test_seam(self):
        """a ⊗ b has positive connectivity."""
        c = connectivity(Seam(Var("a"), Var("b")))
        self.assertGreater(c, 0.0)

    def test_no_seams(self):
        """Edge without seams has 0 connectivity."""
        expr = Edge(Var("a"), Var("b"), Membrane(threshold=0.5))
        c = connectivity(expr)
        self.assertEqual(c, 0.0)


class TestExposure(unittest.TestCase):
    def test_no_edges(self):
        """Expression with no edges has neutral exposure (0.5)."""
        self.assertEqual(exposure(Var("x")), 0.5)
        self.assertEqual(exposure(Seam(Var("a"), Var("b"))), 0.5)

    def test_passing_edge(self):
        """Edge with low threshold passes → exposure = 1.0."""
        expr = Edge(Var("a"), Var("b"), Membrane(threshold=0.1))
        self.assertEqual(exposure(expr, reach=0.5), 1.0)

    def test_holding_edge(self):
        """Edge with high threshold holds → exposure = 0.0."""
        expr = Edge(Var("a"), Var("b"), Membrane(threshold=0.9))
        self.assertEqual(exposure(expr, reach=0.5), 0.0)


class TestStructuralWeight(unittest.TestCase):
    def test_all_visible(self):
        """Without edges, everything is visible."""
        vis, veil = structural_weight(Seam(Var("a"), Var("b")))
        self.assertGreater(vis, 0)

    def test_room_veils(self):
        """Room content is veiled."""
        expr = Room(Var("secret"))
        vis, veil = structural_weight(expr)
        self.assertGreater(veil, 0)

    def test_holding_edge_veils(self):
        """Holding edge veils its children."""
        expr = Edge(Var("a"), Var("b"), Membrane(threshold=0.9))
        _, veil = structural_weight(expr, reach=0.5)
        self.assertGreater(veil, 0)


if __name__ == "__main__":
    unittest.main()
