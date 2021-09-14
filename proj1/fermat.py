import random


def prime_test(N, k):
	# This is main function, that is connected to the Test button. You don't need to touch it.
	return fermat(N,k), miller_rabin(N,k)


def mod_exp(x, y, N):                                               # O(n^3) for function (O(n) for run through + O(n^2))
    if y == 0:                                                      # O(c)
        return 1                                                    # O(c)
    z = mod_exp(x, y/2, N)                                          # O(n^2)
    if y % 2 == 0:                                                  # O(c)
        return z**2 % N                                           # O(n^2)
    return x*(z**2) % N                                           # O(n^2)
    

def fprobability(k):
    return 1 - 1/(2**k)     # FIXME - Explain                           # O(n^2) ?? FIXME


def mprobability(k):
    return 1 - 1/(4**k)     # FIXME - Explain                           # O(n^2) ?? FIXME


def prime_test1(N):
    # pick a random positive number a that is between 1 and N (inclusive)
    a = random.randint(1, N-1)    # N - 1 because A can't == N      # O(c)
    if (a**(N-1)) % N == 1:    # Fermat's little theorem             # FIXME
        print('true')
        return True                                                # O(c)
    print('false')
    return False                                                     # O(c)


def fermat(N,k):    # Essentially prime_test2
    for i in range(0, k):
        print('i',i)
        if prime_test1(N) == False:
            return 'composite'
    return 'prime'

def miller_rabin(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
	#
    # To generate random values for a, you will most likely want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
	return 'composite'
