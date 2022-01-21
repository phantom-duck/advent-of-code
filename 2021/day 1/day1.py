from argparse import ArgumentParser


def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read()
	depth_measurements = [int(x) for x in text.splitlines()]
	
	##### Part 1: count the number of elements that are higher than the previous one
	answer = sum(1 for x_next, x in zip(depth_measurements[1:], depth_measurements) if x_next - x > 0)
	print("# of increases = {}".format(answer))
	
	##### Part 2: count the number of three-consecutive-measurements windows
	##### that have a larger sum than the previous window
	sums_of_three = [x + xn1 + xn2 for x, xn1, xn2 in zip(depth_measurements, depth_measurements[1:], depth_measurements[2:])]
	answer = sum(1 for x_next, x in zip(sums_of_three[1:], sums_of_three) if x_next - x > 0)
	print("# of increases with window of length 3 = {}".format(answer))

if __name__ == "__main__":
	main()