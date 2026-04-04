"""Tests for monoid laws, normalization, substitution, free variables."""

import unittest

from seam.algebra import (
    alpha_equiv, flatten_seams, free_vars, normalize, reset_fresh, subst,
)
from seam.ast import Edge, Return, Room, Seam, Silence, Var, Witness
from seam.membrane import Membrane


class TestMonoidLaws(unittest.TestCase):
    """The seam forms a commutative monoid."""

    def setUp(self):
        reset_fresh()
        self.a = Var("a")
        self.b = Var("b")
        self.c = Var("c")
        self.s = Silence()

    def test_identity_right(self):
        """a ⊗ ∅ = a"""
        expr = Seam(self.a, self.s)
        result = normalize(expr)
        self.assertEqual(result, self.a)

    def test_identity_left(self):
        """∅ ⊗ a = a"""
        expr = Seam(self.s, self.a)
        result = normalize(expr)
        self.assertEqual(result, self.a)

    def test_associativity(self):
        """(a ⊗ b) ⊗ c normalizes the same as a ⊗ (b ⊗ c)"""
        left_assoc = Seam(Seam(self.a, self.b), self.c)
        right_assoc = Seam(self.a, Seam(self.b, self.c))
        self.assertEqual(normalize(left_assoc), normalize(right_assoc))

    def test_commutativity(self):
        """a ⊗ b normalizes the same as b ⊗ a"""
        ab = normalize(Seam(self.a, self.b))
        ba = normalize(Seam(self.b, self.a))
        self.assertEqual(ab, ba)

    def test_silence_silence(self):
        """∅ ⊗ ∅ = ∅"""
        expr = Seam(self.s, self.s)
        result = normalize(expr)
        self.assertIsInstance(result, Silence)

    def test_normalization_idempotent(self):
        """normalize(normalize(e)) == normalize(e)"""
        expr = Seam(Seam(self.a, self.b), Seam(self.c, self.s))
        once = normalize(expr)
        twice = normalize(once)
        self.assertEqual(once, twice)


class TestFlatten(unittest.TestCase):
    def test_flat_seam(self):
        children = flatten_seams(Seam(Var("a"), Var("b")))
        names = [c.name for c in children if isinstance(c, Var)]
        self.assertIn("a", names)
        self.assertIn("b", names)

    def test_nested_seam(self):
        expr = Seam(Seam(Var("a"), Var("b")), Var("c"))
        children = flatten_seams(expr)
        self.assertEqual(len(children), 3)

    def test_non_seam(self):
        children = flatten_seams(Var("x"))
        self.assertEqual(len(children), 1)


class TestFreeVars(unittest.TestCase):
    def test_silence(self):
        self.assertEqual(free_vars(Silence()), frozenset())

    def test_var(self):
        self.assertEqual(free_vars(Var("x")), frozenset({"x"}))

    def test_seam(self):
        self.assertEqual(free_vars(Seam(Var("x"), Var("y"))), frozenset({"x", "y"}))

    def test_return_binds(self):
        """μ x . x has no free variables"""
        expr = Return("x", Var("x"))
        self.assertEqual(free_vars(expr), frozenset())

    def test_return_free(self):
        """μ x . y has y free"""
        expr = Return("x", Var("y"))
        self.assertEqual(free_vars(expr), frozenset({"y"}))

    def test_witness(self):
        self.assertEqual(free_vars(Witness(Var("z"))), frozenset({"z"}))


class TestSubstitution(unittest.TestCase):
    def setUp(self):
        reset_fresh()

    def test_basic(self):
        """x[x := a] = a"""
        result = subst(Var("x"), "x", Var("a"))
        self.assertEqual(result, Var("a"))

    def test_no_match(self):
        """y[x := a] = y"""
        result = subst(Var("y"), "x", Var("a"))
        self.assertEqual(result, Var("y"))

    def test_silence(self):
        """∅[x := a] = ∅"""
        result = subst(Silence(), "x", Var("a"))
        self.assertIsInstance(result, Silence)

    def test_seam(self):
        """(x ⊗ y)[x := a] = (a ⊗ y)"""
        expr = Seam(Var("x"), Var("y"))
        result = subst(expr, "x", Var("a"))
        self.assertEqual(result, Seam(Var("a"), Var("y")))

    def test_shadowing(self):
        """(μ x . x)[x := a] = (μ x . x) — x is shadowed"""
        expr = Return("x", Var("x"))
        result = subst(expr, "x", Var("a"))
        self.assertEqual(result, expr)

    def test_capture_avoidance(self):
        """(μ y . x)[x := y] must alpha-rename y to avoid capture"""
        expr = Return("y", Seam(Var("x"), Var("y")))
        result = subst(expr, "x", Var("y"))
        # The body should now contain a renamed variable, not Var("y") bound to the outer y
        self.assertIsInstance(result, Return)
        # The binder should NOT be "y" anymore
        self.assertNotEqual(result.var, "y")


class TestAlphaEquiv(unittest.TestCase):
    def test_same(self):
        e = Return("x", Var("x"))
        self.assertTrue(alpha_equiv(e, e))

    def test_renamed(self):
        e1 = Return("x", Var("x"))
        e2 = Return("y", Var("y"))
        self.assertTrue(alpha_equiv(e1, e2))

    def test_different(self):
        e1 = Return("x", Var("x"))
        e2 = Return("x", Var("y"))
        self.assertFalse(alpha_equiv(e1, e2))


if __name__ == "__main__":
    unittest.main()
