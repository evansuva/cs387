### Unit 2 Homework

from Crypto.Random import random
from bits import *
from Crypto.Cipher import AES

### PyCrypto defines AES.MODE_CTR, but we write our
### own code for this.  Note that AES.MODE_CTR is
### different from the CTR mode we described, it
### is more like CFB in making a byte-length stream
### cipher.

    
#def bad_hash(s):

class Counter:
    """Implements an incrementing n-bit counter."""
    def __init__(self, nbits, nonce=None):
        self.state = [0] * nbits

    def counter(self):
      result = bits_to_string(self.state)
      bits_inc(self.state)
      return result
    
def bad_hash(s):
    key = '\0' * 16 # key is all 0s
    ctr = Counter(16 * 8)
    cipher = AES.new(key, AES.MODE_CTR, counter = ctr.counter)
    enc = string_to_bits(cipher.encrypt(s))
    print bits_to_hexstring(enc)
    print display_bits(enc)
    assert len(enc) % 128 == 0
    # hash is xor of 16-byte blocks
    h = [0] * 128
    for block in range(0, len(enc) / 128):
        bb = enc[block:block + 128]
        print display_bits("xoring " + str(block) + ": " + display_bits(bb))
        h = xor_bits(h, bb)
    return h    

s1 = bits_to_string(128 * [0] + (126 * [0]) + [1] + [0])
s2 = bits_to_string((127 * [0] + [1]) + (128 * [0]))

def check_match(s1, s2):
    h1 = bad_hash(s1)
    h2 = bad_hash(s2)
    print "h1: " + display_bits(h1)
    print "h2: " + display_bits(h2)
    print display_bits(xor_bits(h1, h2))
    
def generate_sequence(f, n):
    return map(f, range(n))

def alternate(x):
    if x % 3 == 0:
        return 0
    else:
        return 1

def string_selector(s):
    return lambda n: ord(s[n % len(s)]) % 2

def generate_fake_random(n):
    ## generates a trick random sequence - avoids runs > 3
    repetition = 0
    previous = None
    res = []
    for i in range(n):
        x = random.choice([0, 1])
        if x == previous:
            repetition += 1
            if repetition > 2:
                x = (x + 1) % 2
                repetition = 1
                previous = x
        else:
            previous = x
            repetition = 1
        res.append(x)
    return res
    
def random_sequence(n):
    return generate_sequence(lambda n: random.choice([0, 1]), n)

length = 88    
# print generate_sequence(lambda n: 0, length)
#print display_bits(generate_sequence(lambda n: 0 if n % 3 == 0 else 1, length))
#print display_bits(string_to_bits("Anyone who considers arithmetical methods of producing random digits is, of course, in a state of sin.")[:length])
#print display_bits(generate_sequence(lambda n: random.choice([0, 1]), length))
#print display_bits(generate_fake_random(length))


