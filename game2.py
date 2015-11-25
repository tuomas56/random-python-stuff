# WORKING ON:
#	Tile object for render incl. colours. - PRELIM DONE
#	GUI object & GUI#render for various GUIs.
# TODO:
#	Game object & scene manager
#	Main render loop -> using cbreak.

import blessed
from collections import defaultdict
import random
import time
from operator import itemgetter
from sys import argv, exit

def group(s, n):
	result = []
	for i in range(0, len(s), n):
		result.append(s[i:i+n])
	return result

class Side:
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4

class Loc:
	def __init__(self, x, y):
		self.x, self.y = x, y

	def __str__(self):
		return "{s.x}, {s.y}".format(s=self)

class Player:
	def __init__(self,name='',inventory=[],max_weight=0,max_items=0,location=Loc(0,0),health=0):
		self.health=health
		self.name = name
		self.max_items = max_items
		self.max_weight = max_weight
		self.inventory = inventory
		self.location = location
		self.equipped = None

	def pickup(self, object):
		if not object.can_pickup():
			return False

		if object.weight() + sum(x.weight() for x in inventory) <= self.max_weight and len(self.inventory) < self.max_items:
			self.inventory.append(object)
			return True
		return False

	def drop(self, index):
		if len(self.inventory) > index:
			x = self.inventory[index]
			del self.inventory[index]
			return x
		return False

	def equip(self, index):
		if len(self.inventory) < index:
			self.equipped = index
			return True
		return False

	def get_equipped(self):
		if self.equipped is not None:
			return self.inventory[self.equipped]
		return False


	def move(self, loc):
		self.location = loc

	def get_side(self, side):
		x, y = self.location

		if side == Side.UP:
			return x, y - 1
		elif side == Side.DOWN:
			return x, y + 1
		elif side == Side.LEFT:
			return x - 1, y
		elif side == Side.RIGHT:
			return x + 1, y

	def render(self, term):
		return TileObject("😶").render(term)
		#😶

