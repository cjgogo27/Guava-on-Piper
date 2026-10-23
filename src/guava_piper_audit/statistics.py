"""Small paired-binary statistics implementation using Python's standard library."""
from math import comb, sqrt

def exact_mcnemar(rescued, lost):
    if not isinstance(rescued, int) or not isinstance(lost, int) or min(rescued,lost)<0:
        raise ValueError("Nonnegative integer discordant counts required")
    n=rescued+lost
    return min(1.0, 2*sum(comb(n,k) for k in range(min(rescued,lost)+1))/2**n) if n else 1.0

def wilson(k,n,z=1.959963984540054):
    if n<=0 or not 0<=k<=n:raise ValueError("Require 0 <= k <= n and n > 0")
    p=k/n;den=1+z*z/n;c=(p+z*z/(2*n))/den
    e=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [max(0.0,c-e),min(1.0,c+e)]

def holm(pvalues):
    if any(not 0<=p<=1 for p in pvalues):raise ValueError("Invalid p-value")
    order=sorted(range(len(pvalues)),key=pvalues.__getitem__);out=[None]*len(order);last=0.0
    for rank,i in enumerate(order):
        last=max(last,min(1.0,pvalues[i]*(len(order)-rank)));out[i]=last
    return out

def paired_counts(a,b):
    if len(a)!=len(b) or any(type(x) is not bool for x in [*a,*b]):raise ValueError("Paired booleans required")
    return {'rescued':sum(x and not y for x,y in zip(a,b)),
            'lost':sum(y and not x for x,y in zip(a,b))}
