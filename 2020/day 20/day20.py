import sys
from pprint import pprint
import re

class Tile:
	def __init__(self, tilemap, id):
		self.id = id
		if tilemap is None:
			return
		
		self.image_tile = [list(row) for row in tilemap]
		self.top = list(tilemap[0])
		self.bottom = list(tilemap[-1])
		self.left = [s[0] for s in tilemap]
		self.right = [s[-1] for s in tilemap]
		
		self.top_match = 0
		self.bottom_match = 0
		self.left_match = 0
		self.right_match = 0
		
		self.top_match_id = None
		self.bottom_match_id = None
		self.left_match_id = None
		self.right_match_id = None
	
	def length(self):
		return len(self.image_tile[0])
	
	def height(self):
		return len(self.image_tile)
	
	# no bounds check
	def contains(self, other, pivot_i, pivot_j):
		flag = True
		other_image = other.image_tile
		for (i, row) in enumerate(other_image):
			for (j, elem) in enumerate(row):
				if elem == '#' and self.image_tile[pivot_i + i][pivot_j + j] == '.':
					flag = False
		return flag
	
	def remove_borders(self):
		self.image_tile = [row[1:-1] for row in self.image_tile[1:-1]]
		
		# Just zero out everything else, why not
		self.top_match = 0
		self.bottom_match = 0
		self.left_match = 0
		self.right_match = 0
		
		self.top_match_id = None
		self.bottom_match_id = None
		self.left_match_id = None
		self.right_match_id = None
	
	def rotate_clockwise(self):
		self.image_tile = [[row[i] for row in self.image_tile][::-1] for i in range(len(self.image_tile[0]))]
		
		self.top, self.bottom, self.left, self.right = self.left[::-1], self.right[::-1], self.bottom, self.top
		self.top_match, self.bottom_match, self.left_match, self.right_match = self.left_match, self.right_match, self.bottom_match, self.top_match
		self.top_match_id, self.bottom_match_id, self.left_match_id, self.right_match_id = self.left_match_id, self.right_match_id, self.bottom_match_id, self.top_match_id
	
	def reflect_horizontal(self):
		self.image_tile.reverse()
		
		self.top, self.bottom = self.bottom, self.top
		self.top_match, self.bottom_match = self.bottom_match, self.top_match
		self.top_match_id, self.bottom_match_id = self.bottom_match_id, self.top_match_id
		
		self.right.reverse()
		self.left.reverse()
	
	def reflect_vertical(self):
		self.reflect_horizontal()
		self.rotate_clockwise()
		self.rotate_clockwise()
	
	def move_to_match(self, side, match):
		if match == self.top:
			pass
		elif match == self.top[::-1]:
			self.reflect_vertical()
		elif match == self.bottom:
			self.reflect_horizontal()
		elif match == self.bottom[::-1]:
			self.rotate_clockwise()
			self.rotate_clockwise()
		elif match == self.left:
			self.reflect_horizontal()
			self.rotate_clockwise()
		elif match == self.left[::-1]:
			self.rotate_clockwise()
		elif match == self.right:
			self.rotate_clockwise()
			self.rotate_clockwise()
			self.rotate_clockwise()
		elif match == self.right[::-1]:
			self.reflect_horizontal()
			self.rotate_clockwise()
			self.rotate_clockwise()
			self.rotate_clockwise()
		else:
			print("Error: cannot match " + repr(self) + " and side " + str(side))
	
		if side == 't':
			pass
		elif side == 'b':
			self.reflect_horizontal()
		elif side == 'l':
			self.reflect_horizontal()
			self.rotate_clockwise()
		elif side == 'r':
			self.rotate_clockwise()
	
	def linesupwith(self, other):
		ret = 0
		
		# self.top
		if self.top == other.top:
			self.top_match += 1
			self.top_match_id = other.id
		if self.top == other.top[::-1]:
			self.top_match += 1
			self.top_match_id = other.id
		if self.top == other.bottom:
			self.top_match += 1
			self.top_match_id = other.id
		if self.top == other.bottom[::-1]:
			self.top_match += 1
			self.top_match_id = other.id
		if self.top == other.left:
			self.top_match += 1
			self.top_match_id = other.id
		if self.top == other.left[::-1]:
			self.top_match += 1
			self.top_match_id = other.id
		if self.top == other.right:
			self.top_match += 1
			self.top_match_id = other.id
		if self.top == other.right[::-1]:
			self.top_match += 1
			self.top_match_id = other.id
		
		# self.bottom
		if self.bottom == other.top:
			self.bottom_match += 1
			self.bottom_match_id = other.id
		if self.bottom == other.top[::-1]:
			self.bottom_match += 1
			self.bottom_match_id = other.id
		if self.bottom == other.bottom:
			self.bottom_match += 1
			self.bottom_match_id = other.id
		if self.bottom == other.bottom[::-1]:
			self.bottom_match += 1
			self.bottom_match_id = other.id
		if self.bottom == other.left:
			self.bottom_match += 1
			self.bottom_match_id = other.id
		if self.bottom == other.left[::-1]:
			self.bottom_match += 1
			self.bottom_match_id = other.id
		if self.bottom == other.right:
			self.bottom_match += 1
			self.bottom_match_id = other.id
		if self.bottom == other.right[::-1]:
			self.bottom_match += 1
			self.bottom_match_id = other.id
		
		# self.left
		if self.left == other.top:
			self.left_match += 1
			self.left_match_id = other.id
		if self.left == other.top[::-1]:
			self.left_match += 1
			self.left_match_id = other.id
		if self.left == other.bottom:
			self.left_match += 1
			self.left_match_id = other.id
		if self.left == other.bottom[::-1]:
			self.left_match += 1
			self.left_match_id = other.id
		if self.left == other.left:
			self.left_match += 1
			self.left_match_id = other.id
		if self.left == other.left[::-1]:
			self.left_match += 1
			self.left_match_id = other.id
		if self.left == other.right:
			self.left_match += 1
			self.left_match_id = other.id
		if self.left == other.right[::-1]:
			self.left_match += 1
			self.left_match_id = other.id
		
		# self.right
		if self.right == other.top:
			self.right_match += 1
			self.right_match_id = other.id
		if self.right == other.top[::-1]:
			self.right_match += 1
			self.right_match_id = other.id
		if self.right == other.bottom:
			self.right_match += 1
			self.right_match_id = other.id
		if self.right == other.bottom[::-1]:
			self.right_match += 1
			self.right_match_id = other.id
		if self.right == other.left:
			self.right_match += 1
			self.right_match_id = other.id
		if self.right == other.left[::-1]:
			self.right_match += 1
			self.right_match_id = other.id
		if self.right == other.right:
			self.right_match += 1
			self.right_match_id = other.id
		if self.right == other.right[::-1]:
			self.right_match += 1
			self.right_match_id = other.id
		
		return ret
	
	def __hash__(self):
		return hash(self.id)
	
	def __eq__(self, other):
		return self.id == other.id
	
	def __repr__(self):
		return "Tile(" + str(self.id) + ")"

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read().split("\n\n")[:-1]
	
	tiles = [Tile(tile.split(":")[1].split(), int(tile.split(":")[0].split()[1])) for tile in text]
	tile_length = len(text[0].split(":")[1].split()[0])
	tile_height = len(text[0].split(":")[1].split())
	
	print("Number of tiles: ", len(tiles))
	print("Tile length = ", tile_length)
	print("Tile height = ", tile_height)
	
	##### Part 1: rotate, flip and rearrange the tiles in a square pattern
	##### so that their edges line up. Output the product of the corner IDs
	
	## find corners
	matches = {}
	for t1 in tiles:
		for t2 in tiles:
			if t2 != t1:
				t1.linesupwith(t2)
		
		matches[t1] = (t1.top_match, t1.bottom_match, t1.left_match, t1.right_match)
	
	pprint(matches)
	
	corners = set()
	corners_id_prod = 1
	for t, mat in matches.items():
		zeros = [1 for x in mat if x == 0]
		if sum(zeros) == 2:
			corners.add(t)
			corners_id_prod *= t.id
	
	print(corners)
	print(corners_id_prod)
	
	##### Part 2: assemble the image, and search for sea monsters
	
	## start from one corner
	up_left = corners.pop()
	# pprint(up_left.image_tile)
	if up_left.top_match == 0:
		if up_left.left_match == 0:
			pass
		elif up_left.right_match == 0:
			up_left.reflect_vertical()
	elif up_left.bottom_match == 0:
		if up_left.left_match == 0:
			up_left.reflect_horizontal()
		elif up_left.right_match == 0:
			up_left.rotate_clockwise()
			up_left.rotate_clockwise()
	
	print("Up left corner is: ", up_left)
	pprint(up_left.image_tile)
	
	## construct the puzzle
	puzzle_solved = []
	first_in_row = up_left
	while True:
		row_tofind = [first_in_row]
		while True:
			curr_piece = row_tofind[-1]
			if curr_piece.right_match == 0:
				break
			
			for t in tiles:
				if t.id == curr_piece.right_match_id:
					next_piece = t
					break
			
			next_piece.move_to_match('l', curr_piece.right)
			row_tofind.append(next_piece)
		
		puzzle_solved.append(row_tofind)
		if first_in_row.bottom_match == 0:
			break
		
		for t in tiles:
			if t.id == first_in_row.bottom_match_id:
				next_first = t
				break
		
		next_first.move_to_match('t', first_in_row.bottom)
		first_in_row = next_first
	
	# pprint(puzzle_solved)
	# print(len(puzzle_solved))
	# print(len(puzzle_solved[0]))
	# if all(len(row) == 12 for row in puzzle_solved):
		# print("Yiiiissss!")
	
	# with open("image.txt", "w") as outfile:
		# for row in puzzle_solved:
			
			# for i in range(len(row[0].image_tile)):
				# for t in row:
					# outfile.write(''.join(t.image_tile[i]))
					# outfile.write("   ")
				# outfile.write("\n")
			
			# outfile.write("\n")
	
	### Success!!! Now, to find the sea monsters
	
	## First, remove the borders of the tiles
	for row in puzzle_solved:
		for t in row:
			t.remove_borders()
	
	# with open("image_no_borders.txt", "w") as outfile:
		# for row in puzzle_solved:
			
			# for i in range(len(row[0].image_tile)):
				# for t in row:
					# outfile.write(''.join(t.image_tile[i]))
					# outfile.write("   ")
				# outfile.write("\n")
			
			# outfile.write("\n")
	
	## Now, combine them all into a big tile
	big_image_tile = []
	for row in puzzle_solved:
		for i in range(len(row[0].image_tile)):
			big_row = []
			for t in row:
				big_row.extend(t.image_tile[i])
			big_image_tile.append(big_row)
	
	# with open("image_combined.txt", "w") as outfile:
		# for row in big_image_tile:
			# outfile.write(str(row))
			# outfile.write("\n")
	
	image = Tile(big_image_tile, 424242)
	
	## here we define the "cell" which represents the shape of a sea monster
	shape = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.'],
	         ['#', '.', '.', '.', '.', '#', '#', '.', '.', '.', '.', '#', '#', '.', '.', '.', '.', '#', '#', '#'],
	         ['.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '.']]
	sea_monster = Tile(shape, 171717)
	
	## final step. Search for the sea monster in the image, for all 8 symmetries of the image,
	## and keep track of the '#' that are not part of any possible sea monster
	
	def point2bool(ch):
		if ch == '.':
			return False
		elif ch == '#':
			return True
	rough_waters = [list(map(point2bool, row)) for row in big_image_tile]
	rough_waters = Tile(rough_waters, 232323)
	
	
	for ul_i in range(image.height() - sea_monster.height() + 1):
		for ul_j in range(image.length() - sea_monster.length() + 1):
			if image.contains(sea_monster, ul_i, ul_j):
				for (i, row) in enumerate(sea_monster.image_tile):
					for (j, elem) in enumerate(row):
						if elem == '#':
							rough_waters.image_tile[ul_i + i][ul_j + j] = False
	
	image.rotate_clockwise()
	rough_waters.rotate_clockwise()
	for ul_i in range(image.height() - sea_monster.height() + 1):
		for ul_j in range(image.length() - sea_monster.length() + 1):
			if image.contains(sea_monster, ul_i, ul_j):
				for (i, row) in enumerate(sea_monster.image_tile):
					for (j, elem) in enumerate(row):
						if elem == '#':
							rough_waters.image_tile[ul_i + i][ul_j + j] = False
	
	image.rotate_clockwise()
	rough_waters.rotate_clockwise()
	for ul_i in range(image.height() - sea_monster.height() + 1):
		for ul_j in range(image.length() - sea_monster.length() + 1):
			if image.contains(sea_monster, ul_i, ul_j):
				for (i, row) in enumerate(sea_monster.image_tile):
					for (j, elem) in enumerate(row):
						if elem == '#':
							rough_waters.image_tile[ul_i + i][ul_j + j] = False
	
	image.rotate_clockwise()
	rough_waters.rotate_clockwise()
	for ul_i in range(image.height() - sea_monster.height() + 1):
		for ul_j in range(image.length() - sea_monster.length() + 1):
			if image.contains(sea_monster, ul_i, ul_j):
				for (i, row) in enumerate(sea_monster.image_tile):
					for (j, elem) in enumerate(row):
						if elem == '#':
							rough_waters.image_tile[ul_i + i][ul_j + j] = False
	
	image.rotate_clockwise()
	image.reflect_horizontal()
	rough_waters.rotate_clockwise()
	rough_waters.reflect_horizontal()
	for ul_i in range(image.height() - sea_monster.height() + 1):
		for ul_j in range(image.length() - sea_monster.length() + 1):
			if image.contains(sea_monster, ul_i, ul_j):
				for (i, row) in enumerate(sea_monster.image_tile):
					for (j, elem) in enumerate(row):
						if elem == '#':
							rough_waters.image_tile[ul_i + i][ul_j + j] = False
	
	image.rotate_clockwise()
	rough_waters.rotate_clockwise()
	for ul_i in range(image.height() - sea_monster.height() + 1):
		for ul_j in range(image.length() - sea_monster.length() + 1):
			if image.contains(sea_monster, ul_i, ul_j):
				for (i, row) in enumerate(sea_monster.image_tile):
					for (j, elem) in enumerate(row):
						if elem == '#':
							rough_waters.image_tile[ul_i + i][ul_j + j] = False
	
	image.rotate_clockwise()
	rough_waters.rotate_clockwise()
	for ul_i in range(image.height() - sea_monster.height() + 1):
		for ul_j in range(image.length() - sea_monster.length() + 1):
			if image.contains(sea_monster, ul_i, ul_j):
				for (i, row) in enumerate(sea_monster.image_tile):
					for (j, elem) in enumerate(row):
						if elem == '#':
							rough_waters.image_tile[ul_i + i][ul_j + j] = False
	
	image.rotate_clockwise()
	rough_waters.rotate_clockwise()
	for ul_i in range(image.height() - sea_monster.height() + 1):
		for ul_j in range(image.length() - sea_monster.length() + 1):
			if image.contains(sea_monster, ul_i, ul_j):
				for (i, row) in enumerate(sea_monster.image_tile):
					for (j, elem) in enumerate(row):
						if elem == '#':
							rough_waters.image_tile[ul_i + i][ul_j + j] = False
	
	total = 0
	for row in rough_waters.image_tile:
		for flag in row:
			if flag:
				total += 1
	
	print(total)