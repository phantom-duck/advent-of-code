import sys
# from pyparsing import Word, alphas, nums

def gcd(a, b):
	a = abs(a)
	b = abs(b)
	while a > 0 and b > 0:
		if a > b:
			a = a % b
		else:
			b = b % a
	return a + b

def sign(num):
	if num > 0:
		return 1
	elif num < 0:
		return -1
	else:
		return 0

class Planet:
	def __init__(self, x, y, z):
		self.pos = [x, y, z]
		self.vel = [0, 0, 0]
	
	def __repr__(self):
		return "pos=<x=" + str(self.pos[0]) + ", y=" + str(self.pos[1]) + ", z=" + str(self.pos[2]) + ">, " \
				"vel=<x=" + str(self.vel[0]) + ", y=" + str(self.vel[1]) + ", z=" + str(self.vel[2]) + ">"

def run_phase(planets):
	for p in planets:
		for p1 in planets:
			if p1 != p:
				pos_diff = [sign(pos1 - pos) for pos, pos1 in zip(p.pos, p1.pos)]
				p.vel = [v + diff for v, diff in zip(p.vel, pos_diff)]
	
	for p in planets:
		p.pos = [pos + vel for pos, vel in zip(p.pos, p.vel)]

def run_phase_single_coord(positions, velocities):
	for i in range(len(positions)):
		for j in range(len(positions)):
			if j != i:
				velocities[i] += sign(positions[j] - positions[i])
	
	for i in range(len(positions)):
		positions[i] += velocities[i]

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"
	
	with open(filename) as infile:
		text = infile.readlines()
	
	##### Part one
	planets = [Planet(16, -11, 2), Planet(0, -4, 7), Planet(6, 4, -10), Planet(-3, -2, -4)]
	for i in range(1000):
		run_phase(planets)
	
	energy = 0
	for planet in planets:
		pot = sum([abs(pos) for pos in planet.pos])
		kin = sum([abs(pos) for pos in planet.vel])
		energy += pot * kin
	print(energy)
	
	##### Part two
	planets = [Planet(16, -11, 2), Planet(0, -4, 7), Planet(6, 4, -10), Planet(-3, -2, -4)]
	period_x = period_y = period_z = 0
	flag_x = flag_y = flag_z = False
	while True:
		run_phase(planets)
		if not flag_x:
			flag_x = planets[0].pos[0]==16 and planets[1].pos[0]==0 and planets[2].pos[0]==6 and planets[3].pos[0]==-3 \
			and planets[0].vel[0] == planets[1].vel[0] == planets[2].vel[0] == planets[3].vel[0] == 0
			period_x += 1
		if not flag_y:
			flag_y = planets[0].pos[1]==-11 and planets[1].pos[1]==-4 and planets[2].pos[1]==4 and planets[3].pos[1]==-2 \
			and planets[0].vel[1] == planets[1].vel[1] == planets[2].vel[1] == planets[3].vel[1] == 0
			period_y += 1
		if not flag_z:
			flag_z = planets[0].pos[2]==2 and planets[1].pos[2]==7 and planets[2].pos[2]==-10 and planets[3].pos[2]==-4 \
			and planets[0].vel[2] == planets[1].vel[2] == planets[2].vel[2] == planets[3].vel[2] == 0
			period_z += 1
		
		if flag_x and flag_y and flag_z:
			break
	
	print(period_x, period_y, period_z)
	
	period = period_x * period_y // gcd(period_x, period_y)
	period = period * period_z // gcd(period, period_z)
	print(period)