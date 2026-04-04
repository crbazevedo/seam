"""Configuration constants for The Calculus interpreter.

All hard caps exist to prevent unbounded growth.
The v1 interpreter lacked these and exhausted system memory.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CalcConfig:
    # Homeostatic bands
    connectivity_lo: float = 0.3
    connectivity_hi: float = 0.7
    exposure_lo: float = 0.2
    exposure_hi: float = 0.6

    # Convergence
    stability_window: int = 5

    # Hard resource caps — non-negotiable
    max_returns: int = 100
    max_depth: int = 50
    max_nodes: int = 500  # normalize will cull beyond this
    default_reach: float = 0.5


DEFAULT_CONFIG = CalcConfig()
