"""Exact rational checks for the manuscript's uniform illustration.

No numerical search, optimizer, or quadrature is used. The script verifies
finite polynomial integrations and scalar consequences of the proofs
recorded in Section 5 and Appendix B of the accompanying manuscript.
"""
from fractions import Fraction as Q
from pathlib import Path
import json


def integral(coefficients, a, b):
    return sum(Q(c, k + 1) * (b ** (k + 1) - a ** (k + 1))
               for k, c in enumerate(coefficients))


# ell_-(x)=(2x-1)^3/48 on [1/2,1]; min is zero on [0,1/2].
half_overlap = integral([Q(-1, 48), Q(1, 8), Q(-1, 4), Q(1, 6)], Q(1, 2), Q(1))
assert half_overlap == Q(1, 384)
J, p, g = Q(5, 32), Q(1, 2), Q(3, 8)
Qbal = 2 * half_overlap
s0 = 2 * Qbal
norm = J - s0
chi = norm / J
U = J + norm
assert (s0, norm, chi, U) == (Q(1, 96), Q(7, 48), Q(14, 15), Q(29, 96))

# Same-side penalty, sign-reversal strip, and fixed-amplitude lower bound.
omega = Q(1, 2)
same_side_mass, same_side_second_moment = Q(1, 8), Q(1, 48)
strip_coefficient = integral([0, Q(1, 8), Q(-1, 4), Q(1, 8)], Q(0), Q(1))
assert strip_coefficient == Q(1, 96)
lower = (1 + omega) * (J - omega * same_side_second_moment / (1 - omega))
small_tau2_coefficient = (1 + omega) * (g / 2 - omega * same_side_mass / (1 - omega))
small_tau4_coefficient = -(1 + omega) * omega / (96 * (1 - omega))
assert lower == Q(13, 64)
assert (small_tau2_coefficient, small_tau4_coefficient) == (Q(6, 64), Q(-1, 64))
assert small_tau2_coefficient + small_tau4_coefficient == Q(5, 64) > 0
large_threshold_constant = J + g / 2
assert large_threshold_constant == Q(11, 32) > lower
premium = lower / J - 1
assert premium == Q(3, 10)

# The pure-first-coordinate comparison kernel and balanced endpoint have
# the same two minimizing thresholds. Their mixture gives the lower line.
F0 = -J / p + s0 / p
assert F0 == -Q(7, 24)
assert -F0 / (U - s0) == 1
small_slope = 1 / ((1 + omega) * p)
small_intercept = -lower * small_slope
assert (small_slope, small_intercept) == (Q(4, 3), -Q(13, 48))
branch_crossing = (large_threshold_constant / p + small_intercept) / (1 / p - small_slope)
assert branch_crossing == Q(5, 8) > U
upper_kink = (small_intercept + J / p) / (1 / p - small_slope)
assert upper_kink == Q(1, 16)

# FGM moment formulas, evaluated and differentiated by rational algebra.
M0, M1 = Q(3, 1152), -Q(2, 1152)
J0, J1 = Q(75, 480), -Q(14, 480)
JA0, JA1 = J0 - 8 * M0, J1 - 8 * M1
assert (JA0, JA1) == (Q(195, 1440), -Q(22, 1440))
share_derivative_numerator = (JA1 * J0 - JA0 * J1) * 480 ** 2
assert share_derivative_numerator == 360
for theta in (Q(-1, 2), Q(0), Q(1, 4), Q(1, 2)):
    j, mass = J0 + J1 * theta, M0 + M1 * theta
    assert j - 8 * mass == JA0 + JA1 * theta
    # The displayed capacity-gap braces are decreasing. For |theta|<=1/2,
    # its derivative is <=-3/16+1/48+1/16=-5/48<0: the coefficient
    # derivative 1/8-3w^2/16-2w^3/15 lies in [59/960,1/8].
    w = Q(1, 2)
    endpoint_braces = Q(3, 16) - 3*w/16 + w*w/48 + theta*(-Q(1, 16)+w/8-w**3/16-w**4/30)
    assert endpoint_braces > 0
assert Q(1, 8) - Q(3, 64) - Q(1, 60) == Q(59, 960) > 0

report = {
    "scope": "Exact scalar and polynomial checks; all-threshold and kernel-mixture arguments are in Section 5 and Appendix B of the manuscript.",
    "J": str(J), "Q_bal": str(Qbal), "s_lin_gamma0_1": str(s0),
    "projected_imbalance_L1": str(norm), "chi": str(chi),
    "critical_lower_fixed_amplitude": str(lower), "critical_upper_pure_first_coordinate": str(U),
    "guaranteed_relative_premium": str(premium),
    "small_threshold_extra": "tau^2(6-tau^2)/64",
    "large_threshold_cost_constant": str(large_threshold_constant),
    "profile_lower": "2s-5/16 for 0<=s<=1/96; s-29/96 for 1/96<=s<=29/96",
    "profile_upper": "min(2s-5/16, 4s/3-13/48), valid on 0<=s<=29/96",
    "FGM_J": "(75-14theta)/480", "FGM_M_each": "(3-2theta)/1152",
    "FGM_J_a_plus": "(195-22theta)/1440", "FGM_a_plus_derivative": "360/(75-14theta)^2",
    "FGM_covariance": "2theta/9", "FGM_Var_B": "1+4theta/9",
    "all_checks_passed": True,
}
out = Path(__file__).with_name("SIMPLE_EXAMPLE_CHECKS.json")
out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
