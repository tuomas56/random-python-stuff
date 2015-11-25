def interpret(s):
	stacks = [[]]
	currstack = 0
	skip = False
	n = False
	for char in s:
		if skip:
			skip = False
			continue
		if char == '!':
			stacks += []
			stacks[currstack].append(len(stacks) - 1)
		elif char == '$':
			curstack = stacks[currstack].pop()
		elif char == ':':
			if n:
				print(stacks[currstack].pop())
				n = False
			else:
				print(chr(stacks[currstack].pop()))
		elif char == ';':
			if n:
				stacks[currstack].append(int(input()))
				n = False
			else:
				stacks[currstack].append(ord(input()))
		elif char == '+':
			stacks[currstack][-1] += 1
		elif char == '-':
			stacks[currstack][-1] -= 1
		elif char == '<':
			stacks[0].append(stacks[currstack].pop())
		elif char == '>':
			stacks[currstack].append(stacks[0].pop())
		elif char == '0':
			stacks[currstack].append(0)
		elif char == '=':
			stacks[currstack].append(stacks[currstack].pop() == stacks[currstack].pop())
		elif char == '?':
			if stacks[currstack.pop(0)] == 0:
				skip = True
		elif char == 'n':
			n = True

interpret(input())