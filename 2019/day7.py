import sys
from typing import List
import itertools

class Helper:
	@staticmethod
	def get_pars(program, ip, parameter_modes, cnt) -> list:
		pars = []
		for i in range(cnt):
			mode = parameter_modes % 10
			parameter_modes //= 10
			if mode==0:
				pars.append(program[program[ip+i+1]])
			else:
				pars.append(program[ip+i+1])
		return pars

class IOstream:
	def __init__(self):
		self.out_stream = []
		self.in_stream = []
	
	def read(self):
		if len(self.in_stream) == 0:
			# print("Tried to read from empty input stream!")
			return -1
		return self.in_stream.pop(0)
	
	def write(self, a):
		self.out_stream.append(a)
	
	def give_input(self, a):
		self.in_stream.append(a)
	
	def get_output(self):
		if len(self.out_stream) == 0:
			print("Tried get_output with no output!")
			raise Exception
		return self.out_stream.pop(0)

class Intcode:
	def __init__(self, code=None):
		if isinstance(code, str):
			self.init_code_fromCSV(code)
		elif isinstance(code, list):
			self.init_code(code)
		else:
			self.program = None
		
		self.ip = 0
		self.io = IOstream()
	
	def init_code(self, code: List[int]):
		self.program = code.copy()
	
	def init_code_fromCSV(self, code: str):
		self.program = list(map(lambda x: int(x), code.split(",")))
	
	def run(self):
		program = self.program
		while True:
			ip = self.ip
			opcode = program[ip] % 100
			parameter_modes = program[ip] // 100
			
			if opcode==99:
				# Instruction: Halt
				# print("Program has ended.")
				return 0
			elif opcode==1:
				# Instruction: Add first and second parameter, place result in third
				pars = Helper.get_pars(program, ip, parameter_modes, 2)
				program[program[ip+3]] = pars[0] + pars[1]
				self.ip += 4
			elif opcode==2:
				# Instruction: Multiply first and second parameter, place result in third
				pars = Helper.get_pars(program, ip, parameter_modes, 2)
				program[program[ip+3]] = pars[0] * pars[1]
				self.ip += 4
			elif opcode==3:
				# Instruction: Takes a single integer as input, saves it at the position given by the parameter
				val = self.io.read()
				if val < 0:
					return -1
				else:
					program[program[ip+1]] = val
					self.ip += 2
			elif opcode==4:
				# Instruction: Outputs the value of its only parameter
				pars = Helper.get_pars(program, ip, parameter_modes, 1)
				self.io.write(pars[0])
				self.ip += 2
			elif opcode==5:
				# Instruction: jump if true
				# print("jump-if-true: par1 =", program[ip+1], "par2 =", program[ip+2], "par3 =", program[ip+3])
				pars = Helper.get_pars(program, ip, parameter_modes, 2)
				if pars[0] != 0:
					self.ip = pars[1]
				else:
					self.ip += 3
			elif opcode==6:
				# Instruction: jump if false
				# print("jump-if-false: par1 =", program[ip+1], "par2 =", program[ip+2], "par3 =", program[ip+3])
				pars = Helper.get_pars(program, ip, parameter_modes, 2)
				if pars[0] == 0:
					self.ip = pars[1]
				else:
					self.ip += 3
			elif opcode==7:
				# Instruction: less than
				# print("less than: par1 =", program[ip+1], "par2 =", program[ip+2])
				pars = Helper.get_pars(program, ip, parameter_modes, 2)
				if pars[0] < pars[1]:
					program[program[ip+3]] = 1
				else:
					program[program[ip+3]] = 0
				self.ip += 4
			elif opcode==8:
				# Instruction: equals
				# print("equals: par1 =", program[ip+1], "par2 =", program[ip+2])
				pars = Helper.get_pars(program, ip, parameter_modes, 2)
				if pars[0] == pars[1]:
					program[program[ip+3]] = 1
				else:
					program[program[ip+3]] = 0
				self.ip += 4
			else:
				print("Unknown Opcode:", opcode, "Something went wrong...")
				break
	
	def code2readable(self):
		program = self.program
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
			else:
				print("Unknown Opcode:", opcode, "Something went wrong...")
				break
		return ret

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"
	
	with open(filename) as infile:
		text = infile.read()
	
	##### Part One
	# max = 0
	# for phases in itertools.permutations([0,1,2,3,4]):
		# amps = [Intcode(text) for i in range(5)]
		# input = 0
		# for i in range(5):
			# amps[i].io.give_input(phases[i])
			# amps[i].io.give_input(input)
			# amps[i].run()
			# input = amps[i].io.get_output()
		# output = input
		# if output > max:
			# max = output
			# max_perm = phases

	# print(max, max_perm)
	
	##### Part two
	max = 0
	for phases in itertools.permutations([5,6,7,8,9]):
		amps = [Intcode(text) for i in range(5)]
		for i in range(5):
			amps[i].io.give_input(phases[i])
		input = 0
		i = 0
		while True:
			amps[i].io.give_input(input)
			ret = amps[i].run()
			if ret == 0 and i == 4:
				output = amps[i].io.get_output()
				break
			input = amps[i].io.get_output()
			i = (i + 1) % 5
		if output > max:
			max = output
			max_perm = phases
	
	print(max, max_perm)
		
		
	
	
	# disassembly
	# code = Intcode_obj.code2readable()
	# for (pos, command) in code:
		# print(pos, "|", command)
	
	
