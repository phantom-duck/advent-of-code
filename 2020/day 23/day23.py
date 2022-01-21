def run_rounds(circle, T=100):
	N = len(circle)
	max_num = max(circle)
	min_num = min(circle)
	
	for _ in range(T):
		current_cup = circle.pop(0)
		x, y, z = circle.pop(0), circle.pop(0), circle.pop(0)
		
		if current_cup == min_num:
			destination = max_num
		else:
			destination = current_cup - 1
		while destination not in circle:
			if destination == min_num:
				destination = max_num
			else:
				destination -= 1
		
		circle.insert(circle.index(destination) + 1, z)
		circle.insert(circle.index(destination) + 1, y)
		circle.insert(circle.index(destination) + 1, x)
		
		circle.append(current_cup)
	
	i_1 = circle.index(1)
	ret = []
	for i in range(1, N):
		ret.append(circle[(i_1 + i) % N])
	
	return ret

print(run_rounds([3,1,8,9,4,6,5,7,2]))
