import random
import sys

from bigblue import randu

sys.setrecursionlimit(1000000)  # long type,32bit OS 4B,64bit OS 8B(1bit for sign)

# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
# return (g, x, y) a*x + b*y = gcd(x, y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

# https://rosettacode.org/wiki/Miller%E2%80%93Rabin_primality_test
def _try_composite(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True # n  is definitely composite
 
def is_prime(n, _precision_for_huge_n=16):
    if n in _known_primes or n in (0, 1):
        return True
    if any((n % p) == 0 for p in _known_primes):
        return False
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
    if n < 1373653: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467: 
        if n == 3215031751: 
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
    # otherwise
    return not any(_try_composite(a, d, n, s) 
                   for a in _known_primes[:_precision_for_huge_n])

_known_primes = [2, 3]
_known_primes += [x for x in range(5, 1000, 2) if is_prime(x)]
 
def keygen(bits):
    p = q = 3
    while p == q:
        p = 2**(bits/2-2)+randu()
        q = 2**(bits/2-2)+randu()
        p += not(p&1)                             # changes the values from
        q += not(q&1)                             # even to odd

        while is_prime(p) == False:            # checks for primality
            p -= 2
        while is_prime(q) == False:
            q -= 2

    while is_prime(p) == False:            # checks for primality
        return(0,0,0,0,0)
    while is_prime(q) == False:
        return(0,0,0,0,0)
    if p > q:
        x = p
        p = q
        q = x
    n = p * q   
    tot = (p-1) * (q-1)
    #if tot > 3:
        #e = tot
        #while egcd(tot,e)[0] != 1:
            #e = random.randint(3,tot-1)
    #else:
         #return(0,0,0,0,0)
    e=65537
    d = mulinv(tot,e)                       # gets the multiplicative inverse
    while d<0:                            # i can probably replace this with mod
        d = d + tot
    return p,q,e,d,n


bits=2048
p,q,e,d,n=keygen(bits)

# https://github.com/ius/rsatool/blob/master/rsatool.py
print("run: rsatool.py -f PEM -o key.priv -p "+str(p)+" -q "+str(q))
print("run: openssl rsa -in key.priv -pubout > key.pub")
print("run: openssl rsautl -encrypt -pubin -inkey key.pub -ssl -in flag.txt -out flag.enc")
print("run: openssl rsautl -decrypt -inkey key.priv -in flag.enc -out decrypted.txt")
