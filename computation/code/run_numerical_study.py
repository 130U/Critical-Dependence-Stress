"""Run the documented mesh/epsilon study; retain partial results on interruption."""
from numerical_profiles import solve_finite, solve_limit, solve_limit_zero, OUT
import json

def save(name,rows):
    (OUT/name).write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('part',choices=['finite','window','mesh','zero','readback'])
    args=p.parse_args();rows=[]
    if args.part=='finite':
        for n in (8,12,16):
            for eps in (.2,.1,.05,.025):
                for s in (0.,.1,.25):
                    row=solve_finite(n,eps,s);rows.append(row)
                    print(json.dumps(row),flush=True);save('finite-epsilon-study.json',rows)
    elif args.part=='window':
        for U,nu in ((2.,32),(3.,48),(4.,64),(6.,96)):
            for s in (.01,.1,.23,.25):
                row=solve_limit(16,nu,U,s);rows.append(row)
                print(json.dumps(row),flush=True);save('window-study.json',rows)
    elif args.part=='mesh':
        for n,nu in ((8,48),(12,72),(16,96),(24,144)):
            for s in (.01,.1,.23,.25):
                row=solve_limit(n,nu,3.,s);rows.append(row)
                print(json.dumps(row),flush=True);save('mesh-study.json',rows)
    elif args.part=='zero':
        for n,nu,U in ((8,48,3),(12,72,3),(16,96,3),(24,144,3),(32,96,3),
                       (16,32,2),(16,64,4),(16,96,6)):
            row=solve_limit_zero(n,nu,U);rows.append(row)
            print(json.dumps(row),flush=True);save('restricted-zero-study.json',rows)
    else:
        for n,nu,budgets in ((16,48,(.01,.1,.23,.25)),(24,72,(.23,.25))):
            rows=[]
            for s in budgets:
                row=solve_limit(n,nu,3.,s);rows.append(row)
                print(json.dumps(row),flush=True);save(f'threshold-readback-n{n}.json',rows)
