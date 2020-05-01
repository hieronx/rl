import math
import random
from heapq import heappop, heappush

from . import HexEvalMethod

class RandomEval(HexEvalMethod):

    def __init__(self):
        HexEvalMethod.__init__('random')
    
    def evaluate_board(self, board, color):
        return random.random()