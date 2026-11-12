"""Numerical experiments for the uniform benchmark; see NUMERICAL-STUDY.md.

Finite-epsilon problems use all adjacent edges of the cubic grid, hence the
exact Manhattan Wasserstein distance for the discrete marginal laws. The
limiting experiment uses a separately documented restricted kernel family.
"""
from pathlib import Path
import argparse
import json
import time
import numpy as np
from scipy import sparse
from scipy.optimize import linprog, minimize_scalar

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'calculations'

def lp(c, aub, bub, aeq=None, beq=None, bounds=(0, None)):
    r = linprog(c, A_ub=aub, b_ub=bub, A_eq=aeq, b_eq=beq,
                bounds=bounds, method='highs',
                options={'dual_feasibility_tolerance': 1e-8,
                         'primal_feasibility_tolerance': 1e-8})
    if not r.success:
        raise RuntimeError(r.message)
    dual = np.dot(bub, r.ineqlin.marginals)
    if beq is not None:
        dual += np.dot(beq, r.eqlin.marginals)
    return r, float(abs(r.fun-dual))

def finite_model(n, eps):
    if n < 2 or n % 2:
        raise ValueError('The half-mass pruning formula requires an even n >= 2.')
    ids = np.arange(n**3).reshape((n, n, n))
    inds = np.indices((n, n, n)).reshape(3, -1)
    x = (inds+.5)*2/n
    B, A = x.sum(axis=0), x.sum(axis=0)+eps*(x[0]-x[1])
    starts, ends, costs = [], [], []
    for i, gamma in enumerate((1., 1., 2.)):
        left, right = [slice(None)]*3, [slice(None)]*3
        left[i], right[i] = slice(0, -1), slice(1, None)
        a, b = ids[tuple(left)].ravel(), ids[tuple(right)].ravel()
        starts.extend((a, b)); ends.extend((b, a))
        costs.extend((np.full(len(a), gamma*2/n),)*2)
    starts, ends, costs = map(np.concatenate, (starts, ends, costs))
    e, m = len(costs), n**3
    div = sparse.coo_matrix((np.r_[-np.ones(e), np.ones(e)],
                            (np.r_[starts, ends], np.tile(np.arange(e), 2))),
                           shape=(m,e)).tocsr()
    projection = sparse.coo_matrix((np.ones(3*m),
        ((inds+np.arange(3)[:,None]*n).ravel(), np.tile(np.arange(m),3))),
        shape=(3*n,m)).tocsr()
    eq = sparse.hstack((projection@div, sparse.csr_matrix((3*n,1))), format='csr')
    base = np.full(m, 1/m)
    # z is ES_B, expressed as an increment from ES_B(reference).
    tB = np.unique(np.round(B,12))
    hingeB = np.maximum(B[None,:]-tB[:,None],0)*2
    baselineB = np.min(tB+hingeB@base)
    constraints = sparse.vstack((
        sparse.hstack((-div,sparse.csr_matrix((m,1)))),
        sparse.csr_matrix(np.r_[costs,0][None,:]),
        sparse.hstack((-sparse.csr_matrix(hingeB)@div,
                       sparse.csr_matrix(np.ones((len(tB),1)))))
    ),format='csr')
    rhs = np.r_[base, 0., tB+hingeB@base-baselineB]
    return B,A,base,div,eq,constraints,rhs,baselineB,costs

