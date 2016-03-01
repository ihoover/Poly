from functools import reduce
import math

def gcd_2(m,n):
	if n==0:
		return m
	r = m%n
	return(abs(gcd(n,r)))

def gcd(*args):
    return reduce(gcd_2, args)

def tupToDict(tup):
    """
    (a1,a2,a3,...,an) -->
    {(1,0,0,...,0):a1, (0,1,0,...,0):a2, ... ,(0,0,...,1):an}
    """
    
    def basis(i):
        base = [0]*len(tup)
        base[i] = 1
        return tuple(base)
    
    return {basis(i):tup[i] for i in range(len(tup))}

def allSwapsInnerFoil(n_vars, modP):
    """
    ge
    """
    dicts = []
    for i in range(n_vars):
        for j in range(i+1,n_vars):
            term = [0]*n_vars
            term[i] = 1
            term[j] = -1
            dicts.append(foil([tupToDict(term)]*(modP-1),modP))
    
    return dicts


def allSwaps(n_vars, neg=True):
    """
    returns all the dicts representing the polynomial
    (xi-xj) for all i<j and i,j<n_vars
    """
    
    dicts = []
    for i in range(n_vars):
        d = dict()
        for j in range(i+1,n_vars):
            term = [0]*n_vars
            term[i] = 1
            if neg:
                term[j] = -1
            else:
                term[j] = 1
            dicts.append(tupToDict(term))
    
    return dicts

def removeZeros(terms):
    """
    Remove terms that are equal to zero
    """
    
    zero_keys = []
    for k in terms:
        if terms[k]==0:
            zero_keys.append(k)
        
    for k in zero_keys:
        terms.pop(k)

def numTrZs(tup):
    """
    count the trailing zeroes of the tuple
    """
    
    all_zero = 1 #need to add one if they are all zero
    for i in range(len(tup)):
        if tup[-i-1] != 0:
            all_zero = 0
            break
    
    return i + all_zero

def stripTrZs(tup):
    """
    strip trailing zeros. Special case, all zero return (0,)
    """
    zero_tup = (0,)

    if len(tup) == 0:
        return zero_tup
    
    tr_zs = numTrZs(tup)  
    if tr_zs == 0:
        return tup
    
    if tr_zs == len(tup):
        return zero_tup 
    return tup[0:-tr_zs]

class frozendict(dict):
    """
    dict without setters and with hashes
    """
    
    hash_base = 522340537264
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args,**kwargs)
        self._hash = None

        
        # check that all values are hashable
        if any(getattr(x,"__hash__", None) is None for x in self.values()):
            raise TypeError("Can't freeze dict with non-hashable values")
    
    def __hash__(self):
        if self._hash is None:
            num = frozendict.hash_base
            for key in self:
                num ^= hash((key, self[key]))
            self._hash = num
        return self._hash
    
    def __setitem__(self, key, new_value):
        raise TypeError("'frozendict' object doesn't support item assignment")

class Prod(tuple):
    """
    Represents a product of variables
    (1,2,3)-->x*y^2*z^3
    """
    
    def __mul__(self, other):
        length = max(len(self), len(other))
        res = list(0 for i in range(length))
        
        for i in range(length):
            try:
                res[i] += self[i]
            except IndexError:
                pass
            try:
                res[i] += other[i]
            except IndexError:
                pass
        
        return Prod(res)
    
    def __truediv__(self, other):
        length = max(len(self), len(other))
        res = list(0 for i in range(length))
        
        for i in range(length):
            try:
                res[i] += self[i]
            except IndexError:
                pass
            try:
                res[i] -= other[i]
            except IndexError:
                pass
        
        return Prod(res)
    
    def __hash__(self):
        """
        changing the tuple hash function to ignore trailing zeros, so
        (1,2,3) has the same hash as (1,2,3,0,0,0)
        """
        
        return hash(tuple(stripTrZs(self)))
    
    def __eq__(self, other):
        return tuple(stripTrZs(self)) == tuple(stripTrZs(other))

class RingElement(type):
    """
    metaclass for elements of which there is only one instence per
    equivalence set (that is of two instances are equal, they are the same)
    """
    def __call__(self, *args, **kwargs):
        obj = Poly.__new__(Poly, *args, **kwargs)
        return obj
        

