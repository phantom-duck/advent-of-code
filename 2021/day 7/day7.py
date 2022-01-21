from argparse import ArgumentParser
import math

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	
	##### Part 1: minimize total fuel needed to align all crabs
	crab_positions = [int(x) for x in text.split(",")]
	crab_positions.sort()
	n = len(crab_positions)
	best_position_idx = (n // 2) - 1 + (n % 2) # median of all crab positions
	best_position = crab_positions[best_position_idx]
	minimum_fuel = sum(abs(x - best_position) for x in crab_positions)
	print("Best possible position to align: {}".format(best_position))
	print("Minimum fuel needed to align = {}".format(minimum_fuel))
	
	##### Part 2: the same, but now the cost for a crab to move from position
	##### d_i to position x is:
	##### (d * (d + 1)) / 2, where d = abs(d_i - x)
	crab_positions = [int(x) for x in text.split(",")]
	n = len(crab_positions)
	crab_positions_mean = sum(crab_positions) / n
	crab_positions_median = best_position # calculated from Part 1
	
	## Solution explanation: being the sum of two convex functions, the minimum
	## must be somewhere between the two minimums. 
	## So we brute force those values.
	
	left = math.floor(min(crab_positions_mean, crab_positions_median))
	right = math.ceil(max(crab_positions_mean, crab_positions_median))
	minimum_fuel = sum(d**2 + abs(d) for d in crab_positions) // 2
	for pos in range(left, right + 1):
		candidate_minimum = sum((d - pos)**2 + abs(d - pos) for d in crab_positions) // 2
		if candidate_minimum < minimum_fuel:
			minimum_fuel = candidate_minimum
	print("\nPart 2")
	print("Minimum fuel needed to align = {}".format(minimum_fuel))

if __name__ == "__main__":
	main()