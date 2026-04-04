# Paper Outline: Homeostatic Evaluation in a Relational Calculus

## Title Options

1. "Seam: A Term-Rewriting Calculus with Homeostatic Evaluation"
2. "Homeostatic Evaluation: When Computation Regulates Itself"
3. "BIND and VEIL: Structural Self-Regulation in a Relational Calculus"

## Target Venue

- Workshop paper (4-6 pages): ICML workshop on formal methods for AI safety
- Alignment Forum post: broader audience, less formal
- Short paper: POPL or OOPSLA (programming languages, if we get the type system)

## Abstract (draft)

We introduce Seam, a term-rewriting calculus whose evaluator maintains
homeostatic stability rather than reducing to normal form. The evaluator
measures structural metrics (connectivity, exposure) on the expression tree
and applies regulatory transformations (BIND, VEIL) to stay within a target
band. We prove that BIND monotonically increases connectivity, VEIL
monotonically decreases exposure, and the two operations are metrically
confluent. We demonstrate the calculus on AI alignment scenarios where
sycophantic and adversarial structures produce limit cycles while balanced
structures converge, and show the result is robust across a range of
parameter values. We provide a conversation quality monitor as a grounding
application.

## Structure

### 1. Introduction (1 page)
- The problem: alignment as optimization vs. alignment as homeostasis
- Cite prior work (arXiv:2410.00081, cybernetics tradition)
- Our contribution: a formal calculus where evaluation IS homeostasis
- What's new: the cybernetic feedback loop (no existing calculus has this)

### 2. The Calculus (1.5 pages)
- Primitives: silence, seam, edge, return
- Formation rules
- Seam laws (commutative monoid)
- Edge semantics (parameterized membranes, BreathMembrane)
- Metrics: connectivity, exposure (defined on AST)
- Evaluation: μ-return with BIND/VEIL regulation

### 3. Formal Properties (1 page)
- Theorem 1: BIND monotonicity
- Theorem 2: VEIL monotonicity
- Theorem 3: BIND/VEIL orthogonality
- Theorem 4: Termination
- Theorem 5: Sufficient convergence conditions
- Theorem 6: Metric confluence

### 4. Alignment Scenarios (1 page)
- Three archetypes: sycophantic, adversarial, balanced
- Convergence results + sensitivity analysis
- Limit cycle characterization (period depends on band width)
- The corrected claim: non-convergence is a band-width effect,
  not structural impossibility

### 5. Grounding: Conversation Monitor (0.5 pages)
- Encoding: turn metrics → structural archetypes
- Results on 5 synthetic patterns
- Limitations: aggregate, not trajectory

### 6. Related Work (0.5 pages)
- P-systems (membranes without homeostatic coupling)
- Session types (bilateral without structural metrics)
- Cybernetics (homeostasis without formal calculus)
- Homeostatic alignment benchmarks (thesis without mechanism)

### 7. Conclusion and Future Work
- What's proven: 6 theorems, tested
- What's open: tight convergence bounds, trajectory encoding, type system
- The broader claim: computation can regulate itself

## Honest Assessment of Paper Readiness

**Strong:**
- 6 proven theorems with tests
- Clean implementation (122 tests, resource-safe)
- Sensitivity analysis
- Honest about limitations

**Weak:**
- Convergence conditions are sufficient, not necessary
- Grounding example is aggregate-based, not trajectory-sensitive
- No comparison with actual LLM behavior data
- The "so what" for practitioners is still unclear

**Recommendation:** Submit as a workshop paper or Alignment Forum post first.
The formal results are solid but the grounding needs more work before a
top venue.
