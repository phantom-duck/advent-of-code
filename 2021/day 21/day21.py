from argparse import ArgumentParser
from dataclasses import dataclass
from abc import ABC, abstractmethod
import itertools

SPACES_NUMBER = 10

@dataclass
class Player:
	position: int = 0
	score: int = 0
	
	def move(self, roll_total: int) -> None:
		self.position = (self.position + roll_total) % SPACES_NUMBER
		self.score += self.position + 1

class Die(ABC):
	@abstractmethod
	def roll(self) -> int:
		pass

class DeterministicDie(Die):
	sides = 100
	
	def __init__(self):
		self.value_to_roll = 1
		self.times_rolled = 0
	
	def roll(self) -> int:
		ret = self.value_to_roll
		self.value_to_roll = self.value_to_roll % self.sides + 1
		self.times_rolled += 1
		return ret

class Game:
	def __init__(self, die: Die):
		self.players = (Player(position=7), Player(position=1))
		self.curr_player = 0
		self.die = die
	
	def play_round(self):
		roll1, roll2, roll3 = self.die.roll(), self.die.roll(), self.die.roll()
		self.players[self.curr_player].move(roll1 + roll2 + roll3)
		
		# print("Player {} rolls {}+{}+{} and moves to space {} for a total score of {}".format(
			# self.curr_player, 
			# roll1, 
			# roll2, 
			# roll3, 
			# self.players[self.curr_player].position,
			# self.players[self.curr_player].score)
			# )
		
		self.curr_player = (self.curr_player + 1) % 2
	
	def has_finished(self):
		return any(p.score >= 1000 for p in self.players)
	
	def get_scores(self):
		return [p.score for p in self.players]

def main():
	parser = ArgumentParser(description="Advent of Code day 1")
	parser.add_argument("infile", help="input file name")
	args = parser.parse_args()
	
	with open(args.infile) as infile:
		text = infile.read().strip()
	text = text.splitlines()
	
	player1startingpos = int(text[0].split()[4])
	player2startingpos = int(text[1].split()[4])
	
	##### Part 1: Play a practice game, with a deterministic 100-sided die
	##### and multiply the score of the losing player by the number of times
	##### the die was rolled during the game.
	d = DeterministicDie()
	g = Game(die = d)
	while not g.has_finished():
		g.play_round()
	
	print(g.get_scores())
	losing_score = [s for s in g.get_scores() if s < 1000][0]
	times_rolled = d.times_rolled
	print("Part 1: {}x{} = {}".format(losing_score, times_rolled, losing_score * times_rolled))
	
	##### Part 2: play the game with a Dirac dice: branch on all possible die
	##### results, and find out the player that wins the largest number of all
	##### possible games
	game_states_numbers1 = [[[[0 for player2score in range(21)] for player1score in range(21)] for player2pos in range(10)] for player1pos in range(10)]
	game_states_numbers2 = [[[[0 for player2score in range(21)] for player1score in range(21)] for player2pos in range(10)] for player1pos in range(10)]
	
	game_states_numbers1[player1startingpos - 1][player2startingpos - 1][0][0] = 1
	games1win = games2win = 0
	finished = False
	while not finished:
		finished = True
		for player1pos, row1 in enumerate(game_states_numbers1):
			for player2pos, row2 in enumerate(row1):
				for player1score, row3 in enumerate(row2):
					for player2score, games_number in enumerate(row3):
						if games_number == 0:
							continue
						
						finished = False
						for roll1, roll2, roll3 in itertools.product([1,2,3], [1,2,3], [1,2,3]):
							new_player1pos = (player1pos + roll1 + roll2 + roll3) % 10
							new_player1score = player1score + new_player1pos + 1
							if new_player1score > 20:
								games1win += games_number
							else:
								game_states_numbers2[new_player1pos][player2pos][new_player1score][player2score] += games_number
						
						game_states_numbers1[player1pos][player2pos][player1score][player2score] = 0
		
		for player1pos, row1 in enumerate(game_states_numbers2):
			for player2pos, row2 in enumerate(row1):
				for player1score, row3 in enumerate(row2):
					for player2score, games_number in enumerate(row3):
						if games_number == 0:
							continue
						
						finished = False
						for roll1, roll2, roll3 in itertools.product([1,2,3], [1,2,3], [1,2,3]):
							new_player2pos = (player2pos + roll1 + roll2 + roll3) % 10
							new_player2score = player2score + new_player2pos + 1
							if new_player2score > 20:
								games2win += games_number
							else:
								game_states_numbers1[player1pos][new_player2pos][player1score][new_player2score] += games_number
						
						game_states_numbers2[player1pos][player2pos][player1score][player2score] = 0
		
	print("Part 2")
	print(games1win)
	print(games2win)


if __name__ == "__main__":
	main()