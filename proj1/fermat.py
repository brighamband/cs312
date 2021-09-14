import random
import math


def prime_test(N, k):
	# This is main function, that is connected to the Test button. You don't need to touch it.
	return fermat(N,k), miller_rabin(N,k)


def mod_exp(x, y, N):                                                   # O(n^3) for function - O(n) for run through + O(n^2)
    if y == 0:      # Base case                                         # O(1)
        return 1                                                        
    # Recursive call (trunc rounds down to nearest whole number)
    z = mod_exp(x, math.trunc(y/2), N)                                  # O(n^2)
    if y % 2 == 0:                                                      # O(1)
        return (z**2) % N                                               # O(n^2)
    return x*(z**2) % N                                                 # O(n^2)
    

def fprobability(k):                                                    # O(n^2) for function
    return 1 - 1/(2**k)                                                 # O(n^2)


def mprobability(k):                                                    # O(n^2) for function
    return 1 - 1/(4**k)                                                 # O(n^2)


def f_prime_test(N):    # Essentially prime_test_1                      # O(n^3) for function (mod_exp is O(n^3))
    # a is random number a where 1 <= a < n 
    a = 1 if N == 1 else random.randint(1, N - 1)                       # O(log n) - twice as slow for every n bit in range
    if mod_exp(a,N-1,N) == 1:   # Fermat's little theorem               # O(n^3)
        return True     # N is prime (fprobability likelihood)
    return False        # N is composite (100%)                         # O(1)


def fermat(N,k):    # Essentially prime_test2                           # O(n^3) for function - O(kn^3)+O(1)
    for i in range(k):                                                  # k
        if f_prime_test(N) == False:                                    # O(n^3)
            return 'composite'                                          # O(1)
    return 'prime'                                                      # O(1)

def m_prime_test(N): # Tests one number at a time                       # FIXME for function
    # a is random number a where 1 <= a < n 
    a = 1 if N == 1 else random.randint(1, N - 1)                       # O(log n) - twice as slow for every n bit in range
    exponent = N - 1
    while not exponent & 1:                                             # O(log n)? FIXME
        exponent >>= 1      # Right bit shift 1
    if mod_exp(a,exponent,N) == 1:                                      # O(1)
        return True     # N is prime (mprobability likelihood)
    while exponent < N - 1:                                             # O(n^2)? FIXME
        if mod_exp(a,exponent,N) == N - 1:
            return True     # N is prime (mprobability likelihood)
        exponent <<= 1      # Left bit shift 1
    return False    # N is composite (100%)                             # O(1)


def miller_rabin(N,k):                                                  # O(n) for function 
    for i in range(k):                                                  # k
        if m_prime_test(N) == False:                                    # O(1)
            return 'composite'                                          
    return 'prime'                                                      # O(1)
