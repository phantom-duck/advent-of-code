from argparse import ArgumentParser
from typing import List
from abc import ABC, abstractmethod
from collections import deque


def computeParameters(program, ip, rel_base, parameter_modes, count) -> list:
	pars = []
	for i in range(count):
		mode = parameter_modes[-1-i]
		if mode==0:
			pars.append(program[program[ip+i+1]])
		elif mode==1:
			pars.append(program[ip+i+1])
		elif mode==2:
			pars.append(program[rel_base + program[ip+i+1]])
		else:
			raise ValueError("invalid parameter mode")
	return pars

def computeEffectiveAddress(program, ip, rel_base, mode) -> int:
	if mode==0:
		ret = program[ip]
	elif mode==1:
		ret = ip
	elif mode==2:
		ret = rel_base + program[ip]
	else:
		raise ValueError("Mode value invalid")
	return ret



class IOManager(ABC):
	@abstractmethod
	def read() -> int:
		pass
	
	@abstractmethod
	def write(value: int) -> None:
		pass

class SimpleIO(IOManager):
	def read(self) -> int:
		while True:
			user_input = input("Please input an integer: ")
			try:
				ret = int(user_input)
			except ValueError:
				print("Please give a valid integer")
			else:
				break
		return ret
	
	def write(self, value: int) -> None:
		print(value)

