import unittest
import sys
from poly import *


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

    def test_noChange(self):
        for key in self.frozen.keys():
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
    
    def test_numTrZs(self):
        t0 = (1,2,3)
        t1 = (1,2,0)
        t2 = (1,0,0)
        t3 = (0,0,0)
        
        self.assertEqual(stripTrZs(t0), (1,2,3))
        self.assertEqual(stripTrZs(t1), (1,2))
        self.assertEqual(stripTrZs(t2), (1,))
        self.assertEqual(stripTrZs(t3), (0,))
        
    def test_hash(self):
        p1 = Prod((1,2,3,0))
        p2 = Prod((1,2,3))
        p3 = Prod((1,2,0))
        
        self.assertEqual(hash(p1), hash(p2))
        self.assertNotEqual(hash(p1), hash(p3))

class test_poly(unittest.TestCase):

    def test_empty(self):
        p = Poly()
        self.assertEqual(p.terms, {(0,):0})
    
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
    
    def test_types(self):
        p1 = Poly({(1,2):3.0, (2,1):2})
        
        self.assertTrue(isinstance(p1.terms, frozendict))
        
        for term in p1.terms:
            self.assertTrue(isinstance(term, Prod))

    def test_add(self):
        # x^2 + y^2
        p1 = Poly({(2,0):1, (0,2):1})
        
        # xy + y^2
        p2 = Poly({(1,1):1, (0,2):1})
        
        # x^2 + xy + 2y^2
        result = {(2,):1, (0,2):2, (1,1):1}
        
        self.assertEqual(result, (p1+p2).terms)
    
    def test_sub(self):
        # x^2 + y^2
        p1 = Poly({(2,0):1, (0,2):1})
        
        # xy + y^2
        p2 = Poly({(1,1):1, (0,2):1})
        
        # x^2 - xy
        result = {(2,):1, (1,1):-1}
        
        self.assertEqual(result, (p1-p2).terms)
    
    def test_mul(self):
        # x^2 + y^2
        p1 = Poly({(2,0):1, (0,2):1})
        
        # xy + y^2
        p2 = Poly({(1,1):1, (0,2):1})
        
        # x^3y + xy^3 + x^2y^2 + y^4
        result = {(3,1):1, (1,3):1, (2,2):1, (0,4):1}
        
        self.assertEqual(result, (p1*p2).terms)
    
    def test_mul_cancel(self):
        # x^2 + y^2
        p1 = Poly({(2,0):1, (0,2):1})
        
        # x^2 - y^2
        p2 = Poly({(2,0):1, (0,2):-1})
        
        # x^4 - y^4
        result = {(4,):1, (0,4):-1}
        
        self.assertEqual(result, (p1*p2).terms)
    
    def test_mul_diffLen(self):
        # x^2
        p1 = Poly({(2,):1})
        
        # xy + y^2
        p2 = Poly({(1,1):1, (0,2):1})
        
        # x^3y + x^2y^2
        result = {(3,1):1, (2,2):1}
        
        self.assertEqual(result, (p1*p2).terms)

    def test_div_single_remainder(self):
        # x^2 + 1
        p1 = Poly({(2,):1, (0,):1})
        
        # x
        p2 = Poly({(1,):1})
        
        # (x, 1)
        q = p2
        r = Poly({(0,):1})
        
        self.assertEqual(divmod(p1,p2), (q,r))
        
    def test_div_single_remainderII(self):
        # x^3 + x
        p1 = Poly({(3,):1, (1,):1})
        
        # x+1
        p2 = Poly({(1,):1, (0,):1})
        
        # (x, 1)
        q = Poly({(2,):1, (1,):-1, (0,):2})
        r = Poly({(0,):-2})
        
        self.assertEqual(divmod(p1,p2), (q,r))
        
    def test_mul_var_divmod(self):
        #x + y
        p2= Poly({(1,0):1, (0,1):1})
        
        # x^9+x^7-x^4+4
        p1 = Poly({(9,):1, (7,):1, (4,):-1, (0,):4})
        
        divmod(p1,p2)