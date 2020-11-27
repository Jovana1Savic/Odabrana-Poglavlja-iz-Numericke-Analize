"""
@brief Functions used to find best rational approximations of numbers.

@detail Continuous fractions are used to find first and second kind of
rational approximations of given numbers. 
Uses mpmath library to perform high precision calculations.

@date November 2020
@author Jovana Savic 
"""

import mpmath as mp
from mpmath import libmp

math_constants = {
    "pi" : mp.pi,
    "e" : mp.e,
    "phi" : mp.phi,
    "euler" : mp.euler,
    "catalan" : mp.catalan,
    "apery" : mp.apery,
    "khinchin" : mp.khinchin,
    "glaisher" : mp.glaisher,
    "mertens" : mp.mertens,
    "twin prime" : mp.twinprime
}

# Error (of first kind) when num is approximated with p/q.
def difference(num, p, q):
    return mp.fabs(mp.fsub(num, mp.fdiv(p, q)))

# Finds verige approximation and based on rational
# approximations of second kind.
def verige(num, denominator_limit):
    Z = num
    C = []
    P = []
    Q = []
    
    C.append(int(mp.floor(num)))
    Z = mp.fdiv(1, mp.frac(Z))
    C.append(int(mp.floor(Z)))
    
    P.append(C[0])
    P.append(C[0]*C[1] + 1)
    Q.append(1)
    Q.append(C[1])
    
    for k in range(2, 1000000):
        Z =  mp.fdiv(1, mp.frac(Z))
        C.append(int(mp.floor(Z)))

        if Q[-1] > denominator_limit:
            break
        
        P.append(C[k] * P[k-1] + P[k-2])
        Q.append(C[k] * Q[k-1] + Q[k-2])

        
        
    return C, P, Q

# Finds continued fraction for given fraction. 
def find_continued_fraction(fraction):
    """
    Finds a continued fraction of a given fraction. Fraction is
    given as a list where first element is the numerator and the
    second one is denominator.
    """

    assert len(fraction)==2

    [p, q] = fraction
    
    a0 = p // q
    r1 = p % q
    res = [a0]
    
    if r1 == 0:
        return res
    
    a1 = q // r1
    r2 = q % r1

    res.append(a1)

    while not r2 == 0:
        res.append(r1 // r2)
        r3 = r1 % r2
        r1, r2 = r2, r3

    return res

# Returns all approximations.
def find_all_approx(num, N, M):
    
    C, P, Q = verige(num, M)

    res = []
    
    for i in range(1, len(C)):
        m = C[i]
        a1 = P[i-1]
        b1 = Q[i-1]
        a0 = 1
        b0 = 0
        if i > 1:
            a0 = P[i-2]
            b0 = Q[i-2]
        
        d1 = difference(num, a1, b1)
        #print("Verizna: ", a1, "/", b1)
        if b1 >= N and b1 <= M:
            res.append([a1, b1, 1, d1])

        if b1 > M:
            break
        
        for j in range(1, m):
            a2 = a0 + j*a1
            b2 = b0 + j*b1
            
            d2 = difference(num, a2, b2)
            
            if d1 < d2:
                continue
            d1 = d2
            #print("Medjuverizna: ", a2 , "/", b2)
            if b2 >= N and b2 <= M:
                res.append([a2, b2, 0, d2])
            if b2 > M:
                break

    return res


def format_results(num, n, m, sort):

    res = find_all_approx(num, n, m)

    if sort == 1:
        res.sort(key=lambda x: x[3])

    ret = []
    for r in res:
        star = ""
        frac = [r[0], r[1]]
        verige = find_continued_fraction(frac)
        if r[2] == 1:
            star = "*"
        ret.append([ str(frac[0]) + r"/" + str(frac[1]) + "    " + str(verige) + star, mp.nstr(r[3]) ])

    return ret
