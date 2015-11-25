from tkinter import Tk, Canvas, PhotoImage, mainloop

WIDTH, HEIGHT, ITERATIONS = 400, 400, 400

window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#000000")
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")


def mandlebrot(c):
	z = complex(0,0)
	for i in range(ITERATIONS):
		z = z*z + c
		if (z.real*z.real + z.imag*z.imag) >= 4:
			return i
	return ITERATIONS

for x in range(WIDTH):
    for y in range(HEIGHT):
    	color = mandlebrot(complex((4*x/WIDTH) - 2.5,(4*y/HEIGHT) - 2))
    	color = color if color <= 255 else 255
    	img.put('#%02x%02x%02x' % (color%255,(40*(color//255))%4,10*((40*(color//255))//4)),(x,y))
mainloop()