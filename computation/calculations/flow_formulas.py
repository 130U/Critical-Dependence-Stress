"""Polynomial section formulas for the plotted boundary-flow allocation."""
import numpy as np


def qdensity(x, y, dependent=False):
    q = (y-x)**2/16
    if dependent:
        q = q*(1-(x+y-2)**2/4)
    return q


def demand(x, dependent=False):
    r = np.maximum(2*np.asarray(x)-1, 0)
    cube = r*r*r
    if dependent:
        return cube*(30+5*r-r*r)/1920
    return cube/48


def capacity(x, dependent=False):
    """Integral of qdensity(x, y) over 2-x <= y <= 2.

    Horner evaluation uses elementary binary64 operations. Explicit
    multiplication avoids CPU-specific vector power implementations.
    """
    x = np.asarray(x)
    r = 1-x
    if dependent:
        return x*((((-8*r+7)*r+147)*r+77)*r+17)/960
    return x*((7*r+4)*r+1)/48


def ratio(x, dependent=False):
    x = np.asarray(x)
    cap = capacity(x, dependent)
    return np.divide(demand(x, dependent), cap, out=np.zeros_like(x),
                     where=cap > 0)
