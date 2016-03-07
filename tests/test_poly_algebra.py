import os; import sys
sys.path.insert(0, os.path.abspath(os.pardir))
import unittest
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


def mock_divmodSet(denom, basis):
    
    return (None, -denom)

from unittest.mock import patch
class testReduceList(unittest.TestCase):
    
    @patch('poly_algebra.divmodSet', return_value=(None, -1))
    def test_calls_divmodSet_correctly(self, mock_func):
        basis = [0,1,2,3,4,5]
        result = reduceList(basis)
        
        self.assertEqual(result, [-1]*len(basis))
        self.assertEqual(mock_func.call_count, len(basis))
        
        for i in range(len(basis)):
            basis_called_expected = [-1 for x in range(i)] + basis[i+1:]
            args, kwargs = mock_func.call_args_list[i]
            numerator = args[0]
            basis_called = args[1]
            
            self.assertEqual(numerator, basis[i])
            self.assertEqual(basis_called, basis_called_expected)
    
    @patch('poly_algebra.divmodSet', side_effect=mock_divmodSet)
    def test_trim(self, mock_func):
        basis = [-2,-1,0,1,2]
        basis_after = [-x for x in basis if x!=0]
        result = reduceList(basis)
        self.assertEqual(result, basis_after)
    
    @patch('poly_algebra.divmodSet', side_effect=mock_divmodSet)
    def test_noTrim(self, mock_func):
        basis = [-2,-1,0,1,2]
        basis_after = [-x for x in basis]
        result = reduceList(basis, trim=False)
        self.assertEqual(result, basis_after)
    
    @patch('poly_algebra.divmodSet', return_value=(None, -1))
    def test_except_last(self, mock_func):
        basis = [-2,-1,0,1,2]
        basis_after = [-1 for i in range(len(basis)-1) ] + basis[-1:]
        result = reduceList(basis, except_last=True)
        self.assertEqual(result, basis_after)

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
                    terms[stripTrZs(tup)] = 1
                p = Poly(terms)
                self.polys.append(p)
    
    def test2_polys(self):
        g1 = self.g1
        g2 = self.g2
        g3 = self.g3
        
        basis = groebnerBasis(g1, g2)
        for (p1, p2) in combinations(basis, 2):
            (q,r) = divmodSet(normalForm(p1, p2), basis, leadReduce=False)
            self.assertEqual(r, 0)
     
    def test1_poly(self):
        basis = groebnerBasis(self.g1)
        self.assertEqual(len(basis), 1)
        self.assertEqual(basis[0], self.g1)