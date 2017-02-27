from poly import *
import cProfile

x = Poly({(1,):1}, ring="real")
x,y,z,w = indets(4)
p = x+y+z+w

def arith():
    (q,r) = divmod(p**30, p)

cProfile.run("arith()", sort="tottime")
