#import random
import os 
import secrets
import hashlib
import sys

def IsPrime(n, s = 50): # Miller-Rabin primality test
  # Call: IsPrime(n,s) with natural numbers n,s
  # Output: True or False
  #     n is prime => Outputs True with probability 1
  #     n is not prime => Outputs True with probability <= 1/(2**s)
  # Runtime for input (n,s): O(s * |n|**2)
  if n < 2: return False
  for j in range(1, s + 1):
    # a = random.randint(1, n - 1)
    a = secrets.randbelow(n - 1) + 1
    i = n - 1
    b = []
    while (i > 0):
      b.append(i % 2)
      i = i // 2
    d = 1
    for i in range(len(b) - 1, -1, -1):
      x = d
      d = (d * d) % n
      if d == 1 and x != 1 and x != n - 1:
        return False
      if b[i] == 1:
        d = (d * a) % n
    if d != 1:
      return False
  return True

def egcd(ld,d): # Extended Euclidean Algorithm
  # Call: egcd(a,b) with natural numbers a,b>0
  # Output: (d,x,y) where:
  #     d is the greatest common divisor of a and b
  #     x,y are integers such that d = x*a + y*b
  # To be done
  # relatively prime
  if ld == 0:
    return (d, 0, 1)
  else:
    g, x, y = egcd(d % ld, ld)
    lx = y - (d // ld) * x
    ly = x
  return (g,lx,ly)

def ModExp(x,y,n): # Modular exponentiation
  # Call: ModExp(x,y,n) with natural numbers x,y,n and n>=2
  # Output: (x**y)%n
  return pow(x, y, n)

def ModInv(e,n): # Modular inverse
  # Call: ModInv(e,n) with natural numbers e,n>0 and gcd(e,n)=1
  # Output: d in {1,...,n-1} such that (d*e)%n = 1
  g, x, y = egcd(e, n)
  if g != 1:
    raise Exception('Modular inverse does not exist')
  return x % n

def RSAKeyGen(r=1024):
  # Call: RSAKeyGen(r) with natural number r>=5
  # Output: ((n,e),(n,d)) where
  #     n = p*q for random primes p,q with p!=q and
  #         p,q in [2**l, 2**(l+1)), where l = (r+2)//2
  #     e = random integer with 1<e<phi(n) and gcd(e,phi(n))=1
  #     d = inverse of e modulo phi(n),
  #         i.e. 1<d<phi(n) with (e*d) % phi(n) = 1
  #
  # Hint: The command random.randint(a,b) returns a
  #       uniformly distributed random integer from {a, a+1, ..., b}.
  l = (r + 2) // 2
  def get_random_prime(q):
    while True:
      p = secrets.randbelow(2**(l+1) - 2**l) + 2**l
      if IsPrime(p):
        if p and p != q:
          return p
  p = get_random_prime(None)
  q = get_random_prime(p)
  n = p * q
  phi_n = (p - 1) * (q - 1)
  while True:
    # 2 < e < phi_n -1
    e = secrets.randbelow(phi_n - 2) + 2
    g, _, _ = egcd(e, phi_n)
    if g == 1:
      break
  d = ModInv(e, phi_n)  
  return ((n,e),(n,d))

def RSAEncrypt(pk,m):
  # Call: RSAEncrypt(pk,m) with public key pk and plaintext m
  # Output: ciphertext c
  c = ModExp(m, pk[1], pk[0])
  return c

def RSADecrypt(sk,c):
  # Call: RSADecrypt(sk,c) with secure/private key sk and ciphertext c
  # Output: decrypted message m
  m = ModExp(c, sk[1], sk[0])
  return m

def str2int(s): # encodes a string as an integer (for testing RSA)
  # Call: str2int('Das ist ein Test.')
  # Output: 23268733837745479405720608239248647353390
  x = 0
  for i in range(0,len(s)):
    x = (x<<8) + ord(s[i])
  return x

def int2str(x): # encodes an integer as a string (for testing RSA)
  # Call: int2str(23268733837745479405720608239248647353390)
  # Output: 'Das ist ein Test.'
  s = ''
  while(x>0):
    s = chr(x&255) + s
    x = x >> 8
  return s

def RSATest():
  ms = 'NSA from USA hates RSA.'
  m=str2int(ms)
  print("Plaintext as string:      "+ms)
  print("Plaintext as integer:     "+str(m))
  r = len(bin(m))-2                 # determine the bit length of the plaintext
  (pk,sk)=RSAKeyGen(r)
  (n,e)=pk
  (n,d)=sk
  print("n =                       "+str(n))
  print("e =                       "+str(e))
  print("d =                       "+str(d))
  c=RSAEncrypt(pk,m)
  cs=int2str(c)
  print("Ciphertext as integer:    "+str(c))
  b=RSADecrypt(sk,c)
  bs=int2str(b) 
  print("Decrypted text as string: "+bs)
  print("Decrypted text as integer:"+str(b))
  return

# Exercise sheet 15
def Hash(m): # returns the SHA256 hash value for string m in {0,...,2**256-1}
  h=hashlib.sha256(bytearray(m,'UTF8')) # convert to bytearray for SHA
  s=h.hexdigest()                       # string with hash value in hex
  return int(s,16)                      # hash value as integer

def RSASignature(sk,m): # signs a message m
  # Call: RSASignature(sk,m) with secure key sk and message m (String)
  # Output: signed message sig = (m,s)
  s = ModExp(Hash(m), sk[1], sk[0])
  return (m,s)

def RSASignatureVerify(pk,sig): # verifies a signature of a message
  # Call: RSASignatureVerify(pk,sig) with pk=public key, sig=signed message
  # Output: True if signature is valid, False otherwise
  n, e = pk
  # Extract message m and signiture s
  m, s = sig
  h_m = Hash(m)
  h_m_prime = ModExp(s, e, n)
  # Check value hashed by Bob and hash value decrypted using message.
  return h_m == h_m_prime
  #return True

def RSASignatureTest(): # example for RSA signature
  (pk,sk)=RSAKeyGen(257)            # generate RSA modulus n > 2**256
  sys.set_int_max_str_digits(31000) # increase limit for str(...)
  m = str(7777**7777)               # plaintext with 30259 characters
  sig=RSASignature(sk,m)
  print("Signed document: sig = " + str(sig[1]))
  print("Verification: " + str(RSASignatureVerify(pk,sig)))
  return


if __name__ == "__main__":
  RSATest()
  RSASignatureTest()
