from poly import *
import cProfile

x = Poly({(1,):1})
y = Poly({(0,1):1})
z = Poly({(0,0,1):1})

g1 = x**2 * y**4 + y**2*z + z**2
g2 = x**3*y**2*z + x**2
g3 = x**2+y

cProfile.run("basis = groebnerBasis(g1,g2, g3)", sort="tottime")
print(len(basis))

if len(basis) < 10:
    for p in basis:
        print(p)