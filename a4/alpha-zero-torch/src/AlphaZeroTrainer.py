import time
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count

import numpy as np

from src.NN import NetWrapper
from src.utils import progressbar
from src.utils.plot import unique_positions_vis


class AlphaZeroTrainer(object):
	def __init__(self, NN, game, mcts, **params):
		super(AlphaZeroTrainer, self).__init__()
		self.nn_wrapper = NN
		self.game = game
		self.mcts = mcts
		self.queue_len = params['queue_len']
		self.n_games = params['n_games']
		self.eps = params['eps']
		self.temp = params['temp']
		self.replay_buffer = ReplayBuffer(self.queue_len)

	def train(self, game, device, lr=0.1, wd=0.005, **params):
		pool = ThreadPool(cpu_count())
		start_time = int(time.time())

		# Save the initial model before any training
		self.nn_wrapper.save_model("models", "%d.pt" % start_time)

		for i in range(self.eps):
			pool.map(self.play_game, range(self.n_games))
			loss = self.nn_wrapper.train(self.replay_buffer)

			prev_nn_wrapper = NetWrapper(game, device, lr, wd, **params)
			prev_nn_wrapper.load_model("models/%d.pt" % start_time)
			
			prev_wins, new_wins = 0, 0
			num_matchup_games = 20
			for i in progressbar(range(num_matchup_games), desc="Playing matchups"):
				if i % 2 == 0:
					winner = self.play_matchup(prev_nn_wrapper, self.nn_wrapper)
				else:
					winner = self.play_matchup(self.nn_wrapper, prev_nn_wrapper)

				if winner == 1:
					prev_wins += 1
				elif winner == -1:
					new_wins += 1
			
			win_perc = new_wins / num_matchup_games

			if win_perc > 0.6:
				self.nn_wrapper.save_model("models", "%d.pt" % start_time)
				self.nn_wrapper.save_model("models", "best.pt")
				print("Win perc = %.2f, overwriting previous model." % win_perc)
			else:
				self.nn_wrapper.load_model("models/%d.pt" % start_time)
				print("Win perc = %.2f, keeping previous model." % win_perc)

			print("One self play ep: {}/{}, avg loss: {}".format(i,self.eps, loss))

		return loss

	def play_game(self, n_game):
		winner = None
		game = self.game.new_game()
		mcts = self.mcts.new_mcts()
		game_step = 0
		temp = self.temp['before']
		print(f'Playing game number {n_game}...')
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

class ReplayBuffer(object):
	def __init__(self, window_size):
		super(ReplayBuffer, self).__init__()
		self.buffer = []
		self.window_size = window_size

	def save_game(self, game):
	    if len(self.buffer) > self.window_size:
	      self.buffer.pop(0)
	    self.buffer.append(game)

	def sample_batch(self, batch_size):
	    n_positions = self.get_total_positions()

	    games = np.random.choice(
	        self.buffer,
	        size= batch_size)

	    game_pos = [(g, np.random.randint(len(g.history))) for g in games]
	    pos = np.array([[g.make_input(i), *g.make_target(i)] for (g, i) in game_pos])
	    return list(pos[:,0]), list(pos[:,1]), list(pos[:,2])

	def get_total_positions(self):
		return float(sum(len(g.history) for g in self.buffer))
