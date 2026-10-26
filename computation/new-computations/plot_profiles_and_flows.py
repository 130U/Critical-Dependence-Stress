"""Figures evaluated from proved formulas, not from an optimizer of F.

Run: python -X utf8 new-computations/plot_profiles_and_flows.py
Install the packages listed in code/requirements.txt first.
"""
from pathlib import Path
import csv
import hashlib
import json
ROOT = Path(__file__).resolve().parents[1]
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

HERE = ROOT / "new-computations"
OUT = ROOT / "source/en/figures"
OUT.mkdir(parents=True, exist_ok=True)
HERE.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({
    "font.family": "DejaVu Serif", "font.size": 9,
    "mathtext.fontset": "dejavuserif", "axes.linewidth": 0.7,
    "lines.linewidth": 1.4, "pdf.fonttype": 42, "ps.fonttype": 42,
    "savefig.dpi": 220,
})


def integral(fn, left=0., right=1., n=64):
    nodes, weights = np.polynomial.legendre.leggauss(n)
    x = (left+right)/2 + (right-left)*nodes/2
    return float(np.dot(weights, fn(x))*(right-left)/2)


# The manuscript uses a fixed rational midpoint amplitude and the
# already proved pure-first-coordinate comparison kernel.
J, S0, U, C = 5/32, 1/96, 29/96, 13/64
fixed_amplitude = 1/2
relative_premium = C/J-1
small_threshold_slope = 4/3
assert abs(relative_premium-3/10) < 2e-16
s = np.unique(np.r_[np.linspace(0, U, 1201), S0, J, C])
lower = np.where(s <= S0, -5/16+2*s, s-U)
threshold_upper = np.maximum(small_threshold_slope*(s-C), 2*s-11/16)
upper = np.minimum(-5/16+2*s, small_threshold_slope*(s-C))
assert np.max(np.abs(upper-np.minimum(-5/16+2*s,threshold_upper))) < 2e-16
assert np.min(upper-lower) > -2e-14
assert np.max(np.abs(upper[s <= S0]-lower[s <= S0])) < 2e-14
assert upper[np.argmin(abs(s-C))] == 0.
assert abs(lower[-1]) < 1e-14
with (HERE / "profile-envelopes.csv").open("w", newline="", encoding="utf-8") as fh:
    writer = csv.writer(fh)
    writer.writerow(["budget_s", "attainable_lower_F", "rigorous_upper_F",
                     "initial_slope_extrapolation"])
    writer.writerows(zip(s, lower, upper, -5/16+2*s))

fig, ax = plt.subplots(figsize=(6.6, 3.8), layout="constrained")
ax.fill_between(s, lower, upper, color="#b9cedc", alpha=.65,
                label=r"Proved range for $F(s)$")
ax.plot(s, lower, color="#245884", label="Attainable lower profile")
ax.plot(s, upper, color="#111111", label="Upper profile")
ax.plot([0, .32], [-5/16, -5/16+2*.32], color="#9a541c",
        ls="--", lw=1.2, label="Initial-slope extrapolation")
ax.axhline(0, color="#555555", lw=.7)
ax.axvspan(C, U, color="#dddddd", alpha=.55, zorder=-1)
ax.plot([C, U], [0, 0], color="#222222", lw=3)
ax.scatter([J, C, U], [0, 0, 0], s=15, color=["#9a541c", "#222222", "#222222"], zorder=4)
ax.annotate(r"$J=5/32$", (J, 0), xytext=(J-.025, .025), fontsize=8,
            arrowprops={"arrowstyle":"-", "lw":.5, "color":"#555555"})
ax.annotate(r"$13/64\leq s^*\leq 29/96$", ((C+U)/2, 0),
            xytext=(.155, -.105), fontsize=9,
            bbox={"facecolor":"white", "edgecolor":"none", "alpha":.92,
                  "pad":1.6},
            arrowprops={"arrowstyle":"-", "lw":.6, "color":"#555555"})
ax.plot([0, S0], [-5/16, -5/16+2*S0], color="#177051", lw=2.5,
        zorder=5)
