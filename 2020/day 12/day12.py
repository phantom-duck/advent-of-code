import sys
from pprint import pprint

class Ferry:
	def __init__(self, start_x=0, start_y=0, start_dir='E'):
		self.x = start_x
		self.y = start_y
		self.dir = start_dir
	
	def update(self, instruction):
		action = instruction[0]
		value = int(instruction[1:])
		
		if action == 'N':
			self.y += value
		elif action == 'S':
			self.y -= value
		elif action == 'E':
			self.x += value
		elif action == 'W':
			self.x -= value
		elif action == 'L':
			dirs = ['E', 'N', 'W', 'S']
			value = value // 90
			self.dir = dirs[(dirs.index(self.dir) + value) % 4]
		elif action == 'R':
			dirs = ['E', 'S', 'W', 'N']
			value = value // 90
			self.dir = dirs[(dirs.index(self.dir) + value) % 4]
		elif action == 'F':
			dirs = ['N', 'W', 'S', 'E']
			x = dirs.index(self.dir)
			x1, x0 = x // 2, x % 2
			self.x += (1 - 2*(x1 ^ x0)) * x0 * value
			self.y += (1 - 2*(x1 ^ x0)) * (1 - x0) * value			
		else:
			print("Ferry.update, something went wrong")

class Ferry2:
	def __init__(self, start_x=0, start_y=0, way_start_x = 10, way_start_y = 1):
		self.x = start_x
		self.y = start_y
		
		self.way_x = way_start_x
		self.way_y = way_start_y
	
	def update(self, instruction):
		action = instruction[0]
		value = int(instruction[1:])
		
		if action == 'N':
			self.way_y += value
		elif action == 'S':
			self.way_y -= value
		elif action == 'E':
			self.way_x += value
		elif action == 'W':
			self.way_x -= value
		elif action == 'L':
			diff_x = self.way_x - self.x
			diff_y = self.way_y - self.y
			
			costheta = [1, 0, -1, 0]
			sintheta = [0, 1, 0, -1]
			
			cos = costheta[value // 90]
			sin = sintheta[value // 90]
			
			xprime = cos * diff_x - sin * diff_y
			yprime = sin * diff_x + cos * diff_y
			self.way_x = self.x + xprime
			self.way_y = self.y + yprime
		elif action == 'R':
			diff_x = self.way_x - self.x
			diff_y = self.way_y - self.y
			
			costheta = [1, 0, -1, 0]
			sintheta = [0, -1, 0, 1]
			
			cos = costheta[value // 90]
			sin = sintheta[value // 90]
			
			xprime = cos * diff_x - sin * diff_y
			yprime = sin * diff_x + cos * diff_y
			self.way_x = self.x + xprime
			self.way_y = self.y + yprime
		elif action == 'F':
			diff_x = self.way_x - self.x
			diff_y = self.way_y - self.y
			for i in range(value):
				self.x += diff_x
				self.y += diff_y
			self.way_x = self.x + diff_x
			self.way_y = self.y + diff_y
		else:
			print("Ferry.update, something went wrong")

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read().split()
	
	##### Part 1: let the ferry follow the instructions, then output
	##### the sum of its final coordinates
	
	f = Ferry()
	for inst in text:
		f.update(inst)
	
	print(abs(f.x) + abs(f.y))
	
	##### Part 2: the same, but with the revised Ferry2
	
	f = Ferry2()
	for inst in text:
		f.update(inst)
	
	print(abs(f.x) + abs(f.y))