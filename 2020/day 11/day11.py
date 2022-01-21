import sys
from pprint import pprint

def count_occupied_neighbours(seats, i, j):
	N = len(seats)
	M = len(seats[0])
	
	ret = 0
	if i > 0:
		if seats[i - 1][j] == '#':
			ret += 1
		if j > 0 and seats[i - 1][j - 1] == '#':
			ret += 1
		if j < M - 1 and seats[i - 1][j + 1] == '#':
			ret += 1
	if i < N - 1:
		if seats[i + 1][j] == '#':
			ret += 1
		if j > 0 and seats[i + 1][j - 1] == '#':
			ret += 1
		if j < M - 1 and seats[i + 1][j + 1] == '#':
			ret += 1
	if j > 0 and seats[i][j - 1] == '#':
		ret += 1
	if j < M - 1 and seats[i][j + 1] == '#':
		ret += 1
	
	return ret

def find_all_neighbours(seats):
	N = len(seats)
	M = len(seats[0])
	
	ret = [[set() for j in range(M)] for i in range(N)]
	
	## sweep rows
	for i in range(N):
		left = (i, 0)
		for j in range(1, M):
			if seats[i][j] != '.':
				ret[i][j].add(left)
				left = (i, j)
		right = (i, M - 1)
		for j in range(M - 2, -1, -1):
			if seats[i][j] != '.':
				ret[i][j].add(right)
				right = (i, j)
	
	## sweep columns
	for j in range(M):
		up = (0, j)
		for i in range(1, N):
			if seats[i][j] != '.':
				ret[i][j].add(up)
				up = (i, j)
		down = (N - 1, j)
		for i in range(N - 2, -1, -1):
			if seats[i][j] != '.':
				ret[i][j].add(down)
				down = (i, j)
	
	## sweep NW->SE diagonals
	j_start = 0
	for i_start in range(N):
		i, j = i_start + 1, j_start + 1
		UL = (i_start, j_start)
		while i < N and j < M:
			if seats[i][j] != '.':
				ret[i][j].add(UL)
				UL = (i, j)
			i += 1
			j += 1
	i_start = 0
	for j_start in range(M):
		i, j = i_start + 1, j_start + 1
		UL = (i_start, j_start)
		while i < N and j < M:
			if seats[i][j] != '.':
				ret[i][j].add(UL)
				UL = (i, j)
			i += 1
			j += 1
	
	j_start = M - 1
	for i_start in range(N):
		i, j = i_start - 1, j_start - 1
		DR = (i_start, j_start)
		while i >= 0 and j >= 0:
			if seats[i][j] != '.':
				ret[i][j].add(DR)
				DR = (i, j)
			i -= 1
			j -= 1
	i_start = N - 1
	for j_start in range(M):
		i, j = i_start - 1, j_start - 1
		DR = (i_start, j_start)
		while i >= 0 and j >= 0:
			if seats[i][j] != '.':
				ret[i][j].add(DR)
				DR = (i, j)
			i -= 1
			j -= 1
	
	## sweep SW->NE diagonals
	j_start = 0
	for i_start in range(N):
		i, j = i_start - 1, j_start + 1
		DL = (i_start, j_start)
		while i >= 0 and j < M:
			if seats[i][j] != '.':
				ret[i][j].add(DL)
				DL = (i, j)
			i -= 1
			j += 1
	
	i_start = 0
	for j_start in range(M):
		i, j = i_start + 1, j_start - 1
		UR = (i_start, j_start)
		while i < N and j >= 0:
			if seats[i][j] != '.':
				ret[i][j].add(UR)
				UR = (i, j)
			i += 1
			j -= 1
	
	j_start = M - 1
	for i_start in range(N):
		i, j = i_start + 1, j_start - 1
		UR = (i_start, j_start)
		while i < N and j >= 0:
			if seats[i][j] != '.':
				ret[i][j].add(UR)
				UR = (i, j)
			i += 1
			j -= 1
	
	i_start = N - 1
	for j_start in range(M):
		i, j = i_start - 1, j_start + 1
		DL = (i_start, j_start)
		while i >= 0 and j < M:
			if seats[i][j] != '.':
				ret[i][j].add(DL)
				DL = (i, j)
			i -= 1
			j += 1
	
	return ret

def count_occupied_neighbours2(seats, neighbours, i, j):
	ret = 0
	for ii, jj in neighbours[i][j]:
		if seats[ii][jj] == '#':
			ret += 1
	return ret

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read().split()
	
	seat_map = text
	N = len(seat_map)
	M = len(seat_map[0])
	
	##### Part 1: apply the rules by which seats get occupied and unoccupied
	##### again and again (simultaneously for all seats at each step), until
	##### no further changes take place.
	
	prev_seats = [list(row) for row in seat_map]
	# pprint(prev_seats)
	next_seats = [M * ['0'] for i in range(N)]
	# pprint(next_seats)
	while True:
		flag_nochange = True
		for i in range(N):
			for j in range(M):
				if prev_seats[i][j] == 'L' and count_occupied_neighbours(prev_seats, i, j) == 0:
					flag_nochange = False
					next_seats[i][j] = '#'
				elif prev_seats[i][j] == '#' and count_occupied_neighbours(prev_seats, i, j) >= 4:
					flag_nochange = False
					next_seats[i][j] = 'L'
				else:
					next_seats[i][j] = prev_seats[i][j]
		
		if flag_nochange:
			break
		
		# pprint(next_seats)
		# print()
		
		tmp = prev_seats
		prev_seats = next_seats
		next_seats = tmp
		
	
	final_seat_map = next_seats
	occupied = 0
	for row in final_seat_map:
		for seat in row:
			if seat == '#':
				occupied += 1
	
	print(occupied)
	
	
	##### Part 2: same as before, but now the rules for each seat apply to the
	##### first seat that it can "see" in each of the 8 possible directions.
	
	neighbours = find_all_neighbours(seat_map)
	# pprint(seat_map)
	# pprint(neighbours[0])
	
	prev_seats = [list(row) for row in seat_map]
	# pprint(prev_seats)
	next_seats = [M * ['0'] for i in range(N)]
	# pprint(next_seats)
	while True:
		flag_nochange = True
		for i in range(N):
			for j in range(M):
				if prev_seats[i][j] == 'L' and count_occupied_neighbours2(prev_seats, neighbours, i, j) == 0:
					flag_nochange = False
					next_seats[i][j] = '#'
				elif prev_seats[i][j] == '#' and count_occupied_neighbours2(prev_seats, neighbours, i, j) >= 5:
					flag_nochange = False
					next_seats[i][j] = 'L'
				else:
					next_seats[i][j] = prev_seats[i][j]
		
		if flag_nochange:
			break
		
		# pprint(next_seats)
		# print()
		
		tmp = prev_seats
		prev_seats = next_seats
		next_seats = tmp
		
	
	final_seat_map = next_seats
	occupied = 0
	for row in final_seat_map:
		for seat in row:
			if seat == '#':
				occupied += 1
	
	print(occupied)