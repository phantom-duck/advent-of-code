from argparse import ArgumentParser

def east_step(cmap) -> bool:
	n = len(cmap)
	m = len(cmap[0])
	
	to_be_moved = set()
	for i, row in enumerate(cmap):
		for j, tile in enumerate(row):
			if tile == ">" and cmap[i][(j + 1) % m] == ".":
				to_be_moved.add((i, j))
	
	if not to_be_moved:
		return False
	
	for i, j in to_be_moved:
		cmap[i][j] = "."
		cmap[i][(j + 1) % m] = ">"
	
	return True

def south_step(cmap) -> bool:
	n = len(cmap)
	m = len(cmap[0])
	
	to_be_moved = set()
	for i, row in enumerate(cmap):
		for j, tile in enumerate(row):
			if tile == "v" and cmap[(i + 1) % n][j] == ".":
				to_be_moved.add((i, j))
	
	if not to_be_moved:
		return False
	
	for i, j in to_be_moved:
		cmap[i][j] = "."
		cmap[(i + 1) % n][j] = "v"
	
	return True

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	text = text.splitlines()
	
	cucumber_map = [list(line) for line in text]
	
	##### Part 1: Find the first step on which no sea cucumbers move
	step = 1
	while True:
		changed1 = east_step(cucumber_map)
		changed2 = south_step(cucumber_map)
		if not changed1 and not changed2:
			break
		step += 1
	print("Part 1 answer: {}".format(step))


if __name__ == "__main__":
	main()