import hashlib
from functools import partial

def genkeys(num, key, hash):
	for _ in range(num):
		key = hash(key)
		yield key

def F(R, K, hash):
	a, b = hash(R) ^ K, hash(R ^ K)
	return a + b

def encrypt(data, key, hash, rounds):
	L, R = map(partial(int.from_bytes, byteorder="big"), (data[::2], data[1::2]))
	for K in list(genkeys(rounds, key, hash)):
		L, R = R, L ^ F(R, K, hash)
	return (L + R).to_bytes(((L + R).bit_length() + 1)//7, byteorder="big")

def decrypt(data, key, hash, rounds):
	L, R = map(partial(int.from_bytes, byteorder="big"), (data[::2], data[1::2]))
	for K in list(genkeys(rounds, key, hash))[::-1]:
		L, R = R, L ^ F(R, K, hash)
	return (L + R).to_bytes(((L + R).bit_length() + 1)//7, byteorder="big")

def sha256_hash(data):
	m = hashlib.sha256()
	m.update(data.to_bytes((data.bit_length() + 1)//7, byteorder="big"))
	return int.from_bytes(m.digest(), byteorder="big")

a = encrypt("Hey".encode(), 12987312, sha256_hash, 10)
print(a)
b = decrypt(a, 12987312, sha256_hash, 10).decode('utf-8')
print(b)
