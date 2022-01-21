import sys
from pprint import pprint

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read().lstrip().rstrip()
	
	starting_numbers = [int(x) for x in text.split(",")]
	
	##### Part 1: run the game as described in the problem statement, find
	##### the 2020-th number spoken
	
	# global time
	t = 1
	
	history = dict()
	for x in starting_numbers[:-1]:
		history[x] = t
		t += 1
	
	x = starting_numbers[-1]
	while t < 2020:
		if x not in history:
			history[x] = t
			x = 0
			t += 1
		else:
			history[x], x = t, t - history[x]
			t += 1
	
	print(x)
	
	##### Part 2: same, but find the 30000000-th number spoken
	
	# global time
	t = 1
	
	history = dict()
	for x in starting_numbers[:-1]:
		history[x] = t
		t += 1
	
	x = starting_numbers[-1]
	while t < 30000000:
		if x not in history:
			history[x] = t
			x = 0
			t += 1
		else:
			history[x], x = t, t - history[x]
			t += 1
	
	print(x)