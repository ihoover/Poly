from poly import *
import cProfile

x = Poly({(1,):1})
y = Poly({(0,1):1})
z = Poly({(0,0,1):1})

g1 = x**3 * y**2 + z + y**2 - 12
g2 = x**3*y + x**2  - 1
g3 = y - 12*z

cProfile.run("basis = groebnerBasis(g1,g2)", sort="tottime")
print(len(basis))