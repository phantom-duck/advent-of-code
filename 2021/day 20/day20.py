from argparse import ArgumentParser
from functools import reduce

BIT2CHAR = [".", "#"]
CHAR2BIT = {".": 0, "#": 1}

def get_neighbours(image, i, j, infinite_bit=0):
	n = len(image)
	m = len(image[0])
	
	ret = []
	for di in [-1, 0, 1]:
		for dj in [-1, 0, 1]:
			if i + di < 0 or i + di > n - 1 or j + dj < 0 or j + dj > m - 1:
				ret.append(infinite_bit)
			else:
				ret.append(image[i + di][j + dj])
	return ret

def bits2int(bitstring):
	return reduce(lambda acc, curr: 2*acc + curr, bitstring, 0)

def enhance(image, enhancement_algo, infinite_bit=0):
	n = len(image)
	m = len(image[0])
	new_image = [[None] * (m + 2) for _ in range(n + 2)]
	for i, row in enumerate(new_image):
		for j, _ in enumerate(row):
			bits = get_neighbours(image, i - 1, j - 1, infinite_bit)
			idx = bits2int(bits)
			new_image[i][j] = enhancement_algo[idx]
	
	new_infinite_bit = enhancement_algo[bits2int([infinite_bit]*9)]
	
	return new_image, new_infinite_bit

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	
	enhancement_algo = text.split("\n\n")[0]
	input_image = text.split("\n\n")[1].strip().splitlines()
	
	##### Part 1: Enhance the image twice and find how many pixels are lit
	##### in the resulting image
	enhancement_algo_bits = [CHAR2BIT[x] for x in enhancement_algo]
	image_bits = [[CHAR2BIT[pixel] for pixel in row] for row in input_image]
	infinite_bit = 0
	for _ in range(2):
		image_bits, infinite_bit = enhance(image_bits, enhancement_algo_bits, infinite_bit)
	answer = sum(1 for row in image_bits for bit in row if bit == 1)
	print("Part 1: number of lit pixels after two enhancements is {}".format(answer))
	
	##### Part 2: the same, but enhance 50 times
	enhancement_algo_bits = [CHAR2BIT[x] for x in enhancement_algo]
	image_bits = [[CHAR2BIT[pixel] for pixel in row] for row in input_image]
	infinite_bit = 0
	for _ in range(50):
		image_bits, infinite_bit = enhance(image_bits, enhancement_algo_bits, infinite_bit)
	answer = sum(1 for row in image_bits for bit in row if bit == 1)
	print("Part 2: number of lit pixels after 50 enhancements is {}".format(answer))
	print("Final size of image is {}x{} pixels".format(len(image_bits), len(image_bits[0])))
	
	with open("output.txt", "w") as outf:
		outf.write("\n".join("".join(BIT2CHAR[bit] for bit in row) for row in image_bits))


if __name__ == "__main__":
	main()