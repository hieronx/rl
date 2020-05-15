from collections import deque

import numpy as np

from util.hexboard import HexBoard


class ReplayBuffer(object):
    """
    This class holds the history for a specific (queue length) amount of games.
    """

    def __init__(self, window_size):
        """Creates a new replaybuffer using the provided window size as the maximum size for the replay buffer"""
        super(ReplayBuffer, self).__init__()
        self.buffer = deque(maxlen=window_size)

    def save_game(self, game):
        """Appends on game to the replaybuffer"""
        self.buffer.append(game)

    def sample_batch(self, batch_size):
        """Samples a number of frames from randomly sampled games equal to batch size"""
        games = np.random.choice(
            self.buffer,
            size= batch_size)

        game_pos = [(g, np.random.randint(len(g.history))) for g in games]
        pos = np.array([[g.make_input(i), *g.make_target(i)] for (g, i) in game_pos])
        ret = list(pos[:,0]), list(pos[:,1]), list(pos[:,2])

        # for game in games:
        #     for i in range(len(game.history)):
        #         board_np = game.make_input(i)
        #         policy, value = game.make_target(i)

        #         board = HexBoard(7)
        #         board.from_np(board_np, 7, 0).print()
        #         print(policy)
        #         print(value)
        #         print('\n\n\n\n')
        #     print('Winner: %s' % game.check_winner()) 
        #     exit()   

        # board = HexBoard(7)
        # board.from_np(ret[0][0], 7, 0).print()
        # print(ret[1][0])
        # print(ret[2][0])
        # print('\n\n\n\n')
        
        return ret

    def get_total_positions(self):
        """Returns the complete length of ALL the frames in the replay buffer"""
        return float(sum(len(g.history) for g in self.buffer))
