import sys
from pprint import pprint

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read()
	
	groups_answers = [ans.split() for ans in text.split("\n\n")]
	# pprint(groups_answers)
	
	##### Part 1: sum the numbers of questions each group answered with "yes"
	##### meaning, for each element of groups_answers count how many different letters
	##### it contains, and sum those.
	
	curr_sum = 0
	for group in groups_answers:
		group_count = 0
		for letter in "abcdefghijklmnopqrstuvwxyz":
			if any(letter in person for person in group):
				group_count += 1
		
		curr_sum += group_count
	
	print(curr_sum)
	
	##### Part 2: the same, but now we want the questions to which all members 
	##### of the group answered with "yes"
	
	curr_sum = 0
	for group in groups_answers:
		group_count = 0
		for letter in "abcdefghijklmnopqrstuvwxyz":
			if all(letter in person for person in group):
				group_count += 1
		
		curr_sum += group_count
	
	print(curr_sum)