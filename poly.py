from functools import reduce
from fractions import Fraction
import fractions, numbers
import math

def gcd_2(m,n):
    if n==0:
        return m
    r = m%n
    return(abs(gcd(n,r)))

def gcd(*args):
    return reduce(math.gcd, args)

def lcm_2(m,n):
    """
    Returns the least common multiple of integers m and n
    if one is zero, it returns 0
    
    return a non-negative number
    """
    if all((m,n)):
        return m*n//gcd_2(m,n)
    
    # else, return the non-zero
    # unless both zero, in which case return 0
    zero, non_zero = (m,n) if m==0 else (n,m)
    return zero

def lcm(*args):
    return reduce(lcm_2, args)

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

def padZrs(tup, pad_length):
    """
    increase length to 'pad_length' with zeroes
    """
    
    if pad_length < len(tup):
        raise ValueError("can't reduce length with padding")
    
    extra_zrs = pad_length - len(tup)
    if extra_zrs == 0:
        return tup
    
    return tuple(list(tup)+([0]*extra_zrs))

class frozendict(dict):
    """
    dict without setters and with hashes
    """
    
    hash_base = 522340537264
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args,**kwargs)
        self._hash = None
        self._frozen = True

        
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
        if self._frozen:
            raise TypeError("'frozendict' object doesn't support item assignment")
        else:
            super().__setitem__(key, new_value)
    
    def freez(self):
        self._frozen = True
    
    def thaw(self):
        self._frozen = False


class Prod(tuple):
    """
    Represents a product of variables
    (1,2,3)-->x*y^2*z^3
    """
    
    def __init__(self, *args, **kwargs):
        
        super().__init__()
        
        # throw exception if the last element is zero (and not a constant)
        self.length = len(self)
        if self[-1] == 0 and self.length>1:
            msg = str.format('Cannot create `Prod` with terminal zero: {}', self)
            raise ValueError(msg)
        
    
    def __mul__(self, other):
        
        if self.length == other.length:
            return Prod(self[i] + other[i] for i in range(self.length))
        
        longer, shorter = (self, other) if (self.length > other.length) else (other, self)

        res = list(longer)
        
        for i in range(shorter.length):
            res[i] += shorter[i]

        return Prod(res)
        
    def __truediv__(self, other):
    
        if self.length == other.length:
            return Prod(stripTrZs([self[i] - other[i] for i in range(self.length)]))

        longer, shorter = (self, other) if (self.length > other.length) else (other, self)
        res = list(longer)
        if longer is self:
            for i in range(shorter.length):
                res[i] -= shorter[i]
        
        else:
            for i in range(shorter.length):
                res[i] = shorter[i] - longer[i]
            for i in range(shorter.length, longer.length):
                res[i] =- longer[i]

        return Prod(res)

    @classmethod
    def lcm(cls, t1, t2):
        res = []
        for i in range(max(len(t1), len(t2))):
            try:
                res.append(t1[i])
            except IndexError:
                res.append(0)
            
            try:
                if t2[i] > res[-1]:
                    res[-1] = t2[i]
            except IndexError:
                pass
        
        return Prod(res)

class RingElementMeta(type):
    """
    metaclass for elements of which there is only one instence per
    equivalence set (that is of two instances are equal, they are the same)
    """
    def __call__(self, *args, **kwargs):
        obj = Poly.__new__(Poly, *args, **kwargs)
        return obj
        