class World:
	DEFAULT_SETTINGS = sorted([
		('T', 0.05),
		(' ', 1.00)
	], key=itemgetter(1))

	def __init__(self, chunks=dict(), players=dict(), settings=None, seed=None):
		self.chunks = chunks
		self.players = players

		if settings is None:
			self.settings = World.DEFAULT_SETTINGS
		else:
			self.settings = settings

		self.random = random.Random()
		if seed is None:
			self.random.seed(time.time())
		else:
			self.random.seed(seed)

		self.set_location(Loc(0, 0), Wood())

		for name, player in players.items():
			self.set_location(player.location, player)

	def move(self, player, location):
		if self.can_move(player, location):
			self.players[player.name].move(location)
			return True
		return False

	def can_move(self, location):
		return self.get_location(location).is_passable()

	def get_chunk(self, chunk_loc):
		if chunk_loc not in self.chunks:
			self.chunks[chunk_loc] = Chunk.generate_chunk(self.settings, self.random)
		return self.chunks[chunk_loc]

	def get_location(self, location):
		chunk_loc = ((location.x // Chunk.WIDTH)*Chunk.WIDTH, (location.y // Chunk.HEIGHT)*Chunk.HEIGHT)
		rel_locs = Loc(location.x - chunk_loc[0], location.y - chunk_loc[1])

		if chunk_loc not in self.chunks:
			self.chunks[chunk_loc] = Chunk.generate_chunk(self.settings, self.random)

		return self.chunks[chunk_loc].get_location(rel_locs)

	def set_location(self, location, object):
		chunk_loc = ((location.x // Chunk.WIDTH)*Chunk.WIDTH, (location.y // Chunk.HEIGHT)*Chunk.HEIGHT)
		rel_locs = Loc(location.x - chunk_loc[0], location.y - chunk_loc[1])


		if chunk_loc not in self.chunks:
			self.chunks[chunk_loc] = Chunk.generate_chunk(self.settings, self.random)

		self.chunks[chunk_loc].set_location(rel_locs, object)

	def render(self, width, height, active_player, term):
		middle = Loc(width//2, height//2)
		player_loc = self.players[active_player].location

		above = abs(player_loc.y - middle.y) + 1 #overshoot, get rid of it later
		below = above

		left = abs(player_loc.x - middle.x) + 1
		right = left

		top_left = Loc(player_loc.x - left, player_loc.y - above)
		
		result = []
		for y in range(top_left.x, top_left.x + height):
			row = []
			for x in range(top_left.y, top_left.y + width):
				row.append(self.get_location(Loc(x, y)).render(term))

			result.append(''.join(row))

		return '\n'.join(result)



class Chunk:
	WIDTH = 16
	HEIGHT = 16

	def __init__(self, objects=[]):
		self.objects = objects

	def get_location(self, location):
		return self.objects[location.y*Chunk.WIDTH + location.x]

	def set_location(self, location, object):
		self.objects[location.y*Chunk.WIDTH + location.x] = object

	def render(self, term):
		rows = []
		row = ''
		for i in range(Chunk.WIDTH*Chunk.HEIGHT):
			if i % Chunk.WIDTH == 0:
				rows.append(row)
				row = ''
			row += self.objects[i].render(term)
		rows.append(row)

		return rows[1:]

	@staticmethod
	def generate_chunk(settings, random):
		objects = []

		for _ in range(Chunk.WIDTH*Chunk.HEIGHT):
			rand = random.random()
			for name, prob in settings:
				if rand <= prob:
					objects.append(WorldObject.ITEMS[WorldObject.ITEM_IDS[name]]())
					break

		return Chunk(objects)	

class WorldObject:
	ITEM_IDS = {}
	ITEMS = {}

	@staticmethod
	def register(self, name, id):
		WorldObject.ITEM_IDS[name] = id
		WorldObject.ITEMS[id] = self

	def weight(self):
		pass

	def is_passible(self):
		pass

	def can_pickup(self):
		pass

	def render(self, term):
		pass

	def action(self, location, player, world):
		return False

class Nothing(WorldObject):
	def __init__(self):
		self.id = 0
		

	def is_passible(self):
		return True

	def can_pickup(self):
		return False

	def render(self, term):
		return TileObject(" ",background=term.on_green).render(term)

class Tree(WorldObject):
	def __init__(self):
		self.id = 1
		self.health = 3

	def is_passible(self):
		return False

	def can_pickup(self):
		return False

	def render(self, term):
		return TileObject("🌲",foreground=term.bright_white).render(term)
		#🌲

	def action(self, location, player, world):
		if isinstance(player.get_equipped(), Axe):
			self.health = 0
		else:
			self.health -= 1
		if self.health <= 0:	
			world.set_location(location, Wood())
		return True

class Pickup(WorldObject):
	def can_pickup(self):
		return True

	def action(self, location, player, world):
		if player.pickup(self):
			world.set_location(location, Nothing())
			return True
		return False


class Wood(Pickup):
	def __init__(self):
		self.id = 2

	def weight(self):
		return 1

	def is_passible(self):
		return True

	def render(self, term):
		return TileObject("⩸").render(term)


class TileObject:
	def __init__(self, text, foreground='', background=''):
		self.text = text
		self.foreground = foreground
		self.background = background

	def render(self, term):
		return self.foreground + self.background + self.text + term.reset	

class GUI:
	def handle_event(self, evt, data=None):
		if evt == EventType.RENDER_EVENT:
			return self.render(data)
		elif evt == EventType.UPDATE_EVENT:
			return self.update(data)
		elif evt == EventType.KEY_EVENT:
			return self.handle_key(data)

class EventType:
	RENDER_EVENT = 1
	KEY_EVENT = 2
	UPDATE_EVENT = 3

class GameScreen(GUI):
	def __init__(self, world, player):
		self.world = world
		self.player = player

	def render(self, term):
		height, width = term.height, term.width
		result, header_height = self.render_header(term)
		result += self.world.render(width, height - header_height, self.player.name, term)
		return result

	def render_header(self, term):
		info = "|{p.name}|Health: {p.health}|Location: {p.location}|".format(p=self.player)
		width = term.width - len(info) - 2
		info += "="*(width//2) + ("=" if width % 2 == 1 else "") + "+"
		info = "+" + "="*(width//2) + info
		return info, 1

	def update(self, dt):
		pass

	def handle_key(self, key):
		player_loc = self.world.players[self.player.name].location
		if key == "w":
			 self.world.players[self.player.name].location = Loc(player_loc.x, player_loc.y - 1)
		elif key == "s":
			self.world.players[self.player.name].location = Loc(player_loc.x, player_loc.y + 1)
		elif key == "a":
			self.world.players[self.player.name].location = Loc(player_loc.x - 1, player_loc.y)
		elif key == "d":
			self.world.players[self.player.name].location = Loc(player_loc.x + 1, player_loc.y) 

		for name, player in self.world.players.items():
			self.world.set_location(player.location, player)


WorldObject.register(Nothing, ' ',0)
WorldObject.register(Tree, 'T',1)
WorldObject.register(Wood, 'W',2)

player = Player(name='Test')
world = World(players={'Test':player}, seed=int(argv[1]))
screen = GameScreen(world, player)
term = blessed.Terminal()
fps = 5
with term.fullscreen():
	with term.cbreak():
		while True:
			key = term.inkey(timeout=1/fps)
			if key != '':
				print(term.clear)
				print(screen.handle_event(EventType.RENDER_EVENT, data=term),end='')
				screen.handle_event(EventType.KEY_EVENT, data=key)