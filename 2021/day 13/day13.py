from argparse import ArgumentParser
from pprint import pprint

def foldx(dots_set: set, line_pos):
	for dot_x, dot_y in dots_set.copy():
		if dot_x < line_pos:
			continue
		new_dot_x = 2 * line_pos - dot_x
		dots_set.remove((dot_x, dot_y))
		dots_set.add((new_dot_x, dot_y))

def foldy(dots_set: set, line_pos):
	for dot_x, dot_y in dots_set.copy():
		if dot_y < line_pos:
			continue
		new_dot_y = 2 * line_pos - dot_y
		dots_set.remove((dot_x, dot_y))
		dots_set.add((dot_x, new_dot_y))

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	
	dots_strs = text.split("\n\n")[0].splitlines()
	dots_positions = [(int(x), int(y)) for x, y in map(lambda line: line.split(","), dots_strs)]
	folds_strs = text.split("\n\n")[1].splitlines()
	folds = [(x_or_y, int(coord)) for x_or_y, coord in map(lambda line: line.split()[2].split("="), folds_strs)]
	
	##### Part 1: Find how many dots are visible after only the first fold instruction
	dots_positions_set = set(dots_positions)
	fold1 = folds[0]
	if fold1[0] == "x":
		foldx(dots_positions_set, fold1[1])
	elif fold1[0] == "y":
		foldy(dots_positions_set, fold1[1])
	else:
		raise ValueError("Invalid folding direction.")
	
	print("After the first fold, there are {} visible dots".format(len(dots_positions_set)))
	
	##### Part 2: finish all folds, see the final folded transparent paper
	##### and find out the code, which is always 8 capital letters
	dots_positions_set = set(dots_positions)
	for fold_dir, fold_pos in folds:
		if fold_dir == "x":
			foldx(dots_positions_set, fold_pos)
		elif fold_dir == "y":
			foldy(dots_positions_set, fold_pos)
		else:
			raise ValueError("Invalid folding direction.")
	
	# construct the final "transparent paper"
	max_x = max(x for x, y in dots_positions_set) + 1
	max_y = max(y for x, y in dots_positions_set) + 1
	paper = [["."] * max_x for _ in range(max_y)] # beware of multiple references!
	for dot_x, dot_y in dots_positions_set:
		paper[dot_y][dot_x] = "#"
	
	print("\nFinal message:")
	paper = "\n".join("".join(dot for dot in row) for row in paper)
	print(paper)


if __name__ == "__main__":
	main()