###
### Some routines for manipulating bits
###
### (More "pythonic" version, see cs101 version also.)
###

import itertools

BITS = ('0', '1')

def display_bits(b): # converts list of {0, 1}* to string
    return ''.join([BITS[e] for e in b])

def pad_bits(seq, pad): # pads seq with leading 0s up to length pad
    assert len(seq) <= pad
    return [0] * (pad - len(seq)) + seq
        
def convert_to_bits(n): # integer to binary
    result = []
    while n > 0:
        result = [(n % 2)] + result
        n = n / 2
    return result

def bits_to_dec(n):
    result = 0
    for b in n:
        result = result * 2 + b
    return result

def string_to_bits(s):
    return [b for group in map(lambda c: pad_bits(convert_to_bits(ord(c)), 7), s) \
              for b in group ]

def bits_to_char(b):
    assert len(b) == 7
    value = 0
    for e in b:
        value = (value * 2) + e
    return chr(value)

def bits_to_string(b):
    return ''.join([bits_to_char(b[i:i + 7]) for i in range(0, len(b), 7)])



