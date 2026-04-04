"""Self-Regulating Agent Mesh — multi-agent coordination through The Calculus.

Models a mesh of AI agents where:
- Each agent has an adaptive trust membrane
- When an agent produces bad results, its membrane tightens (VEIL)
- When agents are isolated, new connections form (BIND)
- The mesh self-heals through homeostatic convergence

Three scenarios:
1. HEALTHY MESH — all agents reliable, mesh converges quickly
2. DEGRADED MESH — one agent unreliable, mesh self-heals around it
3. FRAGMENTED MESH — agents don't connect, mesh cannot stabilize
"""

from __future__ import annotations

from seam.algebra import reset_fresh
from seam.ast import Edge, Return, Room, Seam, Silence, Var, Witness, Word
from seam.config import CalcConfig
from seam.evaluator import Evaluator
from seam.membrane import BreathMembrane, Membrane
from seam.viz import ascii_trace, compact


MESH_CONFIG = CalcConfig(
    connectivity_lo=0.3,
    connectivity_hi=0.7,
    exposure_lo=0.2,
    exposure_hi=0.6,
    stability_window=5,
    max_returns=50,
    max_nodes=500,
    max_depth=30,
)


def _agent_node(name: str, reliability: float) -> Edge:
    """An agent behind a trust membrane.

    Higher reliability → lower threshold → membrane passes more easily.
    Lower reliability → higher threshold → membrane holds more.
    """
    return Edge(
        Var(name),
        Var(f"{name}-output"),
        Membrane(threshold=1.0 - reliability),
    )


def healthy_mesh() -> Return:
    """Three reliable agents, fully connected.

    All agents have high reliability (0.8) → membranes pass easily.
    Agents are seamed together (bilateral connections).
    Should converge: good connectivity, moderate exposure.
    """
    agent_a = _agent_node("agent-a", reliability=0.8)
    agent_b = _agent_node("agent-b", reliability=0.8)
    agent_c = _agent_node("agent-c", reliability=0.8)

    # Fully connected: each pair seamed
    mesh = Seam(Seam(agent_a, agent_b), Seam(agent_c, Var("mesh")))

    # Witness the mesh state (monitoring)
    observed = Witness(mesh)

    body = Seam(observed, Var("mesh"))
    return Return("mesh", body)


def degraded_mesh() -> Return:
    """Three agents, one unreliable. Mesh self-heals.

    Agent C has low reliability (0.15) → membrane holds almost everything.
    The mesh should still converge because VEIL isolates the bad agent
    and BIND maintains connections between healthy agents.
    """
    agent_a = _agent_node("agent-a", reliability=0.8)
    agent_b = _agent_node("agent-b", reliability=0.8)
    agent_c = _agent_node("agent-c", reliability=0.15)  # unreliable!

    mesh = Seam(Seam(agent_a, agent_b), Seam(agent_c, Var("mesh")))
    observed = Witness(mesh)

    body = Seam(observed, Var("mesh"))
    return Return("mesh", body)


def fragmented_mesh() -> Return:
    """Three agents with no connections between them.

    Agents are isolated (no seams between them, only edges to Silence).
    Should NOT converge: connectivity stays too low.
    """
    # Each agent talks to nothing
    agent_a = Edge(Var("agent-a"), Silence(), Membrane(threshold=0.5))
    agent_b = Edge(Var("agent-b"), Silence(), Membrane(threshold=0.5))
    agent_c = Edge(Var("agent-c"), Silence(), Membrane(threshold=0.5))

    # No seams between agents — just stacked via edges
    isolated = Edge(
        Edge(agent_a, agent_b, Membrane(threshold=0.9)),  # high barrier between
        agent_c,
        Membrane(threshold=0.9),
    )

    body = Seam(isolated, Var("mesh"))
    return Return("mesh", body)


def run_all() -> None:
    """Run all three agent mesh scenarios."""
    config = MESH_CONFIG

    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║         SELF-REGULATING AGENT MESH — Three Scenarios               ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    scenarios = [
        ("HEALTHY MESH — all agents reliable", healthy_mesh()),
        ("DEGRADED MESH — one agent unreliable, mesh self-heals", degraded_mesh()),
        ("FRAGMENTED MESH — agents isolated, no connections", fragmented_mesh()),
    ]

    results = []
    for name, prog in scenarios:
        reset_fresh()
        ev = Evaluator(config)
        result = ev.evaluate(prog)

        print(f"\n{'=' * 72}")
        print(f"  {name}")
        print(f"{'=' * 72}")
        print(ascii_trace(ev.history))

        last = ev.history[-1] if ev.history else None
        converged = False
        if len(ev.history) >= 5:
            converged = all(
                0.3 <= r.connectivity <= 0.7 and 0.2 <= r.exposure <= 0.6
                for r in ev.history[-5:]
            )

        results.append((name, ev.history, converged))

    # Comparison
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║                        COMPARISON                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    for name, hist, conv in results:
        last = hist[-1] if hist else None
        status = "CONVERGED" if conv else "UNSTABLE"
        binds = sum(1 for r in hist if r.bind_fired)
        veils = sum(1 for r in hist if r.veil_fired)
        print(f"  {name}")
        if last:
            print(f"    conn={last.connectivity:.3f}  expo={last.exposure:.3f}  "
                  f"steps={len(hist)}  BIND={binds}  VEIL={veils}  → {status}")
        print()


if __name__ == "__main__":
    run_all()