ax.annotate("Exact initial segment", (S0/2, -5/16+S0),
            xytext=(.035, -.275), fontsize=8,
            arrowprops={"arrowstyle":"-", "lw":.6, "color":"#555555"})
ax.set(xlim=(0, .32), ylim=(-.33, .16),
       xlabel=r"Rescaled stress budget $s$", ylabel="Rescaled paired risk")
ax.xaxis.set_major_locator(MultipleLocator(.05))
ax.yaxis.set_major_locator(MultipleLocator(.1))
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="upper left", fontsize=7.4, frameon=False)
zoom = ax.inset_axes([.575, .065, .385, .30])
zoom_s = np.unique(np.r_[np.linspace(0, .02, 241), S0])
zoom_lower = np.where(zoom_s <= S0, -5/16+2*zoom_s,
                      zoom_s-U)
zoom_upper = np.minimum(-5/16+2*zoom_s,
                       np.maximum(small_threshold_slope*(zoom_s-C),
                                  2*zoom_s-11/16))
zoom.fill_between(zoom_s, zoom_lower, zoom_upper,
                  color="#b9cedc", alpha=.65)
zoom.plot(zoom_s, zoom_lower, color="#245884", lw=1)
zoom.plot(zoom_s, zoom_upper, color="#111111", lw=1)
zoom.plot([0, S0], [-5/16, -5/16+2*S0],
          color="#177051", lw=2.4, zorder=5)
zoom.axvline(S0, color="#177051", lw=.6, ls=":")
zoom.set(xlim=(0, .02), ylim=(-.316, -.270),
         xticks=[0, .01, .02], yticks=[-.31, -.29, -.27])
zoom.tick_params(labelsize=6.5, pad=2, length=2)
zoom.set_title(r"Initial range: $s_{\rm lin}=1/96$", fontsize=7.5, pad=3)
zoom.spines[["top", "right"]].set_visible(False)
for ext in ("pdf", "png", "svg"):
    fig.savefig(OUT / f"budget-comparison.{ext}")
plt.close(fig)


def qdensity(x, y, dependent=False):
    q = (y-x)**2/16
    if dependent:
        q = q*(1-(x+y-2)**2/4)
    return q


def demand(x, dependent=False):
    r = np.maximum(2*np.asarray(x)-1, 0)
    if dependent:
        return r**3*(30+5*r-r*r)/1920
    return r**3/48


def capacity(x, dependent=False):
    # q is polynomial; 8-node Gauss integrates each section exactly up to
    # floating-point arithmetic. The limits are 2-x and 2.
    x = np.asarray(x)
    nodes, weights = np.polynomial.legendre.leggauss(8)
    y = (2-x/2)[..., None]+(x/2)[..., None]*nodes
    return np.sum(qdensity(x[..., None], y, dependent)*weights, axis=-1)*x/2


def ratio(x, dependent=False):
    x = np.asarray(x)
    cap = capacity(x, dependent)
    return np.divide(demand(x, dependent), cap, out=np.zeros_like(x),
                     where=cap > 0)


n = 500
axis = (np.arange(n)+.5)*2/n
xx, yy = np.meshgrid(axis, axis)
domain = (xx < yy) & (xx+yy > 1) & (xx+yy < 3)
same_minus = domain & (yy < 1)
same_plus = domain & (xx > 1)
ea = domain & (xx < 1) & (yy > 1) & (xx+yy > 2)
eb = domain & (xx < 1) & (yy > 1) & (xx+yy <= 2)
flow_records = {}
fig, axes = plt.subplots(2, 3, figsize=(6.6, 4.6), sharex=True,
                         sharey=True, layout="constrained")
