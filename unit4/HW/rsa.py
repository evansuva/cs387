from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import MD5
import math

def square(x): return x*x


### Rewrite this
def int_sqrt(n):
    xn = 1
    xn1 = (xn + n/xn) / 2
    while abs(xn1 - xn) > 1:
        xn = xn1
        xn1 = (xn + n/xn) / 2
    while xn1 * xn1 > n:
        xn1 = xn1 - 1
#    assert square(xn1) == n
    return xn1

def factor_n(n, e, d, totn):
    """Returns True if (e, n) and (e, d) are a correct RSA key pair."""
    #totnx = (e*d - 1) % n
    #assert totnx == totn
    # (p + q) + 1 = Tot(n) - n
    # given e and d, find totn
    ktotn = d*e - 1 # some multiple of totient
    print totn
    print ktotn
    # return totn, ktotn
    # totient must be less than n
    assert ktotn > n
    # number of possible totns
    # try all multiples
    # tot(n) must be less than n
    k = ktotn / n
    possible = []
    while (ktotn / k) > 2:
        if ktotn % k == 0:
            possible.append(ktotn / k)
        k += 1
        
    print "possible: ", len(possible)
    assert totn in possible
    
    pplusq = - (totn - n - 1)
    print "pplusq: ", pplusq
    val = n - totn - 1
    print "val: ", val
    print "square: ", square(val)
    inner = square(val) - 4 * n
    print "inner: ", inner
    pminq = round(math.sqrt(inner))
    # need to try +/-
    pminq = - pminq ### 
    print "pmiq: ", pminq
    # assert (square(pminq - 1) > inner and square(pminq + 1) > inner)
    p = (pplusq + pminq) / 2
    assert (p == int(p))
    q = n / p
    print "p: ", p
    print "q: ", q
    assert (p * q == n)
    return p, q

def sign(key, m):
    h = MD5.new(m).digest()
    sig = RSAkey.sign(h)

def toy_challenge():
    p = 37
    q = 101
    n = p * q
    e = 79
    d = 319
    totn = (p - 1) * (q - 1)
    return factor_n(n, e, d, totn)
        
def toy():
    p = 37
    q = 101
    totn = (p - 1) * (q - 1)
    e = 79 # relatively prime to totn
    n = p * q
    # find d (brute force)
    for d in range(80, p * q):
        if e * d % totn == 1:
            break
    print "Public: (" + str(e) + ", " + str(n) + ")"
    print "Private:(" + str(d) + ", " + str(n) + ")"
    m = 387
    ciphertext = (m ** e) % n
    plaintext = (ciphertext ** d) % n
    assert (plaintext == m)
    print "ciphertext = ", ciphertext

def forge_signature():
    prng = Random.new().read
    key = RSA.generate(1024, prng)
    m1 = 387
    s1 = key.sign(m1, '') # second signing parameter not relevant for RSA
    m2 = 2
    s2 = key.sign(m2, '')
    print key.e
    print key.n
    print s1[0]
    print s2[0]
    
    s3 = ((s1[0] * s2[0]) % key.n, None)
    m3 = m1 * m2
    assert key.verify(m1, s1)
    assert key.verify(m2, s2)
    assert key.verify(m3, s3)
    return s1, s2

    
              
def test():
    prng = Random.new().read
    key = RSA.generate(1024, prng)
    print "n = ", key.n
    print "e = ", key.e
    print "d = ", key.d
    print "p = ", key.p
    print "q = ", key.q
    totn = (key.p - 1) * (key.q - 1)
    factor_n(key.n, key.e, key.d, totn)
    # print "p = ", key.p
    # factor n
    
    #verify_rsakey(key.n, key.e, key.d)
    # newkey = RSA.construct(key.n, key.e, key.d)
