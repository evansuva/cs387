# hw 6
from __future__ import division
import itertools
from bits import *
from Crypto.Random import random

def prob_select(a, v, n):
    return pow(a/v, n)

def find_best(v, n, m):
    for a in range(1, v):
        if prob_select(a, v, n) > m:
            return a - 1

def fact(n):
    res = 1
    for i in range(1, n+1):
        res = res * i
    return res

def nchoosek(n, k):
    return fact(n)/(fact(k) * fact(n-k))        


# create bills to audit
BILL_ID_LENGTH = 64
DEC_LENGTH = 8
NUMBER_OF_IDENTITIES = 4

def create_valid_bill(identity, m, amount):
    r = random_sequence(BILL_ID_LENGTH) # bill ID
    mbits = string_to_bits(identity)
    identities = ""
    for i in range(m):
        i0 = random_sequence(len(mbits))
        i1 = xor_bits(mbits, i0)
        identities += bits_to_hexstring(i0) + bits_to_hexstring(i1)
    msg = string_to_hexstring("Bill:") + bits_to_hexstring(r)
    msg += bits_to_hexstring(pad_bits(dec_to_bits(len(mbits)), DEC_LENGTH))
    msg += identities
    msg += bits_to_hexstring(string_to_bits("$" + str(amount)))
    return msg

def check_bill(bill):
    # first 64 bits are r
    bits = hexstring_to_bits(bill)
    # check start is "Bill:"
    pos = 8 * 5
    bs = bits_to_string(bits[:40])
    assert bs == "Bill:"
    r = bits[pos:pos + BILL_ID_LENGTH]
    pos += BILL_ID_LENGTH
    ibits = bits[pos:pos + DEC_LENGTH]
    pos += DEC_LENGTH
    ilen = bits_to_dec(ibits)
    print "ilen: " + str(ilen)
    # length of each identity
    identities = []
    for i in range(NUMBER_OF_IDENTITIES):
        id0 = bits[pos:pos + ilen]
        pos += ilen
        id1 = bits[pos:pos + ilen]
        pos += ilen
        idx = xor_bits(id0, id1)
        identities.append((id0, id1))
        print bits_to_string(idx)
    ds = bits_to_string(bits[pos:pos+8])
    pos += 8
    assert ds == "$"
    amount = int(bits_to_string(bits[pos:]))
    print amount
    return r, identities, amount

