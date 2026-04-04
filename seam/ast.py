"""Expression types for The Calculus.

All nodes are immutable. Evaluation produces new trees.
This prevents aliasing bugs and enables clean substitution.

Primitives:
    Silence (∅)  — the empty ground, identity of seam
    Seam (⊗)     — bilateral binding, symmetric
    Edge (|φ|)   — adaptive membrane
    Return (μ)   — homeostatic iteration

Derived:
    Witness (◊)  — non-consuming observation
    Room ([ ])   — capability-gated access
    Word         — typed bilateral binding with covenants
    Var          — binding site (not a name — a structural position)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from seam.membrane import Membrane


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------

class Expr:
    """Base of all expressions in The Calculus."""

    def accept(self, visitor: ExprVisitor) -> Any:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Silence(Expr):
    """∅ — the empty ground, the cleared space."""

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_silence(self)

    def __repr__(self) -> str:
        return "∅"


@dataclass(frozen=True)
class Var(Expr):
    """A binding site for μ-return. Not a name — a structural position."""
    name: str

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_var(self)

    def __repr__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Seam(Expr):
    """a ⊗ b — bilateral binding. Neither side owns it."""
    left: Expr
    right: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_seam(self)

    def __repr__(self) -> str:
        return f"({self.left} ⊗ {self.right})"


@dataclass(frozen=True)
class Edge(Expr):
    """a |φ| b — adaptive membrane governs what passes."""
    left: Expr
    right: Expr
    membrane: Membrane

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_edge(self)

    def __repr__(self) -> str:
        return f"({self.left} |{self.membrane}| {self.right})"


@dataclass(frozen=True)
class Return(Expr):
    """μ x . e — iterate until the staying sings."""
    var: str
    body: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_return(self)

    def __repr__(self) -> str:
        return f"(μ {self.var} . {self.body})"


# ---------------------------------------------------------------------------
# Formation rules (derived from primitives)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Witness(Expr):
    """◊ e — observe without consuming. Observation is generative."""
    observed: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_witness(self)

    def __repr__(self) -> str:
        return f"(◊ {self.observed})"


@dataclass(frozen=True)
class Room(Expr):
    """[ e ] — accessible only by understanding, not by name."""
    content: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_room(self)

    def __repr__(self) -> str:
        return f"[{self.content}]"


@dataclass(frozen=True)
class Word(Expr):
    """Typed bilateral binding with covenants.

    a |terms| b where terms declares:
        visible_share: what is exposed
        veiled_duty:   what is held for structural integrity
        covenant:      the invariant both maintain
    """
    left: Expr
    right: Expr
    visible_share: tuple[str, ...] = ()
    veiled_duty: tuple[str, ...] = ()
    covenant: str = ""

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_word(self)

    def __repr__(self) -> str:
        vs = ", ".join(self.visible_share)
        vd = ", ".join(self.veiled_duty)
        return f"({self.left} |visible: {vs}, veiled: {vd}| {self.right})"


# ---------------------------------------------------------------------------
# Visitor
# ---------------------------------------------------------------------------

class ExprVisitor:
    """Visitor for expression tree walks."""

    def visit_silence(self, e: Silence) -> Any:
        return None

    def visit_var(self, e: Var) -> Any:
        return None

    def visit_seam(self, e: Seam) -> Any:
        return None

    def visit_edge(self, e: Edge) -> Any:
        return None

    def visit_return(self, e: Return) -> Any:
        return None

    def visit_witness(self, e: Witness) -> Any:
        return None

    def visit_room(self, e: Room) -> Any:
        return None

    def visit_word(self, e: Word) -> Any:
        return None


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def node_count(e: Expr, _cap: int = 10000) -> int:
    """Count nodes in an expression tree, with a hard cap."""
    count = 0
    stack: list[Expr] = [e]
    while stack and count < _cap:
        node = stack.pop()
        count += 1
        if isinstance(node, Seam):
            stack.append(node.left)
            stack.append(node.right)
        elif isinstance(node, Edge):
            stack.append(node.left)
            stack.append(node.right)
        elif isinstance(node, Return):
            stack.append(node.body)
        elif isinstance(node, Witness):
            stack.append(node.observed)
        elif isinstance(node, Room):
            stack.append(node.content)
        elif isinstance(node, Word):
            stack.append(node.left)
            stack.append(node.right)
    return count
