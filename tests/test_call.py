from common import *

class TestPolyMultiPow(unittest.TestCase):
    
    def setUp(self):
        self.c2 = 2
        self.c3 = 3
        self.c4 = 4
        self.one = 1
        self.zero = 0
        
        self.p_tup = (self.c2, self.c3)
        self.y = Poly({(0,1):1})
        self.x = Poly({(1,):1})
    
    def test_single(self):
        self.assertEqual(Poly.multiPow([self.c2], (self.c3,)), self.c2 ** self.c3)
    
    def test_multiple(self):
        multi_pow = [self.c2, self.c3]
        multi_var = [self.c3, self.c4]
        
        res = self.c3 ** self.c2 * self.c4 ** self.c3
        
        self.assertEqual(Poly.multiPow(multi_var, multi_pow), res)
    
    def test_multi_pow_short(self):
        multi_pow = [self.c2]
        multi_var = [self.c3, self.c4]
        
        res = self.c3 ** self.c2
        
        self.assertEqual(Poly.multiPow(multi_var, multi_pow), res)
        
    def test_multi_var_short(self):
        multi_pow = [self.c2, self.c3]
        multi_var = [self.c4]
        
        res = Poly({(0,self.c3):self.c4 ** self.c2})
        
        self.assertEqual(Poly.multiPow(multi_var, multi_pow), res)
    
    def test_multi_var_short(self):
        multi_pow = [self.c2, self.c3]
        multi_var = [None, self.c4]
        
        res = Poly({(self.c2,):self.c4 ** self.c3})
        
        self.assertEqual(Poly.multiPow(multi_var, multi_pow), res)
    
    def test_multi_var_empty(self):
        multi_pow = [self.c2, self.c3]
        multi_var = []
        
        res = Poly({(self.c2,self.c3):1})
        
        self.assertEqual(Poly.multiPow(multi_var, multi_pow), res)
    
    def test_multi_var_poly(self):
        multi_pow = self.p_tup
        multi_var = [self.x, self.y]
        res = Poly({self.p_tup:1})
        self.assertEqual(Poly.multiPow(multi_var, multi_pow), res)
    
    def test_multi_var_short_poly(self):
        multi_pow = [self.c2, self.c3]
        multi_var = [None, self.x]
        
        res = Poly({(self.c2 + self.c3,):1})
        
        self.assertEqual(Poly.multiPow(multi_var, multi_pow), res)

class TestPolyCall(unittest.TestCase):
    
    def setUp(self):
        self.x = Poly({(1,):1})
        self.y = Poly({(0,1):1})
        self.z = Poly({(0,0,1):1})
        
        self.const = 4
        self.p_const = Poly(self.const)
        
        self.px_pl_y = Poly({(1,):1, (0,1):1})
        self.p1x_sq_pl_x_pl_one = Poly({(2,):1, (0,):1, (1,):1})
        self.p2y_plus_one = Poly({(0,1):1, (0,):1})
        
        self. p1_of_p2 = Poly({(0,2):1, (0,1):3, (0,):3})
        self. p2_of_p1 = Poly({(2,):1, (0,):2})
    
    def test_const(self):
        self.assertEqual(self.p_const(13243), self.const)
        self.assertEqual(self.p_const(self.x), self.const)
    
    def test_number(self):
        for num in range(-10,10):
            self.assertEqual(self.p1x_sq_pl_x_pl_one(num), num**2 + num + 1)
    
    def test_number_None(self):
        self.assertEqual(self.p1x_sq_pl_x_pl_one(None), self.p1x_sq_pl_x_pl_one)
    
    def test_number_ignored(self):
        num1 = 4
        for num2 in range(-10,10):
            self.assertEqual(self.p1x_sq_pl_x_pl_one(num1, num2), self.p1x_sq_pl_x_pl_one(num1))
    
    def test_number_var2(self):
        num=4
        self.assertEqual(self.p2y_plus_one(None, num), num + 1)
    
    def test_number_ignored_var2(self):
        num1 = 4
        for num2 in range(-10,10):
            self.assertEqual(self.p2y_plus_one(num2, num1), self.p2y_plus_one(None, num1))
    
    def test_x_swap_y(self):
        self.assertEqual(self.x(self.y), self.y)