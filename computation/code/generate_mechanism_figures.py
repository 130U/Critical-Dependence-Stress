"""Generate Figures 1 and 2 from the manuscript's schematic constructions.

Figure 1 illustrates a thin tail layer and cancellation of projected CDF
errors. Figure 2 plots one corner geometry with the analytic order bounds.
Neither figure is an empirical plot or an optimized stress distribution.
Run from any directory with: python code/generate_mechanism_figures.py
"""
from pathlib import Path
import json
import hashlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source/en/figures"
DATA = ROOT / "calculations"
OUT.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Serif", "font.size":10,
    "mathtext.fontset":"dejavuserif", "axes.linewidth":1.0,
    "lines.linewidth":1.3, "pdf.fonttype":42, "ps.fonttype":42,
    "savefig.dpi":180})
BLUE = "#245884"
ORANGE = "#9a541c"
GRAY = "#555555"

def save(fig, name):
    for ext in ("pdf", "svg", "png"):
        fig.savefig(OUT / f"{name}.{ext}", bbox_inches="tight", pad_inches=.07)
    plt.close(fig)


fig,axs=plt.subplots(1,2,figsize=(7.1,2.65),layout='constrained')
ax=axs[0]
ax.set_xlim(0,1);ax.set_ylim(-.5,.5)
ax.axhspan(-.13,.13,color=BLUE,alpha=.13)
ax.axhline(0,color=BLUE,linewidth=1.3)
ax.text(.03,.025,r'$B=v$',color=BLUE)
for x,y,dx,dy in [(.22,-.07,.13,.2),(.47,.07,.15,-.23),(.7,-.02,.12,.18)]:
    ax.plot(x,y,'o',color=BLUE,ms=3.8)
    ax.annotate('',(x+dx,y+dy),(x,y),arrowprops=dict(arrowstyle='->',color=BLUE,lw=1.2))
ax.annotate('',(.94,-.13),(.94,.13),arrowprops=dict(arrowstyle='<->',lw=1,color=GRAY))
ax.text(.90,.27,r'$O(\varepsilon)$',ha='center')
ax.text(.05,-.38,r'mass $O(\varepsilon)$ $\times$ distance $O(\varepsilon)$'+'\n'+r'local transport cost $O(\varepsilon^2)$',fontsize=9)
ax.set_xlabel('position along the tail surface')
ax.set_ylabel(r'normal loss coordinate $B-v$')
ax.set_xticks([]);ax.set_yticks([0]);ax.set_title('(a) Local transport in a thin layer',fontsize=10)
ax.spines[['top','right']].set_visible(False)
ax=axs[1];q=np.linspace(0,2,350);d=np.sin(2*np.pi*q)*np.sin(np.pi*q/2)**2
ax.axhline(0,color=GRAY,lw=1)
ax.plot(q,d,color=BLUE,label=r'local discrepancy $\Delta_i$')
ax.plot(q,-d,color=ORANGE,linestyle='--',label=r'remaining plan: $-\Delta_i$')
ax.fill_between(q,0,d,color=BLUE,alpha=.12)
ax.set_xlim(0,2);ax.set_ylim(-1.9,1.6)
ax.text(.08,1.25,r'compensation cost $\gamma_i\int|\Delta_i(q)|\,dq$',fontsize=9)
ax.set_xlabel(r'coordinate value $q$')
ax.set_ylabel('signed marginal CDF discrepancy')
ax.set_yticks([0]);ax.set_xticks([0,2],[r'$\ell_i$',r'$r_i$'])
ax.set_title('(b) Cancellation of full marginal discrepancies',fontsize=10)
ax.legend(frameon=False,fontsize=8,loc='lower left')
ax.spines[['top','right']].set_visible(False)
save(fig,'tail-layer-repair')

