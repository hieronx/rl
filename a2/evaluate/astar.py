import math
from heapq import heappop, heappush
from functools import lru_cache

from . import HexSPEvalMethod

class AStar(HexSPEvalMethod):

    def __init__(self):
        """Stores the eval method that will be used for this evaluate class"""
        super(HexSPEvalMethod, self).__init__('AStar')

    def astar(self, board, from_coord, target_coords, color, opposite_color):
        """Runs the AStar pathfinding algorithm and returns the length of the shortest path to one of the target coordinates"""
        q = []
        h = self.heuristic
        checked = set()

        checked.add(from_coord)
        f = min([h(from_coord, to_coord) for to_coord in target_coords])
        heappush(q, (f, self.distance_to(board.board[from_coord], opposite_color), from_coord))

        while q:
            node_f, node_g, node = heappop(q)
            if node in target_coords:
                return node_g

            for neighbor in board.get_neighbors(node):
                new_g = node_g + self.distance_to(board.board[neighbor], opposite_color)

                if neighbor not in checked:
                    checked.add(neighbor)
                    f = new_g + min([h(from_coord, to_coord) for to_coord in target_coords])
                    heappush(q, (f, new_g, neighbor))
        
        return math.inf

    @lru_cache(maxsize = 512)
    def heuristic(self, source, target):
        """Returns the euclidian distance to the target coordinates"""
        return math.sqrt((source[0] - target[0]) ** 2 + (source[1] - target[1]) ** 2)
