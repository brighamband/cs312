import random


def prime_test(N, k):
	# This is main function, that is connected to the Test button. You don't need to touch it.
	return fermat(N,k), miller_rabin(N,k)


def mod_exp(x, y, N):                                               # O(n^3) for function (O(n) for run through + O(n^2))
    if y == 0:                                                      # O(c)
        return 1                                                    # O(c)
    z = mod_exp(x, y/2, N)                                          # O(n^2)
    if y % 2 == 0:                                                  # O(c)
        return (z**2) % N                                           # O(n^2)
    return (x*(z**2)) % N                                           # O(n^2)
    

def fprobability(k):
    return 1/(2**k)     # FIXME - Explain                           # O(n^2) ?? FIXME


def mprobability(k):
    return 1/(4**k)     # FIXME - Explain                           # O(n^2) ?? FIXME

def prime_test1(N):
    # pick a random number a that is between 0 and N (inclusive)
    a = random.randint(0, N + 1)                                    # O(c)
    if (a^(N-1)) % N == 1:                                          # FIXME
        return "yes"                                                # O(c)
    return "no"                                                     # O(c)

def prime_test2(N, k):     # if not used directly in fermat
    for i in range(k):
        if prime_test1(N) == "no":
            return "no"
    return "yes"

def fermat(N,k):
    if prime_test2(N, k) == "yes":
        return "prime"
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
	#
    # To generate random values for a, you will most likely want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    return "composite"


def miller_rabin(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
	#
    # To generate random values for a, you will most likely want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
	return 'composite'
