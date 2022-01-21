import sys
from pprint import pprint

def gcd(a, b):
	if a == 0 or b == 0:
		return a + b
	
	return gcd(b, a % b)

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.readlines()
	
	my_timestamp = int(text[0])
	periods = [int(x) for x in text[1].split(",") if x != 'x']
	
	##### Part 1: find earliest available bus, output product of
	##### time we will have to wait and bus id (=bus period)
	
	min_value = periods[0] - my_timestamp % periods[0]
	min_bus = periods[0]
	for p in periods:
		if p - my_timestamp % p < min_value:
			min_bus = p
			min_value = p - my_timestamp % p
	
	print(min_bus)
	print(min_value)
	print(min_bus * min_value)
	
	##### Part 2: find minimum timestamp t such that the buses
	##### depart, starting from t, at the exact times dictated by the input
	
	t_start = 0
	t_period = 1
	for i, p in enumerate(text[1].split(",")):
		if p == 'x':
			continue
		
		pp = int(p)
		t = t_start
		while True:
			if (t + i) % pp == 0:
				t_start = t
				t_period *= pp
				break
			t += t_period
	
	print(t)