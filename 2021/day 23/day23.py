from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum, auto
from typing import List

class Type(Enum):
	A = auto()
	B = auto()
	C = auto()
	D = auto()
	HALL = auto()
TYPE_COSTS = {Type.A: 1, Type.B: 10, Type.C: 100, Type.D: 1000}

@dataclass(frozen=True)
class Amphipod:
	type: Type
	compartment: Type
	position: int

@dataclass(frozen=True)
class State:
	amphipods: List[Amphipod]

	def least_energy(self):
		if all(a.type == a.compartment for a in self.amphipods):
		   return 0
		
		min_energy = 100_000
		for a in self.amphipods:
			if a.compartment is a.type:
				if a.position == 0:
					continue
				elif any(aa.compartment == a.compartment and aa.position == 0 for aa in self.amphipods if aa is not a):
					new_state_amphipods = self.amphipods.copy()
				else:
					continue
			

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	
	
	
	##### Part 1: 


if __name__ == "__main__":
	main()