import sys
from pprint import pprint
import re

def playcombat(player1, player2):
	while len(player1) > 0 and len(player2) > 0:
		if player1[0] > player2[0]:
			first1 = player1.pop(0)
			first2 = player2.pop(0)
			player1.append(first1)
			player1.append(first2)
		else:
			first1 = player1.pop(0)
			first2 = player2.pop(0)
			player2.append(first2)
			player2.append(first1)
	
	if len(player1) > 0:
		print("Part 1, player 1")
		return player1
	else:
		print("Part 1, player 2")
		return player2

total_rounds = 0
total_subgames = 0
def playrecursivecombat(player1, player2, return_flag=False):
	global total_rounds
	global total_subgames
	
	total_subgames += 1

	seen_configurations = set()
	player1_win = False
	while len(player1) > 0 and len(player2) > 0:
		total_rounds += 1
		# print("-------------------------------")
		# print(player1)
		# print(player2)
		# print("-------------------------------")
		configuration_string = ''.join(str(x) for x in player1 + ["|"] + player2)
		if configuration_string in seen_configurations:
			player1_win = True
			break
		else:
			seen_configurations.add(configuration_string)
		
		first1 = player1.pop(0)
		first2 = player2.pop(0)
		if len(player1) < first1 or len(player2) < first2:
			if first1 > first2:
				player1.append(first1)
				player1.append(first2)
			else:
				player2.append(first2)
				player2.append(first1)
		else:
			# print("--------------Recursive game------------------")
			# print([first1] + player1)
			# print([first2] + player2)
			# print(player1[:first1])
			# print(player2[:first2])
			# print("----------------------------------------------")
			if playrecursivecombat(player1[:first1], player2[:first2]):
				player1.append(first1)
				player1.append(first2)
			else:
				player2.append(first2)
				player2.append(first1)
	
	if player1_win or len(player1) > 0:
		if return_flag:
			return True, player1
		else:
			return True
	else:
		if return_flag:
			return False, player2
		else:
			return False

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read().split("\n\n")
	
	player1 = [int(x) for x in text[0].split(":")[1].split()]
	player2 = [int(x) for x in text[1].split(":")[1].split()]
	
	# p = player1 + player2
	# p.sort()
	# print(p)
	# print(player1)
	# print(player2)
	
	##### Part 1: play rounds of Combat until one player runs out of cards.
	##### Output the winnig player's "score", as described in the problem
	
	winner = playcombat(player1[:], player2[:])
	winner.reverse()
	
	total = 0
	for i, card in enumerate(winner):
		total += (i + 1) * card
	
	print(total)
	
	##### Part 2: the same, but for recursive Combat
	
	print(player1)
	print(player2)
	
	winbool, winner = playrecursivecombat(player1, player2, True)
	# print(winner)
	# print(winbool)
	winner.reverse()
	
	total = 0
	for i, card in enumerate(winner):
		total += (i + 1) * card
	
	print(total)
	print(total_rounds)
	print(total_subgames)
