from poly import *
import cProfile

t1 = (0,1,2,3,4)
t2 = (1,2,3,4)
t3 = (0,)
reps = 100000

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

cProfile.run("prod_excercises()", sort="cumtime")