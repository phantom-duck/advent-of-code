import sys
from pprint import pprint

def bag_dfs_search_and_count(contains, bag, target_bag, marks):
	if marks[bag] is not None:
		return marks[bag]
	
	bags_in_bag = [b for (b, c) in contains[bag]]
	
	if target_bag in bags_in_bag:
		marks[bag] = True
		return True
	
	marks[bag] = False
	for b in bags_in_bag:
		if bag_dfs_search_and_count(contains, b, target_bag, marks):
			marks[bag] = True
	
	return marks[bag]

def dfs_sum(contains, bag, calculated_sums):
	if bag in calculated_sums:
		return calculated_sums[bag]
	
	bags_in_bag = [b for (b, c) in contains[bag]]
	
	ret = 1
	for b, c in contains[bag]:
		ret += c * dfs_sum(contains, b, calculated_sums)
	
	calculated_sums[bag] = ret
	return ret

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read()
	text = text.split("\n")[:-1]
	
	contains_map = {}
	for entry in text:
		bag = entry.split("contain")[0]
		rest = entry.split("contain")[1].lstrip()
		
		bag = bag.replace(" bags ", "")
		if rest.startswith("no"):
			contains_map[bag] = []
		else:
			bags_list = []
			for b in rest.split(","):
				count = b.split()[0]
				bag_name = b.split()[1] + " " + b.split()[2]
				bags_list.append((bag_name, int(count)))
			contains_map[bag] = bags_list
	
	# pprint(contains_map)
	
	##### Part 1: find how many bag colours can recursively contain a shiny gold bag
	
	bag_mark = {}
	for k in contains_map:
		bag_mark[k] = None
	
	for k in contains_map:
		bag_dfs_search_and_count(contains_map, k, "shiny gold", bag_mark)
	
	count = 0
	for k in contains_map:
		if bag_mark[k]:
			count += 1
	
	# pprint(bag_mark)
	print(count)
	
	##### Part 2: count how many bags are in the shiny gold bag (recursively)
	
	# pprint(contains_map)
	# d = {}
	print(dfs_sum(contains_map, "shiny gold", {}) - 1)
	# pprint(d)