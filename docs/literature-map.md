# The literature behind the question

The project brings together risk aggregation, reverse stress testing, Wasserstein sensitivity, and capacity-constrained transport. The reading strategy was to identify what each framework already explains, then specify the additional object needed for a portfolio decision: **the critical dependence budget for reversing a paired ES comparison**.

The sources below are selected entry points. The [paper](../paper/paper.pdf) contains the full bibliography and mathematical comparisons.

| Research strand | Primary source | What it contributes to the problem |
|---|---|---|
| Fixed-marginal dependence uncertainty | Eckstein, Kupper & Pohl, [*Robust risk aggregation with neural networks*](https://onlinelibrary.wiley.com/doi/full/10.1111/mafi.12280), 2020 | A transport neighborhood with prescribed marginals, strong duality, and numerical risk aggregation. This supplies the established ambiguity-set framework. |
| Local model sensitivity | Bartl, Drapeau, Obłój & Wiesel, [*Sensitivity analysis of Wasserstein distributionally robust optimization problems*](https://arxiv.org/html/2006.12022v2), 2021 | First-order corrections to robust values and optimizers. This makes the attainable initial slope a natural benchmark for the reversal budget. |
| Reverse sensitivity testing | Pesenti, Millossovich & Tsanakas, [*Reverse sensitivity testing: What does it take to break the model?*](https://openaccess.city.ac.uk/id/eprint/18896/), 2019 journal article; linked author version | Start with a specified adverse output and find a nearby stressed model. Here, the target output is a reversal of the ranking between two allocations. |
| Diversification and symmetry | Liu & Liu, [*Portfolio Diversification and Concentration under Dependence Uncertainty: A Majorization Approach*](https://arxiv.org/html/2609.04496v1), 2026 preprint | Relates diversification, exchangeability, majorization, and dependence ambiguity. It makes the distinction between reference symmetry and symmetry of every admissible stress particularly useful. |
| Higher-order robustness | Fiechtner & Blanchet, [*Wasserstein Distributionally Robust Regret Optimization*](https://arxiv.org/html/2504.10796v5), 2026 revision | Develops a second-order regime when a unique empirical-risk minimizer makes first-order regret sensitivity vanish. It provides a nearby decision-comparison problem. |
| Higher-order transport expansions | Sauldubois, [*Higher-Order Sensitivity Analysis of Wasserstein and Adapted Wasserstein Distributionally Robust Optimization Problems*](https://arxiv.org/html/2609.25345v1), 2026 preprint | Studies higher-order expansions, including adapted transport and martingale constraints. The present paper instead tracks the full rescaled profile over the budget interval needed for reversal. |
| Capacity and dual potentials | Korman, McCann & Seis, [*Dual potentials for capacity constrained optimal transport*](https://arxiv.org/abs/1307.7774), 2015 journal article | Provides a mathematical foundation for treating capacity and marginal constraints through dual potentials. The paper's projected flow problem measures how much efficient displacement can be assigned to traded coordinates. |

## The question that connects them

The resulting object is

$$
F(s)=\lim_{\varepsilon\downarrow0}\varepsilon^{-2}
\sup_{\substack{P_i=(P_0)_i\\W_\gamma(P,P_0)\le s\varepsilon^2}}
\left\{ES_p^P(B)-ES_p^P(B+\varepsilon H)\right\}.
$$

Its unique zero locates the leading reversal budget. Keeping the entire profile preserves the cost of full marginal restoration and the adjustment of both ES thresholds. This connects local sensitivity to a finite question in the rescaled budget: whether the initially efficient stress can continue until the nominal gain is exhausted.

The proof then links this question to geometry. Coordinate projections constrain how adverse displacements can be matched; background displacement supplies an alternative channel. The zero-premium classification and projected flow duality make that mechanism explicit in the paper's exchangeable box model.
