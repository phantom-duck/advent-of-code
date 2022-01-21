from argparse import ArgumentParser
from collections import deque

def filter_onlyone(pats_sets, pred):
	results = [i for i, pat_set in enumerate(pats_sets) if pred(pat_set)]
	if len(results) != 1:
		print("Something went wrong. Length of results is not 1.")
	else:
		return results[0]

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	text = text.splitlines()
	
	##### Part 1: find all corrupted lines, calculate their score
	##### and add them up
	illegal_char_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
	opening_chars = ["(", "[", "{", "<"]
	closing2opening = {")": "(", "]": "[", "}": "{", ">": "<"}
	symbol_stack = deque()
	total_syntax_error_score = 0
	for line in text:
		symbol_stack.clear()
		first_illegal_char = None
		for char in line:
			if char in opening_chars:
				symbol_stack.append(char)
				continue
			matching_opening = closing2opening[char]
			last_opening = symbol_stack[-1]
			if matching_opening == last_opening:
				symbol_stack.pop()
			else:
				first_illegal_char = char
				break
		
		if first_illegal_char is not None:
			score = illegal_char_scores[first_illegal_char]
			total_syntax_error_score += score
	
	print("Total syntax error score = {}\n".format(total_syntax_error_score))
	
	##### Part 2: find all incomplete lines, deduce the correct completion
	##### string and calculate their scores. Then, find the median of the scores.
	completion_char_scores = {")": "1", "]": "2", "}": "3", ">": "4"}
	opening_chars = ["(", "[", "{", "<"]
	closing2opening = {")": "(", "]": "[", "}": "{", ">": "<"}
	opening2closing = {"(": ")", "[": "]", "{": "}", "<": ">"}
	symbol_stack = deque()
	lines_completion_scores = []
	for line in text:
		symbol_stack.clear()
		is_corrupted = False
		for char in line:
			if char in opening_chars:
				symbol_stack.append(char)
				continue
			matching_opening = closing2opening[char]
			last_opening = symbol_stack[-1]
			if matching_opening == last_opening:
				symbol_stack.pop()
			else:
				is_corrupted = True
				break
		
		if is_corrupted:
			continue
		if symbol_stack: # it means the line is incomplete
			symbol_stack.reverse()
			char_scores = [completion_char_scores[opening2closing[open_char]] for open_char in symbol_stack]
			score = int("".join(char_scores), base=5)
			lines_completion_scores.append(score)
	
	lines_completion_scores.sort()
	n = len(lines_completion_scores)
	answer = lines_completion_scores[n // 2]
	print("The middle score is {}".format(answer))

if __name__ == "__main__":
	main()