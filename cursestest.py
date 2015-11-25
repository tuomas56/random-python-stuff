from curses import wrapper
import os

def main(scr):
	scr.clear()
	width, height = os.get_terminal_size()
	s = ''
	x, y = 0, 0
	while True:
		k = scr.getch()
		if k < 127:
			s += chr(k)
			if s[-1] == '\n':
				break
			else:
				if x >= width:
					y += 1
					x = 0
				scr.addch(y, x, s[-1])
				x += 1
			scr.refresh()
		elif k == 127 and (x > 0 or y > 0) and s:
			*s, _ = s
			if x > 0:
				x -= 1
			else:
				x = width - 1
				y -= 1
			scr.addch(y, x, ' ')
			scr.move(y, x)
			scr.refresh()
	scr.clear()
	scr.addstr(0, 0, s)
	scr.getch()

wrapper(main)
