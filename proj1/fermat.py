import random


def prime_test(N, k):
	# This is main function, that is connected to the Test button. You don't need to touch it.
	return fermat(N,k), miller_rabin(N,k)


def mod_exp(x, y, N):                                               # O(n^3) for function (O(n) for run through + O(n^2))
    if y == 0:                                                      # O(c)
        return 1                                                    # O(c)
    z = mod_exp(x, y/2, N)                                          # O(n^2)
    if y % 2 == 0:                                                  # O(c)
        return pow(z,2,N)                                           # O(n^2)
    return x*(z**2) % N                                            # O(n^2)
    

def fprobability(k):
    return 1 - 1/(2**k)     # FIXME - Explain                           # O(n^2) ?? FIXME


def mprobability(k):
    return 1 - 1/(4**k)     # FIXME - Explain                           # O(n^2) ?? FIXME


def f_prime_test(N):    # Essentially prime_test_1
    a = 1 if N == 1 else random.randint(1, N - 1)             # 1 < a <= n - 1   
    if pow(a,N-1,N) == 1:   # Fermat's little theorem             # FIXME
        return True                                                # O(c)
    return False                                                     # O(c)


def fermat(N,k):    # Essentially prime_test2
    for i in range(k):
        if f_prime_test(N) == False:
            return 'composite'
    return 'prime'

def m_prime_test(N): # Tests one number at a time
    a = 1 if N == 1 else random.randint(1, N - 1)   # 1 < a <= n - 1

    exponent = N - 1

    while not exponent & 1:
        exponent >>= 1
    
    if pow(a,exponent,N) == 1:
        return True

    while exponent < N - 1:
        if pow(a,exponent,N) == N - 1:
            return True
        exponent <<= 1

    return False


def miller_rabin(N,k):
    for i in range(k):
        if m_prime_test(N) == False:
            return 'composite'
    return 'prime'
