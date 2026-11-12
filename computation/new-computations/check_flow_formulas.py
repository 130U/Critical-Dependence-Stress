"""Check the flow evaluator against exact integration and rational arithmetic."""
from fractions import Fraction
from pathlib import Path
import json
import numpy as np
import sympy as sp
from flow_formulas import capacity, demand, ratio

x, y = sp.symbols('x y', real=True)
q = (y-x)**2/16
capacities = [x*(7*x**2-18*x+12)/48,
              x*(240-360*x+120*x**2+25*x**3-8*x**4)/960]
identities = []
for dependent, formula in zip((False, True), capacities):
    density = q*(1-(x+y-2)**2/4) if dependent else q
    residual = sp.expand(sp.integrate(density, (y, 2-x, 2))-formula)
    assert residual == 0
    implementation = sp.sympify(np.asarray(capacity(x, dependent)).item())
    assert sp.expand(implementation-formula) == 0
    identities.append(str(sp.factor(formula)))

axis = (np.arange(500)+.5)*2/500
points = np.unique(np.r_[0., 1., axis[axis < 1], (2-axis)[axis > 1]])
errors = {}
for dependent, name in ((False, 'U'), (True, 'D')):
    exact = {key: [] for key in ('capacity', 'demand', 'ratio')}
    for value in points:
        z = Fraction.from_float(float(value))
        r = max(2*z-1, 0)
        cap = (z*(240-360*z+120*z*z+25*z**3-8*z**4)/960
               if dependent else z*(7*z*z-18*z+12)/48)
        dem = r**3*(30+5*r-r*r)/1920 if dependent else r**3/48
        exact['capacity'].append(float(cap))
        exact['demand'].append(float(dem))
        exact['ratio'].append(float(dem/cap) if cap else 0.)
    errors[name] = {}
    for key, fn in (('capacity', capacity), ('demand', demand), ('ratio', ratio)):
        error = float(np.max(np.abs(fn(points, dependent)-np.array(exact[key]))))
        assert error <= 16*np.finfo(float).eps, (name, key, error)
        errors[name][key] = error

record = {'capacity_integrals_exact': identities,
          'rational_comparison': 'Exact Fraction values at the actual binary64 plotting coordinates, rounded once to binary64.',
          'coordinate_count': len(points),
          'maximum_absolute_error': errors,
          'independent_check_tolerance': float(16*np.finfo(float).eps),
          'frozen_array_acceptance': 'Exact shape, dtype and byte hash.',
          'all_checks_passed': True}
out = Path(__file__).resolve().parents[1]/'audit/FLOW-FORMULA-CHECK.json'
out.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
print(json.dumps(record, indent=2))
