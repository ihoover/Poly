import os; import sys
sys.path.insert(0, os.path.abspath(os.pardir))
import unittest
from itertools import product, combinations
from poly_algebra import *

class TestPolyArithmetic(unittest.TestCase):
    
    def setUp(self):
        """
        define some useful poynomials
        """
        
        self.x = Poly({(1,):1})
        self.y = Poly({(0,1):1})
        self.z = Poly({(0,0,1):1})

        
        # x^2 + y^2 + 1
        self.p1 = Poly({(2,):1, (0,2):1, (0,):1})
        
        # xy + y^2 - 3
        self.p2 = Poly({(1,1):1, (0,2):1, (0,):-3})
        
        self.one = Poly({(0,):1})
        self.five = Poly({(0,):5})
        
        self.p1_plus_p2 = Poly({(2,):1, (0,2):2, (1,1):1, (0,):-2})
        self.p1_minus_p2 = Poly({(2,):1, (1,1):-1, (0,):4})
        self.p1_plus_1 = Poly({(2,):1, (0,2):1, (0,):2})
        self.p1_minus_1 = Poly({(2,):1, (0,2):1})
        self.one_minus_p1 = Poly({(2,):-1, (0,2):-1})
        
        self.p1_times_p2 = Poly({(3,1):1, (2,2):1, (2,):-3, (1,3):1, 
                                (1,1):1, (0,4):1, (0,2):-2, (0,):-3})
        self.p1_times_five = Poly({(2,):5, (0,2):5, (0,):5})
        
        # x^10+5 x^8 y^2+10 x^6 y^4+10 x^4 y^6+5 x^2 y^8+y^10
        self.p_simple = Poly({(2,):1, (0,2):1})
        self.pow_const = 5
        self.p1_pow_const = Poly({(10,):1, (8,2):5, (6,4):10, (4,6):10, (2,8):5, (0,10):1})
        self.p2_mod_y = Poly({(0,):-3})

    def test_add(self):
        self.assertEqual(self.p1 + self.p2, self.p1_plus_p2)

    def test_add_number(self):
        self.assertIs(self.p1 + 1, self.p1_plus_1)
        self.assertIs(self.one + self.p1, self.p1_plus_1)

    def test_radd_number(self):
        self.assertIs(1 + self.p1, self.p1_plus_1)
        self.assertIs(self.one + self.p1, self.p1_plus_1)

    def test_sub(self):
        self.assertIs(self.p1 - self.p2, self.p1_minus_p2)
    
    def test_sub_number(self):
        self.assertIs(self.p1 - 1, self.p1_minus_1)
        self.assertIs(self.p1 - self.one, self.p1_minus_1)
    
    def test_rsub_number(self):
        self.assertIs(1 - self.p1, self.one_minus_p1)
        self.assertIs(self.one - self.p1, self.one_minus_p1)
    
    def test_mul(self):
        self.assertEqual(self.p1 * self.p2, self.p1_times_p2)
    
    def test_mul_number(self):
        self.assertEqual(self.p1 * 5, self.p1_times_five)
        self.assertEqual(self.p1 * self.five, self.p1_times_five)
    
    def test_rmul_number(self):
        self.assertEqual(5 * self.p1, self.p1_times_five)
        self.assertEqual(self.p1 * self.five, self.p1_times_five)
    
    def test_pow_0(self):
        self.assertEqual(self.p1**0, 1)
    
    def test_pow_1(self):
        self.assertIs(self.p1 ** 1, self.p1)
    
    def test_pow_10(self):
        self.assertIs(self.p_simple ** self.pow_const, self.p1_pow_const)
    
    def test_mul_cancel(self):
        # x^2 + y^2
        p1 = Poly({(2,):1, (0,2):1})
        
        # x^2 - y^2
        p2 = Poly({(2,):1, (0,2):-1})
        
        # x^4 - y^4
        result = {(4,):1, (0,4):-1}
        
        self.assertEqual(result, (p1*p2).terms)
    
    def test_mul_diffLen(self):
        # x^2
        p1 = Poly({(2,):1})
        
        # xy + y^2
        p2 = Poly({(1,1):1, (0,2):1})
        
        # x^3 + x^2y^2
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
    
    def test_div_single_0r(self):
        
        p1=Poly({(9,):3,(7,):-2, (4,):12, (2,):2, (0,):-2})
        self.assertEqual(divmod(p1*p1*p1, p1), (p1*p1, Poly()))
    
    def test_divmod_stability(self):
        
        p = Poly({(2,):1, (0,):1})
        (q,r) = divmod(p**70, p)
        self.assertEqual(r,0)
    
    def test_mul_var_divmod(self):
        #x + y
        p2= Poly({(1,):1, (0,1):1})
        
        # x^2+1
        p1 = Poly({(2,):1, (0,):1})
        
        # x-y
        q = Poly({(1,):1, (0,1):-1})
        # 1+y^2
        r = Poly({(0,2):1, (0,):1})
        
        self.assertEqual(divmod(p1,p2), (q,r))
    
    def test_notJustLeadReduction(self):
        x = self.x
        y = self.y
        z = self.z
        
        den = y**2 +1
        p1 = x * z + den
        
        (q,r) = divmod(p1,den)
        
        self.assertEqual(q, 1)
        self.assertEqual(r, x * z)
    
    def test_neg(self):
        self.assertEqual(-self.p1, self.p1*-1)
    
    def test_mod(self):
        y = Poly({(0,1):1})
        self.assertEqual(self.p2 % y, self.p2_mod_y)
    
    def test_abs_poly(self):
        
        self.assertEqual(abs(self.p1),self.p1)
    
    def test_abs_const(self):
        
        self.assertEqual(abs(self.one), 1)
        self.assertEqual(abs(-self.one), 1)