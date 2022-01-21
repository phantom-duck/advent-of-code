from argparse import ArgumentParser
from collections import deque

def neighbours(i, j, n, m):
	if i > 0:
		yield (i - 1, j)
	if i < n - 1:
		yield (i + 1, j)
	if j > 0:
		yield (i, j - 1)
	if j < m - 1:
		yield (i, j + 1)
	
	if i > 0 and j > 0:
		yield (i - 1, j - 1)
	if i > 0 and j < m - 1:
		yield (i - 1, j + 1)
	if i < n - 1 and j > 0:
		yield (i + 1, j - 1)
	if i < n - 1 and j < m - 1:
		yield (i + 1, j + 1)

def run_step(energies):
	flashing = deque()
	for i, row in enumerate(energies):
		for j, energy in enumerate(row):
			energies[i][j] += 1
			if energies[i][j] > 9:
				flashing.append((i, j))
	
	n = len(energies)
	m = len(energies[0])
	while flashing:
		i, j = flashing.pop()
		if not energies[i][j] > 9:
			continue
		
		energies[i][j] = 0
		for n_i, n_j in neighbours(i, j, n, m):
			if energies[n_i][n_j] == 0:
				continue
			energies[n_i][n_j] += 1
			if energies[n_i][n_j] > 9:
				flashing.append((n_i, n_j))

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	text = text.splitlines()
	
	##### Part 1: given the starting energy levels of the dumbo octopuses,
	##### calculate how many flashes will there have been, in total, after
	##### 100 steps
	octopus_energies = [[int(digit) for digit in line] for line in text]
	total_flashes = 0
	for step in range(100):
		run_step(octopus_energies)
		total_flashes += sum(1 for row in octopus_energies for energy in row if energy == 0)
	
	print("Total flashes after 100 steps = {}".format(total_flashes))
	
	##### Part 2: find the first step during which all octopuses flash
	octopus_energies = [[int(digit) for digit in line] for line in text]
	step = 0
	while True:
		step += 1
		run_step(octopus_energies)
		flashes = sum(1 for row in octopus_energies for energy in row if energy == 0)
		if flashes == sum(1 for row in octopus_energies for energy in row):
			break
	
	print("The first step during which all octopuses flash is {}".format(step))



if __name__ == "__main__":
	main()