def solve_finite(n, eps, s, threshold_stride=1):
    start=time.perf_counter()
    B,A,base,div,eq,aub,rhs,baselineB,costs=finite_model(n,eps)
    rhs[len(base)]=s*eps**2
    values=np.unique(np.round(A,12))
    # If t is an A-median, bringing a reference half-mass to that side
    # costs at least sum of distance to t for the required nearest mass,
    # divided by ||(1+eps,1-eps,1)||_{gamma,*}=1+eps.
    sortA=np.sort(A)
    medlo,medhi=sortA[len(A)//2-1],sortA[len(A)//2]
    def quantile_cost(t):
        if t >= medhi:
            return np.maximum(t-sortA[len(A)//2:],0).sum()/len(A)/(1+eps)
        return np.maximum(sortA[:len(A)//2]-t,0).sum()/len(A)/(1+eps)
    values=np.array([t for t in values if quantile_cost(t)<=s*eps**2+1e-12])
    values=values[::threshold_stride]
    best=-np.inf; bestrow=None; maxgap=0.; maxviolation=0.
    for t in values:
        hinge=2*np.maximum(A-t,0)
        c=np.r_[np.asarray(hinge@div).ravel(),-1.]
        r,gap=lp(c,aub,rhs,eq,np.zeros(eq.shape[0]),
                 [(0,None)]*len(costs)+[(None,None)])
        val=baselineB-t-hinge@base-r.fun
        maxgap=max(maxgap,gap)
        maxviolation=max(maxviolation,float(max(0.,np.max(aub@r.x-rhs))),
                         float(np.max(np.abs(eq@r.x))))
        if val>best:
            q=base+div@r.x[:-1]
            order=np.argsort(A); cum=np.cumsum(q[order])
            ta=A[order[np.searchsorted(cum,.5)]]
            orderb=np.argsort(B); cumb=np.cumsum(q[orderb])
            tb=B[orderb[np.searchsorted(cumb,.5)]]
            direct=tb+2*np.dot(q,np.maximum(B-tb,0))-ta-2*np.dot(q,np.maximum(A-ta,0))
            best=val; bestrow={'threshold_A':float(t),'threshold_B':float(tb),
                'direct_risk':float(direct),
                'used_transport':float(costs@r.x[:-1]),
                'target_minimum_mass':float(q.min())}
    return {'n':n,'epsilon':eps,'s':s,'scaled_value':float(best/eps**2),
            'thresholds_enumerated':len(values),'threshold_stride':threshold_stride,
            'lp_max_primal_dual_gap':maxgap,'lp_max_constraint_violation':maxviolation,
            'seconds':time.perf_counter()-start,**bestrow}

def limit_model(n, nu, U, a=0., b=0.):
    # Equal square cells with midpoint quadrature on the hexagonal section.
    q=(np.arange(n)+.5)*2/n
    xx,yy=np.meshgrid(q,q,indexing='ij')
    zz=np.round(3-xx-yy,12); keep=(zz>=0)&(zz<=2)
    x,y,z=xx[keep],yy[keep],zz[keep]
    h=x-y
    u=(np.arange(nu)+.5)*2*U/nu-U
    H=np.repeat(h,nu); uv=np.tile(u,len(h))
    cellweight=np.where((z==0)|(z==2),.5,1.)
    mass=np.repeat(cellweight,nu)*(2/n)**2/8*(2*U/nu)
    assert abs(mass.sum()/(2*U)-3/8)<1e-12, 'surface quadrature must retain its exact area'
    m=len(H)
    # Identity plus six pure-axis actions, with targets at the two hinge knots.
    targets=np.column_stack((np.full(m,b),a-H))
    w=(targets-uv[:,None])
    directions=np.tile(np.arange(3),2)
    shifts=np.repeat(w,3,axis=1)
    c0=np.maximum(uv[:,None]+shifts-b,0)-np.maximum(uv[:,None]-b,0)
    c1=np.maximum(uv[:,None]+shifts+H[:,None]-a,0)-np.maximum(uv[:,None]+H[:,None]-a,0)
    reward=(c0-c1).ravel()
    normalcost=(np.abs(shifts)*np.tile([1,1,2],2)).ravel()
    cols=np.arange(m*6)
    source=sparse.coo_matrix((np.ones(m*6),(np.repeat(np.arange(m),6),cols)),shape=(m,m*6)).tocsr()
    coordbins=[]; count=0
    for coord in (x,y,z):
        _,inv=np.unique(np.round(coord,12),return_inverse=True)
        coordbins.append(np.repeat(inv,nu)+count); count+=inv.max()+1
    fluxrows=np.stack([coordbins[i] for i in directions],axis=1).ravel()
    flux=sparse.coo_matrix((shifts.ravel(),(fluxrows,cols)),shape=(count,m*6)).tocsr()
    weights=[]
    for i,coord in enumerate((x,y,z)):
        weights.extend([1 if i<2 else 2]*len(np.unique(np.round(coord,12))))
    fluxvars=sparse.eye(count,format='csr')
    aub=sparse.vstack((
        sparse.hstack((source,sparse.csr_matrix((m,count)))),
        sparse.hstack((flux,-fluxvars)),sparse.hstack((-flux,-fluxvars)),
        sparse.csr_matrix(np.r_[normalcost,weights][None,:])
    ),format='csr')
    rhs=np.r_[mass,np.zeros(count*2),0.]
    obj=np.r_[-reward,np.zeros(count)]
    return obj,aub,rhs,m,len(cols),len(x),(uv,H,shifts)

def threshold_readback(uv,H,shifts,weights,c):
    active=weights>1e-12
    src=np.repeat(uv+c*H,6)[active]
    dst=(uv[:,None]+shifts+c*H[:,None]).ravel()[active]
    w=weights[active]/2
    # Averaging with central reflection gives a symmetric kernel of no greater cost. Evaluate
    # both threshold minima independently in the midpoint approximation.
    src=np.r_[src,-src];dst=np.r_[dst,-dst];w=np.r_[w,w]
    events=np.r_[src,dst];jumps=np.r_[-w,w]
    order=np.argsort(events);events=events[order];jumps=jumps[order]
    knots,idx=np.unique(events,return_index=True)
    jumps=np.add.reduceat(jumps,idx)
    if not len(knots):return 0.,0.
    g=3/8;left=knots[0];v=g*left*left/2;offset=0.;best=(float('inf'),0.)
    # Before all events the hinge increments equal the total normal moment,
    # which is zero after central reflection.
    for right,jump in zip(knots,jumps):
        z=-offset/g
        if left<=z<=right:
            vz=v+g*(z*z-left*left)/2+offset*(z-left)
            if vz<best[0]:best=(float(vz),float(z))
        v+=g*(right*right-left*left)/2+offset*(right-left)
        if v<best[0]:best=(float(v),float(right))
        offset+=jump;left=right
    return best

def solve_limit(n,nu,U,s,a=0.,b=0.):
    start=time.perf_counter()
    c,mat,rhs,m,nmove,ns,geometry=limit_model(n,nu,U,a,b)
    rhs[-1]=s
    r,gap=lp(c,mat,rhs)
    # Exact nominal constants. Quadrature enters only the transport increment.
    val=(-5/32+3/16*(b*b-a*a)-r.fun)*2
    active=r.x[:nmove].reshape(m,6).sum(axis=1).reshape(ns,nu)
    extra={}
    if a==0 and b==0:
        g0,t0=threshold_readback(*geometry,r.x[:nmove],0)
        g1,t1=threshold_readback(*geometry,r.x[:nmove],1)
        extra={'paired_risk_readback':-5/16+2*(g0-g1),
               'minimizing_threshold_B':t0,'minimizing_threshold_A':t1,
               'threshold_readback_difference':abs(-5/16+2*(g0-g1)-val)}
    return {'n':n,'nu':nu,'U':U,'s':s,'threshold_A':a,'threshold_B':b,
            'value':float(val),'lp_primal_dual_gap':gap,
            'lp_constraint_violation':float(max(0.,np.max(mat@r.x-rhs))),
            'boundary_active_mass':float(active[:,[0,-1]].sum()),
            'seconds':time.perf_counter()-start,**extra}

def solve_limit_zero(n,nu,U):
    start=time.perf_counter()
    reward,mat,rhs,m,nmove,ns,geometry=limit_model(n,nu,U,0.,0.)
    # Minimize the full effective energy for centered paired value >= 0.
    cost=mat[-1,:].toarray().ravel()
    constraints=sparse.vstack((mat[:-1,:],sparse.csr_matrix(reward[None,:])),format='csr')
    rhs[-1]=-5/32
    r,gap=lp(cost,constraints,rhs)
    g0,t0=threshold_readback(*geometry,r.x[:nmove],0)
    g1,t1=threshold_readback(*geometry,r.x[:nmove],1)
    return {'n':n,'nu':nu,'U':U,'restricted_zero':float(r.fun),
            'paired_risk_readback':-5/16+2*(g0-g1),
            'minimizing_threshold_B':t0,'minimizing_threshold_A':t1,
            'lp_primal_dual_gap':gap,
            'lp_constraint_violation':float(max(0.,np.max(constraints@r.x-rhs))),
            'seconds':time.perf_counter()-start}

def main():
    p=argparse.ArgumentParser(); p.add_argument('mode',choices=['finite','limit','zero'])
    p.add_argument('--n',type=int,default=8);p.add_argument('--nu',type=int,default=32)
    p.add_argument('--U',type=float,default=3.);p.add_argument('--epsilon',type=float,default=.1)
    p.add_argument('--s',type=float,nargs='+',default=[0,.01,.1,.2,.25,.3])
    p.add_argument('--a',type=float,default=0);p.add_argument('--b',type=float,default=0)
    p.add_argument('--output',type=Path);args=p.parse_args(); rows=[]
    for s in ([0] if args.mode=='zero' else args.s):
        if args.mode=='finite': row=solve_finite(args.n,args.epsilon,s)
        elif args.mode=='zero':row=solve_limit_zero(args.n,args.nu,args.U)
        else: row=solve_limit(args.n,args.nu,args.U,s,args.a,args.b)
        rows.append(row);print(json.dumps(row),flush=True)
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
