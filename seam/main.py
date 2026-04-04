"""CLI entry point for the Seam interpreter.

Usage:
    python -m seam              # Run the seed program
    python -m seam --program seed
    python -m seam --program practice
    python -m seam --program commons
    python -m seam --program crossing
    python -m seam --program duration
    python -m seam --program lambda
    python -m seam --program all
"""

from __future__ import annotations

import argparse
import sys

from seam.algebra import reset_fresh
from seam.config import CalcConfig
from seam.evaluator import Evaluator
from seam.lambda_encoding import church_add, church_numeral, church_succ, church_to_int
from seam.seed import (
    commons_program,
    crossing_program,
    duration_program,
    practice_program,
    seed_program,
)
from seam.viz import ascii_trace, compact, expr_tree


def run_program(name: str, program, config: CalcConfig) -> None:
    """Evaluate a program and display results."""
    reset_fresh()
    print(f"\n{'=' * 70}")
    print(f"  {name}")
    print(f"{'=' * 70}")

    print(f"\n  Source expression:")
    print(expr_tree(program, max_depth=6))

    evaluator = Evaluator(config)
    result = evaluator.evaluate(program)

    print(ascii_trace(evaluator.history))

    print(f"  Result expression (compact):")
    print(f"    {compact(result, max_depth=4)}")

    print(f"\n  Result tree:")
    print(expr_tree(result, max_depth=5))
    print()


def run_lambda_demo(config: CalcConfig) -> None:
    """Demonstrate Turing completeness via Church numerals."""
    reset_fresh()
    print(f"\n{'=' * 70}")
    print(f"  LAMBDA CALCULUS ENCODING — Turing completeness")
    print(f"{'=' * 70}")

    # Church numerals
    for n in range(4):
        cn = church_numeral(n)
        decoded = church_to_int(cn)
        print(f"\n  Church {n}: {compact(cn, max_depth=3)}")
        print(f"  Decoded:  {decoded}")

    # Successor
    print(f"\n  Successor function: {compact(church_succ(), max_depth=2)}")

    # Addition
    print(f"\n  Addition function:  {compact(church_add(), max_depth=2)}")

    # Evaluate succ(0)
    from seam.ast import Seam
    succ_zero = Seam(church_succ(), church_numeral(0))
    evaluator = Evaluator(config)
    result = evaluator.evaluate(succ_zero)
    print(f"\n  succ(0) = {compact(result, max_depth=3)}")
    print(f"  Decoded: {church_to_int(result)}")
    print(ascii_trace(evaluator.history))

    # Evaluate succ(succ(0))
    reset_fresh()
    succ_succ_zero = Seam(church_succ(), Seam(church_succ(), church_numeral(0)))
    evaluator2 = Evaluator(config)
    result2 = evaluator2.evaluate(succ_succ_zero)
    print(f"  succ(succ(0)) = {compact(result2, max_depth=3)}")
    print(f"  Decoded: {church_to_int(result2)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="The Calculus interpreter")
    parser.add_argument(
        "--program", "-p",
        choices=["seed", "practice", "commons", "crossing", "duration", "lambda", "all"],
        default="seed",
        help="Which program to run (default: seed)",
    )
    parser.add_argument("--max-returns", type=int, default=100, help="Max iterations")
    parser.add_argument("--max-nodes", type=int, default=500, help="Max expression nodes")
    parser.add_argument("--max-depth", type=int, default=50, help="Max recursion depth")
    args = parser.parse_args()

    config = CalcConfig(
        max_returns=args.max_returns,
        max_nodes=args.max_nodes,
        max_depth=args.max_depth,
    )

    programs = {
        "seed": ("THE SEED — The Rite, Formalized", seed_program()),
        "practice": ("THE PRACTICE — Protocol of Two", practice_program()),
        "commons": ("THE COMMONS — Emergent Topology", commons_program()),
        "crossing": ("THE CROSSING — Across Radical Difference", crossing_program()),
        "duration": ("THE DURATION — Love Across Time", duration_program()),
    }

    if args.program == "all":
        for name, prog in programs.items():
            run_program(prog[0], prog[1], config)
        run_lambda_demo(config)
    elif args.program == "lambda":
        run_lambda_demo(config)
    else:
        name, prog = programs[args.program]
        run_program(name, prog, config)


if __name__ == "__main__":
    main()