for row, (name, dep, exact_j, exact_a) in enumerate([
    ("U", False, 5/32, 13/15), ("D", True, 143/960, 379/429)
]):
    a = np.zeros_like(xx)
    b = np.zeros_like(xx)
    b[same_minus] = 1
    a[same_plus] = 1
    a[ea] = ratio(xx[ea], dep)
    b[eb] = ratio(2-yy[eb], dep)
    c = 1-a-b
    assert np.min(c[domain]) > -2e-14
    assert np.max((a+b)[domain]) < 1+2e-14
    # Independent scalar quadrature of the exact same-side mass.
    same_mass = integral(lambda x: demand(x, dep), .5, 1, n=64)
    share = 1-8*same_mass/exact_j
    assert abs(share-exact_a) < 1e-14
    # Diagnostic midpoint integration of the plotted fields; this check is
    # approximate and is not used to prove feasibility or optimality.
    q = qdensity(xx, yy, dep)
    plotted_mass = float(np.sum(c[domain]*q[domain])*(2/n)**2)
    plotted_share = 2*plotted_mass/exact_j
    flow_records[name] = {
        "J_exact": "5/32" if not dep else "143/960",
        "a_plus_exact": "13/15" if not dep else "379/429",
        "same_side_mass_quadrature": same_mass,
        "a_plus_section_quadrature": share,
        "a_plus_midpoint_heatmap_diagnostic": plotted_share,
        "heatmap_resolution_each_axis": n,
        "max_share_sum_excess": float(np.max((a+b)[domain]-1)),
    }
    np.savez_compressed(HERE / f"flow-shares-{name}.npz",
                        coordinate_axis=axis, domain=domain,
                        a=a, b=b, background=c)
    for col, (field, title) in enumerate([
        (a, r"First coordinate $a$"),
        (b, r"Second coordinate $b$"),
        (c, r"Background $1-a-b$")
    ]):
        ax = axes[row, col]
        shown = np.where(domain, field, np.nan)
        im = ax.imshow(shown, origin="lower", extent=(0, 2, 0, 2),
                       vmin=0, vmax=1, cmap="cividis", interpolation="nearest",
                       aspect="equal", rasterized=True)
        if row == 0:
            ax.set_title(title, fontsize=9)
        ax.set_xticks([0, 1, 2])
        ax.set_yticks([0, 1, 2])
        if row == 1:
            ax.set_xlabel(r"$x$")
        if col == 0:
            ax.set_ylabel(name+"\n"+r"$y$")
        ax.spines[["top", "right"]].set_visible(False)
fig.colorbar(im, ax=axes, shrink=.87, pad=.02, label="Share of normal displacement")
for ext in ("pdf", "png", "svg"):
    fig.savefig(OUT / f"optimal-flow-shares.{ext}")
plt.close(fig)

report = {
    "scope": "Evaluation of proved piecewise-linear risk envelopes and explicit optimal boundary-flow fields. No full F optimization or finite-trade worst-case solver.",
    "numpy_version": np.__version__, "matplotlib_version": matplotlib.__version__,
    "critical_interval_lower_exact": "13/64",
    "critical_interval_upper_exact": "29/96",
    "fixed_midpoint_amplitude_exact": "1/2",
    "guaranteed_relative_premium_exact": "3/10",
    "lower_envelope": "2s-5/16 on [0,1/96]; s-29/96 on [1/96,29/96]",
    "upper_envelope": "min(2s-5/16,4s/3-13/48) on [0,29/96]",
    "all_threshold_check": "The large-threshold branch 2s-11/16 is no larger than 4s/3-13/48 until s=5/8, beyond the plotted interval.",
    "figure3_evaluation": "Exact analytical formulas evaluated in floating-point for rendering; no quadrature.",
    "inset_budget_interval": [0, .02],
    "nominal_J": J, "exact_initial_segment_endpoint": S0,
    "profile_samples": len(s),
    "minimum_upper_minus_lower": float(np.min(upper-lower)),
    "flow_checks": flow_records,
}
outputs = [HERE / "profile-envelopes.csv", HERE / "flow-shares-U.npz", HERE / "flow-shares-D.npz"]
outputs += [OUT / f"{name}.{ext}" for name in ("budget-comparison", "optimal-flow-shares")
            for ext in ("pdf", "png", "svg")]
report["sha256"] = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in outputs}
(HERE / "COMPUTATION_REPORT.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k != "sha256"}, indent=2))
