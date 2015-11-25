import itertools

ascii_printable = [chr(i) for i in range(32,128)]

def poly(codeword,data,encrypt=True):
 return ''.join([ascii_printable[(ascii_printable.index(d) + (ascii_printable.index(c) if encrypt else -ascii_printable.index(c))) % 95] for d,c in zip(data,itertools.cycle(codeword))])


codeword = input("Please enter codeword: ")
data = input("Please enter data: ")
encoded = poly(codeword,data)
print(' '.join(list(codeword)))
print(' '.join(map(str,map(ord,codeword))))
print(' '.join(list(data)))
print(' '.join(map(str,map(ord,data))))
print(' '.join(list(encoded)))
print(' '.join(map(str,map(ord,encoded))))

decoded = poly(codeword,encoded,encrypt=False)

print(' '.join(list(codeword)))
print(' '.join(map(str,map(ord,codeword))))
print(' '.join(list(encoded)))
print(' '.join(map(str,map(ord,encoded))))
print(' '.join(list(decoded)))
print(' '.join(map(str,map(ord,decoded))))