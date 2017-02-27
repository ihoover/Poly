import os; import sys
sys.path.insert(0, os.path.abspath(os.pardir))
import unittest
from poly import *

def isWellFormed(p):
    """
    test that a polynomial is of the right types
    """


    assert type(p)==Poly
    assert type(p.terms)==frozendict

    for key in p.terms.keys():
        assert type(key)==Prod
        for i in key:
            assert type(i)==int
            assert i>=0
