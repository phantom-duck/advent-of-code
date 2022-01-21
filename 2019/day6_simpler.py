import sys

def extract_pair(line: str) -> (str, str):
	return tuple(line.replace("\n", "").split(")"))

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"
	
	with open(filename) as infile:
		text = infile.readlines()
	
	pairs = [extract_pair(line) for line in text]
	
	parents = dict()
	for (parent, child) in pairs:
		parents[child] = parent
	
	##### first half
	
	sum = 0
	for key in parents:
		cnt = 0
		curr_node = key
		while curr_node != "COM":
			cnt += 1
			curr_node = parents[curr_node]
		sum += cnt
	# print(sum)
	
	##### second half
	
	ancestors_YOU = []
	curr_node = "YOU"
	length = 0
	while (curr_node != "COM"):
		ancestors_YOU.append((curr_node, length))
		curr_node = parents[curr_node]
		length += 1
	ancestors_YOU.append(("COM", length))
	
	ancestors_SAN = []
	curr_node = "SAN"
	length = 0
	while (curr_node != "COM"):
		ancestors_SAN.append((curr_node, length))
		curr_node = parents[curr_node]
		length += 1
	ancestors_SAN.append(("COM", length))
	
	ancestors_YOU.reverse()
	ancestors_SAN.reverse()
	# print(parents)
	# print(ancestors_YOU)
	# print(ancestors_SAN)
	
	prev_len = ancestors_SAN[0][1] + ancestors_YOU[0][1]
	for ((YOU_anc, YOU_len),(SAN_anc, SAN_len)) in zip(ancestors_YOU, ancestors_SAN):
		if YOU_anc != SAN_anc:
			print(prev_len)
			break
		else:
			prev_len = YOU_len + SAN_len
	