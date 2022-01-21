def Intcode_run(program):
	ip = 0
	while True:
		opcode = program[ip]
		if opcode==99:
			# print("Program has ended.")
			break
		elif opcode==1:
			program[program[ip+3]] = program[program[ip+1]] + program[program[ip+2]]
		elif opcode==2:
			program[program[ip+3]] = program[program[ip+1]] * program[program[ip+2]]
		else:
			print("Something went wrong...")
			break
		ip = ip + 4

if __name__=="__main__":
	with open("day_2_input.txt") as infile:
		text = infile.read()
	text = text.split(",")

	program = list(map(lambda x: int(x), text))
	
	for i in range(100):
		for j in range(100):
			temp_prog = program.copy()
			
			# program[1]: noun, program[2]: verb
			temp_prog[1] = i
			temp_prog[2] = j
			Intcode_run(temp_prog)
			if temp_prog[0] == 19690720:
				print("noun is:", temp_prog[1], "verb is:", temp_prog[2])
	
	
