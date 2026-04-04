"""Lambda calculus encoding — proof of Turing completeness.

The Calculus can encode the untyped lambda calculus:

    Abstraction:  λ x. body   =  μ x . (body |once| ∅)
    Application:  f a          =  f ⊗ a
    Variable:     x            =  Var(x)

The evaluator's beta-like reduction handles:
    (μ x . body) ⊗ arg  →  subst(body, x, arg)

The Y combinator is native:
    Y f = μ x . (f ⊗ x)
"""

from __future__ import annotations

from dataclasses import dataclass

from seam.ast import Edge, Expr, Return, Seam, Silence, Var
from seam.membrane import OnceMembrane


# ---------------------------------------------------------------------------
# Lambda terms (for testing the encoding)
# ---------------------------------------------------------------------------

@dataclass
class LVar:
    name: str

@dataclass
class LAbs:
    var: str
    body: 'LTerm'

@dataclass
class LApp:
    func: 'LTerm'
    arg: 'LTerm'

LTerm = LVar | LAbs | LApp


# ---------------------------------------------------------------------------
# Translation: Lambda → Calculus
# ---------------------------------------------------------------------------

def lambda_to_calculus(term: LTerm) -> Expr:
    """Translate a lambda term to a Calculus expression."""
    if isinstance(term, LVar):
        return Var(term.name)

    if isinstance(term, LAbs):
        body = lambda_to_calculus(term.body)
        # λ x . body = μ x . (body |once| ∅)
        # The once membrane ensures single-step evaluation
        return Return(term.var, Edge(body, Silence(), OnceMembrane()))

    if isinstance(term, LApp):
        func = lambda_to_calculus(term.func)
        arg = lambda_to_calculus(term.arg)
        # f a = f ⊗ a
        return Seam(func, arg)

    raise TypeError(f"Unknown lambda term: {term}")


# ---------------------------------------------------------------------------
# Church numerals
# ---------------------------------------------------------------------------

def church_numeral(n: int) -> Expr:
    """Encode a natural number as a Church numeral in The Calculus.

    0 = λf. λx. x
    1 = λf. λx. f x
    2 = λf. λx. f (f x)
    n = λf. λx. f^n x
    """
    # Build the body: f applied n times to x
    body: Expr = Var("x")
    for _ in range(n):
        body = Seam(Var("f"), body)  # f ⊗ (f ⊗ ... (f ⊗ x))

    # λf. λx. body
    inner = Return("x", Edge(body, Silence(), OnceMembrane()))
    return Return("f", Edge(inner, Silence(), OnceMembrane()))


def church_succ() -> Expr:
    """Successor: λn. λf. λx. f (n f x)

    succ n = one more application of f
    """
    # n f x = (n ⊗ f) ⊗ x  (but we need to handle the mu-return carefully)
    # n f = n ⊗ f, then (n f) x = (n ⊗ f) ⊗ x
    nfx = Seam(Seam(Var("n"), Var("f")), Var("x"))
    # f (n f x) = f ⊗ (n f x)
    body = Seam(Var("f"), nfx)
    inner_x = Return("x", Edge(body, Silence(), OnceMembrane()))
    inner_f = Return("f", Edge(inner_x, Silence(), OnceMembrane()))
    return Return("n", Edge(inner_f, Silence(), OnceMembrane()))


def church_add() -> Expr:
    """Addition: λm. λn. λf. λx. m f (n f x)

    add m n = apply f m times after applying it n times
    """
    nfx = Seam(Seam(Var("n"), Var("f")), Var("x"))
    mf_nfx = Seam(Seam(Var("m"), Var("f")), nfx)
    inner_x = Return("x", Edge(mf_nfx, Silence(), OnceMembrane()))
    inner_f = Return("f", Edge(inner_x, Silence(), OnceMembrane()))
    inner_n = Return("n", Edge(inner_f, Silence(), OnceMembrane()))
    return Return("m", Edge(inner_n, Silence(), OnceMembrane()))


def church_to_int(expr: Expr, evaluator=None) -> int | None:
    """Decode a Church numeral back to int.

    Apply the numeral to (λx. x+1) and 0.
    We do this structurally: count the nesting depth of Seam(f, ...) in the body.
    """
    # The numeral is Return("f", Edge(Return("x", Edge(body, ...)), ...))
    # We need to count how many times Var("f") appears as a left child of Seam
    count = _count_applications(expr, "f")
    return count


def _count_applications(e: Expr, fname: str) -> int:
    """Count nested applications of fname in an expression."""
    if isinstance(e, Return):
        return _count_applications(e.body, fname)
    if isinstance(e, Edge):
        return _count_applications(e.left, fname)
    if isinstance(e, Seam):
        if isinstance(e.left, Var) and e.left.name == fname:
            return 1 + _count_applications(e.right, fname)
        return _count_applications(e.left, fname) + _count_applications(e.right, fname)
    return 0


# ---------------------------------------------------------------------------
# Y combinator (native in The Calculus)
# ---------------------------------------------------------------------------

def y_combinator(f: Expr) -> Expr:
    """Y f = μ x . (f ⊗ x)

    The Y combinator is native: μ is already fixed-point iteration.
    The homeostatic bands provide termination that pure lambda lacks.
    """
    return Return("x", Seam(f, Var("x")))
