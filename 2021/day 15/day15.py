from argparse import ArgumentParser
from heapq import heappush, heappop
from math import inf as INFINITY

def get_neighbours(i, j, n, m):
	if i > 0:
		yield (i - 1, j)
	if i < n - 1:
		yield (i + 1, j)
	if j > 0:
		yield (i, j - 1)
	if j < m - 1:
		yield (i, j + 1)

def dijkstra(risk_map, start_x, start_y):
	n = len(risk_map)
	m = len(risk_map[0])
	distances_from_source = [[INFINITY] * m for _ in range(n)]
	explored = set()
	
	distances_from_source[start_x][start_y] = 0
	search_front = [(0, (start_x, start_y))]
	while search_front:
		dist, (u_i, u_j) = heappop(search_front)
		if (u_i, u_j) in explored:
			continue
		explored.add((u_i, u_j))
		for v_i, v_j in get_neighbours(u_i, u_j, n, m):
			if dist + risk_map[v_i][v_j] < distances_from_source[v_i][v_j]:
				distances_from_source[v_i][v_j] = dist + risk_map[v_i][v_j]
				heappush(search_front, (distances_from_source[v_i][v_j], (v_i, v_j)))
	
	return distances_from_source

def repeat_sequence(row: list, times: int, modulus: int) -> list:
	n = len(row)
	addant = [i for i in range(times) for _ in range(n)]
	return [(x + y - 1) % (modulus - 1) + 1 for x, y in zip(row * times, addant)]

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	text = text.splitlines()
	
	risk_map = [[int(risk) for risk in line] for line in text]
	
	##### Part 1: calculate lowest total risk of a path from the top left
	##### to the bottom right
	distances_from_source = dijkstra(risk_map, 0, 0)
	answer = distances_from_source[-1][-1]
	print("Part 1: lowest possible risk is {}".format(answer))
	
	##### Part 2: repeat the risk map five times to the right and down, each
	##### time raising the risks by one (with 10 wrapping back to 0). What we
	##### want is the lowest total risk in this map.
	REPEAT_RIGHT = 5
	REPEAT_DOWN = 5
	MODULUS = 10
	
	risk_map_extend_right = [repeat_sequence(row, REPEAT_RIGHT, MODULUS) for row in risk_map]
	risk_map_new_transpose = [repeat_sequence(col, REPEAT_DOWN, MODULUS) for col in zip(*risk_map_extend_right)]
	
	# does not matter if original or traspose for lowest risk value
	distances_from_source = dijkstra(risk_map_new_transpose, 0, 0)
	answer = distances_from_source[-1][-1]
	print("Part 2: lowest possible risk is {}".format(answer))


if __name__ == "__main__":
	main()