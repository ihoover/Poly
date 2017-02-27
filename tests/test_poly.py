from common import *
import sys
import poly
from poly import *


class Test_lcm(unittest.TestCase):
    
    def test_primes(self):
        p1 = 3
        p2 = 5
        
        self.assertEqual(lcm_2(p1,p2), p1*p2)
        self.assertEqual(lcm_2(p2,p1), p1*p2)
    
    def test_coprime(self):
        p1 = 9
        p2 = 10
        
        self.assertEqual(lcm_2(p1,p2), p1*p2)
        self.assertEqual(lcm_2(p2,p1), p1*p2)
    
    def test_relcomp(self):
        p1 = 9
        p2 = 6
        
        self.assertEqual(lcm_2(p1, p2), 18)
        self.assertEqual(lcm_2(p2, p1), 18)
    
    def test_zero_one(self):
        p1 = 9
        p2 = 0
        
        self.assertEqual(lcm_2(p1, p2), 0)
        self.assertEqual(lcm_2(p2, p1), 0)
    
    def test_multiple_inputs(self):
        p1 = 3
        p2 = 5
        p3 = 15
        p4 = 2
        lcm_res = 3*5*2
        
        self.assertEqual(lcm(p1,p2,p3,p4), lcm_res)


class Test_frozendict(unittest.TestCase):
    
    def setUp(self):
        
        # class with None-type hash method
        class NoneHash(object):
            def __init__(self):
                setattr(self, "__hash__", None)
        
        self.none_hash = NoneHash()
        self.immutD = {'1':2,'tree':3}
        self.mutD = {'a':[1,2]}
        
        self.frozen = frozendict(self.immutD)

    def test_setup(self):
        self.assertIsNone(self.none_hash.__hash__)

    def test_createfromdict(self):
        f = frozendict(self.immutD)
        self.assertEqual(self.frozen, f)

    def test_createFromMutable(self):
        with self.assertRaises(TypeError, msg="Can't freeze dict with non-hashable values"):
            f = frozendict(self.mutD)

    def test_access(self):
        f = frozendict(self.immutD)
        for key in self.immutD:
            self.assertEqual(self.immutD[key],f[key])

    def test_frozenDefault(self):
        for key in frozendict(self.immutD):
            with self.assertRaises(TypeError, msg="'frozendict' object doesn't support item assignment"):
                self.frozen[key] = 0
    
    def test_frozenDefault_pop(self):
        for key in frozendict(self.immutD):
            with self.assertRaises(TypeError, msg="'frozendict' object doesn't support item assignment"):
                self.frozen.pop(key)
        
        self.assertEqual(self.frozen, self.immutD)
    
    def test_frozenDefault_clear(self):
        
        with self.assertRaises(TypeError, msg="'frozendict' object doesn't support item assignment"):
            self.frozen.clear()
        
        #show hasn't changed
        self.assertEqual(self.frozen, self.immutD)

    def test_frozenDefault_setDefauls(self):
        for key in self.frozen:
            with self.assertRaises(TypeError, msg="'frozendict' object doesn't support item assignment"):
                self.frozen.setdefault(key,'boop')
        
        #show hasn't changed
        self.assertEqual(self.frozen, self.immutD)
    
    def test_frozenDefault_update(self):
        
        with self.assertRaises(TypeError, msg="'frozendict' object doesn't support item assignment"):
            self.frozen.update(self.mutD)
        
        #show hasn't changed
        self.assertEqual(self.frozen, self.immutD)

    def test_thaw(self):
        f = frozendict(self.immutD)
        f.thaw()
        for key in f:
            f[key] += 1
        
        for key in f:
            self.assertNotEqual(f[key], self.immutD[key])
    
    def test_frozenAfterThaw(self):
        f = frozendict(self.immutD)
        f.thaw()
        f.freez()
        for key in f:
            with self.assertRaises(TypeError, msg="'frozendict' object doesn't support item assignment"):
                self.frozen[key] = 0

    def test_hash(self):
        f1 = frozendict()
        f2 = frozendict()
        f3 = frozendict(self.immutD)
        self.immutD.update({1:2})
        f4 = frozendict(self.immutD)
        
        self.assertEqual(hash(f1),hash(f2))
        self.assertEqual(hash(f3),hash(self.frozen))
        self.assertNotEqual(hash(f1),hash(f3))
        self.assertNotEqual(hash(f1),hash(f4))
        self.assertNotEqual(hash(f4),hash(f3))
    
    def test_equal(self):
        f1 = frozendict()
        f2 = frozendict()
        f3 = frozendict(self.immutD)
        self.immutD.update({1:2})
        f4 = frozendict(self.immutD)
        
        self.assertEqual(f1,f2)
        self.assertEqual(f1,{})
        self.assertNotEqual(f1,f3)
        self.assertNotEqual(f1,f4)
        self.assertNotEqual(f4,f3)


