from argparse import ArgumentParser

def run_step(pair_counts: dict, rules: dict):
	for pair, count in pair_counts.copy().items():
		elem1 = pair[0]
		elem2 = pair[1]
		elem_to_add = rules[pair]
		
		pair_counts[pair] -= count
		pair_counts[elem1 + elem_to_add] += count
		pair_counts[elem_to_add + elem2] += count

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	
	template = text.split("\n\n")[0]
	rules_strs = text.split("\n\n")[1].splitlines()
	rules = {pair: elem for pair, elem in map(lambda rule: rule.split(" -> "), rules_strs)}
	
	pair_counts = {pair: 0 for pair in rules}
	for elem1, elem2 in zip(template, template[1:]):
		pair_counts[elem1 + elem2] += 1
	
	##### Part 1: perform 10 pair insertion steps on the original polymer
	##### template and calculate the quantity of the most common element
	##### minus the quantity of the least common element
	pc = pair_counts.copy()
	for _ in range(10):
		run_step(pc, rules)
	
	quantities = dict()
	first_elem = template[0]
	last_elem = template[-1]
	for pair, count in pc.items():
		elem1 = pair[0]
		q1 = quantities.get(elem1, 0)
		quantities[elem1] = q1 + count
		elem2 = pair[1]
		q2 = quantities.get(elem2, 0)
		quantities[elem2] = q2 + count
	quantities[first_elem] += 1
	quantities[last_elem] += 1
	quantities = {elem: q // 2 for elem, q in quantities.items()}
	
	answer = max(quantities.values()) - min(quantities.values())
	print("Part 1 answer is {}".format(answer))
	
	##### Part 2: the same, but now we must perform 40 insertion steps
	pc = pair_counts.copy()
	for _ in range(40):
		run_step(pc, rules)
	
	quantities = dict()
	first_elem = template[0]
	last_elem = template[-1]
	for pair, count in pc.items():
		elem1 = pair[0]
		q1 = quantities.get(elem1, 0)
		quantities[elem1] = q1 + count
		elem2 = pair[1]
		q2 = quantities.get(elem2, 0)
		quantities[elem2] = q2 + count
	quantities[first_elem] += 1
	quantities[last_elem] += 1
	quantities = {elem: q // 2 for elem, q in quantities.items()}
	
	answer = max(quantities.values()) - min(quantities.values())
	print("Part 2 answer is {}".format(answer))


if __name__ == "__main__":
	main()