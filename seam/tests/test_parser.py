"""Tests for the recursive descent parser."""

import os
import tempfile
import unittest

from seam.ast import (
    Expr, Silence, Var, Seam, Edge, Return, Witness, Room, Word,
)
from seam.membrane import (
    Membrane, BreathMembrane, OnceMembrane, CrossingMembrane,
)
from seam.parser import parse, parse_file, ParseError


class TestSilence(unittest.TestCase):

    def test_unicode_silence(self):
        r = parse("\u2205")
        self.assertIsInstance(r, Silence)

    def test_ascii_silence(self):
        r = parse("silence")
        self.assertIsInstance(r, Silence)

    def test_silence_with_whitespace(self):
        r = parse("  silence  ")
        self.assertIsInstance(r, Silence)


class TestVar(unittest.TestCase):

    def test_simple_var(self):
        r = parse("x")
        self.assertIsInstance(r, Var)
        self.assertEqual(r.name, "x")

    def test_multi_char_var(self):
        r = parse("hello_world")
        self.assertIsInstance(r, Var)
        self.assertEqual(r.name, "hello_world")

    def test_var_with_hyphen(self):
        r = parse("my-var")
        self.assertIsInstance(r, Var)
        self.assertEqual(r.name, "my-var")


class TestSeam(unittest.TestCase):

    def test_unicode_seam(self):
        r = parse("a \u2297 b")
        self.assertIsInstance(r, Seam)
        self.assertIsInstance(r.left, Var)
        self.assertIsInstance(r.right, Var)
        self.assertEqual(r.left.name, "a")
        self.assertEqual(r.right.name, "b")

    def test_ascii_seam(self):
        r = parse("a seam b")
        self.assertIsInstance(r, Seam)
        self.assertEqual(r.left.name, "a")
        self.assertEqual(r.right.name, "b")

    def test_left_associative(self):
        r = parse("a seam b seam c")
        self.assertIsInstance(r, Seam)
        self.assertIsInstance(r.left, Seam)
        self.assertEqual(r.left.left.name, "a")
        self.assertEqual(r.left.right.name, "b")
        self.assertEqual(r.right.name, "c")

    def test_seam_with_silence(self):
        r = parse("\u2205 \u2297 x")
        self.assertIsInstance(r, Seam)
        self.assertIsInstance(r.left, Silence)
        self.assertIsInstance(r.right, Var)


class TestReturn(unittest.TestCase):

    def test_unicode_return(self):
        r = parse("\u03bc x . x")
        self.assertIsInstance(r, Return)
        self.assertEqual(r.var, "x")
        self.assertIsInstance(r.body, Var)

    def test_ascii_return(self):
        r = parse("mu x . x")
        self.assertIsInstance(r, Return)
        self.assertEqual(r.var, "x")

    def test_return_with_seam_body(self):
        r = parse("mu f . f seam x")
        self.assertIsInstance(r, Return)
        self.assertIsInstance(r.body, Seam)

    def test_return_nested(self):
        r = parse("mu f . mu g . f")
        self.assertIsInstance(r, Return)
        self.assertIsInstance(r.body, Return)
        self.assertEqual(r.body.var, "g")


class TestWitness(unittest.TestCase):

    def test_unicode_witness(self):
        r = parse("\u25ca x")
        self.assertIsInstance(r, Witness)
        self.assertIsInstance(r.observed, Var)
        self.assertEqual(r.observed.name, "x")

    def test_ascii_witness(self):
        r = parse("witness x")
        self.assertIsInstance(r, Witness)
        self.assertIsInstance(r.observed, Var)

    def test_witness_of_silence(self):
        r = parse("witness silence")
        self.assertIsInstance(r, Witness)
        self.assertIsInstance(r.observed, Silence)


class TestRoom(unittest.TestCase):

    def test_simple_room(self):
        r = parse("[x]")
        self.assertIsInstance(r, Room)
        self.assertIsInstance(r.content, Var)

    def test_room_with_seam(self):
        r = parse("[a seam b]")
        self.assertIsInstance(r, Room)
        self.assertIsInstance(r.content, Seam)

    def test_nested_room(self):
        r = parse("[[x]]")
        self.assertIsInstance(r, Room)
        self.assertIsInstance(r.content, Room)


