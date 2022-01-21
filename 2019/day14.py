from argparse import ArgumentParser
from collections import deque

class Reaction:
	def __init__(self, line: str):
		reactants_str = line.split("=>")[0].strip().split(",")
		self.reactants = {reactant: int(quantity) for quantity, reactant in map(lambda pair: pair.split(), reactants_str)}
		
		product_str = line.split("=>")[1].strip()
		self.product = product_str.split()[1]
		self.product_quantity = int(product_str.split()[0])

def minimum_ore4fuel(reactions, fuel_amount: int) -> int:
	producer_reactions = {r.product: r for r in reactions}
	available_quantities = dict()
	required_quantities = {"FUEL": fuel_amount}
	insufficient_chemicals = deque(["FUEL"])
	while insufficient_chemicals:
		chemical = insufficient_chemicals.pop()
		if chemical == "ORE":
			continue
		reaction = producer_reactions[chemical]
		
		available = available_quantities.get(chemical)
		if available is None:
			available = available_quantities[chemical] = 0
		required = required_quantities.get(chemical)
		if required is None:
			print("Something went wrong. Required material has no requirement entry.")
		
		# calculate number of times the reaction needs to happen
		if available >= required:
			continue
		extra_needed = required - available
		if extra_needed % reaction.product_quantity == 0:
			multiplier = extra_needed // reaction.product_quantity
		else:
			multiplier = extra_needed // reaction.product_quantity + 1
		
		# update all required reactants
		for reactant, quantity in reaction.reactants.items():
			original_requirement = required_quantities.get(reactant, 0)
			required_quantities[reactant] = original_requirement + multiplier * quantity
			insufficient_chemicals.appendleft(reactant)
		
		# update available product quantity
		available_quantities[chemical] += multiplier * reaction.product_quantity
	
	return required_quantities["ORE"]

def main():
	parser = ArgumentParser(description="Advent of Code 2019 day 13!")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	text = text.splitlines()
	
	##### Part 1: analyze the reactions and calculate the minimum amount of
	##### ORE needed to produce 1 unit of FUEL
	reactions = [Reaction(line) for line in text]
	ore_required = minimum_ore4fuel(reactions, 1)
	
	print("Minimum amount of ORE required is {}".format(ore_required))
	
	
	##### Part 2: Given 1 trillion ORE, what is the maximum amount of FUEL
	##### we can produce? We use binary search to find out!
	reactions = [Reaction(line) for line in text]
	fuel_min = 1
	fuel_max = 1_000_000_000_000
	while fuel_min < fuel_max:
		fuel_mid = (fuel_min + fuel_max) // 2 + 1
		ore_required = minimum_ore4fuel(reactions, fuel_mid)
		if ore_required < 1_000_000_000_000:
			fuel_min = fuel_mid
		elif ore_required > 1_000_000_000_000:
			fuel_max = fuel_mid - 1
		else:
			break
	
	assert fuel_min == fuel_max
	print("With 1 trillion ORE we can produce {} FUEL".format(fuel_min))


if __name__=="__main__":
	main()