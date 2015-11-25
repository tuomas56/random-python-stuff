import getpass

#very bad code but it works. could be made by printing lines
def displayhangman(stage):
	print(["""




_______""","""      
|     
|      
|     
|_______""",""" ______
|      
|     
|       
|     
|_______""",""" ______
|      0
|     
|      
|     
|_______""",""" ______
|      0
|      |
|       
|     
|_______""",""" ______
|      0
|    / | 
|       
|     
|_______""",""" ______
|      0
|    / | \\
|       
|     
|_______""",""" ______
|      0
|    / | \\
|      |
|        
|_______""",""" ______
|      0
|    / | \\
|      |
|     /   
|_______""",""" ______
|      0
|    / | \\
|      |
|     / \\
|_______"""][stage])

def displayword(word,letters):
	print(''.join(list(map(lambda char: char if char in letters else "_",word))))

def iscomplete(word,letters):
	return all(map(lambda c: c in letters,word))

def get(prompt,conv):
	while True:
		try: return conv(input(prompt))
		except Exception as e: print(e)

def charc(letters):
	def m(i):
		if len(str(i)) == 1:
			return str(i)
		elif str(i) in letters:
			raise Exception("You have already picked that.")
		else:
			raise Exception("Must be one character only.")
	return m

def main():
	guesses = 0
	word = getpass.getpass("Enter word: ")
	letters = []
	while guesses < 10:
		print(chr(27) + "[2J")
		displayhangman(guesses)
		print()
		print("Word:")
		displayword(word,letters)
		print()
		print("Used letters:"," ".join(sorted(set(letters))))
		print()
		l = get("Enter a letter: ",charc(letters))
		if l not in word:
			guesses += 1
		letters.append(l)
		if iscomplete(word,letters):
			return True
	return False

print(chr(27) + "[2J")
print(chr(27) + "[2JYou Won!" if main() else chr(27) + "[2JGame Over. You Lost.")
