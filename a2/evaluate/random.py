import math
from heapq import heappop, heappush

from . import HexEvalMethod

class Random(HexEvalMethod):

    def __init__(self):
        super(HexEvalMethod, self).__init__('random')
    
    def evaluate_board(self, board, color):
        return random.random()