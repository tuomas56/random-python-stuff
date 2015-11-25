for _ in range(int(input())):
    N = int(input())
    h = 1
    for x in range(1,N+1):
    	if x % 2 == 1:
    		h *= 2
    	else:
    		h += 1
    print(h)