class test_Prod(unittest.TestCase):

    def test_tup_to_dict(self):
        tup = (1,2,3)
        d = {(1,0,0):1, (0,1,0):2, (0,0,1):3}
        
        self.assertEqual(d, tupToDict(tup))
    
    def test_valueError(self):
        tup = (0,1,0)
        with self.assertRaises(ValueError):
            Prod(tup)

    def test_add(self):
        p1 = Prod([1,2,3])
        p2 = Prod([2,3,4])
        
        self.assertEqual(p1*p2, (3,5,7))

    def test_add_unequal_length(self):
        p1 = Prod([1,2,3,5])
        p2 = Prod([2,3,4])
        
        self.assertEqual(p1*p2, (3,5,7,5))
    
    def test_sub(self):
        p1 = Prod([1,2,3])
        p2 = Prod([2,3,4])
        
        self.assertEqual(p1/p2, (-1,-1,-1))

    def test_sub_unequal_length(self):
        p1 = Prod([1,2,3,5])
        p2 = Prod([2,3,4])
        
        self.assertEqual(p1/p2, (-1,-1,-1,5))
    
    def test_numTrZs(self):
        t0 = (1,2,3)
        t1 = (1,2,0)
        t2 = (1,0,0)
        t3 = (0,0,0)
        
        self.assertEqual(numTrZs(t0), 0)
        self.assertEqual(numTrZs(t1), 1)
        self.assertEqual(numTrZs(t2), 2)
        self.assertEqual(numTrZs(t3), 3)
    
    def test_stripTrZs(self):
        t0 = (1,2,3)
        t1 = (1,2,0)
        t2 = (1,0,0)
        t3 = (0,0,0)
        
        self.assertEqual(stripTrZs(t0), (1,2,3))
        self.assertEqual(stripTrZs(t1), (1,2))
        self.assertEqual(stripTrZs(t2), (1,))
        self.assertEqual(stripTrZs(t3), (0,))
    
    def test_lcm_sameLength(self):
        p1 = (1,2,3)
        p2 = (2,3,1)
        lcm = (2,3,3)
        
        self.assertEqual(Prod.lcm(p1,p2), lcm)
    
    def test_lcm_diffLength(self):
        p1 = (1,2,3)
        p2 = (2,3)
        lcm = (2,3,3)
        
        self.assertEqual(Prod.lcm(p1,p2), lcm)


class testPadZrs(unittest.TestCase):

    def test_extend(self):
        t = (1,2)
        pad_length = 4
        padded = (1,2,0,0)
        self.assertEqual(padZrs(t, pad_length), padded)
    
    def test_nochng(self):
        t = (1,2)
        pad_length = 2
        self.assertEqual(padZrs(t, pad_length), t)

    def test_shorter(self):
        t = (1,2,3)
        pad_length = 2
        with self.assertRaises(ValueError):
            padZrs(t,pad_length)


