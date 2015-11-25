import pygame
import time
import random
from pygame.locals import *
import pygame.image
import sys


class Actor:
	def __init__(self, _parent=None,_index=None):
		self._parent = _parent
		self._index = _index

	def draw(self,surface):
		pass

	def load(self):
		pass

	def __del__(self):
		if self._index is not None:
			del self._parent[self._index]

class Asset:
	def __init__(self):
		pass

	def load(self):
		pass

	def value(self):
		pass

class ImageAsset(Asset):
	def __init__(self, image):
		self._image = image

	def value(self):
		return self._image

class ImageFromFile(ImageAsset):
	def __init__(self, filename):
		self._name = filename

	def load(self):
		self._image = pygame.image.load(self._name)
		if self._image.get_alpha() is None:
			self._image = image.convert()
		else:
			self._image = image.convert_alpha()

class RawSurface:
	def __init__(self,surface):
		self._surface = surface

	def set_pixel(self,x,y,color):
		self._surface.set_at((x,y),color)

	def get_pixel(self,x,y):
		return self._surface.get_at((x,y))



class Game:
	def __init__(self,width=640,height=480,title='Game',background=(250,250,250),cls=True):
		self._width = width
		self._height = height
		self._title = title
		self._background = background
		self._prev = 0
		self._cls = cls
		self.actors = []

	@property
	def width(self):
	    return self._width

	@width.setter
	def width(self,value):
		self._width = value
		self._screen = pygame.display.set_mode((self.width,self.height))

	@property
	def height(self):
	    return self._height

	@height.setter
	def height(self,value):
		self._height = value
		self._screen = pygame.display.set_mode((self.width,self.height))

	@property
	def title(self):
	    return self._title
	
	@title.setter
	def title(self,value):
		self._title = value
		pygame.display.set_caption(self._title)

	def run(self):
		pygame.init()
		self._screen = pygame.display.set_mode((self.width,self.height))
		pygame.display.set_caption(self._title)
		self._surface = pygame.Surface(self._screen.get_size()).convert()
		self._surface.fill(self._background)
		self.surface = RawSurface(self._surface)
		self.preload()
		self._prev = time.time()
		while True:
			self._loop()

	def preload(self):
		pass

	def update(self, delta_time):
		pass

	def handle_event(self, event):
		pass

	def addActor(self, actor):
		self.actors.append(actor)
		actor._parent = self.actors
		actor._index = len(self.actors) - 1
		
	def draw(self):
		if self._cls:
			self._surface.fill(self._background)
		for actor in self.actors:
			actor.draw(self._surface)

	def _loop(self):
		for event in pygame.event.get():
			self.handle_event(event)

		self.update(time.time()-self._prev)
		self._prev = time.time()
		self.draw()
		self._screen.blit(self._surface, (0, 0))
		pygame.display.flip()

class TestGame(Game):
	def preload(self):
		pass

	def update(self,dt):
		pass

	def handle_event(self,event):
		if event.type == QUIT:
			sys.exit()
		elif event.type == KEYDOWN:
			print("Key Pressed!",flush=True)
		elif event.type == KEYUP:
			print("Key Released!",flush=True)

game = TestGame()
game.run()