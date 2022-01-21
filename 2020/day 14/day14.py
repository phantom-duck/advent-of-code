import sys
from pprint import pprint

def gen_addresses(base_addr, floats):
	addr_str = list(bin(base_addr)[2:])
	addr_str = (36 - len(addr_str))*["0"] + addr_str
	# print(addr_str)
	
	for s in range(2**len(floats)):
		subset = bin(s)[2:]
		subset = (len(floats) - len(subset))*"0" + subset
		# print(subset)
		for i, bit in enumerate(floats):
			addr_str[bit] = subset[i]
		yield int("".join(addr_str), 2)

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.readlines()
	
	##### Part 1: run program as instructed, and ouput the sum
	##### of all values in memory at the end
	
	mask0 = 0b1111_1111_1111_1111_1111_1111_1111_1111_1111
	mask1 = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000
	memory = dict()
	for command in text:
		if command.startswith("mask"):
			mask0 = int(command.split()[-1].replace("X", "1"), 2)
			mask1 = int(command.split()[-1].replace("X", "0"), 2)
		elif command.startswith("mem"):
			address = int(command.split()[0].split("[")[1][:-1])
			value = int(command.split()[-1])
			value = (value & mask0) | mask1
			memory[address] = value
		else:
			print("Invalid command")
	
	total = 0
	for k in memory:
		total += memory[k]
	
	print(total)
	
	##### Part 1: same, but now bitmask affects the address
	##### 0: same, 1: turns to 1, X: floating (takes all values)
	
	floating = []
	mask1 = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000
	memory = dict()
	for command in text:
		if command.startswith("mask"):
			floating = [i for (i, x) in enumerate(command.split()[-1]) if x == "X"]
			mask1 = int(command.split()[-1].replace("X", "0"), 2)
		elif command.startswith("mem"):
			address = int(command.split()[0].split("[")[1][:-1])
			value = int(command.split()[-1])
			address = address | mask1
			# print(address, floating)
			for add in gen_addresses(address, floating):
				memory[add] = value
			# pprint(memory)
		else:
			print("Invalid command")
	
	total = 0
	for k in memory:
		total += memory[k]
	
	# pprint(memory)
	print(total)