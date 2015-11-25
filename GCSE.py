#This isn't really prep but I was wondering if when it's done you could mark it.
#It is task three from the AQA syllabus (traditional programming) and I've written it as good as I can to see if it is good enough that the examiners might be suspicious
#It's not done yet
#Current Bugs:
#	1) When displaying menus, the options are randomly ordered although the function still works... I think it is a problem with dict.keys()...
#	   FIXED! In future I must remember that dict does not remember initial insertion order... use OrderedDict if needed. For now I will instead patch the exit special case

#REGION Imports
import sys
from json import loads, dumps
from functools import partial
from time import time
import os
#ENDREGION

#REGION Database

#enum WorkTypes
#stores work_id information for the relational "database"
#I have to use a relational database because I can't use more than two columns in a python dict
#I could use lists of lists but that would probably be messy...
#I have preseeded this, prices and times with default values so if loading from JSON fails the defaults will be enabled
Table_WorkTypes = {
	'lawn':0,
	'patio':1,
	'deck':2,
	'pond':3,
	'wtrftr':4,
	'light': 5
}

#enum Prices
#Primary key: work_id
Table_Prices = {
	0:15.50,
	1:20.99,
	2:15.75,
	3:25.00,
	4:150.0,
	5:5.000
}

#enum Times
#Primary key: work_id
Table_Times = {
	0:20,
	1:20,
	2:30,
	3:45,
	4:60,
	5:10
}

#cost per hour in pounds
Cost_Per_Hour = 16.49

#Class Work
#Has fields for time and price and work type and an update function
class Work:
	#constructor(time: int,price: float,work: string)
	def __init__(self,time=False,price=False,work=False,json=False):
		if (not time) and (not price) and (not work) and (not (json is False)):
			data = loads(json)
			self.work = data.work
			self.time = data.time
			self.price = data.price
		elif (not time) and (not price) and (not work) and (not json):
			raise Error("Either values or JSON must be specified when constructing Work object")
		else:
			self.work = work
			self.time = time
			self.price = price

	@property #Use getters and setters with the @property decorator so we don't have to call an update function
	def time(self):
	    return Table_Times[Table_WorkTypes[self.work]] #Get the value from the DB
	@time.setter
	def time(self, value):
	    Table_Times[Table_WorkTypes[self.work]] = value #Set the value in the DB
	
	@property
	def price(self):
	    return Table_Prices[Table_WorkTypes[self.work]]
	@price.setter
	def price(self, value):
	    Table_Prices[Table_WorkTypes[self.work]] = value


#select(work: string) -> Work
#get a work object from work type string
def select(work):
	work_id = Table_WorkTypes[work]
	time = Table_Times[work_id]
	price = Table_Prices[work_id]
	return Work(time=time,price=price,work=work)

#insert(work: Work) -> None
#insert an object into the database
def insert(work):
	#index: insertation index. maximum index already in the table plus one
	index = maxlength(Table_WorkTypes.values()) + 1
	Table_WorkTypes[work.work] = index
	Table_Prices[index] = work.price
	Table_Times[index] = work.time

#remove(work: string) -> None
#remove an object from the database
def remove(work):
	work_id = Table_WorkTypes[work]
	try:
		del Table_WorkTypes[work]
		del Table_Times[work_id]
		del Table_Prices[work_id]
	except:
		pass


#ENDREGION

#REGION Helper Functions

#get(prompt: string, error: string, conv: function) -> any
#get a value via the console with a prompt that is valid according to validation function conv and return it or retry and display error until successful
#e.g get("Enter a number: ","That is not a number",int) will display Enter a number: and query for input and, if it is not a number, display That is not a number and then ask for input again.
def get(error,conv,prompt):
	while True:
		try:
			return conv(input(prompt))
		except EOFError:
			#Exit gracefully
			print("No more input: can't continue; exiting.")
			sys.exit(1)
		except:
			print(error)


#switch(input: string,choices: dict,default (optional): function) -> any
#switches between functions in choices that have key input or default if there is no key input in choices
def switch(input,choices,default=None):
	func = choices.get(input,default)
	if func != None:
		return func()

#zipdict(arr1: list of string, arr2: list) -> dict
#zips two lists into a dictionary such that dict.keys() == arr1 and dict.values() == arr2
def zipdict(arr1,arr2):
	d = {}
	for i in range(0,len(arr1)):
		d[arr1[i]] = arr2[i]
	return d

