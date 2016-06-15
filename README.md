# poly
## the basics
A library for doing polynomial math in python3. We will start by initializing our indeterminates:

    form poly import *
    x, y, z = indets(3)
    p = y**3 + x*y*z + x**2 + z*y
    
Now that we have our polynomial `p`, there are a few things we can do with it. Most importantly, we
can treat it just like a number that doesn't do division.

    >>> p**2 + 1
    Poly:[1 y2^6 + 2 y1y2^4y3 + 1 y1^2y2^2y3^2 + 2 y1^2y2^3 + 2 y1^3y2y3 + 2 y2^4y3 + 2 y1y2^2y3^2 + 1 y1^4 + 2 y1^2y2y3 + 1 y2^2y3^2 + 1 ]
    >>> p + p
    Poly:[2 y2^3 + 2 y1y2y3 + 2 y1^2 + 2 y2y3]
    >>> p+x**3
    Poly:[1 y1^3 + 1 y2^3 + 1 y1y2y3 + 1 y1^2 + 1 y2y3]

We see here that our first indeterminate will always print as y1, the second as y2 etc regardless of being called `x` and `y`. Its ugly, but there it is.
We can evaluate the polynomial (on numbers or on other polynomials):

    >>> p(1,2,3)
    Poly:[21 ]
    >>> p(1,x+2,y)
    Poly:[1 y1^3 + 6 y1^2 + 2 y1y2 + 12 y1 + 4 y2 + 9 ]
    >>> 

With two polynomials, we can reduce one by the other (that is, perform long division if we are in single variable land). The input is of the form `(p1, p2)` to reduce `p1` by `p2`. The output is a tuple `(q,r)`, `q`uotient and `r`emainder.

    >>> divmod((x**2+2)**3 + x + 1, (x**2+2))
    (Poly:[1 y1^4 + 4 y1^2 + 4 ], Poly:[1 y1 + 1 ])
    >>> divmod(p, y+x)
    (Poly:[1 y2y3 + 1 y1 + -1 y2], Poly:[1 y2^3 + -1 y2^2y3 + 1 y2^2 + 1 y2y3])
    >>> 

To reduce by a set, we have `divmodSet`. The input is of the form `(p, [p1, p2, ...])` to reduce `p` by the elements of the list. The output is a list of quotients, and the remainder `([q1, q2,...], r)` where `qi` corresponds with `pi`.

    >>> divmodSet((x**2 + 1)*y + (-y*x +y)*x, [x**2+1, -y*x+y])
    ([0, Poly:[-1 ]], Poly:[2 y2])

Of course, the universe hates us and getting a non-zero remainder does not mean `p` is not some combination of `[p1, p2, ...]`. Thus we have a way of calculating a Groebner basis:

    >>> divmodSet((x**2 + 1)*y + (-y*x +y)*x, groebnerBasis(x**2+1, -y*x+y))
    ([0, Poly:[1 y1 + 1 ]], Poly:[0 ])

groebnerBasis takes a variable unmber of arguments, and outpus a list of polynomials.


##to do...
While the previous is all well and good, its pretty minimal. In the future I will hopefully implement the following:

* root finding, even just floating point approximations
* support for polynomials over finite fields and potentially other rings.