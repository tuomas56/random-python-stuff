def bncof(n,k):
	return 1 if (n == k or k == 0) else bncof(n-1,k-1)+bncof(n-1,k);

def bnthm(x,y,n):
	return sum([(bncof(n,k) * x**(n - k) * y**k) for k in range(n+1)]);

print(bnthm(3,4,2));