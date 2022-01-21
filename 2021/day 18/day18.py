from argparse import ArgumentParser
from ast import literal_eval
from dataclasses import dataclass, field
from typing import Optional, Union, TypeVar
from enum import Enum, auto
from collections import deque

class PairType(Enum):
	LEAF = auto()
	NODE = auto()

# @dataclass
# class Leaf:
	# number: int

Pair = TypeVar("Pair")

@dataclass
class Pair:
	number: Optional[int] = None
	left: Optional[Pair] = None
	right: Optional[Pair] = None
	parent: Optional[Pair] = field(default=None, repr=False)
	
	@property
	def type(self):
		if self.left is None and self.right is None:
			return PairType.LEAF
		else:
			return PairType.NODE
	
	def init_from_list(self, pairs_list, parent=None) -> Pair:
		left = pairs_list[0]
		if type(left) == int:
			self.left = Pair(left, None, None, self)
		else:
			self.left = Pair().init_from_list(left, parent=self)
		
		right = pairs_list[1]
		if type(right) == int:
			self.right = Pair(right, None, None, self)
		else:
			self.right = Pair().init_from_list(right, parent=self)
		
		self.parent = parent
		
		return self
	
	def reduce(self):
		while True:
			changed1 = self.explodeLeftmostDepth4()
			if changed1:
				continue
			changed2 = self.splitLeftmost10OrGreater()
			if not changed2:
				return
	
	def explodeLeftmostDepth4(self) -> bool:
		bfs_front = deque([(self, 0)])
		while True:
			if not bfs_front:
				break
			
			u, u_depth = bfs_front.pop()
			if u_depth == 4 and u.type is PairType.NODE:
				u.explode()
				return True
			
			if u.left is not None:
				bfs_front.appendleft((u.left, u_depth + 1))
			if u.right is not None:
				bfs_front.appendleft((u.right, u_depth + 1))
		
		return False
	
	def splitLeftmost10OrGreater(self) -> bool:
		# print("splitLeftmost10OrGreater called with:")
		# print(self)
		def find_first(u):
			if u.type is PairType.LEAF:
				if u.number >= 10:
					return u
				return None
			
			result = find_first(u.left) or find_first(u.right)
			return result
		
		leftmost_10_or_greater = find_first(self)
		if leftmost_10_or_greater is not None:
			leftmost_10_or_greater.split()
			return True
		return False
	
	def explode(self):
		# print("Pair.explode called with:")
		# print(self)
		curr = self
		curr_parent = self.parent
		while curr_parent.parent is not None and curr_parent.left is curr:
			curr = curr_parent
			curr_parent = curr_parent.parent
		
		if curr_parent.left is not curr:
			curr = curr_parent.left
			while curr.type is not PairType.LEAF:
				curr = curr.right
			# exploding pairs will always consist of two regular numbers
			curr.number += self.left.number
		
		curr = self
		curr_parent = self.parent
		while curr_parent.parent is not None and curr_parent.right is curr:
			curr = curr_parent
			curr_parent = curr_parent.parent
		
		if curr_parent.right is not curr:
			curr = curr_parent.right
			while curr.type is not PairType.LEAF:
				curr = curr.left
			# exploding pairs will always consist of two regular numbers
			curr.number += self.right.number
		
		self.number = 0
		self.left = self.right = None
	
	def split(self):
		self.left = Pair(self.number // 2, None, None, self)
		self.right = Pair(self.number // 2 + self.number % 2, None, None, self)
		self.number = None
	
	def __add__(self, value):
		ret_left = self.deep_copy()
		ret_right = value.deep_copy()
		ret = Pair(None, ret_left, ret_right, None)
		ret_left.parent = ret
		ret_right.parent = ret
		ret.reduce()
		return ret
	
	def deep_copy(self):
		if self.type is PairType.LEAF:
			return Pair(self.number, None, None, self.parent)
		
		ret_left = self.left.deep_copy()
		ret_right = self.right.deep_copy()
		ret = Pair(None, ret_left, ret_right, None)
		ret_left.parent = ret
		ret_right.parent = ret
		
		return ret
	
	def magnitude(self):
		if self.type is PairType.LEAF:
			return self.number
		elif self.type is PairType.NODE:
			return 3 * self.left.magnitude() + 2 * self.right.magnitude()
		else:
			raise ValueError("Invalid pair type")
	
	def to_list(self):
		if self.type is PairType.LEAF:
			return self.number
		elif self.type is PairType.NODE:
			return [self.left.to_list(), self.right.to_list()]
		else:
			raise ValueError("Invalid pair type")




def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	text = text.splitlines()
	
	pairs_lists = [literal_eval(line) for line in text]
	
	##### Part 1: Add all the snailfish numbers in sequence, from top to
	##### bottom, and find the magnitude of the result, as in the instructions.
	pairs = [Pair().init_from_list(pairs_list) for pairs_list in pairs_lists]
	pairs_sum = sum(pairs[1:], pairs[0])
	print(pairs_sum.to_list())
	print("Part 1 answer = {}".format(pairs_sum.magnitude()))
	
	##### Part 2: find the maximum magnitude of the sum of any two pairs
	##### from the list of snailfish numbers (i.e. pairs)
	pairs = [Pair().init_from_list(pairs_list) for pairs_list in pairs_lists]
	max_magnitude = max((p1 + p2).magnitude() for p1 in pairs for p2 in pairs if p1 is not p2)
	print("Part 2 answer = {}".format(max_magnitude))


if __name__ == "__main__":
	main()