class Poly(metaclass=RingElement):
    """
    Class representing polynomial.  Initialized with dictionary representing the polynomial in sumOfProds form:
        12 - 4x^2y + 6xy^3 --> {(0,0):12, (2,1):-4, (1,3):6}
        0 --> Poly()
    """
    
    _instances = {}
    _zero_terms = {(0,):0}
    
    def __new__(cls, *args, **kwargs):
        
        
        if (len(args) < 1):
            terms = Poly._zero_terms
        else:
            terms = args[0]
        
        if isinstance(terms, Poly):
            return terms
        
        # assume (it acts like) a number if not a dict (catch None)
        if not(isinstance(terms, dict)) and not(terms is None):
            terms = {(0,):terms}
        
        if (not terms) or (all(terms[key] == 0 for key in terms)):
            terms = Poly._zero_terms

        if not(isinstance(terms, frozendict)):
            for key in list(terms.keys()):
                if isinstance(key, Prod):
                    continue
                else:
                    new_key = Prod(key)
                    value = terms.pop(key)
                    terms[new_key] = value
        
        fterms = frozendict(terms)
        if fterms in Poly._instances:
            return Poly._instances[fterms]
        
        new = super().__new__(cls)
        new.__init__(fterms, **kwargs)
        Poly._instances[fterms] = new
        return new
    
    def __init__(self, terms):
        
        self.terms = terms
        self._lead = None
        self.nVars = max(len(tup) for tup in terms.keys())
        # self.isZero = 

    def __radd__(self, other):
        return self.__add__(other)
    
    def __add__(self, other):
        """
        produce new polynomial
        """
        other = Poly(other)
        newTerms = dict(self.terms)
        
        for key in other.terms:
            if key in newTerms:
                newTerms[key] += other.terms[key]
            else:
                newTerms[key] = other.terms[key]
        removeZeros(newTerms)
        return Poly(newTerms)

    def __rsub__(self, other):
        return self.__sub__(other) * -1

    def __sub__(self, other):
        """
        produce new polynomial
        """
        other = Poly(other)
        newTerms = dict(self.terms)
        
        for key in other.terms:
            if key in newTerms:
                newTerms[key] -= other.terms[key]
            else:
                newTerms[key] = -other.terms[key]
        
        removeZeros(newTerms)
        return Poly(newTerms)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        """
        produce new polynomial
        """
        
        newTerms = {}
        
        # convert to Poly if it isn't (assumed to be a number in that case)
        other = Poly(other)
        
        for t1 in self.terms.keys():
            for t2 in other.terms.keys():
                t3 = t1 * t2
                # t3 = Prod(addTuples(t1,t2))
                value = self.terms[t1]*other.terms[t2]
                
                if t3 in newTerms:
                    newTerms[t3] += value
                else:
                    newTerms[t3] = value

        removeZeros(newTerms)
        return Poly(newTerms)
        
    def __divmod__(self, other):
        """
        polynomial long division
        self/other -> (quotient, remainder)
        """
        
        working = self
        q = Poly({(1,):0})
        # import pdb; pdb.set_trace()
        while all(x >=0 for x in working.lead/other.lead):
            factor = working.lead / other.lead
            coeff = working.terms[working.lead]/other.terms[other.lead]

            q += Poly({factor:coeff})
            working = self - q*other

        return (q, working)
    
    def __eq__(self, other):
        return self is Poly(other)
    
    def __pow__(self, n):
        """
        Simple implementation of fast power raising
        THis really should inherit from Element from the algebra project ...
        """
        if (type(n) != int and type(n) != long) or (n<0):
            raise TypeError(str.format("Can't raise element to {}.\n Must be non-negative integer.",n))
        
        bin_pow = format(n,'b')[::-1]
        prod = 1 # start with the identity
        square = prod
        mask = 1
        while mask <= n:
            bit = n & mask
            if square == 1:
                square = self
            else:
                square = square * square
            if bit != 0:
                prod = prod * square
            mask <<= 1
        return prod
    
    def __repr__(self):
        return "Poly:[" + self.__str__() + "]"
    
    def __str__(self):
        
        ys = ['y'+str(i+1) for i in range(self.nVars)]
        
        def _strKey(key):
            res = ""
            for i in range(len(key)):
                if key[i] != 0:
                    if key[i] > 1:
                        res += ys[i]+'^'+str(key[i])
                    else:
                        res += ys[i]
            
            return res
        
        return " + ".join([str(self.terms[key])+" "+ _strKey(key) for key in sorted(list(self.terms.keys()))])
    
    @property
    def lead(self):
        """
        return leading term
        """
        if self._lead is None:
            self._lead = Prod(sorted(self.terms.keys())[-1])
        return self._lead