from argparse import ArgumentParser
from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class UndirectedGraph:
	adj_list: Dict[str, List[str]] = field(default_factory=dict)
	
	def add_edge(self, u: str, v: str):
		self.adj_list.setdefault(u, [])
		self.adj_list.setdefault(v, [])
		
		self.adj_list[u].append(v)
		self.adj_list[v].append(u)
	
	def squash_big_caves(self):
		for big_cave, neighbours in self.adj_list.items():
			if big_cave.isupper():
				for u1 in neighbours:
					self.adj_list[u1].remove(big_cave)
					for u2 in neighbours:
						self.adj_list[u1].append(u2)
	
	def paths_number(self, start: str, end: str, visited: set):
		# print(start, end=",")
		if start == end:
			# print(end)
			return 1
		
		ret = 0
		for u in self.adj_list[start]:
			if u in visited:
				continue
			
			visited.add(u)
			ret += self.paths_number(u, end, visited)
			visited.remove(u)
		return ret
	
	def paths_number2(self, start: str, end: str, visited: set, small_available=True, print_prefix=""):
		# print(start, end=",")
		if start == end:
			# print("reached end")
			# print(print_prefix + end)
			return 1
		
		ret = 0
		for u in self.adj_list[start]:
			if u in visited:
				if small_available and u != "start":
					# print("Call starts.")
					ret += self.paths_number2(u, end, visited, small_available=False, print_prefix=print_prefix+start+",")
					# print("Call finishes.")
				continue
			
			visited.add(u)
			ret += self.paths_number2(u, end, visited, small_available=small_available, print_prefix=print_prefix+start+",")
			visited.remove(u)
		return ret

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	text = text.splitlines()
	
	edges = [tuple(line.split("-")) for line in text]
	source = "start"
	target = "end"
	
	##### Part 1: Calculate the total number of paths from "start" to "end"
	##### that pass through small caves at most once.
	g = UndirectedGraph()
	for u, v in edges:
		g.add_edge(u, v)
	g.squash_big_caves()
	# print(g)
	print("Part 1. Total number of paths = {}".format(g.paths_number(source, target, {source})))
	
	##### Part 2: the same, but now we can visit a single small cave twice,
	##### except for the "start" and "end" caves.
	g = UndirectedGraph()
	for u, v in edges:
		g.add_edge(u, v)
	g.squash_big_caves()
	print(g)
	print("Part 2. Total number of paths = {}".format(g.paths_number2(source, target, {source}, small_available=True)))


if __name__ == "__main__":
	main()