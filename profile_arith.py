from poly import *
import cProfile

x = Poly({(1,):1}, ring="real")

p = x+1

def arith():
    (q,r) = divmod(p**1000, p)

cProfile.run("arith()", sort="tottime")
print(divmod(p**1000, p))