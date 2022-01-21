from argparse import ArgumentParser
from typing import List
from abc import ABC, abstractmethod


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

class GatherArcadeOutput(IOManager):
	tileid2name = ["empty", "wall", "block", "paddle", "ball"]

	def __init__(self):
		self.instruction_buffer = []
		self.drawn_tiles_history = {"empty": set(), "wall": set(), "block": set(), "paddle": set(), "ball": set()}
	
	def read(self) -> int:
		return int(input("Give me: "))
	
	def write(self, value: int) -> None:
		self.instruction_buffer.append(value)
		if len(self.instruction_buffer) == 3:
			self.add_tile(*self.instruction_buffer)
			self.instruction_buffer.clear()
	
	def add_tile(self, x, y, tile_id):
		tile_name = self.tileid2name[tile_id]
		self.drawn_tiles_history[tile_name].add((x, y))

# virtually "plays" the game by following the position of the ball
class ArcadeIO(IOManager):
	tileid2name = ["empty", "wall", "block", "paddle", "ball"]
	joystick_inputs = {"neutral": 0, "left": -1, "right": 1}
	
	def __init__(self):
		self.instruction_buffer = []
		
		self.ball_x = self.ball_y = None
		self.pad_x = self.pad_y = None
		
		self.score = 0
		
		### debug
		# self.ball_history = set()
	
	def read(self) -> int:
		if self.pad_x < self.ball_x:
			return self.joystick_inputs["right"]
		elif self.pad_x > self.ball_x:
			return self.joystick_inputs["left"]
		else:
			return self.joystick_inputs["neutral"]
	
	def write(self, value: int) -> None:
		self.instruction_buffer.append(value)
		if len(self.instruction_buffer) == 3:
			self.add_tile(*self.instruction_buffer)
			self.instruction_buffer.clear()
	
	def add_tile(self, x, y, tile_id) -> None:
		if x == -1 and y == 0:
			self.score = tile_id
			return
	
		if self.tileid2name[tile_id] == "ball":
			self.ball_x = x
			self.ball_y = y
			### debug
			# self.ball_history.add((x, y))
		elif self.tileid2name[tile_id] == "paddle":
			self.pad_x = x
			self.pad_y = y
		

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

def main():
	parser = ArgumentParser(description="Advent of Code 2019 day 13!")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read()
	program = [int(x) for x in text.split(",")]
	
	##### Part 1: count the number of block tiles on the screen when the 
	##### program exits
	io_log = GatherArcadeOutput()
	arcade = Intcode(program, io=io_log)
	print(arcade.run())
	answer = len(io_log.drawn_tiles_history["block"])
	print("# of blocks on the screen = {}".format(answer))
	
	##### Just some test code to see the initial tiles with their positions
	# io_log = GatherArcadeOutput()
	# arcade = Intcode(program, io=io_log)
	# arcade.run()
	# print(io_log.drawn_tiles_history)
	# for tile_type, tile_set in io_log.drawn_tiles_history.items():
		# xs = [pos[0] for pos in tile_set]
		# ys = [pos[1] for pos in tile_set]
		
		# print(tile_type)
		# print("Maximum x = {}".format(max(xs)))
		# print("Minimum x = {}".format(min(xs)))
		# print("Maximum y = {}".format(max(ys)))
		# print("Minimum y = {}".format(min(ys)))
	
	##### Part 2: play the full game (with joystick and score). What is the
	##### score after the last block is broken?
	program[0] = 2
	io_virtual = ArcadeIO()
	arcade = Intcode(program, io=io_virtual)
	arcade.run()
	print("Final score is {}".format(io_virtual.score))
	# print("Ball position history:")
	# print(io_virtual.ball_history)

if __name__=="__main__":
	main()