class Poly(metaclass=RingElementMeta):
    """
    Class representing polynomial.  Initialized with dictionary representing the polynomial in sumOfProds form:
        12 - 4x^2y + 6xy^3 --> {(0,0):12, (2,1):-4, (1,3):6}
        0 --> Poly()
    """
    
    _instances = {}
    _zero_terms = {(0,):0}
    _rings = ["real", "frac", None]
    
    @classmethod
    def mul_terms(cls, terms1, terms2):
        """
        returns new dictionary of the product
        """
        
        new_terms = {}
        
        for t1 in terms1.keys():
            for t2 in terms2.keys():
                t3 = t1 * t2
                value = terms1[t1]*terms2[t2]
                new_terms[t3] = new_terms.get(t3, 0) + value
        
        removeZeros(new_terms)
        return new_terms
    
    @classmethod
    def add_terms(cls, terms1, terms2, extend=False):
        """
        retursn the dict of the sum
        
        Extend: if true will exted terms1 with the result and not return a new dictionary
        """
        
        if extend:
            new_terms = terms1
        else:
            new_terms = dict(terms1)
        
        for t2 in terms2:
            new_terms[t2] = new_terms.get(t2, 0) + terms2[t2]
        
        removeZeros(new_terms)
        return new_terms
    
    @classmethod
    def sub_terms(cls, terms1, terms2, extend=False):
        """
        retursn dict of diff, terms1 - terms2
        
        Extend: if true will exted terms1 with the result and not return a new dictionary
        """
        
        if extend:
            new_terms = terms1
        else:
            new_terms = dict(terms1)
        
        for t2 in terms2:
            new_terms[t2] = new_terms.get(t2, 0) - terms2[t2]
        
        removeZeros(new_terms)
        return new_terms
    
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
        
        check = kwargs.get("check", True)
        if check:
            if not(isinstance(terms, frozendict)):
                for key in list(terms.keys()):
                    if isinstance(key, Prod):
                        continue
                    else:
                        new_key = Prod(key)
                        value = terms.pop(key)
                        terms[new_key] = value
        
        
        ring = kwargs.get("ring", None)
        fterms = frozendict(terms)
        if (fterms, ring) in Poly._instances:
            return Poly._instances[(fterms, ring)]
        
        new = super().__new__(cls)
        new.__init__(fterms, **kwargs)
        
        Poly._instances[(fterms, ring)] = new
        return new
    
    def __init__(self, terms, ring=None, check=True):
    
        """
        should put more expensive stuff here, since I go out of my way to minimize number of calls
        
        In the future, more support for different types of rings. Now specifying none along with 
        integer (or Fraction) coefficients means it will convert all the coeffs to Fraction objects
        to de exact arithmetic.
        
        If "real" is specified, the coeffs are letf alone, which might improve the speed of certain
        computations
        
        check: if True, will run a type check (and conversions) on the coefficients. If False, will
        assume they are correct.
        """
        
        self.terms = terms
        self._lead = None
        self._sorted_terms = None
        self.nVars = max(len(tup) for tup in terms.keys())
        self.isConstant = False 
        self.value = None

        if len(self.terms) == 1 and (0,) in self.terms:
            self.isConstant = True
            self.value = self.terms[(0,)]
        
        if ring not in Poly._rings:
            msg = str.format("Specified ring not supported: '{}'.", ring)
            raise ValueError(msg)
        
        self.ring = ring
        
        if check:
            if ring is None:
                self.terms.thaw()
                if all(isinstance(coeff, numbers.Rational) for coeff in self.terms.values()):
                    for term in self.terms:
                        self.terms[term] = Fraction(self.terms[term])
                else:
                    for term in self.terms:
                        self.terms[term] = float(self.terms[term])
                self.terms.freez()
            
            if ring is "real":
                self.terms.thaw()
                for term in self.terms:
                    self.terms[term] = float(self.terms[term])
                self.terms.freez()

    def __radd__(self, other):
        return self.__add__(other)
    
    def __add__(self, other):
        """
        produce new polynomial
        """
        
        other = Poly(other)
        if not all([self.ring, other.ring]):
            new_ring = self.ring if self.ring else other.ring

        return Poly(Poly.add_terms(self.terms, other.terms), ring = new_ring, check = False)

    def __rsub__(self, other):
        return self.__sub__(other) * -1

    def __sub__(self, other):
        """
        produce new polynomial
        """
        other = Poly(other)
        if not all([self.ring, other.ring]):
            new_ring = self.ring if self.ring else other.ring
        return Poly(Poly.sub_terms(self.terms, other.terms), ring=new_ring, check = False)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        """
        produce new polynomial
        """
        other = Poly(other)
        if not all([self.ring, other.ring]):
            new_ring = self.ring if self.ring else other.ring
        
        else:
            # maybe add coersion?
            msg = str.format("Can't multiply polys in rings {} and {}.", self.ring, other.ring)
            raise ValueError(msg)
        
        return Poly(Poly.mul_terms(self.terms, other.terms), ring = new_ring, check = False)
    
    def __divmod__(self, other):
        """
        reduce self by other, producing a quotient and remainder
        """
        
        working_terms = dict(self.terms)
        q_terms = {Prod((1,)):0}
        
        break_now = False
        while True:
            break_now = True
            for term in reversed(sorted(working_terms.keys())):
                factor = term/other.lead
                if all(x >=0 for x in factor):
                    coeff  = working_terms[term]/other.terms[other.lead]
                    Poly.add_terms(q_terms, {factor: coeff}, extend=True)
                    Poly.sub_terms(working_terms, Poly.mul_terms({factor: coeff}, other.terms), extend=True)
                    
                    break_now = False
                    break
            
            if break_now:
                break
        
        return (Poly(q_terms, check = False), Poly(working_terms, check = False))
    
    def leadReduce(self, other):
        """
        applies the reduction only to the leading term
        self/other -> (quotient, remainder)
        """
        
        working = self
        q = Poly({(1,):0})
        
        
        while all(x >=0 for x in working.lead/other.lead):
            factor = working.lead / other.lead
            coeff = working.terms[working.lead]/other.terms[other.lead]

            q += Poly({factor:coeff})
            working = self - q*other

        return (q, working)
    
    def __mod__(self, other):
        """
        returns the remainder from divmod
        """
        
        (q,r) = divmod(self,other)
        return r
    
    def __eq__(self, other):
        return self is Poly(other)
    
    def __pow__(self, n):
        """
        Simple implementation of fast power raising
        Poly really should inherit from Element from the algebra project ...
        """
        if (type(n) != int and type(n) != long) or (n<0):
            raise TypeError(str.format("Can't raise element to {}.\n Must be non-negative integer.",n))
        
        bin_pow = format(n,'b')[::-1]
        prod_terms = {Prod((0,)):1} # start with the identity
        square_terms = {Prod((0,)):1}
        mask = 1
        while mask <= n:
            bit = n & mask
            if square_terms == {(0,):1}:
                square_terms = self.terms
            else:
                square_terms = Poly.mul_terms(square_terms, square_terms)
            if bit != 0:
                prod_terms = Poly.mul_terms(prod_terms, square_terms)
            mask <<= 1
        return Poly(prod_terms, check=False)
    
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
        
        return " + ".join([str(self.terms[key])+" "+ _strKey(key) for key in self.sorted_terms])
    
    def __abs__(self):
        if self.isConstant:
            return abs(self.value)
        else:
            return self
    
    def __neg__(self):
        return self*-1
    
    @classmethod
    def multiPow(cls, multi_var, multi_pow):
        """
        raise a multivariable to a multipower
        (2,4,5,2), (1,3,0,5) -> 2**1 * 4**3 * 5**0 * 2**5
        None is provided for variables which are to stay as variables
        multi_var is padded with None's if it is shorter
        multi_pow is padded with zeroes if it is shorter
        """
        
        coeff = 1
        pows_left = list(multi_pow)
        for i in range(min(len(multi_pow), len(multi_var))):
            if multi_var[i] is not None:
                coeff *= multi_var[i]**multi_pow[i]
                pows_left[i] = 0
        
        # we multiply the coeff on the outside in case it is not a number but a Poly
        if pows_left[-1] == 0 and len(pows_left) > 1:
            pows_left = stripTrZs(pows_left)
        return Poly({Prod(pows_left):1}, check=False) * coeff

    def __call__(self, *args):
        res = 0
        for term in self.terms:
            res += self.multiPow(args, term) * self.terms[term]
        
        return res
    
    @property
    def lead(self):
        """
        return leading term
        """
        if self._lead is None:
            self._lead = self.sorted_terms[0]
        return self._lead
    
    @property
    def sorted_terms(self):
        """
        list of terms in grvlex ordering
        """
        if self._sorted_terms is None:
            pad_length = max(len(x) for x in self.terms.keys())
            def key_func(key_tuple):
                return (sum(key_tuple), tuple(-x for x in padZrs(key_tuple, pad_length)[::-1]))
        
        
            self._sorted_terms = sorted(self.terms.keys(), key=key_func, reverse=True)
        return self._sorted_terms
    
    def scale_int(self):
        """
        if the ring is real, don't do anything?
        return this polynomial scaled so all coeffs are integers
        """
        
        if self.ring == "real":
            raise ValueError("what are you even doing? Trying to scale real values to integers...")
       
        nums = [coeff.numerator for coeff in self.terms.values()]
        denoms = [coeff.denominator for coeff in self.terms.values()]
        
        
        scale_factor = Fraction(lcm(*denoms), gcd(*nums))
        if scale_factor == 1:
            return self
        return self*scale_factor
        

##########################################
#
#   now import extras so "import poly" imports the whole package
#
##########################################

from poly_algebra import *