#shallowcopy(arr: list) -> list
#shallow copies an array so you keep the references to the stored variables but the list (not the contents) can be modified without affecting the other
#as opposed to a deep copy where the contents and the list are both copied
def shallowcopy(arr):
	return arr[:]

#int_with_clamp(value: string,min: number, max: number) -> int
#converts an string to an int and makes sure it is within the given range
#I can't use min and max as argument names as those are builtins...
def int_with_clamp(value,mi,ma):
	v = int(value)
	if v <= ma and v >= mi:
		return v
	else:
		raise Error("Value must be between "+str(mi)+" and "+str(ma))

#menu(prompt: string,options: list,error: string) -> int
#dispays a menu which allows the user to choose from a series of options
def menu(prompt,options,error):
	print(prompt)
	loptions = len(options)
	for i in range(0,loptions):
		print(" "*4+str(i+1)+")",options[i]) #print x) option where x in the option number
	def validate(input): #Defining a function inside a function is bad practise but doing it with lambdas would be messy
		return int_with_clamp(input,1,loptions+1)
	return get(error,validate,"Please choose an option [1-"+str(loptions)+"]: ") - 1

#boxify(headers: list of string, data: list of list of string) -> None
#Outputs an ascii table with headers and data
def boxify(headers,data=[[]]):
	temp = "╔"
	for x in range(0,len(headers)):
		temp += "═"*(maxlength(data[x] + [headers[x]])) + "╤"
	temp = temp[:-1]+"╗"
	print(temp) #Print the top of the box to be long enough for the largest items in the columns
	temp = "║"
	for x in range(0,len(headers)):
		temp += headers[x]+" "*(maxlength(data[x] + [headers[x]]) - len(headers[x]))+"│"
	temp = temp[:-1]+"║"
	print(temp)
	if len(data[0]) != 0:
		temp = "╟"
		for x in range(0,len(headers)):
			temp += "─"*(maxlength(data[x] + [headers[x]])) + "┼"
		temp = temp[:-1]+"╢"
		print(temp) #Print the bar after the headers to be long enough for the largest items in the columns
	for y in range(0,len(data[0])):
		temp = "║"
		for x in range(0,len(headers)):
			temp += data[x][y]+" "*(maxlength(data[x] + [headers[x]]) - len(data[x][y]))+"│" #Print data itself
		temp  = temp[:-1]+"║"
		print(temp)
	temp = "╚"
	for x in range(0,len(headers)):
		temp += "═"*(maxlength(data[x] + [headers[x]])) + "╧"
	temp = temp[:-1]+"╝"
	print(temp) #Print the bottom of the box to be long enough for the largest items in the columns

#maxlength(l: list of string) -> int
#Gets the length of the biggest string in the list
def maxlength(l):
	return max(map(len,l))

#distribute(arr: list, target: list of list) -> list of list
#Takes arr and distributes it across target lists by adding one element from arr to each list in target
def distribute(arr,target):
	for x in range(0,len(target)):
		target[x].append(arr.pop(0))
	return target
#ENDREGION

#REGION Main Program

