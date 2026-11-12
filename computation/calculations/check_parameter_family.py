"""Exact polynomial checks of the density family and fixed-amplitude potential.

These checks integrate the formulas directly. SymPy is used only for finite
polynomial algebra.
"""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
import sympy as sp

x, y, z, s, h, r, t, omega = sp.symbols("x y z s h r t omega", real=True)
q = (y-x)**2 * (1-t*(x+y-2)**2)/16
ell = sp.factor(sp.integrate(q, (x, 1-y, y)))
cap = sp.factor(sp.integrate(q, (y, 2-x, 2)))
gap = sp.factor((cap-ell.subs(y, x)).subs(x, 1-r))
mass = sp.factor(sp.integrate(ell, (y, sp.Rational(1, 2), 1)))
j = sp.factor(2*sp.integrate(
    sp.integrate(h**2*(1-t*(s-2)**2)/32, (h, 0, s)),
    (s, 1, 2)))
# Reflection across s=2 supplies the second half of the section.
j *= 2
ja = sp.factor(j-8*mass)
share = sp.factor(ja/j)
dshare = sp.factor(sp.diff(share, t))
assert sp.simplify(j-(75-14*t)/480) == 0
assert sp.simplify(mass-(3-2*t)/1152) == 0
assert sp.simplify(ja-(195-22*t)/1440) == 0
assert sp.simplify(gap-r*(
    sp.Rational(3, 16)-3*r/16+r*r/48
    +t*(-sp.Rational(1, 16)+r/8-r**3/16-r**4/30))) == 0

# The section gap is affine in t. At both endpoints of [-1/2,1/2],
# retain only nonnegative terms and bound each negative monomial by r<=1/2.
endpoint_lower = {}
for v in [-sp.Rational(1, 2), sp.Rational(1, 2)]:
    polynomial = sp.Poly(sp.expand((gap/r).subs(t, v)), r)
    lower = sum(
        coeff if power == 0 else
        coeff*sp.Rational(1, 2)**power if coeff < 0 else 0
        for (power,), coeff in polynomial.terms())
    assert lower > 0
    endpoint_lower[str(v)] = str(lower)

# The manuscript uses a simpler bound valid throughout the parameter
# interval: the t-free part is >=3/32, and the t coefficient is in
# [-1/16,0]. The latter follows from r/8<=1/16 and
# r*(1/8-r^2/16-r^3/30)>=0.
coefficient = -sp.Rational(1, 16)+r/8-r**3/16-r**4/30
assert sp.expand(coefficient+sp.Rational(1, 16)
                 -r*(sp.Rational(1, 8)-r**2/16-r**3/30)) == 0
assert sp.Rational(1, 8)-sp.Rational(1, 64)-sp.Rational(1, 240) > 0
uniform_gap_lower = sp.Rational(3, 32)-sp.Rational(1, 32)
assert uniform_gap_lower == sp.Rational(1, 16)

f = (1+t*(x+y-2)*(z-1))/8
marginals = [
    sp.integrate(f, (y, 0, 2), (z, 0, 2)),
    sp.integrate(f, (x, 0, 2), (z, 0, 2)),
    sp.integrate(f, (x, 0, 2), (y, 0, 2)),
]
assert marginals == [sp.Rational(1, 2)]*3
covariance = sp.integrate((x+y-2)*(z-1)*f,
                          (x, 0, 2), (y, 0, 2), (z, 0, 2))
assert sp.simplify(covariance-2*t/9) == 0

# Fixed-amplitude illustration: no parameter optimization.
fixed_amplitude = sp.Rational(1,2)
potential_bound = (1+omega)*(sp.Rational(5,32)-omega/(48*(1-omega)))
fixed_bound = sp.simplify(potential_bound.subs(omega,fixed_amplitude))
fixed_premium = sp.simplify(fixed_bound/sp.Rational(5,32)-1)
assert fixed_bound == sp.Rational(13,64)
assert fixed_premium == sp.Rational(3,10)
threshold_remainder_lower = sp.Rational(3,2)*(sp.Rational(3,16)-sp.Rational(1,8)-sp.Rational(1,96))
assert threshold_remainder_lower == sp.Rational(5,64)>0
large_threshold_constant=sp.Rational(11,32)
assert fixed_bound<large_threshold_constant
upper_envelope_slope=sp.Rational(4,3)
half_overlap=sp.integrate((2*x-1)**3/48,(x,sp.Rational(1,2),1))
Q_bal=2*half_overlap
s_lin=2*Q_bal
imbalance=sp.Rational(5,32)-s_lin
pure_coordinate_upper=sp.Rational(5,32)+imbalance
assert (s_lin,imbalance,pure_coordinate_upper)==(sp.Rational(1,96),sp.Rational(7,48),sp.Rational(29,96))
same_side_mass = 2*sp.integrate(sp.Rational(1, 8), (y, 1-x, 1), (x, 0, 1))
same_side_h2 = 2*sp.integrate((x-y)**2/8, (y, 1-x, 1), (x, 0, 1))
tau = sp.symbols("tau", positive=True)
shifted_cross_moment = sp.integrate((tau-h)**2*h/8, (h, 0, tau))
assert same_side_mass == sp.Rational(1, 8)
assert same_side_h2 == sp.Rational(1, 48)
assert shifted_cross_moment == tau**4/96

report = {
    "scope": "Exact polynomial integration for the parameter family and fixed-amplitude potential; no full risk-profile optimization.",
    "sympy_version": sp.__version__,
    "parameter_interval": "-1/2 < vartheta < 1/2",
    "marginal_densities": [str(v) for v in marginals],
    "covariance": str(covariance),
    "same_side_section_demand": str(ell),
    "capacity_minus_demand_at_x_1_minus_r": str(gap),
    "capacity_gap_over_r_endpoint_lower_bounds": endpoint_lower,
    "manuscript_uniform_capacity_gap_over_r_lower": str(uniform_gap_lower),
    "J": str(j), "M_minus_equals_M_plus": str(mass),
    "J_a_plus": str(ja), "a_plus": str(share),
    "a_plus_derivative": str(dshare),
    "a_plus_minus_uniform": str(sp.factor(share-sp.Rational(13, 15))),
    "J_a_plus_minus_uniform": str(sp.factor(ja-sp.Rational(13, 96))),
    "fixed_midpoint_amplitude": str(fixed_amplitude),
    "fixed_two_level_lower_bound": str(fixed_bound),
    "fixed_two_level_relative_premium": str(fixed_premium),
    "small_threshold_remainder_lower": str(threshold_remainder_lower),
    "large_threshold_cost_constant": str(large_threshold_constant),
    "upper_envelope_slope": str(upper_envelope_slope),
    "balanced_moment": str(Q_bal),
    "s_lin_gamma0_1": str(s_lin),
    "projected_imbalance": str(imbalance),
    "pure_coordinate_upper": str(pure_coordinate_upper),
    "two_level_same_side_mass": str(same_side_mass),
    "two_level_same_side_H2": str(same_side_h2),
    "two_level_shifted_cross_moment": str(shifted_cross_moment),
    "all_checks_passed": True,
}
(ROOT / "calculations/PARAMETER_FAMILY_CHECK.json").write_text(
    json.dumps(report, indent=2)+"\n", encoding="utf-8")
print(json.dumps(report, indent=2))
