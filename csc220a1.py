# file: csc220a1.py

from time import time

def fib (n):
    if n < 1:
        return abs (n)
    else:
        return fib (n-1) + fib (n-2)

def getBaseline ():
    start = time ()
    i = 0
    end = start + 1
    current = start
    while current < end:
        i = i + 1
        current = time ()
    return (current - start) / i

def timeIt (n, baseline):
    start = time ()
    i = 0
    end = start + 1
    current = start
    while current < end:
        i = i + 1
        result = fib (n)
        current = time ()
    elapsed = (current - start) / i - baseline
    return (result, elapsed)

def test ():
    done = False
    baseline = getBaseline ()
    i = 1
    while not done:
        result, elapsed = timeIt (i, baseline)
        print ('time = %14.9fs, fib (%2d) = %12d' % (elapsed, i, result))
        done = elapsed > 3600.0
        i = i + 1



test ()