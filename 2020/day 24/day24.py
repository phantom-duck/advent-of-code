import sys
from pprint import pprint

class Hexagon:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	
	def move(self, direction):
		if direction == 'e':
			self.x += 1
		elif direction == 'w':
			self.x -= 1
		elif direction == 'ne':
			self.y += 1
		elif direction == 'sw':
			self.y -= 1
		elif direction == 'nw':
			self.x -= 1
			self.y += 1
		elif direction == 'se':
			self.x += 1
			self.y -= 1
	
	def set(self, x, y):
		self.x = x
		self.y = y

def split_directions(direc):
	i = 0
	while i < len(direc):
		if direc[i] == 'e':
			yield 'e'
			i += 1
		elif direc[i] == 'w':
			yield 'w'
			i += 1
		elif direc[i] == 'n':
			yield direc[i:i+2]
			i += 2
		elif direc[i] == 's':
			yield direc[i:i+2]
			i += 2

def generate_neighbours(x, y):
	ret = []
	ret.append((x + 1, y))
	ret.append((x - 1, y))
	ret.append((x, y + 1))
	ret.append((x, y - 1))
	ret.append((x + 1, y - 1))
	ret.append((x - 1, y + 1))
	
	return ret

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		directions = infile.read().split()
	
	##### Part 1: follow directions to find tiles to flip.
	##### Output the final number of black tiles
	
	blacks = set()
	tile = Hexagon()
	for dir in directions:
		for step in split_directions(dir):
			tile.move(step)
		
		new_tile = (tile.x, tile.y)
		if new_tile in blacks:
			blacks.discard(new_tile)
		else:
			blacks.add(new_tile)
		
		tile.set(0, 0)
	
	print(len(blacks))
	
	##### Part 2: starting with the configuration found above, flip
	##### the tiles as instructed at each step (game of life - like).
	##### Output the number of black tiles after 100 steps
	
	## This is basically the exact same code as day 17
	for _ in range(100):
		count_black_neighbours = {}
		for b_x, b_y in blacks:
			for neighbour in generate_neighbours(b_x, b_y):
				if neighbour not in count_black_neighbours:
					count_black_neighbours[neighbour] = 1
				else:
					count_black_neighbours[neighbour] += 1
		
		for b in blacks:
			if b not in count_black_neighbours:
				count_black_neighbours[b] = 0
		
		for candidate, n in count_black_neighbours.items():
			if candidate in blacks and n != 1 and n != 2:
				blacks.discard(candidate)
			elif candidate not in blacks and n == 2:
				blacks.add(candidate)
	
	print(len(blacks))