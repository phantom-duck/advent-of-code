import sys
from pprint import pprint




if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.readlines()
	
	program = [line.split() for line in text]
	
	##### Part 1: value of accumulator immediately before any instruction is executed twice
	
	pc = 0
	accumulator = 0
	instructions_run = set()
	while True:
		if pc in instructions_run:
			break
		instructions_run.add(pc)
		
		command = program[pc][0]
		argument = int(program[pc][1])
		
		next_pc = pc + 1
		
		if command == "acc":
			accumulator += argument
		elif command == "jmp":
			next_pc = pc + argument
		elif command == "nop":
			pass
		
		pc = next_pc
	
	print(accumulator)
	
	##### Part 2: change exactly one command of "jmp" or "nop" to "nop" or "jmp", respectively,
	##### so that the program terminates. Output the final value of the accumulator.
	
	for i, instruction in enumerate(program[:]):
		if instruction[0] == "acc":
			continue
		elif instruction[0] == "jmp":
			program[i][0] = "nop"
		elif instruction[0] == "nop":
			program[i][0] = "jmp"
		
		pc = 0
		accumulator = 0
		instructions_run = set()
		while pc < len(program):
			if pc in instructions_run:
				break
			instructions_run.add(pc)
			
			command = program[pc][0]
			argument = int(program[pc][1])
			
			next_pc = pc + 1
			
			if command == "acc":
				accumulator += argument
			elif command == "jmp":
				next_pc = pc + argument
			elif command == "nop":
				pass
			
			pc = next_pc
		
		if pc >= len(program):
			break
		
		if instruction[0] == "jmp":
			program[i][0] = "nop"
		elif instruction[0] == "nop":
			program[i][0] = "jmp"
	
	print(accumulator)