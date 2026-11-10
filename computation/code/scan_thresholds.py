from numerical_profiles import solve_limit, OUT
import json
from scipy.optimize import minimize_scalar

rows=[]
for a in [0,.125,.25,.375,.5,.75,1.,1.25]:
    evaluations=[]
    def fun(b):
        row=solve_limit(8,48,3,.24,a,b)
        evaluations.append(row)
        return row['value']
    r=minimize_scalar(fun,bounds=(-1.5,1.5),method='bounded',options={'xatol':1e-5})
    row={'a':a,'b':r.x,'value':r.fun,'evaluations':evaluations}
    rows.append(row)
    print(json.dumps({k:v for k,v in row.items() if k!='evaluations'}),flush=True)
    (OUT/'threshold-scan.json').write_text(json.dumps(rows,indent=2)+'\n')
