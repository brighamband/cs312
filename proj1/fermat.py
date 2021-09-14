import random
import math


def prime_test(N, k):
	# This is main function, that is connected to the Test button. You don't need to touch it.
	return fermat(N,k), miller_rabin(N,k)


def mod_exp(x, y, N):                                                   # O(n^3) for function (O(n) for run through + O(n^2))
    if y == 0:      # Base case                                         # O(c)
        return 1                                                        # O(c)
    # Recursive call (trunc rounds down to nearest whole number)
    z = mod_exp(x, math.trunc(y/2), N)                                  # O(n^2)
    if y % 2 == 0:                                                      # O(c)
        return (z**2) % N                                               # O(n^2)
    return x*(z**2) % N                                                 # O(n^2)
    

def fprobability(k):
    return 1 - 1/(2**k)                                                 # O(n^2)


def mprobability(k):
    return 1 - 1/(4**k)                                                 # O(n^2)


def f_prime_test(N):    # Essentially prime_test_1
    # a is random number a where 1 <= a < n 
    a = 1 if N == 1 else random.randint(1, N - 1)  
    if mod_exp(a,N-1,N) == 1:   # Fermat's little theorem               # O(n^3)
        return True     # N is prime (fprobability likelihood)          # O(c)
    return False        # N is composite (100%)                         # O(c)


def fermat(N,k):    # Essentially prime_test2
    for i in range(k):                                                  # O(n)
        if f_prime_test(N) == False:                                    # O(c)
            return 'composite'                                          # O(c)
    return 'prime'                                                      # O(c)

def m_prime_test(N): # Tests one number at a time
    # a is random number a where 1 <= a < n 
    a = 1 if N == 1 else random.randint(1, N - 1)
    exponent = N - 1
    while not exponent & 1:
        exponent >>= 1
    if mod_exp(a,exponent,N) == 1:
        return True     # N is prime (mprobability likelihood)
    while exponent < N - 1:
        if mod_exp(a,exponent,N) == N - 1:
            return True     # N is prime (mprobability likelihood)
        exponent <<= 1
    return False    # N is composite (100%)


def miller_rabin(N,k):
    for i in range(k):                                                  # O(n)
        if m_prime_test(N) == False:                                    # O(c)
            return 'composite'                                          # O(c)
    return 'prime'                                                      # O(c)
