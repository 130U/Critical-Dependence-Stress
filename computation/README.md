# Computational companion

This companion reproduces the four manuscript figures and the exact calculations behind three results: the **30% critical-budget premium**, the **$1/96$ initial linear segment** and the **86.67% to 88.34% background-share comparison**.

All inputs are analytical formulas and synthetic grids, so a run needs no external data and no network access.

## Run

From this directory, in Python 3.13:

```bash
python -m pip install -r requirements.txt
python code/run_all.py
```

For the exact scalar checks using only the Python standard library:

```bash
python new-computations/check_simple_example.py
```

The tested environment uses CPython 3.13.12, NumPy 2.5.4, Matplotlib 3.11.2 and SymPy 1.14.0. The full environment snapshot is in [requirements-lock.txt](requirements-lock.txt).

## Outputs

| Output | What it shows |
|---|---|
| [Budget comparison](source/en/figures/budget-comparison.png) | Proved upper and attainable lower stress profiles; exact initial segment; rigorous critical interval. |
| [Optimal flow shares](source/en/figures/optimal-flow-shares.png) | Explicit optimal displacement allocation for independent and dependent reference laws. |
| [Tail-layer mechanism](source/en/figures/tail-layer-repair.png) | Schematic local transport and marginal compensation. |
| [Corner geometry](source/en/figures/corner-capacity.png) | The quadratic-demand versus quartic-capacity obstruction. |
| [Profile table](new-computations/profile-envelopes.csv) | 1,204 evaluations of the analytical envelope formulas. |
| [Parameter-family checks](new-computations/PARAMETER_FAMILY_CHECK.json) | Exact symbolic marginal, covariance, section-moment and sensitivity identities. |
| [Scalar checks](new-computations/SIMPLE_EXAMPLE_CHECKS.json) | Exact rational verification of the displayed constants. |

Figures are also available as PDF and SVG in `source/en/figures/`. The flow archives `new-computations/flow-shares-U.npz` and `flow-shares-D.npz` contain the 500-by-500 evaluation grids.

## Verification

The public companion was run on **12 November 2026**. All three entry-point stages passed. The output comparison passed all scientific checks and matched all four reference PNGs exactly. See [execution status](audit/RUN_ALL.json), [output comparisons](audit/OUTPUT_READBACK.json), and [calculation provenance](audit/SOURCE_PROVENANCE.json).

The runner recomputes the figures and formulas before comparing them with the frozen reference. It checks exact scalar expressions, numerical array contents and the profile CSV; PNG identity is recorded separately because fonts and platforms can affect rendering. The 500-by-500 midpoint sums are numerical diagnostics of analytically established flow formulas. The continuous existence, conservation, optimality and critical-budget statements are proved in the [paper](../paper/paper.pdf).

The flow evaluator uses the exact integrated section polynomials in `r = 1-x` and forms cubes by multiplication. Symbolic integration verifies both polynomial identities; exact rational arithmetic checks the plotting coordinates. The [formula checks](audit/FLOW-FORMULA-CHECK.json) record these identities. Array acceptance requires exact byte hashes. CI exercises native and baseline NumPy CPU dispatch.

The budget plot shows the proved envelopes. It is not a numerical solution of the full profile, and the source keeps the analytical and the computational roles apart. Later runs overwrite the generated figures, data and execution reports.

## Numerical profile study

The [numerical study](NUMERICAL-STUDY.md) adds finite-epsilon transport optimizations and a discretized family of limiting kernels. It records solver gaps, mesh refinement, normal-window sensitivity and separate ES-threshold checks. The limiting calculation gives a restricted-kernel candidate near `0.23`; for the unrestricted coefficient the proved interval above still stands. The finite-epsilon runs are kept as recorded, including the loss of the quadratic signal on coarse grids and the cases that have not converged.

Install the optional optimizer with `python -m pip install -r numerical-requirements.txt`, then run `python code/check_numerical_profiles.py` for the small independent checks. The full study and output files are described in its methods note.