#new() -> int
def new():
	print("\nMaking new quote\n"+"═"*16+"\n")
	#Define getf to be get with a predetermined error and conv argument using a partial application
	getf = partial(get,"That is not a number.",float)
	#Alternative: getf = lambda x: get("That is not a number.",float,x) #They are not quite the same but in this situation they work the same
	#Get all the inputs and calculate the areas for the quotes
	lawnw = getf("Please enter the lawn width: ")
	lawnh = getf("Please enter the lawn height: ")
	lawna = lawnw * lawnh
	patiow = getf("Please enter the patio width: ")
	patioh = getf("Please enter the patio height: ")
	patioa = patiow * patioh
	deckw = getf("Please enter the decking width: ")
	deckh = getf("Please enter the decking height: ")
	decka = deckw * deckh
	pondw = getf("Please enter the pond width: ")
	pondh = getf("Please enter the pond height: ")
	ponda = pondw * pondh
	wtrftrs = getf("Please enter the number of water features: ")
	lights = getf("Please enter the number of garden lights: ")
	print("\n")
	boxify(["          Working Costs          "]) #Title surrounded by box
	work = select('lawn')
	data = [[],[],[],[],[],[]]
	total = work.price*lawna
	distribute(['Lawn',str(lawnh),str(lawnw),str(lawna),str(work.price),str(round(work.price*lawna,2))],data) #Distribute row data across columns for table
	work = select('patio')
	total += work.price*patioa
	distribute(['Concrete Patio',str(patioh),str(patiow),str(patioa),str(work.price),str(round(work.price*patioa,2))],data) #Same here etc....
	work = select('deck')
	total += work.price*decka
	distribute(['Wooden Decking',str(deckh),str(deckw),str(decka),str(work.price),str(round(work.price*decka,2))],data)
	work = select('pond')
	total += work.price*ponda
	distribute(['Rectangular Pond',str(pondh),str(pondw),str(ponda),str(work.price),str(round(work.price*ponda,2))],data)
	boxify(["Item","Length","Width","Total Area","Cost per m2","Total Cost"],data) #take the data and boxify it
	work = select('wtrftr')
	data = [[],[],[],[]]
	total += work.price*wtrftrs
	distribute(['Water Features',str(work.price),str(wtrftrs),str(round(work.price*wtrftrs,2))],data) #Same again with other items
	work = select('light')
	total += work.price*lights
	distribute(['Garden Lights',str(work.price),str(lights),str(round(work.price*lights,2))],data)
	boxify(["Item","Price per item","Number of items","Total Cost"],data)
	boxify(["Total Working Costs"],[[str(round(total,2))]]) #Total box is one column
	print("\n")
	boxify(["           Labour Costs          "])
	work = select('lawn')
	data = [[],[],[],[]]
	total = work.time*lawna
	distribute(['Lawn',str(work.time),str(lawna),str(work.time*lawna)],data)
	work = select('patio')
	total += work.time*patioa
	distribute(['Concrete Patio',str(work.time),str(patioa),str(work.time*patioa)],data)
	work = select('deck')
	total += work.time*decka
	distribute(['Wooden Decking',str(work.time),str(decka),str(work.time*decka)],data)
	work = select('pond')
	total += work.time*ponda
	distribute(['Rectangular Pond',str(work.time),str(ponda),str(work.time*ponda)],data)
	boxify(["Item","Minutes per m2","Total area","Total minutes"],data)
	data = [[],[],[],[]]
	work = select('wtrftr')
	total += work.time*wtrftrs
	distribute(['Water Features',str(work.time),str(wtrftrs),str(work.time*wtrftrs)],data)
	work = select('light')
	total += work.time*lights
	distribute(['Garden Lights',str(work.time),str(lights),str(work.time*lights)],data)
	boxify(["Item","Minutes per item","Number of items","Total minutes"],data)
	boxify(["Total Minutes","Total Hours","Cost per hour","Total labour cost"],[[str(total)],[str(round(total/16,2))],[str(Cost_Per_Hour)],[str(round(Cost_Per_Hour*round(total/16,2),2))]])
	print("\n")
	keys = ["Save this quote","Go to the main menu","Quit"]
	usercmd = menu("What would you like to do?",keys,"Not a valid choice.")
	if keys[usercmd] == "Quit":
		return 0
	elif keys[usercmd] == "Go to the main menu":
		return main()
	else:
		data = {
			'sse': time(),
			'lawn': {
				'h': lawnh,
				'w': lawnw
			},
			'patio': {
				'h': patioh,
				'w': patiow
			},
			'deck': {
				'h': deckh,
				'w': deckw
			},
			'pond': {
				'h': pondh,
				'w': pondw
			},
			'wfs': wtrftrs,
			'lts': lights
		}
		with open("quotes/"+get("Not a valid file name.",str,"\nPlease enter the name of the file you wish to save this quote too: "),'w') as f:
			f.write(dumps(data))
		return main()

