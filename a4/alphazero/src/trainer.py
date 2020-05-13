import os
import pickle
import time
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool

import numpy as np

from alphazero.src.nn.wrapper import ModelWrapper
from alphazero.src.utils import print_progressbar, progressbar
from alphazero.src.utils.plot import unique_positions_vis
from alphazero.src.utils.replay_buffer import ReplayBuffer


class AlphaZeroTrainer(object):
	def __init__(self, NN, game, mcts, **params):
		super(AlphaZeroTrainer, self).__init__()
		self.nn_wrapper = NN
		self.game = game
		self.mcts = mcts
		self.queue_len = params['queue_len']
		self.n_games = params['n_games']
		self.iterations = params['iterations']
		self.temp = params['temp']
		self.replay_buffer = ReplayBuffer(self.queue_len)

	def train(self, game, device,  **params):
		run_start_time = int(time.time())

		# Save the initial model before any training
		self.nn_wrapper.save_model("models", "%d.pt" % run_start_time)

		for i in progressbar(range(self.iterations), desc="Overall progress", position=0):
			completed_games = 0
			start_time = time.time()
			print_progressbar(desc='Playing games', completed=0, start_time=start_time, total=self.n_games, position=1)
			for _ in range(self.n_games):
				self.play_game(i)
				completed_games += 1
				print_progressbar(desc='Playing games', completed=completed_games, start_time=start_time, total=self.n_games, position=1)

			loss = self.nn_wrapper.train(self.replay_buffer)

			self.nn_wrapper.save_model("models", "%d.pt" % run_start_time)
			pickle.dump(self.replay_buffer, open(os.path.join("models", "%d-rb.p" % run_start_time), "wb"))

			# print("Finished self-play iteration %d/%d, avg loss: %.2f" % (i+1, self.iterations, loss))

		return loss

	def play_game(self, i):
		winner = None
		game = self.game.new_game()
		mcts = self.mcts.new_mcts()
		game_step = 0
		temp = self.temp['before']
		while winner == None:
			if game_step < self.temp['treshold']:
				temp = self.temp['after']
			
			action_probs = mcts.simulate(game, self.nn_wrapper, temp)
			action = np.argmax(action_probs)
			game.play(action)
				
			winner = game.check_winner()
			game_step += 1
		
		self.replay_buffer.save_game(game)
