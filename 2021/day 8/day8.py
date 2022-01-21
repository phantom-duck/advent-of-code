from argparse import ArgumentParser

def filter_onlyone(pats_sets, pred):
	results = [i for i, pat_set in enumerate(pats_sets) if pred(pat_set)]
	if len(results) != 1:
		print("Something went wrong. Length of results is not 1.")
	else:
		return results[0]

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	text = text.splitlines()
	
	##### Part 1: count how many times digits 1, 4, 7, 8 appear
	##### in the output values
	output_values = [line.split(" | ")[1].split() for line in text]
	output_values_lengths = [len(outv) for display in output_values for outv in display]
	answer = sum(1 for l in output_values_lengths if l == 2 or l == 4 or l == 3 or l == 7)
	print("Digits 1, 4, 7, 8 appear {} times".format(answer))
	
	##### Part 2: fully decode the permutations of the segments, and find the
	##### sum of all output values
	unique_patterns = [line.split(" | ")[0].split() for line in text]
	unique_patterns = [["".join(sorted(pat)) for pat in display] for display in unique_patterns]
	output_values = [line.split(" | ")[1].split() for line in text]
	output_values = [["".join(sorted(digit)) for digit in display] for display in output_values]
	
	output_values_sum = 0
	for pats, outvs in zip(unique_patterns, output_values):
		pattern2digit = dict()
		pats = sorted(pats, key=len) # now, the lengths are 2, 3, 4, 5, 5, 5, 6, 6, 6, 7
		pats_sets = [set(pat) for pat in pats]
		
		pattern2digit[pats[0]] = 1
		pattern2digit[pats[1]] = 7
		pattern2digit[pats[2]] = 4
		pattern2digit[pats[-1]] = 8
		
		digit0_idx = filter_onlyone(pats_sets, lambda pat_set: len(pat_set) == 6 and len(pat_set & pats_sets[0]) == 2 and len(pat_set & pats_sets[2]) == 3)
		digit0 = pats[digit0_idx]
		pattern2digit[digit0] = 0
		
		digit2_idx = filter_onlyone(pats_sets, lambda pat_set: len(pat_set) == 5 and len(pat_set & pats_sets[2]) == 2)
		digit2 = pats[digit2_idx]
		pattern2digit[digit2] = 2
		
		digit3_idx = filter_onlyone(pats_sets, lambda pat_set: len(pat_set - pats_sets[0]) == 3)
		digit3 = pats[digit3_idx]
		pattern2digit[digit3] = 3
		
		digit5_idx = filter_onlyone(pats_sets, lambda pat_set: len(pat_set) == 5 and len(pat_set & pats_sets[0]) == 1 and len(pat_set & pats_sets[2]) == 3)
		digit5 = pats[digit5_idx]
		pattern2digit[digit5] = 5
		
		digit6_idx = filter_onlyone(pats_sets, lambda pat_set: len(pat_set) == 6 and len(pat_set & pats_sets[0]) == 1)
		digit6 = pats[digit6_idx]
		pattern2digit[digit6] = 6
		
		digit9_idx = filter_onlyone(pats_sets, lambda pat_set: len(pat_set) == 6 and len(pat_set & pats_sets[2]) == 4)
		digit9 = pats[digit9_idx]
		pattern2digit[digit9] = 9
		
		output_value_digits = [str(pattern2digit[pat]) for pat in outvs]
		output_value = int("".join(output_value_digits))
		output_values_sum += output_value
		
		# print("{} {} {} {}: {}".format(*outvs, output_value))
	
	print("Sum of output values = {}".format(output_values_sum))

if __name__ == "__main__":
	main()