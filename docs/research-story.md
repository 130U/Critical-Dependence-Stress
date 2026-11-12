# From diversification to a measurable failure boundary

**How much dependence stress does it take to overturn a portfolio improvement?**

The paper turns this question into a variational problem and answers it asymptotically. Along the way a concrete reallocation decision meets optimal transport, the geometry of the tail, marginal conservation and a continuous flow duality. The [paper](../paper/paper.pdf) has the proofs; this page explains how the problem and the method took shape.

## Choosing the question

I started in model-free pricing and martingale optimal transport and then read more widely in dependence uncertainty and risk aggregation. I was looking for a financial decision whose answer had to be structural: a boundary that can be measured, a reason for where it sits, and results that hold beyond one numerical example.

The fixed-marginal transport and sensitivity literature narrowed the target. Its tools describe the worst aggregate risk and the first response to a small model perturbation. The question I wanted answered concerns a specific action: once a reallocation has improved Expected Shortfall under a reference model, how far must dependence move before that advantage is gone?

The modeling choice that mattered most was to compare both portfolios under **the same stressed law**:

$$
\sup_P\{ES_p^P(B)-ES_p^P(A_\varepsilon)\}.
$$

Each ES keeps its own optimizing threshold. The comparison then tests one adverse scenario against an actual decision. The background book stays in the model although its holding does not change, because it determines which joint states enter the tail.

## The mathematical intuition

Consider a transfer from holdings $(1+\varepsilon,1-\varepsilon)$ to $(1,1)$ with the background holding fixed. Under the reference symmetry the first-order change in risk vanishes, and the nominal gain is of order $\varepsilon^2$.

The adverse movement that matters lives near the tail boundary. A layer of width $O(\varepsilon)$ holds $O(\varepsilon)$ of mass, and moving that mass a distance $O(\varepsilon)$ costs $O(\varepsilon^2)$ in transport and changes risk by the same order. Hence the critical scaling $\rho=s\varepsilon^2$.

Three quantities have to survive the rescaling: the local displacement, the cost of restoring every marginal, and the two separately optimized ES thresholds. A move that is cheap locally can run out of matching capacity. From then on marginal conservation makes further stress more expensive, even when the initial slope is attained exactly.

The construction follows this geometry: rescale the tail layer, represent displacement by kernels, and restore the marginals with coordinatewise quantile maps. The limiting transport energy keeps the full projected compensation cost. The resulting risk profile is strictly increasing, so its unique zero is the critical reversal coefficient.

## How the work developed

| Stage | What I did | What went into the paper |
|---|---|---|
| 1 | Compared robust pricing, dependence uncertainty and neighboring financial questions. | A focus on decisions that have a measurable stress budget. |
| 2 | Traced the existing transport and tail-risk results before settling on a contribution. | The paired ES comparison under fixed marginals and one common law. |
| 3 | Matched the trade scale to the transport scale and worked out marginal restoration. | The critical risk profile and its variational construction. |
| 4 | Asked when local efficiency can last all the way to reversal. | The zero-premium classification and the projection-capacity mechanism. |
| 5 | Tied the mechanism to analytical examples and to flow duality. | Explicit bounds, optimal shares and sensitivity formulas. |
| 6 | Reorganized the proofs around the question each construction answers. | One continuous argument, with the mathematical and computational material that supports it. |

## What the theory makes measurable

In the paper's exchangeable box model with a positive continuous density, Theorems 3.1 and 3.3 give the limiting profile and the leading coefficient that a tie and a strict reversal share. Theorem 4.2 says exactly when marginal restoration adds no premium: the background direction has to be among the cheapest effective displacement directions.

In the independent uniform benchmark with weights $(1,1,2)$, Corollary 5.2 proves that the asymptotic reversal budget is **at least 30% above the initial-slope prediction**. Proposition 5.3 gives an exact dependence family along which the required background share rises while the absolute budget sensitivity falls.

For reverse stress testing this means a distance to decision reversal that comes with its mechanism: what uses up the budget, and what the background book has to do with it.
