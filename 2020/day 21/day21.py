import sys
from pprint import pprint

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.readlines()
	
	foods = [line.split("(contains")[0].split() for line in text]
	allergens = [line.split("(contains")[1].lstrip().rstrip(")\n").split(", ") for line in text]
	
	# print(foods)
	# print(allergens)
	
	##### Part 1: find which ingredients cannot contain any allergen
	
	allergen_candidates = {}
	for food, all_list in zip(foods, allergens):
		ingredients_set = set(food)
		for allergen in all_list:
			if allergen not in allergen_candidates:
				allergen_candidates[allergen] = ingredients_set
			else:
				allergen_candidates[allergen] = allergen_candidates[allergen].intersection(ingredients_set)
	
	suspicious_ingredients = set()
	for allergen in allergen_candidates:
		suspicious_ingredients = suspicious_ingredients.union(allergen_candidates[allergen])
	
	total = 0
	for food in foods:
		for ing in food:
			if ing not in suspicious_ingredients:
				total += 1
	
	print(total)
	
	##### Part 2: find which ingredient contains which allergen, and arrange these
	##### ingredients alphabetically by their allergen, separated by commas.
	
	pprint(allergen_candidates)
	
	changed = True
	while changed:
		changed = False
		for allergen in allergen_candidates:
			if len(allergen_candidates[allergen]) == 1:
				single_ingredient = allergen_candidates[allergen].pop()
				for allergen1 in allergen_candidates:
					allergen_candidates[allergen1].discard(single_ingredient)
				allergen_candidates[allergen].add(single_ingredient)
			else:
				changed = True
	
	pprint(allergen_candidates)
	
	l = list(allergen_candidates.items())
	l.sort()
	print([y for (x, y) in l])