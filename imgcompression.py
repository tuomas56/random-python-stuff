import operator
import struct
from math import cos, pi
from collections import namedtuple
from functools import partial

###SECTION Quantization

qltable = [16, 11, 10, 16, 24, 40, 51, 61, 
		   12, 12, 14, 19, 26, 58, 60, 55,
		   14, 13, 16, 24, 40, 57, 69, 56,
		   14, 17, 22, 29, 51, 87, 80, 62,
		   18, 22, 37, 56, 69, 109,103,77,
		   24, 36, 55, 64, 64, 104,113,92,
		   49, 64, 78, 87,102,121,120,101,
		   72, 92, 95, 98,112,100,103, 99]

qctable = [17, 18, 24, 47, 99, 99, 99, 99,
		   18, 21, 26, 66, 99, 99, 99, 99,
		   24, 25, 56, 99, 99, 99, 99, 99,
		   47, 66, 99, 99, 99, 99, 99, 99,
		   99, 99, 99, 99, 99, 99, 99, 99,
		   99, 99, 99, 99, 99, 99, 99, 99,
		   99, 99, 99, 99, 99, 99, 99, 99,
		   99, 99, 99, 99, 99, 99, 99, 99]

def quantize(data):
	for i in range(len(data)):
		data[i] = (data[i][0]//qltable[i], data[i][1]//qctable[i], data[i][2]//qctable[i])
	return data

###SECTION Downsampling

def downsample(data, xdir, ydir):
	for i in range(len(data)):
		for j in range(len(data[i])):
			if not (i % xdir == 0 and i % ydir == 0):
				data[i][j] = (data[i][j][0],None,None)

###SECTION Blocks

def blocks(n):
	height = len(n)
	width = len(n[0])
	if height % 8 != 0:
		while height % 8 != 0:
			n += [(0,0,0)]*width
			height = len(n)
	if width % 8 != 0:
		while width % 8 != 0:
			for i in range(height):
				n[i] += (0,0,0)
			width = len(n[0])
	for i in range(0, height, 8):
		for j in range(0, width, 8):
			yield map(lambda x: x[j:j + 8], n[i:i+8])	

###SECTION Y'CbCr

def rgb_to_ycbcr(color):
	Y = color[0] * 0.299 + color[1] * 0.587 + color[2] * 0.114
	Cb = 128 - 0.168736 * color[0] - 0.331264 * color[1] + 0.5 * color[2]
	Cr = 128 + 0.5 * color[0] - 0.418688 * color[1] + 0.081312 * color[2]
	return (Y, Cb, Cr)

def ycbcr_to_rgb(color):
	R = color[0] + 1.402 * (color.[2] - 128)
	G = color[0] - 0.34414 * (color[1] - 128) - 0.71414 * (color[2] - 128)
	B = color[0] + 1.772 * (color[1] - 128)
	return (R, G, B) 

###SECTION DCT

def dct(data):
	N = len(data)
	x = data
	def X(k):
		return sum(x[n]*cos((pi/N)*(n + 0.5)*k) for n in range(N))
	return [X(k) for k in range(N)]

def idct(data):
	N = len(data)
	x = data
	def X(k):
		return 0.5*x[0] + sum(x[n]*cos((pi/N)*n*(k + 0.5)) for n in range(N))
	return [X(k) for k in range(N)]

###SECTION Huffman Coding

def generate_probs(data):
	probs = list(set([(data.count(item),item) for item in data]))
	probs = [(count/len(data),item) for count,item in probs]
	return probs

def generate_huffman_tree(probs):
	pqueue = []

	for item in probs:
		pqueue.append(item)
		pqueue.sort(key=operator.itemgetter(0))

	while len(pqueue) > 1:
		n1,n2,*pqueue = pqueue
		pqueue.append((n1[0] + n2[0],(n1,n2)))
		pqueue.sort(key=operator.itemgetter(0))
	return pqueue[0]

def get_symbol_prefix(tree,symbol):
	if tree[1] == symbol:
		return ''
	elif isinstance(tree[1],int):
		raise Exception()
	else:
		try:
			return '0' + get_symbol_prefix(tree[1][0],symbol)
		except:
			return '1' + get_symbol_prefix(tree[1][1],symbol)

def symbol_from_prefix(tree,prefix):
	for char in prefix:
		if char == '0':
			tree = tree[1][0]
		else:
			tree = tree[1][1]
	return tree

def encode_tree(tree):
	if isinstance(tree[1],int):
		return struct.pack('>b',tree[1])
	else:
		return b'\xFF' + encode_tree(tree[1][0]) + encode_tree(tree[1][1])

def dynamic_huffman(data):
	probs = generate_probs(data)
	tree = generate_huffman_tree(probs)

	edata = int(''.join([get_symbol_prefix(tree,symbol) for symbol in data]),2)
	edata = edata.to_bytes(((edata.bit_length() + 7) // 8 + 1),'big')
	edata += encode_tree(tree)

	return edata