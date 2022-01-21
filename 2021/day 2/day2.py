from argparse import ArgumentParser
from functools import reduce

def command2coord(command: str):
	num = int(command.split()[1])
	if command.startswith("forward"):
		return (num, 0)
	elif command.startswith("down"):
		return (0, num)
	elif command.startswith("up"):
		return (0, -num)
	else:
		raise ValueError("Invalid command name")

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read()
	
	##### Part 1: find final position of the submarine
	increments = [command2coord(x) for x in text.splitlines()]
	def addTuple(tup1, tup2):
		return [sum(x) for x in zip(tup1, tup2)]
	answer = reduce(addTuple, increments, (0, 0)) # initial position and depth are 0
	print("Final horizontal position = {}".format(answer[0]))
	print("Final depth = {}".format(answer[1]))
	print("Product = {}".format(answer[0] * answer[1]))
	
	##### Part 2: changed regime where there is another coordinate, aim
	increments = [command2coord(x) for x in text.splitlines()]
	x, depth, aim = 0, 0, 0
	for dx, daim in increments:
		aim += daim
		x += dx
		depth += aim * dx
	print("Final horizontal position = {}".format(x))
	print("Final depth = {}".format(depth))
	print("Final aim = {}".format(aim))
	print("Product = {}".format(x * depth))

if __name__ == "__main__":
	main()