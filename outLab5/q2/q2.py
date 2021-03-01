import functools
import operator
from functools import reduce
def collapse(L) :
	
    d = ' '
    R = reduce(operator.add,L)
    P = reduce(lambda x,y : x + d + y,R)
    return P