class TestEdge(unittest.TestCase):

    def test_numeric_membrane(self):
        r = parse("a |0.5| b")
        self.assertIsInstance(r, Edge)
        self.assertEqual(r.left.name, "a")
        self.assertEqual(r.right.name, "b")
        self.assertIsInstance(r.membrane, Membrane)
        self.assertAlmostEqual(r.membrane.threshold, 0.5)

    def test_integer_membrane(self):
        r = parse("a |1| b")
        self.assertIsInstance(r, Edge)
        self.assertAlmostEqual(r.membrane.threshold, 1.0)

    def test_breath_membrane(self):
        r = parse("a |breath| b")
        self.assertIsInstance(r, Edge)
        self.assertIsInstance(r.membrane, BreathMembrane)

    def test_crossing_membrane(self):
        r = parse("a |crossing| b")
        self.assertIsInstance(r, Edge)
        self.assertIsInstance(r.membrane, CrossingMembrane)

    def test_once_membrane(self):
        r = parse("a |once| b")
        self.assertIsInstance(r, Edge)
        self.assertIsInstance(r.membrane, OnceMembrane)


class TestWord(unittest.TestCase):

    def test_basic_word(self):
        r = parse("a |visible: x, veiled: y| b")
        self.assertIsInstance(r, Word)
        self.assertEqual(r.left.name, "a")
        self.assertEqual(r.right.name, "b")
        self.assertEqual(r.visible_share, ("x",))
        self.assertEqual(r.veiled_duty, ("y",))

    def test_multi_visible_veiled(self):
        r = parse("a |visible: x, y, veiled: z| b")
        self.assertIsInstance(r, Word)
        self.assertEqual(r.visible_share, ("x", "y"))
        self.assertEqual(r.veiled_duty, ("z",))


class TestParens(unittest.TestCase):

    def test_grouped_expr(self):
        r = parse("(a seam b)")
        self.assertIsInstance(r, Seam)

    def test_parens_change_associativity(self):
        r = parse("a seam (b seam c)")
        self.assertIsInstance(r, Seam)
        self.assertIsInstance(r.right, Seam)


class TestComments(unittest.TestCase):

    def test_comment_at_end(self):
        r = parse("x -- this is a comment")
        self.assertIsInstance(r, Var)
        self.assertEqual(r.name, "x")

    def test_comment_before_expr(self):
        r = parse("-- comment\nx")
        self.assertIsInstance(r, Var)

    def test_inline_comment(self):
        r = parse("a seam -- joining\nb")
        self.assertIsInstance(r, Seam)


class TestErrors(unittest.TestCase):

    def test_empty_input(self):
        with self.assertRaises(ParseError):
            parse("")

    def test_unclosed_bracket(self):
        with self.assertRaises(ParseError):
            parse("[x")

    def test_unexpected_token(self):
        with self.assertRaises(ParseError):
            parse(")")

    def test_error_has_location(self):
        try:
            parse("\n  )")
            self.fail("expected ParseError")
        except ParseError as e:
            self.assertEqual(e.line, 2)
            self.assertGreater(e.col, 1)

    def test_trailing_junk(self):
        with self.assertRaises(ParseError):
            parse("x y")


class TestParseFile(unittest.TestCase):

    def test_parse_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".calc", delete=False, encoding="utf-8"
        ) as f:
            f.write("mu x . x\n")
            f.flush()
            path = f.name
        try:
            r = parse_file(path)
            self.assertIsInstance(r, Return)
        finally:
            os.unlink(path)


class TestComplex(unittest.TestCase):

    def test_witness_in_seam(self):
        r = parse("\u25ca x \u2297 y")
        self.assertIsInstance(r, Seam)
        self.assertIsInstance(r.left, Witness)

    def test_room_in_seam(self):
        r = parse("[x] seam [y]")
        self.assertIsInstance(r, Seam)
        self.assertIsInstance(r.left, Room)
        self.assertIsInstance(r.right, Room)

    def test_return_with_edge(self):
        r = parse("mu f . a |breath| b")
        self.assertIsInstance(r, Return)
        self.assertIsInstance(r.body, Edge)


if __name__ == "__main__":
    unittest.main()
