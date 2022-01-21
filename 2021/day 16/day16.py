from argparse import ArgumentParser
from functools import reduce
from operator import mul

class CustomError(Exception):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

class Packet:
	def __init__(self, bitstream):
		self.version = int(bitstream[:3], base=2)
		self.type_id = int(bitstream[3:6], base=2)
		self.length_type_id = None
		self.value = None
		self.children = None
		self.bitstream = bitstream[6:]
		self.length = 6
		
		self.parse_body()
	
	def parse_body(self):
		if self.type_id == 4:
			self.value, length_consumed = parse_literal(self.bitstream)
			self.length += length_consumed
			self.bitstream = self.bitstream[length_consumed:]
		else:
			self.length_type_id = int(self.bitstream[0], base=2)
			self.bitstream = self.bitstream[1:]
			self.length += 1
			if self.length_type_id == 0:
				subtree_bitlength = int(self.bitstream[:15], base=2)
				self.bitstream = self.bitstream[15:]
				self.length += 15 + subtree_bitlength
				while subtree_bitlength != 0:
					if subtree_bitlength < 0:
						raise CustomError("Something went wrong. Children are longer than specified.")
					
					next_packet = Packet(self.bitstream)
					subtree_bitlength -= next_packet.length
					self.bitstream = self.bitstream[next_packet.length:]
					if self.children is None:
						self.children = [next_packet]
					else:
						self.children.append(next_packet)
			elif self.length_type_id == 1:
				subtrees_count = int(self.bitstream[:11], base=2)
				self.bitstream = self.bitstream[11:]
				self.length += 11
				for _ in range(subtrees_count):
					next_packet = Packet(self.bitstream)
					self.bitstream = self.bitstream[next_packet.length:]
					self.length += next_packet.length
					if self.children is None:
						self.children = [next_packet]
					else:
						self.children.append(next_packet)
			else:
				raise ValueError("Invalid bit value.")
		
	def version_sum(self):
		ret = self.version
		if self.type_id != 4:
			ret += sum(child.version_sum() for child in self.children)
		return ret
	
	def evaluate_expression(self):
		if self.type_id == 0:
			return sum(child.evaluate_expression() for child in self.children)
		elif self.type_id == 1:
			return reduce(mul, (child.evaluate_expression() for child in self.children), 1)
		elif self.type_id == 2:
			return min(child.evaluate_expression() for child in self.children)
		elif self.type_id == 3:
			return max(child.evaluate_expression() for child in self.children)
		elif self.type_id == 4:
			return self.value
		elif self.type_id == 5:
			val1 = self.children[0].evaluate_expression()
			val2 = self.children[1].evaluate_expression()
			return 1 if val1 > val2 else 0
		elif self.type_id == 6:
			val1 = self.children[0].evaluate_expression()
			val2 = self.children[1].evaluate_expression()
			return 1 if val1 < val2 else 0
		elif self.type_id == 7:
			val1 = self.children[0].evaluate_expression()
			val2 = self.children[1].evaluate_expression()
			return 1 if val1 == val2 else 0
	
	def __str__(self):
		return self.stringify("")
	
	def stringify(self, indent):
		ret = indent + "Version: {} Type: {}".format(self.version, self.type_id)
		if self.type_id == 4:
			ret += " Literal with value: {}".format(self.value)
		else:
			ret += "\n" + indent + "Operator packet with length type id {} and subpackets:\n".format(self.length_type_id)
			for child in self.children:
				ret += child.stringify(indent + "  ") + "\n"
			ret += "\n"
		
		return ret

def parse_literal(bitstream):
	ret = []
	bitlength = 0
	while True:
		bitlength += 5
		next_five = bitstream[:5]
		bitstream = bitstream[5:]
		
		ret.extend(next_five[1:])
		if next_five[0] == "0":
			break
	
	return int("".join(ret), base=2), bitlength

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	
	# TODO: restore leading zeros. For the specific input file it does not
	# matter, but in general it does
	bits = bin(int(text, base=16))[2:] # drop the initial '0b' part
	
	##### Part 1: Decode the packet hierarchy given in the BITS transmission
	##### (the input) and calculate the sum of all version numbers.
	packet_tree = Packet(bits)
	print("Total sum of all version numbers is {}".format(packet_tree.version_sum()))
	
	##### Part 2: evaluate the expression represented by the transmission
	print("Expression evaluates to {}".format(packet_tree.evaluate_expression()))


if __name__ == "__main__":
	main()