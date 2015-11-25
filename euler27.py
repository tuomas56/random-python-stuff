primes = [1,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]

def is_prime(n):
	if n <= 3:
		return n >= 2
	if n % 2 == 0 or n % 3 == 0:
		return False
	for i in range(5, int(n ** 0.5) + 1, 6):
		if n % i == 0 or n % (i + 2) == 0:
			return False
	return True

def do_run(a, b):
	i = 0
	while is_prime(i**2 + i*a + b):
		i += 1
	return i

results = []
for a in primes:
	for b in primes:
		results.append((do_run(a, b),a,b))
		results.append((do_run(-a, b),-a,b))
		results.append((do_run(a, -b),a,-b))
		results.append((do_run(-a, -b),-a,-b))
		print("next")

result = max(results)
print(result[1]*result[2])