from argparse import ArgumentParser
import re

def possible_y(vy0: int, x_left, x_right, y_down, y_up) -> bool:
	n_xxcross = 2 * vy0 + 1
	
	for vx0 in range(1, x_right + 1):
		n = 1
		while True:
			x = n * vx0 - n * (n - 1) // 2 if n < vx0 else vx0 * (vx0 + 1) // 2
			y = n * vy0 - n * (n - 1) // 2
			if x_left <= x <= x_right and y_down <= y <= y_up:
				return True
			if x > x_right or y < y_down:
				break
			n += 1
	
	return False

def possible(vx0: int, vy0: int, x_left, x_right, y_down, y_up) -> bool:
	n = 1
	while True:
		x = n * vx0 - n * (n - 1) // 2 if n < vx0 else vx0 * (vx0 + 1) // 2
		y = n * vy0 - n * (n - 1) // 2
		if x_left <= x <= x_right and y_down <= y <= y_up:
			return True
		if x > x_right or y < y_down:
			break
		n += 1
	return False

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	
	input_re = r"target area: x=(?P<x_min>-?\d*)..(?P<x_max>-?\d*), y=(?P<y_min>-?\d*)..(?P<y_max>-?\d*)"
	match_object = re.match(input_re, text)
	
	target_x_min = int(match_object.group("x_min"))
	target_x_max = int(match_object.group("x_max"))
	target_y_min = int(match_object.group("y_min"))
	target_y_max = int(match_object.group("y_max"))
	print(target_x_min, target_x_max, target_y_min, target_y_max)
	
	##### Part 1: find the maximum initial y velocity for which the target
	##### area is reachable, and calculate the corresponding highest y position
	left_vy0 = 1
	right_vy0 = abs(target_y_min) - 1
	for vy0 in range(right_vy0, left_vy0, -1):
		if possible_y(vy0, target_x_min, target_x_max, target_y_min, target_y_max):
			max_vy0 = vy0
			break
	max_height = max_vy0 * (max_vy0 + 1) // 2
	print("Part 1 answer = {}".format(max_height))
	
	##### Part 2: find how many distinct initial velocity values cause the
	##### probe to reach the target area
	velocity_count = 0
	vx0_max = target_x_max
	vx0_min = 1
	vy0_max = abs(target_y_min) - 1
	vy0_min = target_y_min - 1
	for vx0 in range(vx0_min, vx0_max + 1):
		for vy0 in range(vy0_min, vy0_max + 1):
			if possible(vx0, vy0, target_x_min, target_x_max, target_y_min, target_y_max):
				velocity_count += 1
	print("Part 2 answer = {}".format(velocity_count))


if __name__ == "__main__":
	main()