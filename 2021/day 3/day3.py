from argparse import ArgumentParser
from typing import List

class CustomError(Exception):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

def str2bits(line: str) -> List[int]:
	return [int(bit) for bit in list(line)]

def filter_bit_criteria(bit_arrays, bit_position, keep_most_common=True, tie_breaker=1):
	relevant_bits = [array[bit_position] for array in bit_arrays]
	total = len(relevant_bits)
	ones = sum(relevant_bits)
	zeros = total - ones
	
	if ones == zeros:
		return [array for array in bit_arrays if array[bit_position] == tie_breaker]
	
	most_common = 1 if ones > zeros else 0
	if keep_most_common:
		return [array for array in bit_arrays if array[bit_position] == most_common]
	else:
		return [array for array in bit_arrays if array[bit_position] != most_common]
	

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read()
	
	##### Part 1: calculate gamma rate and epsilon rate
	bit_arrays = [str2bits(line) for line in text.splitlines()]
	
	total_count = len(bit_arrays)
	ones_counts = [sum(tup) for tup in zip(*bit_arrays)]
	zeros_counts = [total_count - ones_count for ones_count in ones_counts]
	
	gamma_rate_bit_array = [1 if ones_count > zeros_count else 0 for ones_count, zeros_count in zip(ones_counts, zeros_counts)]
	epsilon_rate_bit_array = [1 if gamma == 0 else 0 for gamma in gamma_rate_bit_array]
	
	gamma_rate = int("".join(map(str, gamma_rate_bit_array)), base=2)
	epsilon_rate = int("".join(map(str, epsilon_rate_bit_array)), base=2)
	
	print("Gamma rate = {}".format(gamma_rate))
	print("Epsilon rate = {}".format(epsilon_rate))
	print("Product = {}".format(gamma_rate * epsilon_rate))
	
	
	
	##### Part 2: calculate oxygen generator rating and CO2 scrubber rating
	print()
	print("Part 2")
	bit_arrays = [str2bits(line) for line in text.splitlines()]
	bit_length = len(bit_arrays[0])
	
	# calculate oxygen generator rating
	bit_arrays_copy = [array.copy() for array in bit_arrays]
	for pos in range(bit_length):
		bit_arrays_copy = filter_bit_criteria(bit_arrays_copy, pos)
		if len(bit_arrays_copy) == 1:
			break
	
	if len(bit_arrays_copy) > 1:
		raise CustomError("Something went wrong with filtering. Final bit array has more than 1 element.")
	
	oxygen = int("".join(map(str, bit_arrays_copy[0])), base=2)
	print("Oxygen generator rating = {}".format(oxygen))
	
	# calculate CO2 scrubber rating
	bit_arrays_copy = [array.copy() for array in bit_arrays]
	for pos in range(bit_length):
		bit_arrays_copy = filter_bit_criteria(bit_arrays_copy, pos, keep_most_common=False, tie_breaker=0)
		if len(bit_arrays_copy) == 1:
			break
	
	if len(bit_arrays_copy) > 1:
		raise CustomError("Something went wrong with filtering. Final bit array has more than 1 element.")
	
	co2 = int("".join(map(str, bit_arrays_copy[0])), base=2)
	print("CO2 scrubber rating = {}".format(co2))
	
	print("Product = {}".format(oxygen * co2))

if __name__ == "__main__":
	main()