from poly import *

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
    new_polys = []
    i_old = 0 # reduces redundant pair checks
    while True:
        # append new polys
        polys.extend(new_polys)
        new_polys[:] = []
        
        # compute normal forms and remainders for all pairs
        for i in range(i_old + 1, len(polys)):
            for j in range(0, i):
                
                normal_form = normalForm(polys[i], polys[j])
                (q,r) = divmodSet(normal_form, polys, leadReduce=False)
                
                if r != 0:
                    new_polys.append(r)
                    
        i_old = i
        if not new_polys:
            # guarenteed to break by Hilbert's Basis theorem... Woo!
            break
    
    return polys