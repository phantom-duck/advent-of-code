from argparse import ArgumentParser
import re
from dataclasses import dataclass
from typing import List, TypeVar

Interval = TypeVar("Interval")

@dataclass
class Interval:
	x_min: int
	x_max: int
	y_min: int
	y_max: int
	z_min: int
	z_max: int
	
	def volume(self):
		return (self.x_max - self.x_min + 1) * (self.y_max - self.y_min + 1) * (self.z_max - self.z_min + 1)
	
	def splitBy(self, i: Interval) -> List[Interval]:
		if i.x_max < self.x_min or i.x_min > self.x_max or i.y_max < self.y_min or i.y_min > self.y_max or i.z_max < self.z_min or i.z_min > self.z_max:
			return [self]
		
		i = Interval(max(self.x_min, i.x_min), min(self.x_max, i.x_max), max(self.y_min, i.y_min), min(self.y_max, i.y_max), max(self.z_min, i.z_min), min(self.z_max, i.z_max))
		
		ret = []
		for x_min, x_max in [(self.x_min, i.x_min - 1), (i.x_min, i.x_max), (i.x_max + 1, self.x_max)]:
			for y_min, y_max in [(self.y_min, i.y_min - 1), (i.y_min, i.y_max), (i.y_max + 1, self.y_max)]:
				for z_min, z_max in [(self.z_min, i.z_min - 1), (i.z_min, i.z_max), (i.z_max + 1, self.z_max)]:
					if all(c == ic for c, ic in zip([x_min, x_max, y_min, y_max, z_min, z_max], [i.x_min, i.x_max, i.y_min, i.y_max, i.z_min, i.z_max])):
						continue
					if x_min <= x_max and y_min <= y_max and z_min <= z_max:
						ret.append(Interval(x_min, x_max, y_min, y_max, z_min, z_max))
		
		return ret

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	text = text.splitlines()
	
	line_re = r"(?P<on_or_off>\w+) x=(?P<x_min>-?\d*)\.\.(?P<x_max>-?\d*),y=(?P<y_min>-?\d*)\.\.(?P<y_max>-?\d*),z=(?P<z_min>-?\d*)\.\.(?P<z_max>-?\d*)"
	line_re_compiled = re.compile(line_re)
	match_objects = [re.fullmatch(line_re_compiled, line) for line in text]
	reboot_steps = [(m.group("on_or_off"), int(m.group("x_min")), int(m.group("x_max")), int(m.group("y_min")), int(m.group("y_max")), int(m.group("z_min")), int(m.group("z_max"))) for m in match_objects]
	
	##### Part 1: Find how many cubes are on after all reboot steps
	##### Consider only cubes in the region x=-50..50,y=-50..50,z=-50..50
	cubes = [[["off" for _ in range(101)] for _ in range(101)] for _ in range(101)]
	for on_or_off, x_min, x_max, y_min, y_max, z_min, z_max in reboot_steps:
		if not (-50 <= x_min <= x_max <= 50 and -50 <= y_min <= y_max <= 50 and -50 <= z_min <= z_max <= 50):
			continue
		x_min = x_min + 50
		x_max = x_max + 50
		y_min = y_min + 50
		y_max = y_max + 50
		z_min = z_min + 50
		z_max = z_max + 50
		for x in range(x_min, x_max + 1):
			for y in range(y_min, y_max + 1):
				for z in range(z_min, z_max + 1):
					cubes[x][y][z] = on_or_off
	
	answer = sum(1 for x_section in cubes for xy_section in x_section for val in xy_section if val == "on")
	print("Part 1 answer = {}".format(answer))
	
	##### Part 2: the same, but now take into account all reboot steps
	##### (some of which are very large)
	reboot_insts = [(Interval(x_min, x_max, y_min, y_max, z_min, z_max), on_or_off) for on_or_off, x_min, x_max, y_min, y_max, z_min, z_max in reboot_steps]
	running_union = []
	answer = 0
	for interval, on_or_off in reversed(reboot_insts):
		cut_interval = [interval]
		for cutter_i in running_union:
			cut_interval = [i for cuttee_i in cut_interval for i in cuttee_i.splitBy(cutter_i)]
		extra_vol = sum(i.volume() for i in cut_interval)
		if on_or_off == "on":
			answer += extra_vol
		
		running_union.append(interval)
	print("Part 2 answer = {}".format(answer))


if __name__ == "__main__":
	main()