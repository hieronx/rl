import math
from heapq import heappop, heappush

from . import HexEvalMethod

class Dijkstra(HexEvalMethod):

    def __init__(self):
        """Stores the eval method that will be used for this evaluate class"""
        HexEvalMethod.__init__('Dijkstra')

    def get_score(self, board, from_coord, target_coords, color, opposite_color):
        """Runs Dijkstra's algorithm between the two provided coords on the provided board"""
        q = []
        dist = {}
        
        for node in board.board:
            dist[node] = math.inf
            
        dist[from_coord] = 1 if board.board[from_coord] == board.EMPTY else 0
        heappush(q, (dist[from_coord], from_coord))

        while q:
            node_dist, node = heappop(q)

            if node in target_coords:
                return dist[node]

            for neighbor in board.get_neighbors(node):
                new_dist = node_dist + self.distance_to(board.board[neighbor], opposite_color)
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    heappush(q, (new_dist, neighbor))

        return math.inf
        