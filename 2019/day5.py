import sys
from typing import List

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

def Intcode_run(program: List[int]):
	ip = 0
	while True:
		opcode = program[ip] % 100
		parameter_modes = program[ip] // 100
		
		if opcode==99:
			# Instruction: Halt
			# print("Program has ended.")
			break
		elif opcode==1:
			# Instruction: Add first and second parameter, place result in third
			pars = get_pars(program, ip, parameter_modes, 2)
			program[program[ip+3]] = pars[0] + pars[1]
			ip += 4
		elif opcode==2:
			# Instruction: Multiply first and second parameter, place result in third
			pars = get_pars(program, ip, parameter_modes, 2)
			program[program[ip+3]] = pars[0] * pars[1]
			ip += 4
		elif opcode==3:
			# Instruction: Takes a single integer as input, saves it at the position given by the parameter
			print("(input)")
			program[program[ip+1]] = int(input())
			ip += 2
		elif opcode==4:
			# Instruction: Outputs the value of its only parameter
			pars = get_pars(program, ip, parameter_modes, 1)
			print(pars[0])
			ip += 2
		elif opcode==5:
			# Instruction: jump if true
			# print("jump-if-true: par1 =", program[ip+1], "par2 =", program[ip+2], "par3 =", program[ip+3])
			pars = get_pars(program, ip, parameter_modes, 2)
			if pars[0] != 0:
				ip = pars[1]
			else:
				ip += 3
		elif opcode==6:
			# Instruction: jump if false
			# print("jump-if-false: par1 =", program[ip+1], "par2 =", program[ip+2], "par3 =", program[ip+3])
			pars = get_pars(program, ip, parameter_modes, 2)
			if pars[0] == 0:
				ip = pars[1]
			else:
				ip += 3
		elif opcode==7:
			# Instruction: less than
			# print("less than: par1 =", program[ip+1], "par2 =", program[ip+2])
			pars = get_pars(program, ip, parameter_modes, 2)
			if pars[0] < pars[1]:
				program[program[ip+3]] = 1
			else:
				program[program[ip+3]] = 0
			ip += 4
		elif opcode==8:
			# Instruction: equals
			# print("equals: par1 =", program[ip+1], "par2 =", program[ip+2])
			pars = get_pars(program, ip, parameter_modes, 2)
			if pars[0] == pars[1]:
				program[program[ip+3]] = 1
			else:
				program[program[ip+3]] = 0
			ip += 4
		else:
			print("Unknown Opcode:", opcode, "Something went wrong...")
			break
	

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"
	
	with open(filename) as infile:
		text = infile.read()
	text = text.split(",")
	program = list(map(lambda x: int(x), text))
	
	Intcode_run(program)
	print("Program has ended")
	
	
