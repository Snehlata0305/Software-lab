import itertools as it
# import operator as op

def myFunc(deg, vals, coeffs):
    i=0
    while i!=(deg):
        yield "x"+"*x"*(deg-i-1)+"*y"*(i)+" -> "+ str(coeffs[i]*(vals[0]**(deg-i))*(vals[1]**i))
        i+=1
    yield "y"+"*y"*(deg-1)+" -> "+str(coeffs[-1]*(y**(deg)))