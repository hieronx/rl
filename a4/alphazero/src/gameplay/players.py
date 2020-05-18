from math import inf as infinity

import numpy as np

from alphazero.src.mcts import MCTS


class Player(object):
	def __init__(self):
		super(Player, self).__init__()

	def get_action(self, game):
		pass

class RandomPlayer(Player):
	def __init__(self):
		super(RandomPlayer, self).__init__()

	def get_action(self, game):
		possible_actions = np.nonzero(game.get_possible_actions())[0]

		return np.random.choice(possible_actions)

class AlphaZeroPlayer(Player):
	def __init__(self, nn, mcts):
		super(AlphaZeroPlayer, self).__init__()
		self.mcts = mcts
		self.nn = nn

	def get_action(self, game):
		action_probs = self.mcts.simulate(game, self.nn)
		action = np.argmax(action_probs)
		# print(action_probs)
		return action

	def get_action_for_board(self, game, board, time_limit=None):
		game.set_board(board)
		action_probs = self.mcts.simulate(game, self.nn, time_limit=time_limit)
		action = np.argmax(action_probs)
		return action

	def get_nn(self):
		return self.nn

class HumanPlayer(Player):
	def __init__(self):
		super(HumanPlayer, self).__init__()

	def get_action(self, game):
		possible_actions = np.nonzero(game.get_possible_actions())[0]
		
		action = input ("Enter an action:")
		action = int(action)
		
		while action not in possible_actions:
			action = input ("Invalid action. Enter an action:")
			action = int(action)

		return action
