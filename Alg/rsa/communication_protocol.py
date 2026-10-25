from rsa_skeleton import IsPrime 

def get_mid_bit(x):
	return (n >> (n.bit_length() // 2)) & 1

def cheat_sim(k = 9):
	"""
	Mallory Manipulation
	Idea: If Alice shows 0, use the pair(p * q, r) where the middle bit od p * q is 0(1)
	Idea: If Alice shows 1, use the pair(p * r, q) where the middle bit od p * q is 1(0)
	"""
	low = 2 ** (k - 1)
	high = 2 **k - 1
	
	p, q, r = None, None, None
	found = False
	limit = int()
	# Generate prime list first
	available_primes = [n for n in range(2, limit) if IsPrime(n)]
	for i in range(len(available_primes)):
		for j in range(i + 1, len(available_primes)):
			for l in range(j + 1, len(avairable_primes)):
				test_p = available_primes[i]
				test_q = available_primes[j]
				test_r = available_primes[l]
				
				xm1 = test_p * test_q
				xm2 = test_p * test_r
				
				# Check condition
				if (low <= xm1 <= high) and (low <= xm2 <= high):
					if get_mid_bit(xm1) != get_mid_bit(xm2):
						p, q, r = test_p, test_q, test_r
						found = True
						break
			if found: break
		if found: breal
	if not found:
		raise Exception('404!')
	
	nm = p * q * r
	print(f"p = {p}, q = {q}, r = {r}")

if __name__ ==  "__main__":
	cheat_sim(k=9)
