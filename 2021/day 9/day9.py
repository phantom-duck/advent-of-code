from argparse import ArgumentParser
from collections import deque
from pprint import pprint

# returns the map of explored - unexplored - under exploration points
def traverseBFS(map, i, j):
	n = len(map)
	m = len(map[0])
	mark_map = [["Unexplored" for elem in row] for row in map]
	queue = deque([(i, j)])
	while queue:
		u_i, u_j = queue.pop()
		mark_map[u_i][u_j] = "Explored"
		if u_i > 0 and map[u_i - 1][u_j] != 9 and mark_map[u_i - 1][u_j] == "Unexplored":
			v = (u_i - 1, u_j)
			queue.appendleft(v)
			mark_map[u_i - 1][u_j] = "Under exploration"
		if u_i < n - 1 and map[u_i + 1][u_j] != 9 and mark_map[u_i + 1][u_j] == "Unexplored":
			v = (u_i + 1, u_j)
			queue.appendleft(v)
			mark_map[u_i + 1][u_j] = "Under exploration"
		if u_j > 0 and map[u_i][u_j - 1] != 9 and mark_map[u_i][u_j - 1] == "Unexplored":
			v = (u_i, u_j - 1)
			queue.appendleft(v)
			mark_map[u_i][u_j - 1] = "Under exploration"
		if u_j < m - 1 and map[u_i][u_j + 1] != 9 and mark_map[u_i][u_j + 1] == "Unexplored":
			v = (u_i, u_j + 1)
			queue.appendleft(v)
			mark_map[u_i][u_j + 1] = "Under exploration"
	
	return mark_map

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	text = text.splitlines()
	
	##### Part 1: find all local minima of the height map and calculate
	##### the sum of their (height + 1)
	height_map = [list(map(int, line)) for line in text]
	n = len(height_map)
	m = len(height_map[0])
	answer = 0
	for i, row in enumerate(height_map):
		for j, height in enumerate(row):
			is_minimum = True
			if i > 0:
				is_minimum = is_minimum and height < height_map[i-1][j]
			if i < n - 1:
				is_minimum = is_minimum and height < height_map[i+1][j]
			if j > 0:
				is_minimum = is_minimum and height < height_map[i][j-1]
			if j < m - 1:
				is_minimum = is_minimum and height < height_map[i][j+1]
			
			if is_minimum:
				answer += height + 1
	
	print("Sum of risk levels = {}".format(answer))
	
	##### Part 2: find the three largest basins and multiply their sizes
	
	# first step is to find all low points, same way as Part 1
	height_map = [list(map(int, line)) for line in text]
	n = len(height_map)
	m = len(height_map[0])
	low_points = set()
	for i, row in enumerate(height_map):
		for j, height in enumerate(row):
			is_minimum = True
			if i > 0:
				is_minimum = is_minimum and height < height_map[i-1][j]
			if i < n - 1:
				is_minimum = is_minimum and height < height_map[i+1][j]
			if j > 0:
				is_minimum = is_minimum and height < height_map[i][j-1]
			if j < m - 1:
				is_minimum = is_minimum and height < height_map[i][j+1]
			
			if is_minimum:
				low_points.add((i, j))
	
	# now, start traversal from all low points until you hit a "wall" of 9s
	# then, you have calculated the basin
	basin_sizes = []
	for (start_i, start_j) in low_points:
		basin = traverseBFS(height_map, start_i, start_j)
		basin_size = sum(1 for row in basin for mark in row if mark == "Explored")
		basin_sizes.append(basin_size)
	basin_sizes.sort(reverse=True)
	answer = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]
	print("The product of the three biggest basin sizes is: {}".format(answer))

if __name__ == "__main__":
	main()