import logging

import torch
import yaml

from alphazero.src.gameplay.players import AlphaZeroPlayer
from alphazero.src.games.hex import Hex
from alphazero.src.mcts import MCTS
from alphazero.src.nn.wrapper import ModelWrapper
from search import HexSearchMethod

logger = logging.getLogger(__name__)

class AlphaZero(HexSearchMethod):

    def __init__(self, model_path, name, board_size):
        self.model_path = model_path
        self.name = name
        self.board_size = board_size
        
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            
        with open("alphazero/config.yaml", 'r') as f:
            config = yaml.safe_load(f)

        self.game = Hex(board_size=[board_size, board_size])
        self.nn = ModelWrapper(self.game, device, **config['NN'])
        self.nn.load_model(self.model_path)

        self.mcts = MCTS(**config['MCTS'])
        self.player = AlphaZeroPlayer(self.nn, self.mcts)
        
    def get_next_move(self, board, color):
        action = self.player.get_action_for_board(self.game, board)

        x = int(action / self.board_size)
        y = int(action % self.board_size)
        move = (x, y)

        # print('Move: %s' % str(move))

        return move
    
    def __str__(self):
        """"Simple toString implementation, useful for debugging only"""
        return 'AlphaZero(%s)' % (
            self.name
        )
