# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 11:47:39 2017
NPQ : Given an integer N, and two sigle digit number p and q, 
output all the numbers from 1 to N, separate with comma
However any number divisible by p or q should be replaced by "OUT"
and the number whose digital representation include p or q should be replaced by "THINK"
If both satisfied replace with "OUTTHINK"
>>> NPQ (20,3,4)
'1,2,OUTTHINK,OUTTHINK,5,OUT,7,OUT,OUT,10,11,OUT,THINK,THINK,OUT,OUT,17,OUT,19,OUT'

>>> NPQ (7,2,3)
'1,OUTTHINK,OUTTHINK,OUT,5,OUT,7'
@author: chens
"""

def NPQ(N, p, q):
    resultList = []
    for x  in range(1, N + 1):
        mark1 = 0
        mark2 = 0
        listelement = str(x)
        if x % q == 0 or x % p == 0:
            listelement = "OUT"
            mark1 = -1
        if q in [int(d) for d in str(x)] or p in [int(d) for d in str(x)]:
            listelement = "THINK"
            mark2 = -1
        if mark1*mark2 > 0:
            listelement = "OUTTHINK"
        resultList.append(listelement)
        #convert list to comma separated string
    return ','.join(resultList)

if __name__ == "__main__":
    resultStr = NPQ (20,3,4)
    resultStr2 = NPQ (7,2,3)
    print(resultStr)
    print(resultStr2)