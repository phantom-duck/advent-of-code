from argparse import ArgumentParser

class Line:
	def __init__(self, description: str):
		p1 = description.split(" -> ")[0]
		p2 = description.split(" -> ")[1]
		self.x1 = int(p1.split(",")[0])
		self.y1 = int(p1.split(",")[1])
		self.x2 = int(p2.split(",")[0])
		self.y2 = int(p2.split(",")[1])
	
	def is_horizontal(self):
		return self.y1 == self.y2
	
	def is_vertical(self):
		return self.x1 == self.x2
	
	def is_diagonal(self):
		return abs(self.y1 - self.y2) == abs(self.x1 - self.x2)
	
	def is_descending(self):
		return self.y2 - self.y1 == self.x2 - self.x1
	
	def list_points(self):
		if self.is_horizontal():
			x_max = max(self.x1, self.x2)
			x_min = min(self.x1, self.x2)
			return [(x, self.y1) for x in range(x_min, x_max + 1)]
		elif self.is_vertical():
			y_max = max(self.y1, self.y2)
			y_min = min(self.y1, self.y2)
			return [(self.x1, y) for y in range(y_min, y_max + 1)]
		elif self.is_diagonal():
			x_max = max(self.x1, self.x2)
			x_min = min(self.x1, self.x2)
			y_max = max(self.y1, self.y2)
			y_min = min(self.y1, self.y2)
			x_list = [x for x in range(x_min, x_max + 1)]
			y_list = [y for y in range(y_min, y_max + 1)]
			if not self.is_descending():
				y_list.reverse()
			return zip(x_list, y_list)
		else:
			raise NotImplementedError("I do not know what to do for crooked lines")

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read()
	
	##### Part 1: find the number of points where at least two lines overlap.
	##### Consider only horizontal and vertical lines
	vent_lines = [Line(text_line) for text_line in text.splitlines()]
	vent_lines_hv = [l for l in vent_lines if l.is_horizontal() or l.is_vertical()]
	
	lines_counts = dict()
	for line in vent_lines_hv:
		for p in line.list_points():
			if p in lines_counts:
				lines_counts[p] += 1
			else:
				lines_counts[p] = 1
	
	answer = sum(1 for k, v in lines_counts.items() if v > 1)
	print("Number of points with at least two lines = {}".format(answer))
	
	##### Part 2: the same, but also with the diagonal lines
	vent_lines = [Line(text_line) for text_line in text.splitlines()]
	
	lines_counts = dict()
	for line in vent_lines:
		for p in line.list_points():
			if p in lines_counts:
				lines_counts[p] += 1
			else:
				lines_counts[p] = 1
	
	answer = sum(1 for k, v in lines_counts.items() if v > 1)
	print("Number of points with at least two lines = {}".format(answer))

if __name__ == "__main__":
	main()