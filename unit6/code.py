from __future__ import division
import crypto

def prob_caught(votes, audited, cheat):
    noncheat = votes - cheat
    safeaudits = 1
    for i in range(noncheat - audited + 1, noncheat + 1):
        safeaudits = safeaudits * i
        print safeaudits, i
    print safeaudits, votes, cheat
    return safeaudits / (votes ** audited)


