import math
import numpy as np

from functools import lru_cache
from util import cls
from hexboard import HexBoard
from minimax import Minimax
from heapq import heappop, heappush

class Evaluate:

    def evaluate_board(self, board, color):
        return np.random.uniform(0, 1)