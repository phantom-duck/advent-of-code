import sys
from typing import List, Tuple

class Tree:
	def __init__(self, pairs: List[Tuple[str]]):
		self.adj_list = dict()
		for (u, v) in pairs:
			if u in self.adj_list:
				self.adj_list[u].append(v)
			else:
				self.adj_list[u] = [v]
	
	def DFS_init(self, start):
		self.depths = dict()
		self.DFS(start, 0)
	
	def DFS(self, u, depth):
		self.depths[u] = depth
		if u in self.adj_list:
			for v in self.adj_list[u]:
				self.DFS(v, depth + 1)
	
	def add_depths(self):
		sum = 0
		for key in self.depths:
			sum += self.depths[key]
		return sum

def extract_pair(line: str) -> (str, str):
	return tuple(line.replace("\n", "").split(")"))

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"
	
	with open(filename) as infile:
		text = infile.readlines()
	
	pairs = [extract_pair(line) for line in text]
	tree = Tree(pairs)
	
	# tree.DFS_init("COM")
	# print(tree.add_depths())
	
	