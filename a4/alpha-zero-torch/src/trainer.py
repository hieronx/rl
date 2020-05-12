import time
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool

import numpy as np

from src.nn.wrapper import ModelWrapper
from src.utils import print_progressbar, progressbar
from src.utils.plot import unique_positions_vis
from src.utils.replay_buffer import ReplayBuffer


class AlphaZeroTrainer(object):
	def __init__(self, NN, game, mcts, **params):
		super(AlphaZeroTrainer, self).__init__()
		self.nn_wrapper = NN
		self.game = game
		self.mcts = mcts
		self.queue_len = params['queue_len']
		self.arena_compare = params['arena_compare']
		self.update_threshold = params['update_threshold']
		self.n_games = params['n_games']
		self.iterations = params['iterations']
		self.temp = params['temp']
		self.replay_buffer = ReplayBuffer(self.queue_len)

	def train(self, game, device,  **params):
		pool = ThreadPool(cpu_count())
		start_time = int(time.time())

		# Save the initial model before any training
		self.nn_wrapper.save_model("models", "%d.pt" % start_time)

		for i in progressbar(range(self.iterations), desc="Training", position=0):
			completed_games = 0
			start_time = time.time()
			print_progressbar(desc='Playing games', completed=0, start_time=start_time, total=self.n_games, position=1)
			# pool.map(self.play_game, range(self.n_games))
			for _ in pool.imap_unordered(self.play_game, range(self.n_games)):
				completed_games += 1
				print_progressbar(desc='Playing games', completed=completed_games, start_time=start_time, total=self.n_games, position=1)

			loss = self.nn_wrapper.train(self.replay_buffer)

			prev_nn_wrapper = ModelWrapper(game, device, **params)
			prev_nn_wrapper.load_model("models/%d.pt" % start_time)
			
			prev_wins, new_wins = 0, 0
			for j in progressbar(range(self.arena_compare), desc="Playing matchups", position=1):
				if j % 2 == 0:
					winner = self.play_matchup(prev_nn_wrapper, self.nn_wrapper)
				else:
					winner = self.play_matchup(self.nn_wrapper, prev_nn_wrapper)

				if winner == 1:
					prev_wins += 1
				elif winner == -1:
					new_wins += 1
			
			win_perc = new_wins / self.arena_compare

			if win_perc > self.update_threshold:
				self.nn_wrapper.save_model("models", "%d.pt" % start_time)
				self.nn_wrapper.save_model("models", "best.pt")
				print("Win perc = %.2f, overwriting previous model." % win_perc)
			else:
				self.nn_wrapper.load_model("models/%d.pt" % start_time)
				print("Win perc = %.2f, keeping previous model." % win_perc)

			print("Finished self-play iteration %d/%d, avg loss: %.2f" % (i+1, self.iterations, loss))

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

	def play_matchup(self, player1_nn, player2_nn):
		winner = None
		game = self.game.new_game()
		mcts = self.mcts.new_mcts()
		game_step = 0
		temp = self.temp['before']

		current_player_idx = 1
		while winner == None:
			if game_step < self.temp['treshold']:
				temp = self.temp['after']
			
			current_player_nn = player1_nn if current_player_idx == 1 else player2_nn

			action_probs = mcts.simulate(game, current_player_nn, temp)
			action = np.argmax(action_probs)
			game.play(action)
				
			winner = game.check_winner()
			game_step += 1

			current_player_idx = 2 if current_player_idx == 1 else 1
		
		return winner
