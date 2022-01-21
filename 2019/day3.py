import sys

class point_with_steps:
	def __init__(self, row, col, st):
		self.i = row
		self.j = col
		self.steps = st
	
	def __eq__(self, value):
		return self.i==value.i and self.j==value.j

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"
	
	with open(filename) as infile:
		text = infile.read()
	
	text = text.split("\n")
	wire1 = text[0].split(",")
	wire2 = text[1].split(",")
	
	# print(text)
	# print(wire1)
	# print(wire2)
	
	wire1_points = []
	wire1_steps = dict()
	point_i = 0
	point_j = 0
	steps = 0
	for line in wire1:
		dir = line[0]
		dist = int(line[1:])
		if dir=="L":
			for i in range(dist):
				point_j = point_j - 1
				steps = steps + 1
				wire1_points.append((point_i, point_j))
				wire1_steps[str((point_i, point_j))] = steps
		elif dir=="R":
			for i in range(dist):
				point_j = point_j + 1
				steps = steps + 1
				wire1_points.append((point_i, point_j))
				wire1_steps[str((point_i, point_j))] = steps
		elif dir=="U":
			for i in range(dist):
				point_i = point_i - 1
				steps = steps + 1
				wire1_points.append((point_i, point_j))
				wire1_steps[str((point_i, point_j))] = steps
		elif dir=="D":
			for i in range(dist):
				point_i = point_i + 1
				steps = steps + 1
				wire1_points.append((point_i, point_j))
				wire1_steps[str((point_i, point_j))] = steps
	
	wire2_points = []
	wire2_steps = dict()
	point_i = 0
	point_j = 0
	steps = 0
	for line in wire2:
		dir = line[0]
		dist = int(line[1:])
		if dir=="L":
			for i in range(dist):
				point_j = point_j - 1
				steps = steps + 1
				wire2_points.append((point_i, point_j))
				wire2_steps[str((point_i, point_j))] = steps
		elif dir=="R":
			for i in range(dist):
				point_j = point_j + 1
				steps = steps + 1
				wire2_points.append((point_i, point_j))
				wire2_steps[str((point_i, point_j))] = steps
		elif dir=="U":
			for i in range(dist):
				point_i = point_i - 1
				steps = steps + 1
				wire2_points.append((point_i, point_j))
				wire2_steps[str((point_i, point_j))] = steps
		elif dir=="D":
			for i in range(dist):
				point_i = point_i + 1
				steps = steps + 1
				wire2_points.append((point_i, point_j))
				wire2_steps[str((point_i, point_j))] = steps
	
	wire1_set = set(wire1_points)
	wire2_set = set(wire2_points)
	inter = wire1_set.intersection(wire2_set)
	
	# min_manhattan = 10**100
	# for (x, y) in inter:
		# manh = abs(x) + abs(y)
		# if manh < min_manhattan:
			# min_manhattan = manh
	
	# print(min_manhattan)
	
	min_steps = 10**100
	for (x, y) in inter:
		steps1 = wire1_steps[str((x, y))]
		steps2 = wire2_steps[str((x, y))]
		if steps1 + steps2 < min_steps:
			min_steps = steps1 + steps2
	
	print(min_steps)
	