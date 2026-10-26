# From diversification to a measurable failure boundary

**How much dependence stress does it take to overturn a portfolio improvement?**

This project turns that question into a variational problem with a precise asymptotic answer. It connects a concrete reallocation decision to optimal transport, tail geometry, marginal conservation, and continuous flow duality. The [paper](../paper/paper.pdf) develops the proofs; this page explains how the problem and method took shape.

## Choosing the question

The research began with model-free pricing and martingale optimal transport, then broadened into dependence uncertainty and risk aggregation. The selection criterion was a financial decision that required a structural mathematical answer: a measurable boundary, an explanation of what determines it, and results extending beyond a numerical example.

Reading the fixed-marginal transport and sensitivity literature sharpened the target. Existing tools could describe worst aggregate risk and the first response to a small model perturbation. The useful next question was about a specific action: after a reallocation improves Expected Shortfall under a reference model, how far must dependence move before that advantage disappears?

The decisive modeling choice was to compare both portfolios under **the same stressed law**:

$$
\sup_P\{ES_p^P(B)-ES_p^P(A_\varepsilon)\}.
$$

Each ES keeps its own optimizing threshold. This tests a common adverse scenario for an actual decision. The unchanged background book remains in the model because it determines which joint states enter the tail.

## The mathematical intuition

Consider a transfer from holdings $(1+\varepsilon,1-\varepsilon)$ to $(1,1)$, keeping the background holding fixed. Under the reference symmetry, the first-order risk change vanishes, leaving a nominal gain of order $\varepsilon^2$.

The corresponding adverse movement lives near the tail boundary. A layer of width $O(\varepsilon)$ contains $O(\varepsilon)$ mass; moving it a distance $O(\varepsilon)$ produces an $O(\varepsilon^2)$ transport cost and risk effect. This identifies the critical scaling $\rho=s\varepsilon^2$.

Three quantities must survive this rescaling: local displacement, the cost of restoring every marginal, and the separately optimized ES thresholds. A locally cheap move can exhaust its matching capacity. Marginal conservation then makes continued stress more expensive, even when the initial slope is exactly attainable.

The construction follows this geometry. Rescale the tail layer, represent displacement by kernels, and use coordinatewise quantile maps to restore the marginals. The limiting transport energy retains the full projected compensation cost. Strict growth of the resulting risk profile then turns its unique zero into the critical reversal coefficient.

## How the work developed

| Stage | Research decision | Result carried into the paper |
|---|---|---|
| 1. Explore | Compare robust pricing, dependence uncertainty, and adjacent financial questions. | A focus on decisions with a measurable stress budget. |
| 2. Position | Trace existing transport and tail-risk results before selecting the contribution. | A paired ES comparison under fixed marginals and one common law. |
| 3. Build | Match the trade scale to the transport scale and resolve marginal restoration. | The critical risk profile and its variational construction. |
| 4. Explain | Determine when local efficiency can persist. | A zero-premium classification and a projection-capacity mechanism. |
| 5. Quantify | Connect the mechanism to analytical examples and flow duality. | Explicit bounds, optimal shares, and sensitivity formulas. |
| 6. Refine | Organize proofs around the questions each construction answers. | A continuous argument supported by mathematical and computational material. |

## What the theory makes measurable

For the paper's positive continuous exchangeable box model, Theorems 3.1 and 3.3 establish the limiting profile and the common leading coefficient for a tie and a strict reversal. Theorem 4.2 characterizes exactly when marginal restoration adds no premium: the background direction must be among the cheapest effective displacement directions.

In the independent uniform benchmark with weights $(1,1,2)$, Corollary 5.2 proves that the asymptotic reversal budget is **at least 30% above the initial-slope prediction**. Proposition 5.3 gives an exact dependence family where the required background share rises while the absolute budget sensitivity falls.

These results give reverse stress testing an interpretable output: a distance to decision reversal, the mechanism consuming that budget, and the role of the background book.
