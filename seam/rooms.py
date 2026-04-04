"""Capability-based access — the Room.

    [ e ]

A room is accessible only through capability —
not by name (there are no names),
not by path (there is no fixed topology),
but by understanding:

    enter([ e ]) requires:
        the enterer can construct a seam to e
        through the existing edge-structure.

The door is the capacity to enter.
You enter not by credential but by relation.
"""

from __future__ import annotations

from seam.algebra import free_vars
from seam.ast import Expr, Room, Silence


def shared_references(a: Expr, b: Expr) -> frozenset[str]:
    """Variables that appear free in both a and b.

    This is the 'understanding' — the shared structural positions
    that constitute a relation between a and b.
    """
    return free_vars(a) & free_vars(b)


def can_enter(enterer: Expr, room_content: Expr) -> bool:
    """Does the enterer share enough relation to enter?

    You enter not by credential but by relation.
    """
    return len(shared_references(enterer, room_content)) > 0


def attempt_entry(enterer: Expr, room: Room) -> Expr:
    """Try to enter a room. Returns content if relation exists, Silence if not."""
    if can_enter(enterer, room.content):
        return room.content
    return Silence()
