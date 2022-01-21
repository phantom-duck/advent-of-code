import sys
from pprint import pprint

def tree_encounters(treemap, slope_x, slope_y):
	N = len(treemap)
	M = len(treemap[0])
	
	n_col = 0
	i = j = 0
	while i < N:
		if treemap[i][j] == '#':
			n_col += 1
		i = i + slope_y
		j = (j + slope_x) % M
	
	return n_col

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read()
	
	treemap = text.split("\n")[:-1]
	N = len(treemap)
	M = len(treemap[0])
	
	## pprint(treemap)
	
	##### Part 1: find number of collisions for slope (3, 1)
	
	print(tree_encounters(treemap, 3, 1))
	
	##### Part 2: find number of collisions for slopes: (1, 1), (3, 1),
	##### (5, 1), (7, 1), (1, 2) and multiply
	
	print(tree_encounters(treemap, 1, 1)
		* tree_encounters(treemap, 3, 1)
		* tree_encounters(treemap, 5, 1)
		* tree_encounters(treemap, 7, 1)
		* tree_encounters(treemap, 1, 2))
	
	