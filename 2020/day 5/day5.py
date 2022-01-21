import sys
from pprint import pprint

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read()
	text = text.split("\n")[:-1]
	
	boarding_passes = [int(entry.replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0"), 2) for entry in text]
	
	##### Part 1: find highest seat ID, where seat ID = 8 * row + column
	print(max(boarding_passes))
	
	##### Part 2: find your seat ID. It is the one that is missing, but previous and next should be there
	
	check_list = [False] * 1024
	for b in boarding_passes:
		check_list[b] = True
	
	for seat in range(1, 1023):
		if check_list[seat - 1] and (not check_list[seat]) and check_list[seat + 1]:
			res = seat
			break
	print(res)