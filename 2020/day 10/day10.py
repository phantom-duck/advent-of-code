import sys
from pprint import pprint

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.readlines()
	
	jolt_ratings = [int(x) for x in text]
	jolt_ratings.sort()
	
	##### Part 1: find a chain that uses all the adapters, plus the charging
	##### outlet at the beginning and our device at the end, and count the
	##### successive joltage differences. Output the number of 1-jolt
	##### differences times the number of 3-jolt differences
	
	n_1jolt = 0
	n_3jolt = 1
	prev = 0
	for j in jolt_ratings:
		if j - prev == 1:
			n_1jolt += 1
		elif j - prev == 3:
			n_3jolt += 1
		
		prev = j
	
	print(n_1jolt * n_3jolt)
	
	
	##### Part 2: count all possible feasible chains (sequences) of adapters
	##### that can connect the charging outlet (0) to our device (max + 3)
	
	## We use sort of dynamic programming, counting, step by step, the number
	## of chains that start at the charging outlet (0) and end at adapter i.
	jolt_ratings = [0] + jolt_ratings
	ways_0_to_i = [1] + ([0] * (len(jolt_ratings) - 1))
	for i, jolt in enumerate(jolt_ratings):
		ways = 0
		previous_in_chain = i
		while previous_in_chain >= 0 and jolt_ratings[previous_in_chain] >= jolt - 3:
			ways += ways_0_to_i[previous_in_chain]
			previous_in_chain -= 1
		
		ways_0_to_i[i] = ways
	
	# print(jolt_ratings)
	# print(ways_0_to_i)
	print(ways_0_to_i[-1])
		