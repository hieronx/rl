import numpy as np

from alphazero.src.games.game import Game
from alphazero.src.utils.hexboard import HexBoard


class Hex(Game):
	def __init__(self,  player = 1, history = None, probs = None,  **params):
		self.params = params
		self.board_size = params['board_size']
		self.board = HexBoard(params['board_size'][0])
		self.player = player
		self.history = history or []
		self.probs = probs or []

	def set_board(self, board):
		raise NotImplementedError

	def reset(self):
		self.player = 1
		self.board = HexBoard(self.board_size[0])

	def new_game(self):
		return Hex(**self.params)

	def get_action_size(self):
		return self.board_size[0] * self.board_size[1]

	def get_board_dimensions(self):
		return self.board_size

	def get_input_planes(self):
		return 1

	def get_output_planes(self):
		return 1

	def get_possible_actions(self):
		valids = np.zeros(self.get_action_size())
		moves = self.board.get_possible_moves()

		for x, y in moves:
			valids[self.board_size[0] * x + y] = 1

		return valids

	def get_possible_actions_index(self):
		return np.argwhere(self.get_possible_actions() != 0).flatten()

	def get_player(self):
		return self.player

	def play(self, action):
		x = int(action / self.board_size[0])
		y = int(action % self.board_size[1])

		assert self.board.board[(x, y)] == HexBoard.EMPTY, "Trying to play a piece where another piece already is, this shouldn't happen"

		color = HexBoard.RED if self.player == 1 else HexBoard.BLUE
		self.board.place((x, y), color)
		# self.board[x][y] = self.player

		self.player = self.player * -1
		self.history.append(np.copy(self.board.as_np()))
	
	def add_policy(self, p):
		self.probs.append(p)

	def make_input(self, i):
		player = -1 if i % 2 == 0 else 1  
		return player * self.history[i]

	def make_target(self, i):
		player = -1 if i % 2 == 0 else 1  
		winner = self.check_winner()		

		return self.probs[i], winner*self.get_player()*player 

	def check_winner(self):
		winner = self.board.get_winner()

		if winner == None:
			return None
		elif winner == HexBoard.EMPTY:
			return 0
		else:
			return 1 if winner == HexBoard.RED else -1

	def print_board(self):
		self.board.print()

	def get_board(self):
		raise NotImplementedError

	def get_input_representation(self):
		raise NotImplementedError

	def hashed_board(self):
		raise NotImplementedError

	def get_canonical_board(self):
		return self.board.get_mirrored_board().as_np() if self.player == -1 else self.board.as_np()

	def copy_game(self):
		g = Hex(player = self.get_player(), 
			history = list(self.history), 
			probs = list(self.probs), 
			**self.params)
		g.board = self.board.copy()
		return g
