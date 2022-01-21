import sys
from pprint import pprint

class Cube:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
	
	def generate_neighbours(self):
		for ix in [-1,0,1]:
			for iy in [-1,0,1]:
				for iz in [-1,0,1]:
					if ix == iy == iz == 0:
						continue
					yield Cube(self.x + ix, self.y + iy, self.z + iz)
	
	def __hash__(self):
		return hash((self.x, self.y, self.z))
	
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z
	
	def __repr__(self):
		return "Cube(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

def generate_neighbours(x, y, z):
	for ix in [-1,0,1]:
		for iy in [-1,0,1]:
			for iz in [-1,0,1]:
				if ix == iy == iz == 0:
					continue
				yield (x + ix, y + iy, z + iz)

def generate_neighbours4d(x, y, z, w):
	for ix in [-1,0,1]:
		for iy in [-1,0,1]:
			for iz in [-1,0,1]:
				for iw in [-1,0,1]:
					if ix == iy == iz == iw == 0:
						continue
					yield (x + ix, y + iy, z + iz, w + iw)

def points_to_map(points):
	x_min = min(x for (x, y, z) in points)
	x_max = max(x for (x, y, z) in points)
	y_min = min(y for (x, y, z) in points)
	y_max = max(y for (x, y, z) in points)
	z_min = min(z for (x, y, z) in points)
	z_max = max(z for (x, y, z) in points)
	
	dimension = [[(z_max + 1) * ['.'] for y in range(y_max + 1)] for x in range(x_max + 1)]
	for x, y, z in points:
		# print(x, x_max, y, y_max, z, z_max)
		dimension[x][y][z] = '#'
	
	return dimension

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read().split()
	
	##### Part 1: Run six updates, output how many active cubes are left
	
	actives = set()
	for i, row in enumerate(text):
		for j, point in enumerate(row):
			if point == '#':
				actives.add((i, j, 0))
	
	pprint(points_to_map(actives))
	print()
	
	T = 6
	for i in range(T):
		## phase one: for each adjacent cube, find the count of active neighbours
		active_neighbours = dict()
		for cube_x, cube_y, cube_z in actives:
			for neighbour in generate_neighbours(cube_x, cube_y, cube_z):
				if neighbour not in active_neighbours:
					active_neighbours[neighbour] = 1
				else:
					active_neighbours[neighbour] += 1
		## final touch, drove me mad
		for c in actives:
			if c not in active_neighbours:
				active_neighbours[c] = 0
		
		## phase two: activate inactives with 3 active neighbours
		## deactivate actives with <2 or >3 active neighbours
		for c, act in active_neighbours.items():
			if c in actives:
				if act != 2 and act != 3:
					actives.discard(c)
			else:
				if act == 3:
					actives.add(c)
		
		# print("-----------------------------")
		# pprint(points_to_map(actives))
		# print("-----------------------------")
		# print()
	
	print(len(actives))
	
	
	##### Part 2: same, but in 4 dimensions
	
	actives = set()
	for i, row in enumerate(text):
		for j, point in enumerate(row):
			if point == '#':
				actives.add((i, j, 0, 0))
	
	# pprint(actives)
	# print()
	
	T = 6
	for i in range(T):
		## phase one: for each adjacent cube, find the count of active neighbours
		active_neighbours = dict()
		for cube_x, cube_y, cube_z, cube_w in actives:
			for neighbour in generate_neighbours4d(cube_x, cube_y, cube_z, cube_w):
				if neighbour not in active_neighbours:
					active_neighbours[neighbour] = 1
				else:
					active_neighbours[neighbour] += 1
		## final touch, drove me mad
		for c in actives:
			if c not in active_neighbours:
				active_neighbours[c] = 0
		
		## phase two: activate inactives with 3 active neighbours
		## deactivate actives with <2 or >3 active neighbours
		for c, act in active_neighbours.items():
			if c in actives:
				if act != 2 and act != 3:
					actives.discard(c)
			else:
				if act == 3:
					actives.add(c)
		
		# print("-----------------------------")
		# pprint(actives)
		# print("-----------------------------")
		# print()
	
	print(len(actives))