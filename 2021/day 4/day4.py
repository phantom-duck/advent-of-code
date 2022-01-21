from argparse import ArgumentParser

class CustomError(Exception):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

class Board:
	def __init__(self, grid):
		self.grid = grid
		self.rows = len(grid)
		self.cols = len(grid[0])
		self.marks = [[False] * self.cols for _ in range(self.rows)]
	
	def mark(self, num: int):
		for i in range(self.rows):
			for j in range(self.cols):
				if self.grid[i][j] == num:
					self.marks[i][j] = True
	
	def check_win(self):
		return any(all(row) for row in self.marks) or any(all(col) for col in zip(*self.marks))
	
	def score(self):
		ret = 0
		for i in range(self.rows):
			for j in range(self.cols):
				if self.marks[i][j] is False:
					ret += self.grid[i][j]
		return ret

def str2board(lines: str):
	return Board([list(map(int, line.split())) for line in lines.splitlines()])

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read()
	text = text.split("\n\n")
	numbers_called = list(map(int, text[0].split(",")))
	boards = list(map(str2board, text[1:]))
	
	##### Part 1: find the winning board, and calculate its final score,
	##### (sum of unmarked numbers) x (final number called)
	winning_board = None
	number_called = None
	for number in numbers_called:
		for board in boards:
			board.mark(number)
		
		try:
			winning_board = [b.check_win() for b in boards].index(True)
			number_called = number
			break
		except ValueError:
			pass
	
	final_score = boards[winning_board].score() * number_called
	print("Winning board = {}".format(winning_board))
	print("Sum of unmarked numbers = {}".format(boards[winning_board].score()))
	print("Final number called = {}".format(number_called))
	print("Final winning score = {}".format(final_score))
	
	##### Part 2: find which board will win last, and its final score
	final_number_called = None
	for number in numbers_called:
		for board in boards:
			board.mark(number)
		
		if all(b.check_win() for b in boards):
			final_number_called = number
			break
		
		for i, board in enumerate(boards):
			if board.check_win():
				del boards[i]
	
	final_score = boards[0].score() * final_number_called
	print("\nPart 2:")
	print("Sum of unmarked numbers = {}".format(boards[0].score()))
	print("Final number called = {}".format(final_number_called))
	print("Final winning score = {}".format(final_score))

if __name__ == "__main__":
	main()