import sys
from dtest import test, do_tests

def get(prompt,error,*funcs):
	while True: #loop until input valid
		try: #validate will throw an error if the input is invalid
			x = input(prompt)
			for validate in funcs:
				x = validate(x)
			return x
		except EOFError: 
			#this is thrown by input, 
			#not in case of an invalid value and if it is raised once, 
			#it will be again if we ask for input again.
			print("No input available.\nUnable to continue, exiting.")
			sys.exit(1)
		except:
			print(error) #validate errored so print an error message and loop

@test("Numbers")
def eg1():
	an_int = get("Please enter a whole number: ","Invalid entry.",int)
	print(an_int)
	a_float = get("Please enter a number: ","Invalid entry.",float)
	print(a_float)

def question(x): #this validates whether something is yes or no
	if x == "yes" or x == "y":
		return True
	elif x == "no" or x == "n":
		return False
	else:
		raise ValueError("Not a valid answer.") #throw an error because it is not valid

@test("Question")
def eg2():
	a_bool = get("Please enter yes or no: ","Not valid.",question)
	print(a_bool)

def default(x): #returns a function that replaces "" with x
	def wrapper(y):
		if y == "":
			return x
		else:
			return y
	return wrapper

@test("Default")
def eg3():
	default_answer = get("Please enter a word (default 'hi'): ","Invalid",default("hi"))
	print(default_answer)

#if you want to use more than one validation function then you compose() them together
#e.g if i am asking a yes/no question and I want to default to yes then the validation function
#would be compose(question,default("yes"))

@test("Default Question")
def eg4():
	default_question = get("Please enter yes/no (default - yes): ","Invalid entry.",default('yes'), question)
	print(default_question)

if __name__ == "__main__":
	do_tests()
	