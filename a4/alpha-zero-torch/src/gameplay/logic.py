from math import inf as infinity

import numpy as np

from src.mcts import MCTS
from src.utils import progressbar


def play_game(game, p1, p2, print_b = False):
	game.reset()
	winner = None
	current_player = p1 

	while winner == None:
		action = current_player.get_action(game)
		game.play(action)
		winner = game.check_winner()
		current_player = p2 if current_player == p1 else p1
		
		if print_b:
			game.print_board()

	return winner*game.get_player()

def player_vs_player(game, p1, p2, n_games = 10, treshold = 0.5, print_b = False): 
	draws = 0
	wins_p1 = 0
	for i in progressbar(range(n_games), desc="Playing"):
		print("Game: {}/{}".format(i,n_games))
		winner = play_game(game = game, p1 = p1, p2 = p2, print_b = print_b) #todo: we should probabily vary who plays first, some games are biased torwards first players
		if winner == 0:
			draws += 1
		elif winner == 1:
			wins_p1 +=1

	print("Player 1 won:{}%, lost:{}%, drew:{}%".format(wins_p1, n_games - wins_p1 - draws, draws))

	winner_model = p1 if wins_p1/n_games > treshold else p2

	return winner
