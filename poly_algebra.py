from poly import *
from itertools import combinations

def divmodSet(numerator, basis, leadReduce=False):
    """
    Apply euclidean division to divide `p` by the polynomials in `basis`
    Returns (quotient, remainder):
        quotient: the factor for each polynomial in `basis`, in the order of `basis`
        remainder: the remainder
    """
    q_list = [0]*len(basis)
    for i in range(len(basis)):
        if leadReduce:
            (q,numerator) = numerator.leadReduce(basis[i])
        else:
            (q,numerator) = divmod(numerator, basis[i])
        q_list[i] = q
        if numerator == 0:
            break
    
    # list of quotients, and the remainder
    return (q_list, numerator)

def reduceList(polys, trim=True, except_last=False):
    """
    reduces each polynomial by the others.
    Trim: if true removes polynomials that reduce to zero
    except_last: if true, treats the last as already reduced
    """
    if len(polys) <= 1:
        return polys
    print(len(polys))
    offset = 0
    if except_last:
        offset = 1

    remainders = []
    for i in range(len(polys) - offset):
        temp_basis = remainders + polys[i+1:]
        (q,r) = divmodSet(polys[i], temp_basis, leadReduce=False)
        if (r != 0) or (not trim):
            remainders.append(r)
    
    remainders.extend(polys[i+1:])
    
    return remainders

def normalForm(p1, p2):
    """
    copmute m1*p1 - m2*p2, where m1 and m2 are the smallest monomials such that the leading terms of
    m1*p1 and m2*p2 cancel, leaving us only with the lower order stuff
    """
    
    # first, compute the lcm of the leading terms
    lcm_leading_terms = Prod.lcm(p1.lead, p2.lead)

    # then, the smalles possible monomials
    m2 = Poly({lcm_leading_terms/p2.lead : 1})
    m1 = Poly({lcm_leading_terms/p1.lead : 1})
            
    return m1*p1 - m2*p2

def groebnerBasis(*args):
    """
    compute a groebnerBasis from the polynomials in args via Buchberger's algorithm
    """
    polys = list(args)
    if len(polys) == 1:
        return polys
    polys = reduceList(polys)
    new_polys = []
    i_old = 0 # reduces redundant pair checks

    while True:
        all_done = True
        for (p1, p2) in combinations(polys, 2):
            normal_form = normalForm(p1, p2)
            (q,r) = divmodSet(normal_form, polys)
            if r != 0:
                polys.append(r)
                polys = reduceList(polys, except_last=True)
                all_done = False
                break
        
        if all_done:
            break
    
    return polys