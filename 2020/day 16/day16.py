import sys
from pprint import pprint

def range_str2tuple(x):
	return tuple(map(int, x.split("-")))

def check_value_ranges(value, valid_ranges):
	for low, high in valid_ranges:
		if value in range(low, high + 1):
			return True
	return False

def check_validity(value, rules):
	return any([check_value_ranges(value, rules[k]) for k in rules])

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read().split("\n\n")
	
	rules = [(rule.split(": ")[0], rule.split(": ")[1].split(" or ")) for rule in text[0].split("\n")]
	rules = {field_name : list(map(range_str2tuple, valid_ranges)) for (field_name, valid_ranges) in rules}
	
	myticket = list(map(int, text[1].split("\n")[1].split(",")))
	
	nearby_tickets = [list(map(int, t.split(","))) for t in text[2].rstrip().split("\n")[1:]]
	
	##### Part 1: find all nearby ticket values which are invalid for every field,
	##### and output their sum.
	
	result = 0
	for t in nearby_tickets:
		for v in t:
			if not check_validity(v, rules):
				# print(v)
				result += v
	
	print(result)
	
	##### Part 2: first, discard all invalid tickets. Then, from the values of
	##### all other tickets, deduce in what order the fields appear on the tickets
	
	valid_tickets = [t for t in nearby_tickets if all([check_validity(v, rules) for v in t])]
	valid_tickets.append(myticket)
	
	field_order = {}
	for field in rules:
		field_order[field] = set()
		for column in range(len(valid_tickets[0])):
			if all(check_value_ranges(t[column], rules[field]) for t in valid_tickets):
				field_order[field].add(column)
	
	changed = True
	while changed:
		changed = False
		for f in field_order:
			if len(field_order[f]) == 1:
				elem = field_order[f].pop()
				for f1 in field_order:
					field_order[f1].discard(elem)
				field_order[f].add(elem)
			else:
				changed = True
	
	field_order = {f : field_order[f].pop() for f in field_order}
	
	result = 1
	for field in rules:
		if field.startswith("departure"):
			result *= myticket[field_order[field]]
	
	# pprint(field_order)
	print(result)
	