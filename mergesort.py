from functools import partial

#split(ls: list[l]<T>) -> list[2]<list[l//2]<T>,list[l - l//2]<T>>
#split ls into 2 lists
def split(ls):
	middle = len(ls)//2
	return [ls[:middle],ls[middle:]]

#merge(left: list[l]<T>,right: list[l]<T>,f: func(T,T) -> bool) -> list[2*l]<T>
#merges two sorted list into one sorted list based on comparison function f
def merge(left,right,f):
	result = []
	while len(left) > 0 or len(right) > 0:
		if len(left) > 0 and len(right) > 0:
			if f(left[0],right[0]):
				result.append(left.pop(0))
			else:
				result.append(right.pop(0))
		elif len(left) > 0:
			result.append(left.pop(0))
		elif len(right) > 0:
			result.append(right.pop(0))
	return result

#sort(ls: list[l]<T>,[f: func(T,T) -> bool]?) -> list[l]<T>
#sorts a list based on the comparison function f
#(f is optional - defaults to smallest -> largest - i.e a < b)
def sort(ls,f=lambda a,b: a < b):
	if len(ls) == 2:
		return [ls.pop(0) if f(ls[0],ls[1]) else ls.pop(1),ls[0]]
	elif len(ls) == 1:
		return ls
	else:
		ls = list(map(partial(sort,f=f),split(ls)))
		return merge(ls[0],ls[1],f)

print(sort([1,4,2,4,2,8,3,5,3,7,4,6],lambda a,b: a == 3))


