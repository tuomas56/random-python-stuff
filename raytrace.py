from tkinter import Tk, Canvas, PhotoImage, mainloop
from math import sin

WIDTH, HEIGHT = 640, 480

window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#000000")
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

def intersect(x,y):
    return isPrime(x);

def isPrime(n):
    return len(list(filter(lambda x: x % n == 0,range(n)))) == 2

def pixel(x,y,r,g,b):
    img.put('#%02x%02x%02x' % (r,g,b),(x,y));

def main():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if intersect(x,y):
                pixel(x,y,255,255,255);
            else:
                pixel(x,y,0,0,0);
main();
