import numpy as np
from collections import deque

class ReplayBuffer(object):
	def __init__(self, window_size):
		super(ReplayBuffer, self).__init__()
		self.buffer = deque(maxlen=window_size)
		self.window_size = window_size

	def save_game(self, game):
	    self.buffer.append(game)

	def sample_batch(self, batch_size):
	    games = np.random.choice(
	        self.buffer,
	        size= batch_size)

	    game_pos = [(g, np.random.randint(len(g.history))) for g in games]
	    pos = np.array([[g.make_input(i), *g.make_target(i)] for (g, i) in game_pos])
	    return list(pos[:,0]), list(pos[:,1]), list(pos[:,2])

	def get_total_positions(self):
		return float(sum(len(g.history) for g in self.buffer))
