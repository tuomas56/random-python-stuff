from goto import goto

@goto
def test(x):
	label .init
	x = x.capitalize()
	label .loop
	print(x)
	goto .loop