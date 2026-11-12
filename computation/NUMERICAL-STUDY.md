# Numerical approximation of the uniform benchmark

The numerical study separates a finite-law transport problem from a discretized family of limiting kernels. Its reference is the independent uniform law on `[0,2]^3`, with `p=1/2`, `beta=1` and transport weights `(1,1,2)`.

The proved coefficient remains in `[13/64, 29/96]`. The limiting-kernel calculation gives a candidate near `0.23`. The finite-epsilon runs expose the mesh resolution needed to retain the quadratic nominal gain.

The [minimum-cost LP records](calculations/restricted-zero-study.json) give the following centered-family zeros at `U=3`. The final column evaluates the two threshold minima independently after solving the LP.

| Surface grid `n` | Normal grid `nu` | Candidate zero | Absolute paired-risk readback |
|---|---|---|---|
| 8 | 48 | 0.2292041774 | 3.4e-16 |
| 12 | 72 | 0.2310117554 | 2.3e-15 |
| 16 | 96 | 0.2318075456 | 8.4e-16 |
| 24 | 144 | 0.2322833871 | 1.3e-14 |
| 32 | 96 | 0.2324074378 | 1.7e-16 |

At fixed `n=16` and normal spacing `0.125`, expanding the window from `U=4` to `U=6` gives the same candidate, `0.2318262369`. These mesh and window differences are sensitivity measurements, not confidence intervals or proved error bounds.

## Finite-epsilon problem

Each marginal has `n` equally weighted midpoint atoms. The independent reference has `n^3` atoms. A target law is represented by its masses at the same lattice points, with all three marginal sums fixed to `1/n`.

Transport uses nonnegative flows on both orientations of every adjacent lattice edge. The cost of an edge in coordinate `i` is `2 gamma_i/n`. This representation has the exact weighted Manhattan transport cost on the finite lattice: every source-to-target shipment decomposes into shortest coordinate paths, and every feasible flow decomposes into paths and removable cycles. Intermediate nodes permit transshipment; target masses stay nonnegative. Thus the graph representation does not restrict the discrete transport plans.

For a fixed threshold `a` of loss A, the LP maximizes `ES_B - a - 2 E(A-a)_+`. A scalar LP variable represents `ES_B` and is bounded above by every B-threshold objective. It suffices to use the finitely many B loss values. The outer maximization enumerates every feasible A loss value. Enumeration retains asymmetric target laws and does not impose a common ES threshold.

We prune only thresholds with a scalar necessary transport cost above the budget. To raise the A median to `a`, at least the reference upper half must be brought above `a`. Its minimal scalar transport cost is the average of `(a-A)_+` over that half. The analogous lower-half formula handles downward shifts. Dividing by `||A||_{gamma,*}=1+epsilon` gives a lower bound on the original transport cost. Every retained threshold is solved; `threshold_stride=1` in all recorded experiments.

The LP results are global for these **discrete marginal laws**. Solver primal/dual gaps and constraint violations measure optimization error for that finite problem. They do not bound the error against the continuous uniform model.

For an independent check, `check_numerical_profiles.py` compares six graph solutions with a full source-by-target coupling LP on the two-point grid. It also evaluates both ES values directly from the returned target masses.

## Limiting-kernel calculation

The surface `x+y+z=3` is integrated by a square midpoint rule in `(x,y)`. The cells cut by `x+y=1` or `x+y=3` receive half weight; their boundary midpoint represents the half cell. The normal coordinate `u` has an independent midpoint grid on `[-U,U]`. The exact nominal constants are `g=3/8` and `J=5/32`.

For prescribed thresholds `(a,b)`, each source may stay fixed or choose one of six pure-coordinate moves. The normal target is either `b` or `a-H`, the two hinge breakpoints. Every coordinate projection has an auxiliary absolute-flux variable, so the budget includes both the displacement moment and the marginal-restoration penalty in (3.1).

