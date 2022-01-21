from argparse import ArgumentParser

LANTERNFISH_CYCLE = 7
NEW_LANTERNFISH_CYCLE = 9

def run_day(groups):
	fish_zero = groups.pop(0)
	groups.append(fish_zero)
	groups[LANTERNFISH_CYCLE - 1] += fish_zero

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read()
	
	starting_fish_counters = [int(days) for days in text.strip().split(",")]
	
	##### Part 1: find how many lanternfish would there be after 80 days
	fish_groups = [sum(1 for fc in starting_fish_counters if fc == days) for days in range(NEW_LANTERNFISH_CYCLE)]
	for t in range(80):
		run_day(fish_groups)
	print("Number of lanternfish after 80 days = {}".format(sum(fish_groups)))
	
	##### Part 2: the same, but after 256 days
	fish_groups = [sum(1 for fc in starting_fish_counters if fc == days) for days in range(NEW_LANTERNFISH_CYCLE)]
	for t in range(256):
		run_day(fish_groups)
	print("Number of lanternfish after 256 days = {}".format(sum(fish_groups)))

if __name__ == "__main__":
	main()