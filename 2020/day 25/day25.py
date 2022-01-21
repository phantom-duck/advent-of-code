import sys
from pprint import pprint

MODULUS = 20201227

def transform(subject, loop_size):
	res = 1
	for i in range(loop_size):
		res = (res * subject) % MODULUS
	return res

def reverse_transform(subject, public_key):
	res = 1
	exponent = 0
	while True:
		res = (res * subject) % MODULUS
		exponent += 1
		if res == public_key:
			return exponent

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read().split()
	
	pk1 = int(text[0])
	pk2 = int(text[1])
	
	##### Part 1: Find Diffie Hellman final shared secret key
	
	sk1 = reverse_transform(7, pk1)
	encryption_key = transform(pk2, sk1)
	
	print(encryption_key)