fig,axs=plt.subplots(1,2,figsize=(7.1,2.9),gridspec_kw={'width_ratios':[1,1.15]},layout='constrained')
ax=axs[0];delta=.35
omega=np.array([[0,.25],[.25,0],[2,0],[2,1.75],[1.75,2],[0,2]])
ax.add_patch(Polygon(omega,facecolor='#edf0f2',edgecolor=GRAY,lw=1))
ax.add_patch(Rectangle((0,2-delta),delta,delta,facecolor=BLUE,edgecolor=BLUE,alpha=.75,lw=1))
for pts in [[[0,0],[delta,0],[delta,delta]],[[2-delta,2-delta],[2,2-delta],[2,2]]]:
    ax.add_patch(Polygon(pts,facecolor='none',edgecolor=ORANGE,hatch='////',lw=1.1))
ax.plot([0,2],[0,2],linestyle='--',color=GRAY,lw=1)
ax.text(1.1,.7,r'$x=y$',rotation=44,fontsize=9)
ax.text(.60,1.3,r'$\Omega$',fontsize=15)
ax.annotate(r'$E_\delta$',(.17,1.84),(.53,2.12),arrowprops=dict(arrowstyle='->',lw=1),fontsize=11)
ax.annotate(r'$R_1$',(.25,.12),(.68,.2),arrowprops=dict(arrowstyle='->',lw=1,color=ORANGE),color=ORANGE)
ax.annotate(r'$R_2$',(1.9,1.77),(2.13,1.48),arrowprops=dict(arrowstyle='->',lw=1,color=ORANGE),color=ORANGE)
ax.set_xlim(-.05,2.35);ax.set_ylim(-.06,2.25);ax.set_aspect('equal')
ax.set_xticks([0,2],[r'$\xi_-$',r'$\xi_+$']);ax.set_yticks([0,2],[r'$\xi_-$',r'$\xi_+$'])
ax.set_xlabel(r'$x$');ax.set_ylabel(r'$y$');ax.set_title('Projected source geometry',fontsize=10)
ax.spines[['top','right']].set_visible(False)
ax=axs[1];ax.axis('off')
texts=[
(.93,'Positive corner demand',BLUE),
(.77,r'$|E_\delta|\geq\delta^2/2,\quad y-x\geq\Delta/2$',GRAY),
(.62,r'$M_\delta\geq\frac{\lambda\Delta^2}{16\beta}\,\delta^2$',BLUE),
(.42,'Available return capacity',ORANGE),
(.26,r'$|R_i|\leq\delta^2/2,\quad |x-y|\leq\delta$',GRAY),
(.10,r'$N_1+N_2\leq\frac{\Lambda}{12\beta}\,\delta^4$',ORANGE)]
for y,t,c in texts: ax.text(.01,y,t,color=c,fontsize=11,transform=ax.transAxes)
save(fig,'corner-capacity')

report = {
    "scope": "Two schematic mechanism figures; no optimization or empirical data.",
    "tail_layer": {
        "thin_layer_halfwidth_illustration": 0.13,
        "discrepancy_curve": "sin(2*pi*q)*sin(pi*q/2)**2",
        "interpretation": "Illustrative signed local CDF discrepancy and its opposite; not a computed optimizer."
    },
    "corner": {
        "support": "[0,2]^3", "beta": 1.75, "v": 3.75,
        "delta": float(delta), "a": 0.0, "b_star": 2.0,
        "lower_section_sum": 0.25, "upper_section_sum": 3.75,
        "hatched_triangles": "Bounding regions may extend outside Omega.",
        "demand_order": "delta^2", "capacity_order": "delta^4"
    },
    "numpy_version": np.__version__,
    "matplotlib_version": matplotlib.__version__,
}
files = [OUT / f"{name}.{ext}"
         for name in ("tail-layer-repair", "corner-capacity")
         for ext in ("pdf", "png", "svg")]
report["sha256"] = {
    path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
    for path in files
}
(DATA / "MECHANISM_FIGURES.json").write_text(
    json.dumps(report, indent=2)+"\n", encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k != "sha256"}, indent=2))
