import functools as ft

def Fib(n):
    primes = ft.reduce(lambda x,y: x+ list(range(y*y,n+1,y)),range(2,n+1),[])
    return(list(filter(lambda x: x not in primes,range(2,n+1))))
