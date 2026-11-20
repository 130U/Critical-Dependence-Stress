"""Independent small-grid transport and direct-ES checks."""
import numpy as np
from scipy import sparse
from numerical_profiles import solve_finite, lp, solve_limit, solve_limit_zero

def complete_transport(n,eps,s):
    ids=np.indices((n,n,n)).reshape(3,-1)
    x=(ids+.5)*2/n; m=n**3
    B=x.sum(axis=0);A=B+eps*(x[0]-x[1])
    dist=(np.abs(x[:,:,None]-x[:,None,:])*np.array([1,1,2])[:,None,None]).sum(axis=0)
    # pi[source,target] with source sum fixed and all target marginals fixed.
    rows=[]
    for i in range(m):
        row=np.zeros((m,m));row[i,:]=1;rows.append(row.ravel())
    for axis in range(3):
        for k in range(n):rows.append(np.tile(ids[axis]==k,m))
    eq=sparse.csr_matrix(np.column_stack((np.array(rows),np.zeros(len(rows)))))
    beq=np.r_[np.full(m,1/m),np.full(3*n,1/n)]
    tB=np.unique(B);hinges=np.maximum(B[None,:]-tB[:,None],0)*2
    aub=sparse.csr_matrix(np.vstack((np.r_[dist.ravel(),0],
        np.column_stack((-np.tile(hinges,(1,m)),np.ones(len(tB)))))))
    bub=np.r_[s*eps**2,tB]
    best=-np.inf
    for t in np.unique(A):
        c=np.r_[np.tile(2*np.maximum(A-t,0),m),-1]
        r,_=lp(c,aub,bub,eq,beq,[(0,None)]*(m*m)+[(None,None)])
        best=max(best,-r.fun-t)
    return best/eps**2

if __name__=='__main__':
    for eps in (.2,.1):
        for s in (0.,.1,.25):
            graph=solve_finite(2,eps,s)
            direct=complete_transport(2,eps,s)
            assert abs(graph['scaled_value']-direct)<1e-9,(graph,direct)
            assert abs(graph['direct_risk']/eps**2-direct)<1e-9
    for s in (0.,.005,1/96):
        row=solve_limit(16,48,3.,s)
        assert abs(row['value']-(2*s-5/16))<1e-9,row
        assert row['threshold_readback_difference']<1e-9,row
    zero=solve_limit_zero(8,48,3.)
    profile=solve_limit(8,48,3.,zero['restricted_zero'])
    assert abs(zero['paired_risk_readback'])<1e-9
    assert abs(profile['paired_risk_readback'])<1e-9
    print('PASS: 6 complete-coupling comparisons, 6 direct ES readbacks, 3 exact linear-profile checks, and the minimum-cost zero/profile cross-check.')
