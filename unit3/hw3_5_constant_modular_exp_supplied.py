# HW3-5 Version 1
#
# Implement constant_mod_exp
#

# use square and mult instead of doing
# the respective operations on your own
#
# These functions will keep track of
# how often they are called
# During grading your code will most likely fail
# if you don't use these functions.
mult_count = 0

def square(x):
    return mult(x, x)

def mult(x, y):
    global mult_count
    mult_count += 1
    return x * y

def constant_mod_exp(a, b, p, max_b):
    """returns a**b mod p"""
    #############
    ## Start of your code
    return 0
    ## End of your code
    #############

def reset_count():
    global mult_count
    tmp = mult_count
    mult_count = 0
    return tmp

def test():
    a = constant_mod_exp(5, 10, 13, 100)
    assert a == 5**10 % 13
    a_count = reset_count()

    b = constant_mod_exp(5, 95, 13, 100)
    assert b == 5**95 % 13
    b_count = reset_count()
    assert a_count == b_count
    print "Test passed"

# uncomment to run test
# test()
