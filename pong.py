width, height = 45, 25
score = 0
xplayer = width//2 - 4
xai = xplayer
ballx, bally = width//2, height//2

def print_frame():
	print(chr(27) + "[2J")
	print(xplayer*" "+"="*8+(width-xplayer-7)*" ")
	print((" "*width+"\n")*(bally-2)+" "*width)
	print(" "*(ballx-1)+"O"+(width-ballx)*" ")
	print((" "*width +"\n")*(height-bally-2)+" "*width)
	print(xai*" "+"="*8+(width-xai-7)*" ")
	print("score:",score)

print_frame()