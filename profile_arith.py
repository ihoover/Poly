from poly import *
import cProfile

x = Poly({(1,):1})
p = x+1

def arith():
    divmod(p**1000, p)

cProfile.run("arith()", sort="tottime")