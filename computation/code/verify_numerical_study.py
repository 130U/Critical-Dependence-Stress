"""Check recorded numerical outputs and bind them to the study source files."""
from pathlib import Path
from fractions import Fraction
from itertools import product
import hashlib,json,platform
import scipy,numpy

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'calculations'

def read(name):return json.loads((DATA/name).read_text(encoding='utf-8'))
def lower(s):return 2*s-5/16 if s<=1/96 else s-29/96
def upper(s):return min(2*s-5/16,4*s/3-13/48)
def nominal(e):
    def hinge(e):
        widths=(2*(1+e),2*(1-e),Fraction(2))
        return sum((-1)**sum(bits)*max(Fraction(3)-sum(a*b for a,b in zip(widths,bits)),0)**4
            for bits in product((0,1),repeat=3))/(24*widths[0]*widths[1]*widths[2])
    return float(2*(hinge(Fraction(0))-hinge(e))/(e*e))

finite=read('finite-epsilon-study.json')+read('finite-n24-e01.json')
mesh=read('mesh-study.json');window=read('window-study.json')
zeros=read('restricted-zero-study.json')
assert len(finite)==39 and len(mesh)==16 and len(window)==16 and len(zeros)==8
assert all(x['threshold_stride']==1 for x in finite)
assert all(abs(x['direct_risk']/x['epsilon']**2-x['scaled_value'])<1e-8 for x in finite)
assert all(lower(x['s'])-1e-9<=x['value']<=upper(x['s'])+1e-9 for x in mesh+window)
assert all(abs(x['paired_risk_readback'])<1e-8 for x in zeros)
assert all(13/64<x['restricted_zero']<29/96 for x in zeros)
assert all(x['threshold_readback_difference']<1e-8 for x in mesh)
u4={x['s']:x['value'] for x in window if x['U']==4}
u6={x['s']:x['value'] for x in window if x['U']==6}
data_names=['finite-epsilon-study.json','finite-n24-e01.json','mesh-study.json',
            'window-study.json','restricted-zero-study.json','threshold-scan.json',
            'threshold-readback-n16.json','threshold-readback-n24.json']
files=[DATA/n for n in data_names]+[ROOT/'code'/n for n in (
    'numerical_profiles.py','run_numerical_study.py','scan_thresholds.py',
    'check_numerical_profiles.py','verify_numerical_study.py')]
record={
    'checked_client_date':'2026-11-09',
    'environment':{'python':platform.python_version(),'scipy':scipy.__version__,'numpy':numpy.__version__},
    'all_record_consistency_checks_passed':True,
    'finite_epsilon_instances':len(finite),'finite_global_scope':'exact discrete marginal laws; every admissible A threshold enumerated',
    'finite_max_primal_dual_gap':max(x['lp_max_primal_dual_gap'] for x in finite),
    'finite_max_constraint_violation':max(x['lp_max_constraint_violation'] for x in finite),
    'finite_max_direct_es_difference':max(abs(x['direct_risk']/x['epsilon']**2-x['scaled_value']) for x in finite),
    'limiting_mesh_instances':len(mesh),'limiting_window_instances':len(window),
    'limiting_mesh_all_within_analytical_envelopes':True,
    'restricted_zero_instances':len(zeros),
    'restricted_zero_max_primal_dual_gap':max(x['lp_primal_dual_gap'] for x in zeros),
    'restricted_zero_max_absolute_risk_readback':max(abs(x['paired_risk_readback']) for x in zeros),
    'mesh_max_threshold_readback_difference':max(x['threshold_readback_difference'] for x in mesh),
    'U4_U6_max_profile_difference_at_fixed_n_and_du':max(abs(u4[s]-u6[s]) for s in u4),
    'exact_continuous_nominal_values':{str(float(e)):nominal(e) for e in (Fraction(1,5),Fraction(1,10),Fraction(1,20),Fraction(1,40))},
    'continuous_global_certificate':False,
    'finite_epsilon_convergence_established':False,
    'sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(ROOT/'audit/NUMERICAL-VERIFICATION.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k!='sha256'},indent=2))
