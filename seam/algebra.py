"""Algebra of The Calculus — normalization, substitution, free variables.

The seam forms a commutative monoid:
    Associative:  (a ⊗ b) ⊗ c  =  a ⊗ (b ⊗ c)
    Commutative:  a ⊗ b  =  b ⊗ a
    Identity:     a ⊗ ∅  =  a

Normalization flattens seam chains, removes silence, sorts for canonical form.
This prevents the exponential blowup that killed v1.
"""

from __future__ import annotations

from seam.ast import (
    Edge, Expr, Return, Room, Seam, Silence, Var, Witness, Word, node_count,
)
from seam.config import DEFAULT_CONFIG

# ---------------------------------------------------------------------------
# Fresh variable generation
# ---------------------------------------------------------------------------

_fresh_counter = 0


def fresh(prefix: str = "v") -> str:
    global _fresh_counter
    _fresh_counter += 1
    return f"{prefix}${_fresh_counter}"


def reset_fresh() -> None:
    global _fresh_counter
    _fresh_counter = 0


# ---------------------------------------------------------------------------
# Free variables
# ---------------------------------------------------------------------------

def free_vars(e: Expr) -> frozenset[str]:
    """Collect all free variable names in e. Iterative to avoid stack overflow."""
    free: set[str] = set()
    bound: set[str] = set()
    # Stack of (expr, bound_set_snapshot)
    stack: list[tuple[Expr, frozenset[str]]] = [(e, frozenset())]
    cap = DEFAULT_CONFIG.max_nodes * 2
    visited = 0

    while stack and visited < cap:
        node, bnd = stack.pop()
        visited += 1

        if isinstance(node, Silence):
            continue
        elif isinstance(node, Var):
            if node.name not in bnd:
                free.add(node.name)
        elif isinstance(node, Seam):
            stack.append((node.left, bnd))
            stack.append((node.right, bnd))
        elif isinstance(node, Edge):
            stack.append((node.left, bnd))
            stack.append((node.right, bnd))
        elif isinstance(node, Return):
            stack.append((node.body, bnd | {node.var}))
        elif isinstance(node, Witness):
            stack.append((node.observed, bnd))
        elif isinstance(node, Room):
            stack.append((node.content, bnd))
        elif isinstance(node, Word):
            stack.append((node.left, bnd))
            stack.append((node.right, bnd))

    return frozenset(free)


# ---------------------------------------------------------------------------
# Capture-avoiding substitution
# ---------------------------------------------------------------------------

def subst(e: Expr, var: str, val: Expr, _depth: int = 0) -> Expr:
    """Substitute val for var in e. Capture-avoiding. Depth-limited."""
    if _depth > DEFAULT_CONFIG.max_depth:
        return e  # safety: stop substituting at depth limit

    if isinstance(e, Silence):
        return e

    if isinstance(e, Var):
        return val if e.name == var else e

    if isinstance(e, Seam):
        return Seam(
            subst(e.left, var, val, _depth + 1),
            subst(e.right, var, val, _depth + 1),
        )

    if isinstance(e, Edge):
        return Edge(
            subst(e.left, var, val, _depth + 1),
            subst(e.right, var, val, _depth + 1),
            e.membrane,
        )

    if isinstance(e, Return):
        if e.var == var:
            return e  # var is shadowed by this binder
        if e.var in free_vars(val):
            # Capture: alpha-rename the binder
            new_var = fresh(e.var)
            renamed_body = subst(e.body, e.var, Var(new_var), _depth + 1)
            return Return(new_var, subst(renamed_body, var, val, _depth + 1))
        return Return(e.var, subst(e.body, var, val, _depth + 1))

    if isinstance(e, Witness):
        return Witness(subst(e.observed, var, val, _depth + 1))

    if isinstance(e, Room):
        return Room(subst(e.content, var, val, _depth + 1))

    if isinstance(e, Word):
        return Word(
            subst(e.left, var, val, _depth + 1),
            subst(e.right, var, val, _depth + 1),
            e.visible_share,
            e.veiled_duty,
            e.covenant,
        )

    return e


# ---------------------------------------------------------------------------
# Normalization (monoid laws)
# ---------------------------------------------------------------------------

def _structural_key(e: Expr) -> str:
    """Deterministic key for sorting seam children into canonical order."""
    if isinstance(e, Silence):
        return "0"
    if isinstance(e, Var):
        return f"1:{e.name}"
    if isinstance(e, Seam):
        return f"2:{_structural_key(e.left)}:{_structural_key(e.right)}"
    if isinstance(e, Edge):
        return f"3:{_structural_key(e.left)}:{_structural_key(e.right)}"
    if isinstance(e, Return):
        return f"4:{e.var}:{_structural_key(e.body)}"
    if isinstance(e, Witness):
        return f"5:{_structural_key(e.observed)}"
    if isinstance(e, Room):
        return f"6:{_structural_key(e.content)}"
    if isinstance(e, Word):
        return f"7:{_structural_key(e.left)}:{_structural_key(e.right)}"
    return "9"