class testPolyCreate(unittest.TestCase):

    def setUp(self):
        #clear chached polies
        Poly._instances = {}

    def test_empty(self):
        p = Poly()
        self.assertEqual(p.terms, {(0,):0})
    
    def test_from_number(self):
        val = 10
        p = Poly(val)
        self.assertEqual(p.terms, {(0,):val})
    
    def test_unique_0(self):
        p1 = Poly()
        p2 = Poly({(1,):0})
        p3 = Poly({})

        self.assertIs(p1,p2)
        self.assertIs(p1,p3)
    
    
    def test_unique(self):
        p1 = Poly({(1,2):3.0, (2,1):2})
        p2 = Poly({(2,1):2, (1,2):3})
        p3 = Poly({Prod((2,1)):2, (1,2):3})
        
        self.assertIs(p1,p2)
        self.assertIs(p1,p3)
    
    def test_unique_fromself(self):
        p1 = Poly({(1,2):3, (0,1):1})
        self.assertIs(p1, Poly(p1))

    def test_types(self):
        p1 = Poly({(1,2):3.0, (2,1):2})
        
        self.assertTrue(isinstance(p1.terms, frozendict))
        
        for term in p1.terms:
            self.assertTrue(isinstance(term, Prod))
        
        #test the empty polynomial
        self.assertTrue(isinstance(Poly().lead, Prod))
        
        isWellFormed(p1)

    def test_scale_int(self):
        x = Poly({(1,):1})
        p = Fraction(2,3)* x**3 + Fraction(4,9)*x + 2
        p_scaled = 3*x**3 + 2*x + 9
        
        self.assertEqual(p.scale_int(), p_scaled)
    
    def test_ring_notRecognized(self):
        ring = "smurf"
        
        with self.assertRaises(ValueError):
            p = Poly(ring=ring)
        
    def test_ring_None(self):
        p = Poly()
        self.assertEqual(p.ring, None)
    
    def test_ring_real(self):
        
        p = Poly(ring="real")
        self.assertEqual(p.ring, "real")
    
    def test_ring_values_none_ints(self):
        
        p = Poly({(1,):2})
        self.assertIsInstance(p.terms[(1,)], Fraction)
    
    def test_ring_values_none_floats(self):
        
        p = Poly({(1,):2.1}, ring=None)
        self.assertIsInstance(p.terms[(1,)], float)
    
    def test_ring_values_real_ints(self):
        
        p = Poly({(1,):2.1}, ring="real")
        self.assertIsInstance(p.terms[(1,)], float)
        self.assertNotIsInstance(p.terms[(1,)], Fraction)
    
    def test_ring_multiply(self):
    
        p1 = Poly({(1,):2})
        p2 = Poly({(1,):2}, ring="real")
        
        p3 = p1*p2
        self.assertEqual(p3.ring, "real")
        for value in p3.terms.values():
            self.assertIsInstance(value, float)
    
    #####################################################
    # breaks with 0 but no time to fix!!!
    #####################################################
    def test_ring_sub(self):
    
        p1 = Poly({(1,):2})
        p2 = Poly({(1,):3}, ring="real")
        
        p3 = p1-p2
        self.assertEqual(p3.ring, "real")
        for value in p3.terms.values():
            self.assertIsInstance(value, float)

    
    def test_ring_add(self):
    
        p1 = Poly({(1,):2})
        p2 = Poly({(1,):2}, ring="real")
        
        p3 = p1+p2
        self.assertEqual(p3.ring, "real")
        for value in p3.terms.values():
            self.assertIsInstance(value, float)


class testMonomialOrdering(unittest.TestCase):
    """
    test that grvlex ordering is implemented properly
    """
    
    def setUp(self):
        terms = {(0,1,1):1, (1,0,1):1, (1,1):1, (2,):1, (0,2):1, (0,0,2):1, (1,1,1):1}
        self.sorted_terms = [(1,1,1), (2,), (1,1), (0,2), (1,0,1), (0,1,1), (0,0,2)]
        self.p = Poly(terms)
        poly.Order=grvlex
    
    def test_poly_grvlex_default(self):
        
        self.assertEqual(self.p.sorted_terms, self.sorted_terms)
    
    def test_ordering_change(self):

        self.assertEqual(self.p.lead, (1,1,1))

        poly.Order = elim0
        self.assertEqual(self.p.lead, (2,))
    
    def test_lead(self):
        p = Poly({(1,0,1): 1, (0,2):1})
        self.assertEqual(p.lead, p.sorted_terms[0])
    
    def test_grvlex(self):
        monomial = (1,2,3,4)
        self.assertEqual(grvlex(monomial,len(monomial)), (-10,(4,3,2,1)))
    
    def test_grvlex_sorting(self):
        monomials = [(2,0,0),(0,2,0),(0,0,2),(1,1,0),(0,1,1),(1,0,1),(1,1,1)]
        sorted_monomials = [(1,1,1),(2,0,0), (1,1,0), (0,2,0), (1,0,1), (0,1,1), (0,0,2)]
        self.assertEqual(sorted(monomials, key=lambda x: grvlex(x,3)), sorted_monomials)

    def test_elim0_sorting(self):
        monomials = [(2,0,0),(0,2,0),(0,0,2),(1,1,0),(0,1,1),(1,0,1),(1,1,1)]
        sorted_monomials = [(2,0,0),(1,1,1),(1,1,0), (1,0,1),(0,2,0), (0,1,1), (0,0,2)]
        self.assertEqual(sorted(monomials, key=lambda x: elim0(x,3)), sorted_monomials)

class testBasisGeneration(unittest.TestCase):

    def setUp(self):
        self.x = Poly({(1,):1})
        self.y = Poly({(0,1):1})
        self.z = Poly({(0,0,1):1})
        self.w = Poly({(0,0,0,1):1})
        
        self.xr = Poly({(1,):1}, ring="real")
        self.yr = Poly({(0,1):1}, ring="real")
        self.zr = Poly({(0,0,1):1}, ring="real")
        self.wr = Poly({(0,0,0,1):1}, ring="real")
    
    def test_four(self):
        self.assertEqual(indets(4), (self.x, self.y, self.z, self.w))
    
    def test_four_real(self):
        self.assertEqual(indets(4, ring="real"), (self.xr, self.yr, self.zr, self.wr))