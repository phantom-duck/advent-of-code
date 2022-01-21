from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Optional, List

ROTATIONS = [[[1, 0, 0],
			[0, 1, 0],
			[0, 0, 1]],
			[[1, 0, 0],
			[0, -1, 0],
			[0, 0, -1]],
			[[1, 0, 0],
			[0, 0, 1],
			[0, -1, 0]],
			[[1, 0, 0],
			[0, 0, -1],
			[0, 1, 0]],
			[[-1, 0, 0],
			[0, 1, 0],
			[0, 0, -1]],
			[[-1, 0, 0],
			[0, -1, 0],
			[0, 0, 1]],
			[[-1, 0, 0],
			[0, 0, 1],
			[0, 1, 0]],
			[[-1, 0, 0],
			[0, 0, -1],
			[0, -1, 0]],
			[[0, 1, 0],
			[-1, 0, 0],
			[0, 0, 1]],
			[[0, 1, 0],
			[1, 0, 0],
			[0, 0, -1]],
			[[0, 1, 0],
			[0, 0, 1],
			[1, 0, 0]],
			[[0, 1, 0],
			[0, 0, -1],
			[-1, 0, 0]],
			[[0, -1, 0],
			[0, 0, -1],
			[1, 0, 0]],
			[[0, -1, 0],
			[0, 0, 1],
			[-1, 0, 0]],
			[[0, -1, 0],
			[1, 0, 0],
			[0, 0, 1]],
			[[0, -1, 0],
			[-1, 0, 0],
			[0, 0, -1]],
			[[0, 0, 1],
			[1, 0, 0],
			[0, 1, 0]],
			[[0, 0, 1],
			[-1, 0, 0],
			[0, -1, 0]],
			[[0, 0, 1],
			[0, 1, 0],
			[-1, 0, 0]],
			[[0, 0, 1],
			[0, -1, 0],
			[1, 0, 0]],
			[[0, 0, -1],
			[-1, 0, 0],
			[0, 1, 0]],
			[[0, 0, -1],
			[1, 0, 0],
			[0, -1, 0]],
			[[0, 0, -1],
			[0, 1, 0],
			[1, 0, 0]],
			[[0, 0, -1],
			[0, -1, 0],
			[-1, 0, 0]]
			]

@dataclass(frozen=True)
class Vector:
	x: int
	y: int
	z: int
	
	def __add__(self, v):
		return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
	
	def __sub__(self, v):
		return Vector(self.x - v.x, self.y - v.y, self.z - v.z)
	
	def inner(self, v):
		return self.x*v.x + self.y*v.y + self.z*v.z
	
	def rotate(self, rotation):
		return Point(self.inner(rotation[0]), self.inner(rotation[1]), self.inner(rotation[2]))

@dataclass
class Scanner:
	beacon_list: List[Vector]
	
	def match(self, scanner):
		for v1 in self.beacon_list:
			for v2 in scanner.beacon_list:
				v1_relatives = {x - v1 for x in self.beacon_list}
				v2_relatives = {x - v2 for x in scanner.beacon_list}
				for rotation in ROTATIONS:
					v2_relatives_rotated = {x.rotate(rotation) for x in v2_relatives}
					if len(v1_relatives & v2_relatives_rotated) >= 12:
						return ...
		return None


def rotate(point, rotation):
	def dot(v1, v2):
		return sum(x*y for x, y in zip(v1, v2))
	
	return tuple(dot(row, point) for row in rotation)

def match_scanners(scanner1_measurements, scanner2_measurements):
	for p1x, p1y, p1z in scanner1_measurements:
		for p2x, p2y, p2z in scanner2_measurements:
			pivot1_relatives = {(x - p1x, y - p1y, z - p1z) for x, y, z in scanner1_measurements}
			pivot2_relatives = {(x - p2x, y - p2y, z - p2z) for x, y, z in scanner2_measurements}
			for rotation in ROTATIONS:
				pivot2_relatives_rotated = {rotate(point, rotation) for point in pivot2_relatives}
				# print(len(pivot1_relatives & pivot2_relatives_rotated))
				if len(pivot1_relatives & pivot2_relatives_rotated) >= 12:
					p2xx, p2yy, p2zz = rotate((p2x, p2y, p2z), rotation)
					displacement = (p1x - p2xx, p1y - p2yy, p1z - p2zz)
					return displacement, rotation
	print("NO")
	return False

def parse_input(text:str):
	text = text.split("\n\n")
	scanners_measurements = [[tuple(map(int, line.split(","))) for line in scanner_text.splitlines()[1:]] for scanner_text in text]
	return scanners_measurements

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	
	text = text.split("\n\n")
	scanners_measurements = [[tuple(map(int, line.split(","))) for line in scanner_text.splitlines()[1:]] for scanner_text in text]
	
	##### Part 1: assemble the full map of beacons. How many beacons are there?
	scanners_done = [scanners_measurements[0]]
	rotations = [ROTATIONS[0]]
	displacements = [(0, 0, 0)]
	scanners_not_done = scanners_measurements[1:]
	i = 0
	while scanners_not_done:
		print(len(scanners_not_done))
		reference_scanner = scanners_done[i]
		matches = [(candidate_scanner, match_scanners(reference_scanner, candidate_scanner)) for candidate_scanner in scanners_not_done]
		matches_success = [(c, m) for c, m in matches if m is not False]
		for c, m in matches_success:
			(d_x, d_y, d_z), rotation = m
			points_rotated = [rotate(point, rotation) for point in c]
			scanners_done.append([(d_x + x, d_y + y, d_z + z) for x, y, z in points_rotated])
			rotations.append(rotation)
			displacements.append((d_x, d_y, d_z))
		# matches_failures = [(c, m) for c, m in matches if m is False]
		scanners_not_done = [c for c, m in matches if m is False]
		i = (i + 1) % len(scanners_done)
	
	print(len({beacon for scanner in scanners_done for beacon in scanner}))
	
	##### Part 2: find the maximum Manhattan distance between any two scanners.
	##### We will use the scanners found from part 1.
	answer = max(sum(abs(coord1 - coord2) for coord1, coord2 in zip(d1, d2)) for d1 in displacements for d2 in displacements)
	print("Part 2 answer = {}".format(answer))


if __name__ == "__main__":
	main()