def flatten_seams(e: Expr) -> list[Expr]:
    """Flatten nested seams into a list of children (associativity)."""
    result: list[Expr] = []
    stack: list[Expr] = [e]
    cap = DEFAULT_CONFIG.max_nodes
    while stack and len(result) < cap:
        node = stack.pop()
        if isinstance(node, Seam):
            stack.append(node.right)
            stack.append(node.left)
        else:
            result.append(node)
    return result


def _build_seam_tree(children: list[Expr]) -> Expr:
    """Right-fold a list of children into nested Seam nodes."""
    if not children:
        return Silence()
    result = children[-1]
    for i in range(len(children) - 2, -1, -1):
        result = Seam(children[i], result)
    return result


def normalize(e: Expr, _depth: int = 0) -> Expr:
    """Apply monoid laws to produce canonical form. Depth-limited.

    1. Recursively normalize children
    2. Flatten seam chains
    3. Remove Silence elements (identity law)
    4. Sort by structural key (commutativity → canonical form)
    5. Rebuild right-associated seam tree
    6. Cap total node count
    """
    if _depth > DEFAULT_CONFIG.max_depth:
        return e

    if isinstance(e, Silence):
        return e

    if isinstance(e, Var):
        return e

    if isinstance(e, Seam):
        # Flatten, normalize children, remove silence, sort, rebuild
        children = flatten_seams(e)
        normed = [normalize(c, _depth + 1) for c in children]
        # Remove silence (identity law)
        filtered = [c for c in normed if not isinstance(c, Silence)]
        if not filtered:
            return Silence()
        if len(filtered) == 1:
            return filtered[0]
        # Sort for canonical form (commutativity)
        filtered.sort(key=_structural_key)
        result = _build_seam_tree(filtered)
        # Node count guard
        if node_count(result) > DEFAULT_CONFIG.max_nodes:
            # Truncate: keep first N children
            half = DEFAULT_CONFIG.max_nodes // 4
            result = _build_seam_tree(filtered[:half])
        return result

    if isinstance(e, Edge):
        return Edge(
            normalize(e.left, _depth + 1),
            normalize(e.right, _depth + 1),
            e.membrane,
        )

    if isinstance(e, Return):
        return Return(e.var, normalize(e.body, _depth + 1))

    if isinstance(e, Witness):
        return Witness(normalize(e.observed, _depth + 1))

    if isinstance(e, Room):
        return Room(normalize(e.content, _depth + 1))

    if isinstance(e, Word):
        return Word(
            normalize(e.left, _depth + 1),
            normalize(e.right, _depth + 1),
            e.visible_share,
            e.veiled_duty,
            e.covenant,
        )

    return e


# ---------------------------------------------------------------------------
# Alpha-equivalence
# ---------------------------------------------------------------------------

def alpha_equiv(a: Expr, b: Expr) -> bool:
    """Check if two expressions are equal up to alpha-renaming."""
    return _alpha_eq(a, b, {}, {})


def _alpha_eq(a: Expr, b: Expr, env_a: dict[str, int], env_b: dict[str, int]) -> bool:
    if type(a) is not type(b):
        return False

    if isinstance(a, Silence):
        return True

    if isinstance(a, Var):
        assert isinstance(b, Var)
        # Both bound → compare de Bruijn indices; both free → compare names
        ia = env_a.get(a.name)
        ib = env_b.get(b.name)
        if ia is not None and ib is not None:
            return ia == ib
        if ia is None and ib is None:
            return a.name == b.name
        return False

    if isinstance(a, Seam):
        assert isinstance(b, Seam)
        return (_alpha_eq(a.left, b.left, env_a, env_b)
                and _alpha_eq(a.right, b.right, env_a, env_b))

    if isinstance(a, Edge):
        assert isinstance(b, Edge)
        return (_alpha_eq(a.left, b.left, env_a, env_b)
                and _alpha_eq(a.right, b.right, env_a, env_b))

    if isinstance(a, Return):
        assert isinstance(b, Return)
        depth = len(env_a)
        new_a = {**env_a, a.var: depth}
        new_b = {**env_b, b.var: depth}
        return _alpha_eq(a.body, b.body, new_a, new_b)

    if isinstance(a, Witness):
        assert isinstance(b, Witness)
        return _alpha_eq(a.observed, b.observed, env_a, env_b)

    if isinstance(a, Room):
        assert isinstance(b, Room)
        return _alpha_eq(a.content, b.content, env_a, env_b)

    if isinstance(a, Word):
        assert isinstance(b, Word)
        return (_alpha_eq(a.left, b.left, env_a, env_b)
                and _alpha_eq(a.right, b.right, env_a, env_b)
                and a.visible_share == b.visible_share
                and a.veiled_duty == b.veiled_duty)

    return False
