#!/usr/bin/env python3
##
# RSA decryption by computing the private key exponent.
# This version needs the prime numbers.
#

import sys;
import operator;
import functools;

##
# Computes Euler's totient function value for the modulus.
#
def euler_totient(primes):
	phi = 1
	for p in primes:
		phi *= (p - 1)
	return phi

##
# Extended GCD
#
def egcd(a, b):
	x,y, u,v = 0,1, 1,0
	while a != 0:
		q, r = b//a, b%a
		m, n = x-u*q, y-v*q
		b,a, x,y, u,v = a,r, u,v, m,n
	gcd = b
	return gcd, x, y

##
# Modular inverse with Extended Euclidean algorithm.
#
def modinv(a, m):
	gcd, x, y = egcd(a, m)
	if gcd != 1:
		return None  # modular inverse does not exist
	else:
		return x % m

##
# Main
#
if len(sys.argv) < 6:
	print("Usage: " + sys.argv[0] + " <ciphertext> <public key exponent> <modulus> <prime factor 1> <prime factor 2>...");
	quit()

# Ciphertext parameter can be omitted:
ciphertext = -1
if sys.argv[1] != '-':
	ciphertext = int(sys.argv[1])

e = int(sys.argv[2])

# Modulus parameter can be omitted:
n = -1
if sys.argv[3] != '-':
	n = int(sys.argv[3])

# Records the prime numbers:
primes = []
for i in range(4, len(sys.argv)):
	primes.append(int(sys.argv[i]))

# Multiply all the prime numbers together.
primes_together = functools.reduce(operator.mul, primes, 1)
if n == -1:
# Modulus parameter was omitted.
	n = primes_together
elif primes_together != n:
# Modulus parameter can be verified.
		print("Incorrect prime factors.")
		exit()

phi = euler_totient(primes)
print("phi(n) = " + str(phi))
d = modinv(e, phi)
print("d = " + str(d))
if ciphertext > 0:
# Ciphertext was omitted or incorrect.
	plaintext = pow(ciphertext, d, n)
	print("plaintext = " + str(plaintext))