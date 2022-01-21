import sys
from collections import OrderedDict

def gcd(a, b):
	a = abs(a)
	b = abs(b)
	while (a > 0 and b > 0):
		if a > b:
			a = a % b
		else:
			b = b % a
	return a + b

def best_asteroid(map):
	Nrows = len(map)
	Ncols = len(map[0])
	asteroids = []
	for i in range(Nrows):
		for j in range(Ncols):
			if map[i][j] == '#':
				asteroids.append((i, j))
	# visibles = [len(asteroids) - 1] * len(asteroids)
	
	visibles = dict()
	for (asteroid_i, asteroid_j) in asteroids:
		visibles[(asteroid_i, asteroid_j)] = len(asteroids) - 1
		for (other_i, other_j) in (x for x in asteroids if x != (asteroid_i, asteroid_j)):
			diff_i = other_i - asteroid_i
			diff_j = other_j - asteroid_j
			g = gcd(diff_i, diff_j)
			diff_i //= g
			diff_j //= g
			# if asteroid_i == other_i:
				# diff_j = 1 * (diff_j // abs(diff_j))
			# if asteroid_j == other_j:
				# diff_i = 1 * (diff_i // abs(diff_i))
			move_i = diff_i
			move_j = diff_j
			while asteroid_i + move_i != other_i or asteroid_j + move_j != other_j:
				if map[asteroid_i + move_i][asteroid_j + move_j] == '#':
					visibles[(asteroid_i, asteroid_j)] -= 1
					break
				move_i += diff_i
				move_j += diff_j
	
	max_key = max(visibles, key=visibles.get)
	return max_key, visibles[max_key]

# def helper(item):
	# unary_i = item[0][0]
	# unary_j = item[0][1]

class T:
	def __init__(self, item):
		self.i = item[0][0]
		self.j = item[0][1]
	def __eq__(self, other):
		return self.i == other.i and self.j == other.j
	def __ne__(self, other):
		return self.i != other.i or self.j != other.j
	def __lt__(self, other):
		if self.i < 0 and other.i >= 0:
			return True
		elif self.i >= 0 and other.i >= 0:
			if self.j >= 0 and other.j < 0:
				return True
			elif self.j >= 0 and other.j >= 0 and abs(self.i * other.j) < abs(other.i * self.j):
				return True
			elif self.j < 0 and other.j < 0 and abs(self.i * other.j) > abs(other.i * self.j):
				return True
		elif self.i < 0 and other.i < 0:
			if self.j < 0 and other.j >= 0:
				return True
			elif self.j >= 0 and other.j >= 0 and abs(self.i * other.j) > abs(other.i * self.j):
				return True
			elif self.j < 0 and other.j < 0 and abs(self.i * other.j) < abs(other.i * self.j):
				return True
		
		return False
	# def __gt__(self, other):
		# pass
	# def __le__(self, other):
		# pass
	# def __ge__(self, other):
		# pass

def next_vaped(map):
	Nrows = len(map)
	Ncols = len(map[0])
	lines = dict()
	for i in range(Nrows):
		for j in range(Ncols):
			if map[i][j] == '#' and (station_i != i or station_j != j):
				diff_i = i - station_i
				diff_j = j - station_j
				g = gcd(diff_i, diff_j)
				diff_i //= g
				diff_j //= g
				if (diff_i, diff_j) not in lines:
					lines[(diff_i, diff_j)] = [(i, j)]
				else:
					lines[(diff_i, diff_j)].append((i, j))
	
	for key in lines:
		lines[key] = sorted(lines[key], key = lambda ij: abs(ij[0] - station_i) + abs(ij[1] - station_j))
	
	# print(lines)
	lines = OrderedDict(sorted(lines.items(), key = T))
	# print(lines)
	
	it = iter(lines)
	line = next(it)
	while line != (-1, 0):
		line = next(it)
	
	while True:
		if len(lines[line]) > 0:
			asteroid_destroyed = lines[line].pop(0)
			yield asteroid_destroyed
		try:
			line = next(it)
		except StopIteration:
			it = iter(lines)
			line = next(it)

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename) as infile:
		text = infile.read()
	map = [st for st in text.split("\n") if len(st) > 0]

	##### Test inputs
	# print(best_asteroid(map))

	##### Part One
	# print(best_asteroid(map))

	##### Part two
	# (station_i, station_j) = best_asteroid(map)[0]
	# print(station_i, station_j)
	# gen = next_vaped(map)
	
	# for i in range(200):
		# asteroid_destroyed = next(gen)
	# print(asteroid_destroyed)