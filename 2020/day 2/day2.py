import sys
import re

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read()
	
	input_spec = re.compile(r'(\d*)-(\d*) ([a-z]): ([a-z]*)')
	
	##### for question 1
	n_valid = 0
	for low, high, char, password in input_spec.findall(text):
		low = int(low)
		high = int(high)
		
		n_char = len([x for x in password if x == char])
		
		if n_char >= low and n_char <= high:
			n_valid += 1
	
	print(n_valid)
	
	##### for question 2
	n_valid = 0
	for pos1, pos2, char, password in input_spec.findall(text):
		pos1 = int(pos1) - 1
		pos2 = int(pos2) - 1		
		if (password[pos1] == char and password[pos2] != char) or (password[pos1] != char and password[pos2] == char):
			n_valid += 1
	
	print(n_valid)