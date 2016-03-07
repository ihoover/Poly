from poly import *
import cProfile

t1 = (0,1,2,3,4)
t2 = (1,2,3,4)
t3 = (0,)
reps = 1000

def prod_excercises():
    p1 = Prod(t1)
    p2 = Prod(t2)
    p3 = Prod(t3)
    
    for i in range(reps):
        p1*p2
        p1*p3
        p2*p3
        p2*p2
        p3*p3
        p1*p1
        
        p1/p2
        p1/p3
        p2/p3
        p2/p2
        p3/p3
        p1/p1

# cProfile.run("prod_excercises()", sort="cumtime")

import timeit
s1 = Prod((2,2,2))
s2 = Prod((3,3,3,3,3,3))
s3 = Prod((2,2,2,2,2,2))
print("Time for 1000000 unequal divisions")
print(timeit.timeit("s1/s2; s2/s1", setup="from __main__ import s1, s2", number=500000))

print("Time for 1000000 equal divisions")
print(timeit.timeit("s2/s3", setup="from __main__ import s3, s2", number=1000000))