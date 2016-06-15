from poly import *
import cProfile

x = Poly({(1,):1})
y = Poly({(0,1):1})
z = Poly({(0,0,1):1})

g1 = x**8* y**4 + x**2 + y**2
g2 = x**5*y**2 + x**2+z
g3 = x**2+y*z**5

cProfile.run("basis = groebnerBasis(g1,g2, g3)", sort="tottime")
print(len(basis))

if len(basis) < 10:
    for p in basis:
        print(p)