class Intcode:
	def __init__(self, code: List[int]=None, io: IOManager=None):
		self.program = code if code is not None else [99]
		self.program += [0]*100000
		self.ip = 0
		self.io = io if io is not None else SimpleIO()
		self.rel_base = 0
	
	def run(self):
		program = self.program
		while True:
			ip = self.ip
			rel_base = self.rel_base
			opcode = program[ip] % 100
			
			# for parameter_modes:
			# 1) integer division by 100 to toss the opcode (last two digits)
			# 2) make it a string and each element an int, to get a list of digits
			# 3) pad with zeros for the case of leading zeros
			parameter_modes = [0]*3 + [int(digit) for digit in str(program[ip] // 100)]
			
			if opcode==99:
				# Instruction: Halt
				# print("Program has ended.")
				return 0
			elif opcode==1:
				# Instruction: Add first and second parameter, place result in third
				# print(ip, ":", parameter_modes, "ADD: par1 =", program[ip+1], "par2 =", program[ip+2], "par3 =", program[ip+3])
				if parameter_modes[-3] != 0 and parameter_modes[-3] != 2:
					raise ValueError("invalid parameter mode for l-value")
				src1_addr = computeEffectiveAddress(program, ip + 1, rel_base, parameter_modes[-1])
				src2_addr = computeEffectiveAddress(program, ip + 2, rel_base, parameter_modes[-2])
				trgt_addr = computeEffectiveAddress(program, ip + 3, rel_base, parameter_modes[-3])
				program[trgt_addr] = program[src1_addr] + program[src2_addr]
				self.ip += 4
			elif opcode==2:
				# Instruction: Multiply first and second parameter, place result in third
				# print(ip, ":", parameter_modes, "MUL: par1 =", program[ip+1], "par2 =", program[ip+2], "par3 =", program[ip+3])
				if parameter_modes[-3] != 0 and parameter_modes[-3] != 2:
					raise ValueError("invalid parameter mode for l-value")
				src1_addr = computeEffectiveAddress(program, ip + 1, rel_base, parameter_modes[-1])
				src2_addr = computeEffectiveAddress(program, ip + 2, rel_base, parameter_modes[-2])
				trgt_addr = computeEffectiveAddress(program, ip + 3, rel_base, parameter_modes[-3])
				program[trgt_addr] = program[src1_addr] * program[src2_addr]
				self.ip += 4
			elif opcode==3:
				# Instruction: Takes a single integer as input, saves it at the position given by the parameter
				# print(ip, ":", parameter_modes, "IN: par =", program[ip+1])
				val = self.io.read()
				if parameter_modes[-1] != 0 and parameter_modes[-1] != 2:
					raise ValueError("invalid parameter mode for l-value")
				trgt_addr = computeEffectiveAddress(program, ip + 1, rel_base, parameter_modes[-1])
				program[trgt_addr] = val
				self.ip += 2
			elif opcode==4:
				# Instruction: Outputs the value of its only parameter
				src_addr = computeEffectiveAddress(program, ip + 1, rel_base, parameter_modes[-1])
				self.io.write(program[src_addr])
				self.ip += 2
			elif opcode==5:
				# Instruction: jump if true
				# print("jump-if-true: par1 =", program[ip+1], "par2 =", program[ip+2], "par3 =", program[ip+3])
				pars = computeParameters(program, ip, rel_base, parameter_modes, 2)
				if pars[0] != 0:
					self.ip = pars[1]
				else:
					self.ip += 3
			elif opcode==6:
				# Instruction: jump if false
				# print("jump-if-false: par1 =", program[ip+1], "par2 =", program[ip+2], "par3 =", program[ip+3])
				pars = computeParameters(program, ip, rel_base, parameter_modes, 2)
				if pars[0] == 0:
					self.ip = pars[1]
				else:
					self.ip += 3
			elif opcode==7:
				# Instruction: less than
				# print("less than: par1 =", program[ip+1], "par2 =", program[ip+2])
				if parameter_modes[-3] != 0 and parameter_modes[-3] != 2:
					raise ValueError("invalid parameter mode for l-value")
				src1_addr = computeEffectiveAddress(program, ip + 1, rel_base, parameter_modes[-1])
				src2_addr = computeEffectiveAddress(program, ip + 2, rel_base, parameter_modes[-2])
				trgt_addr = computeEffectiveAddress(program, ip + 3, rel_base, parameter_modes[-3])
				
				if program[src1_addr] < program[src2_addr]:
					program[trgt_addr] = 1
				else:
					program[trgt_addr] = 0
				self.ip += 4
			elif opcode==8:
				# Instruction: equals
				# print("equals: par1 =", program[ip+1], "par2 =", program[ip+2])
				if parameter_modes[-3] != 0 and parameter_modes[-3] != 2:
					raise ValueError("invalid parameter mode for l-value")
				src1_addr = computeEffectiveAddress(program, ip + 1, rel_base, parameter_modes[-1])
				src2_addr = computeEffectiveAddress(program, ip + 2, rel_base, parameter_modes[-2])
				trgt_addr = computeEffectiveAddress(program, ip + 3, rel_base, parameter_modes[-3])
				
				if program[src1_addr] == program[src2_addr]:
					program[trgt_addr] = 1
				else:
					program[trgt_addr] = 0
				self.ip += 4
			elif opcode==9:
				# Instruction: add the parameter to the relative base
				pars = computeParameters(program, ip, rel_base, parameter_modes, count=1)
				self.rel_base += pars[0]
				self.ip += 2
			else:
				print("Unknown Opcode:", opcode, "something went wrong...")
				break
	
def disassembler(program):
	ip = 0
	ret = []
	while ip < len(program):
		opcode = program[ip] % 100
		par_modes = program[ip] // 100
		if opcode==99:
			# Instruction: Halt
			ret.append((ip, "HALT"))
			rest = program[ip + 1:]
			ret += list(zip(range(ip + 1, len(program)), rest))
			break
		elif opcode==1:
			# Instruction: Add first and second parameter, place result in third
			names = ["ADD_PP", "ADD_PI", "ADD_IP", "ADD_II"]
			text = names[par_modes % 10 + (par_modes // 10) % 10] \
				 + " " + str(program[ip + 1]) \
				 + " " + str(program[ip + 2]) \
				 + " " + str(program[ip + 3])
			ret.append((ip, text))
			ip += 4
		elif opcode==2:
			# Instruction: Multiply first and second parameter, place result in third
			names = ["MUL_PP", "MUL_PI", "MUL_IP", "MUL_II"]
			text = names[par_modes % 10 + (par_modes // 10) % 10] \
				 + " " + str(program[ip + 1]) \
				 + " " + str(program[ip + 2]) \
				 + " " + str(program[ip + 3])
			ret.append((ip, text))
			ip += 4
		elif opcode==3:
			# Instruction: Takes a single integer as input, saves it at the position given by the parameter
			text = "IN" + " " + str(program[ip+1])
			ret.append((ip, text))
			ip += 2
		elif opcode==4:
			# Instruction: Outputs the value of its only parameter
			names = ["OUT_P", "OUT_I"]
			text = names[par_modes % 10] + " " + str(program[ip + 1])
			ret.append((ip, text))
			ip += 2
		elif opcode==5:
			# Instruction: jump if true
			names = ["JIT_PP", "JIT_PI", "JIT_IP", "JIT_II"]
			text = names[par_modes % 10 + (par_modes // 10) % 10] \
				 + " " + str(program[ip + 1]) \
				 + " " + str(program[ip + 2])
			ret.append((ip, text))
			ip += 3
		elif opcode==6:
			# Instruction: jump if false
			names = ["JIF_PP", "JIF_PI", "JIF_IP", "JIF_II"]
			text = names[par_modes % 10 + (par_modes // 10) % 10] \
				 + " " + str(program[ip + 1]) \
				 + " " + str(program[ip + 2])
			ret.append((ip, text))
			ip += 3
		elif opcode==7:
			# Instruction: less than
			names = ["LT_PP", "LT_PI", "LT_IP", "LT_II"]
			text = names[par_modes % 10 + (par_modes // 10) % 10] \
				 + " " + str(program[ip + 1]) \
				 + " " + str(program[ip + 2]) \
				 + " " + str(program[ip + 3])
			ret.append((ip, text))
			ip += 4
		elif opcode==8:
			# Instruction: equals
			names = ["EQ_PP", "EQ_PI", "EQ_IP", "EQ_II"]
			text = names[par_modes % 10 + (par_modes // 10) % 10] \
				 + " " + str(program[ip + 1]) \
				 + " " + str(program[ip + 2]) \
				 + " " + str(program[ip + 3])
			ret.append((ip, text))
			ip += 4
		elif opcode==9:
			# Instruction: change relative base
			pass
		else:
			print("Unknown Opcode:", opcode, "Something went wrong...")
			break
	return ret

class DroidFinishedException(Exception):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

def neighbours(i, j):
	return [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]

class DroidControl(IOManager):
	move_commands = {"north": 1, "south": 2, "west": 3, "east": 4}
	moves = ["north", "south", "west", "east"]
	status = ["Wall", "Move", "Oxygen"]

	def __init__(self):
		self.costs = {(0, 0): 0}
		self.marks = {(0, 0): "U"}
		self.search_front = deque([0])
		self.oxygen = None
		
		self.curr_vertex = 0
		self.curr_dir = 0
	
	def read(self) -> int:
		self.curr_dir += 1
		if self.curr_dir > 3:
			next_vertex = self.search_front.pop()
			self.marks[next_vertex] = "E"
			self.curr_dir = 0
			return self.move_commands["north"]
		else:
			return self.move_commands[self.moves[self.curr_dir]]
	
	def write(self, value: int) -> None:
		status = self.status[value]
		if status == "Wall":
			pass
		elif status == "Move":
			pass
		elif status == "Oxygen":
			pass
		else:
			raise ValueError("Invalid output value from the Intcode program")

# class ExplorerDroid:
	# move_commands = {"north": 1, "south": 2, "west": 3, "east": 4}
	# status = ["Wall", "Move", "Oxygen"]
	
	# def __init__(self):
		# self.

def main():
	parser = ArgumentParser(description="Advent of Code 2019 day 13!")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read()
	program = [int(x) for x in text.split(",")]
	
	##### Part 1: 
	droid = DroidControl()
	computer = Intcode(program, io=droid)
	try:
		computer.run()
	except DroidFinishedException:
		print("Droid finished exploration")
	...

if __name__=="__main__":
	main()