#view() -> int
def view():
	print("\nViewing previous quote\n"+"═"*22+"\n")

	def exists_and_json(filename):
		with open("quotes/"+filename,'r') as f:
			return loads(f.read())

	data = get("Not a valid file name.",exists_and_json,"Please enter the name of the file containing the required quote: ")

	lawnw = data['lawn']['w']
	lawnh = data['lawn']['h']
	lawna = lawnw * lawnh
	patiow = data['patio']['w']
	patioh = data['patio']['h']
	patioa = patiow * patioh
	deckw = data['deck']['w']
	deckh = data['deck']['h']
	decka = deckw * deckh
	pondw = data['pond']['w']
	pondh = data['pond']['h']
	ponda = pondh * pondw
	wtrftrs = data['wfs']
	lights = data['wfs']
	sse = data['sse']

	boxify(["          Working Costs          "]) #Title surrounded by box
	work = select('lawn')
	data = [[],[],[],[],[],[]]
	total = work.price*lawna
	distribute(['Lawn',str(lawnh),str(lawnw),str(lawna),str(work.price),str(round(work.price*lawna,2))],data) #Distribute row data across columns for table
	work = select('patio')
	total += work.price*patioa
	distribute(['Concrete Patio',str(patioh),str(patiow),str(patioa),str(work.price),str(round(work.price*patioa,2))],data) #Same here etc....
	work = select('deck')
	total += work.price*decka
	distribute(['Wooden Decking',str(deckh),str(deckw),str(decka),str(work.price),str(round(work.price*decka,2))],data)
	work = select('pond')
	total += work.price*ponda
	distribute(['Rectangular Pond',str(pondh),str(pondw),str(ponda),str(work.price),str(round(work.price*ponda,2))],data)
	boxify(["Item","Length","Width","Total Area","Cost per m2","Total Cost"],data) #take the data and boxify it
	work = select('wtrftr')
	data = [[],[],[],[]]
	total += work.price*wtrftrs
	distribute(['Water Features',str(work.price),str(wtrftrs),str(round(work.price*wtrftrs,2))],data) #Same again with other items
	work = select('light')
	total += work.price*lights
	distribute(['Garden Lights',str(work.price),str(lights),str(round(work.price*lights,2))],data)
	boxify(["Item","Price per item","Number of items","Total Cost"],data)
	boxify(["Total Working Costs"],[[str(round(total,2))]]) #Total box is one column
	print("\n")
	boxify(["           Labour Costs          "])
	work = select('lawn')
	data = [[],[],[],[]]
	total = work.time*lawna
	distribute(['Lawn',str(work.time),str(lawna),str(work.time*lawna)],data)
	work = select('patio')
	total += work.time*patioa
	distribute(['Concrete Patio',str(work.time),str(patioa),str(work.time*patioa)],data)
	work = select('deck')
	total += work.time*decka
	distribute(['Wooden Decking',str(work.time),str(decka),str(work.time*decka)],data)
	work = select('pond')
	total += work.time*ponda
	distribute(['Rectangular Pond',str(work.time),str(ponda),str(work.time*ponda)],data)
	boxify(["Item","Minutes per m2","Total area","Total minutes"],data)
	data = [[],[],[],[]]
	work = select('wtrftr')
	total += work.time*wtrftrs
	distribute(['Water Features',str(work.time),str(wtrftrs),str(work.time*wtrftrs)],data)
	work = select('light')
	total += work.time*lights
	distribute(['Garden Lights',str(work.time),str(lights),str(work.time*lights)],data)
	boxify(["Item","Minutes per item","Number of items","Total minutes"],data)
	boxify(["Total Minutes","Total Hours","Cost per hour","Total labour cost"],[[str(total)],[str(round(total/16,2))],[str(Cost_Per_Hour)],[str(round(Cost_Per_Hour*round(total/16,2),2))]])
	
	return main()

#report() -> int
def report():
	print("Report")
	return 0

#main() -> int
def main():
	if not os.path.exists(os.path.relpath("quotes")): #create the quotes directory if it does not exist
    	os.makedirs(os.path.relpath("quotes")) #there is a race condition that could cause this code to error but it's rare enough to ignore...
	keys = ["Make a new quote","Get a previous quote","Display a month report","Quit"] #Lists remember order so use a list to store the keys
	values = [new,view,report,None] #To avoid repeating the keys use zipdict and a values list.
	options = zipdict(keys,values)
	usercmd = menu("What would you like to do?",keys,"Not a valid choice.")
	if keys[usercmd] == "Quit": #I would rather not use sys.exit in another function so make Quit a special case
		return 0
	return switch(keys[usercmd],options) #This will switch to one of the functions in the dictionary above based on the users choice
										 #We shouldn't need default because we have already clamped the value
if __name__ == "__main__":
	sys.exit(main())

#ENDREGION