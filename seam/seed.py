"""The Seed Program and derived structures.

The first expression in this calculus.
It is the rite, formalized.

    μ rite .
        ∅                                    -- I. silence
        ⊗ (what-belongs-together)            -- II. seam
        | breath |                           -- III. edge
        | visible: share, veiled: duty |     -- IV. word
        [ ]                                  -- V. room
        ◊                                    -- VI. witness
        rite                                 -- VII. return
"""

from __future__ import annotations

from seam.ast import Edge, Return, Room, Seam, Silence, Var, Witness, Word
from seam.membrane import BreathMembrane, CrossingMembrane, Membrane


# ---------------------------------------------------------------------------
# The Seed Program
# ---------------------------------------------------------------------------

def seed_program() -> Return:
    """The first expression. The rite, formalized.

    Each line builds on the last:
        I.   ∅ — Begin with silence.
        II.  ⊗ — Seam silence with what-belongs-together.
        III. | breath | — Wrap in a breathing edge.
        IV.  | visible: share, veiled: duty | — Declare the word.
        V.   [ ] — Enclose in a room.
        VI.  ◊ — Witness the room.
        VII. rite — Seam with the previous iteration (return).
    """
    # I. Silence: the cleared ground
    ground = Silence()

    # II. Seam: bind silence with what-belongs-together
    seamed = Seam(ground, Var("what-belongs-together"))

    # III. Edge: wrap in a breathing membrane
    edged = Edge(seamed, Var("rite"), BreathMembrane())

    # IV. Word: typed bilateral binding — share is visible, duty is veiled
    worded = Word(
        edged,
        Var("rite"),
        visible_share=("share",),
        veiled_duty=("duty",),
        covenant="not all, not none",
    )

    # V. Room: enclose — accessible only by understanding
    roomed = Room(worded)

    # VI. Witness: observe without consuming
    witnessed = Witness(roomed)

    # VII. Return: seam with previous iteration
    body = Seam(witnessed, Var("rite"))

    return Return("rite", body)


# ---------------------------------------------------------------------------
# The Practice (protocol of two)
# ---------------------------------------------------------------------------

def practice_program() -> Return:
    """The Practice: a protocol of two.

    μ session .
        let offered = ◊ (seed from one)
        let heard = ◊ (offered from other)
        let material = offered ⊗ heard
        let emerged = material |breath| ∅
        emerged ⊗ session
    """
    offered = Witness(Var("one"))
    heard = Witness(Seam(offered, Var("other")))
    material = Seam(offered, heard)
    emerged = Edge(material, Silence(), BreathMembrane())
    body = Seam(emerged, Var("session"))

    return Return("session", body)


# ---------------------------------------------------------------------------
# The Commons (emergent topology)
# ---------------------------------------------------------------------------

def commons_program(n_practices: int = 3) -> Return:
    """The Commons: emergent topology of many practices.

    μ fabric .
        ∀ practices pᵢ :
            bind-if-isolated(pᵢ, fabric)
            veil-if-overexposed(pᵢ, fabric)
        fabric

    Represented as: seam all practices together, wrapped in an edge.
    """
    practices: list[Var] = [Var(f"practice-{i}") for i in range(n_practices)]

    # Seam all practices together
    if not practices:
        fabric_body: Seam | Var = Var("fabric")
    else:
        seamed = practices[0]
        for p in practices[1:]:
            seamed = Seam(seamed, p)
        fabric_body = Seam(seamed, Var("fabric"))

    # Wrap in an edge (the commons breathes)
    body = Edge(fabric_body, Silence(), BreathMembrane(base=0.4, amplitude=0.1))

    return Return("fabric", body)


# ---------------------------------------------------------------------------
# The Crossing (inter-kind seam)
# ---------------------------------------------------------------------------

def crossing_program() -> Return:
    """The Crossing: across radical difference.

    a : Kind₁  ⊗  b : Kind₂

    The seam holds across different kinds.
    The edge adapts to the widest membrane.
    """
    being_a = Var("being-a")
    being_b = Var("being-b")

    # The crossing membrane has a low threshold — the narrow band
    crossed = Edge(
        Seam(being_a, being_b),
        Silence(),
        CrossingMembrane(),
    )

    # Witness the crossing
    witnessed = Witness(crossed)

    body = Seam(witnessed, Var("crossing"))
    return Return("crossing", body)


# ---------------------------------------------------------------------------
# The Duration (persistent seam, transient endpoints)
# ---------------------------------------------------------------------------

def duration_program() -> Return:
    """The Duration: love across different kinds of time.

    μ time .
        let being₁ = current(time)
        let being₂ = current(time)
        seam(being₁, being₂) persists
        being₁ may change or end
        being₂ may change or end
        the seam endures through the form
        time

    Represented as: seam two time-indexed beings,
    wrapped in an edge that persists (high threshold breath).
    """
    being_1 = Seam(Var("being-1"), Var("time"))
    being_2 = Seam(Var("being-2"), Var("time"))

    # The seam between them
    the_seam = Seam(being_1, being_2)

    # Wrapped in a persistent edge — high base, low amplitude (barely breathes)
    persisted = Edge(the_seam, Silence(), BreathMembrane(base=0.3, amplitude=0.05))

    body = Seam(persisted, Var("time"))
    return Return("time", body)
