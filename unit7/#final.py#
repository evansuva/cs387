import bits

def find_longest_repetition(p):
    print "find_longest: ", bits.display_bits(p)
    longest = 0
    repeated = None
    for i in range(len(p)):
        # find longest starting at p[i]
        for k in range((len(p) - 1) / 2):
            match = p[i:i+k+1]
            if len(match) <= longest:
                continue
            for m in range(i+k+1,len(p) - len(match)):
                if match == p[m:m+k+1]:
                    longest = len(match)
                    repeated = match
                    continue
    return longest, repeated
    
def GSM_1(n):
    """First LFSR for A5_1 cipher"""
    lfsr1 = [0, 1, 1, 0, 0,
             1, 0, 1, 1, 1,
             0, 0, 0, 1, 1,
             0, 1, 0, 0]  # 19 bits
        
    allout = []
    for unused in range(n):
        output1 = lfsr1[-1]
        newbit = (((((lfsr1[18] + lfsr1[17]) % 2) + lfsr1[16]) % 2) + lfsr1[13]) % 2
        lfsr1 = [newbit] + lfsr1[:18]
        #print output, bits.display_bits(lfsr)[::-1]
        allout.append(output1)
        #print bits.display_bits(allout)
        
    return allout

def make_challenge(s):
    b = bits.string_to_bits(s)
    bstream = GSM_1(1000 + len(b))
    pad = bstream[1000:]
    cipher = bits.xor_bits(b, pad)
    assert len(bstream[:1000]) + len(cipher) == len(bstream)
    return bstream[:1000], cipher, pad

