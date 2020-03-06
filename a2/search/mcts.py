import logging

from . import HexSearchMethod

logger = logging.getLogger(__name__)

class MCTS(HexSearchMethod):
    """This object houses all the code necessary for the MCTS implementation"""

    def __init__(self, size, evaluate_class, live_play = True):
        self.size = size
        self.evaluate_class = evaluate_class
        self.live_play = live_play

    def get_next_move(self, board, color):
        logger.error('MCTS still needs to be implemented.')
        return self.get_possible_moves(board)[0]