The main mesh and window tables use `a=b=0`. Averaging a computed kernel with its central reflection gives a symmetric kernel of no greater cost. The code independently minimizes both resulting piecewise quadratic threshold objectives and reports the paired-risk readback. A separate minimum-cost LP finds the zero of this prescribed centered family directly. The threshold scan uses a bounded scalar search over `b` for each sampled `a`. Its action set changes with the thresholds, so it searches prescribed-threshold surrogates rather than evaluating one common kernel. It is a diagnostic without a proof of unimodality or an exhaustive outer global certificate.

The LP is globally solved within its finite action, quadrature and prescribed-threshold problem. A proof that this family attains the unrestricted maximum in (3.3), with uniform error control between threshold samples, is still needed to identify its zero with the unrestricted `s*`. The candidate estimate should therefore be read as a **restricted-kernel numerical estimate**.

## Error accounting

| Error | What is measured | What the record establishes |
|---|---|---|
| Optimization | LP primal/dual gap, primal residuals; direct ES evaluation; complete-coupling comparison | Finite LP optimality to the recorded floating-point tolerance |
| Surface and normal grids | Separate `n`, `nu` refinements | Numerical stability; no continuum error rate is asserted |
| Normal-window truncation | `U=2,3,4,6`, with fixed normal spacing | Window sensitivity at the stated mesh; no continuum truncation bound |
| Threshold and policy restriction | Sampled A thresholds, bounded scalar search over B; centered-kernel readback | Diagnostic evidence for the centered candidate; no unrestricted global certificate |
| Finite-epsilon discretization | Three independent lattice resolutions and four epsilon values | Underresolution becomes more severe as epsilon shrinks at fixed `n` |

The finite-epsilon experiment includes `epsilon = 0.2, 0.1, 0.05, 0.025`, `s = 0, 0.1, 0.25`, and `n = 8, 12, 16`. A finer `n=24` run at `epsilon=0.1` checks the grid trend. For example, the scaled nominal gain at `epsilon=0.1` is `-0.078125`, `-0.21604938`, and `-0.263671875` on the first three grids. The exact continuous value is `-0.3122895623`. At `n=16`, the discrete nominal value at `epsilon=0.025` is zero, whereas the exact continuous value is `-0.3124869710`. These results show a lost quadratic signal, so this run does not establish convergence to `F`.

The exact nominal comparator follows by integrating the three-uniform convolution. For widths `L=(2(1+epsilon),2(1-epsilon),2)`, the lower hinge expectation at the symmetry threshold 3 is

`sum_{S subset {1,2,3}} (-1)^|S| (3-sum_{i in S}L_i)_+^4 / (24 L_1 L_2 L_3)`.

Writing this expectation as `H(epsilon)`, the paired nominal ES difference is `D_epsilon(0)=2*(H(0)-H(epsilon))`.

## Reproduce

From `computation/`:

```bash
python -m pip install -r requirements.txt -r numerical-requirements.txt
python code/check_numerical_profiles.py
python code/run_numerical_study.py finite
python code/run_numerical_study.py window
python code/run_numerical_study.py mesh
python code/run_numerical_study.py zero
python code/run_numerical_study.py readback
python code/scan_thresholds.py
python code/numerical_profiles.py zero --n 16 --nu 96 --U 3
python code/numerical_profiles.py finite --n 24 --epsilon .1 --s 0 .1 .25 --output calculations/finite-n24-e01.json
python code/verify_numerical_study.py
```

The full study is separate from the original analytical-figure runner. The small independent checks and record verification run in CI; full optimization runs retain partial JSON records after each solved instance. The [verification record](audit/NUMERICAL-VERIFICATION.json) binds data to source hashes and reports the observed gaps and readback differences. The numerical optimizer is SciPy 1.18.1's HiGHS interface. Its [official documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html) describes solver status, primal residuals and dual marginals.
