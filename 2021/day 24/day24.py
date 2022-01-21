##### No code used. I simply analyzed the input

from argparse import ArgumentParser

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	text = text.splitlines()
	
	##### Part 1: 


if __name__ == "__main__":
	main()