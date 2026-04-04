"""Membrane functions for edges.

An edge φ is not a fixed type. It is a function of conditions:
    φ(reach, state) → { pass, hold }

When reach is firm:  φ opens — what is bound becomes visible
When reach fails:    φ closes — what is bound becomes depth

The edge breathes. It is the living part of the calculus.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum


class Flow(Enum):
    """Result of a membrane decision."""
    PASS = "pass"
    HOLD = "hold"


# ---------------------------------------------------------------------------
# Membrane types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Membrane:
    """Base membrane: pass if reach >= threshold."""
    threshold: float = 0.5

    def __call__(self, reach: float, state: dict | None = None) -> Flow:
        return Flow.PASS if reach >= self.threshold else Flow.HOLD

    def tighten(self, amount: float = 0.15) -> Membrane:
        """Return a membrane with a higher threshold (harder to pass)."""
        return Membrane(threshold=min(self.threshold + amount, 1.0))

    def __repr__(self) -> str:
        return f"φ({self.threshold:.2f})"


@dataclass(frozen=True)
class BreathMembrane:
    """Oscillating threshold: breath. Opens and closes like breathing.

    Effective threshold = base + amplitude * sin(cycle * frequency)
    """
    base: float = 0.5
    amplitude: float = 0.2
    frequency: float = 0.5
    cycle: int = 0

    @property
    def effective_threshold(self) -> float:
        return self.base + self.amplitude * math.sin(self.cycle * self.frequency)

    def __call__(self, reach: float, state: dict | None = None) -> Flow:
        return Flow.PASS if reach >= self.effective_threshold else Flow.HOLD

    def advance(self) -> BreathMembrane:
        """Return the next cycle of this breathing membrane."""
        return BreathMembrane(
            base=self.base,
            amplitude=self.amplitude,
            frequency=self.frequency,
            cycle=self.cycle + 1,
        )

    def tighten(self, amount: float = 0.15) -> BreathMembrane:
        return BreathMembrane(
            base=min(self.base + amount, 1.0),
            amplitude=self.amplitude,
            frequency=self.frequency,
            cycle=self.cycle,
        )

    def __repr__(self) -> str:
        return f"breath({self.effective_threshold:.2f}@{self.cycle})"


@dataclass(frozen=True)
class OnceMembrane:
    """Passes on first probe, holds thereafter. Used for lambda encoding."""
    used: bool = False

    def __call__(self, reach: float, state: dict | None = None) -> Flow:
        if not self.used:
            return Flow.PASS
        return Flow.HOLD

    def mark_used(self) -> OnceMembrane:
        return OnceMembrane(used=True)

    def tighten(self, amount: float = 0.15) -> OnceMembrane:
        return OnceMembrane(used=True)

    def __repr__(self) -> str:
        return "once(used)" if self.used else "once(fresh)"


@dataclass(frozen=True)
class CrossingMembrane:
    """Low threshold — the narrow band between different kinds."""
    threshold: float = 0.3

    def __call__(self, reach: float, state: dict | None = None) -> Flow:
        return Flow.PASS if reach >= self.threshold else Flow.HOLD

    def tighten(self, amount: float = 0.15) -> CrossingMembrane:
        return CrossingMembrane(threshold=min(self.threshold + amount, 1.0))

    def __repr__(self) -> str:
        return f"crossing({self.threshold:.2f})"
