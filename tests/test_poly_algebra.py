import os; import sys
sys.path.insert(0, os.path.abspath(os.pardir))
import unittest
import sys
from itertools import product, combinations
from poly_algebra import *


class TestDivmodSet(unittest.TestCase):
    
    def setUp(self):
        self.x = Poly({(1,):1})
        self.y = Poly({(0,1):1})
        self.z = Poly({(0,0,1):1})
    
    def test_0rem_1var(self):
        p1 = self.x**2 + self.x
        (q,r) = divmodSet(p1, (self.x**2, self.x))
        self.assertEqual(r,0)
        self.assertEqual(q, [1,1])
    
    def test_rem_1var(self):
        fac = self.x**2+1
        p1 = (fac)**2 + self.x
        basis = [fac]
        (q,r) = divmodSet(p1, basis)
        self.assertEqual(len(q), 1)
        self.assertEqual(q[0]*basis[0] + r, p1)
        self.assertEqual(r, self.x)
        self.assertEqual(q[0], fac)
    
    def test_0rem_multivar(self):
        p1 = self.x + self.z**3*self.y + self.y**3
        basis = [self.x, self.y, self.z]
        (q,r) = divmodSet(p1, basis)
        self.assertEqual(r, 0)
        self.assertEqual(sum([q[i]*basis[i] for i in range(len(basis))]), p1)
    
    def test_rem_multivar(self):
        x = self.x
        y = self.y
        z = self.z
        
        p1 = x**3*y**4*z + 12*x**4 - 4 *(x+y+z)**3 + 3*x + 4*z**2 - 7*y -7
        basis = [x**2+1, y+1, 2*z]
        (q,r) = divmodSet(p1, basis)
        self.assertEqual(sum([q[i]*basis[i] for i in range(len(basis))]) + r, p1)


class TestNormalForm(unittest.TestCase):
    
    def setUp(self):
        self.x = Poly({(1,):1})
        self.y = Poly({(0,1):1})
        self.z = Poly({(0,0,1):1})
    
    def test_normalForm(self):
        x = self.x
        y = self.y
        z = self.z
        
        p1 = x * y**2 * z**3 + y**2
        p2 = x**2 * y * z**3 + z
        
        normal_form = x*p1 - y*p2
        self.assertEqual(normalForm(p1,p2), normal_form)


class TestGroebnerBasis(unittest.TestCase):
    
    def setUp(self):
        self.x = Poly({(1,):1})
        self.y = Poly({(0,1):1})
        self.z = Poly({(0,0,1):1})
        x = self.x
        y = self.y
        z = self.z
        
        # some rando polynomials
        self.g1 = x**3 * y**2 + z + y**2 - 12
        self.g2 = x**2 * z + x**2  - 1
        self.g3 = z**2 * y**2 * z + y**2 - 12*z**2
        
        # create a whole lot of polynomials
        self.polys = []
        for num_terms in range(1,2,3):
            for combo in combinations(product(range(3), repeat=3), num_terms):
                terms = {}
                for tup in combo:
                    terms[tup] = 1
                p = Poly(terms)
                self.polys.append(p)
    
    def test2(self):
        g1 = self.g1
        g2 = self.g2
        g3 = self.g3
        
        basis = groebnerBasis(g1, g2)
        for (p1, p2) in combinations(self.polys, 2):
            for c2 in [-1,2,3]:
                (q,r) = divmodSet(p1*g1 + c2*p2*g2, basis)
                self.assertEqual(r, 0)