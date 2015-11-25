from itertools import accumulate
import operator

fact = lambda n: 1 if n == 1 else fact(n-1)*n
bncoff = lambda n,k: fact(n)/(fact(k)*fact(n-k))
print(bncoff(40,20))