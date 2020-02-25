import math
import numpy as np

from util import cls
from hexboard import HexBoard
from minimax import Minimax
from heapq import heappop, heappush

class Evaluate:

    def __init__(self, eval_method):
        self.eval_method = eval_method

    def find_shortest_path_to_border(self, board, color):
        source_coords = board.get_source_coordinates(color)
        target_coords = board.get_target_coordinates(color)
        opposite_color = board.get_opposite_color(color)
        
        min_score = board.size**2

        #For every combination of target and source coord
        for from_coord in source_coords:
            for to_coord in target_coords:
                # skip if the target or destination coord is already taken by the enemy team
                # if board.get_color(from_coord) == opposite_color or board.get_color(to_coord) == opposite_color:
                #     continue

                # Only count nodes without placed positions of this color
                score = self.get_path_length_between(board, from_coord, to_coord, color)

                if score < min_score:
                    min_score = score
        
        if min_score == board.size**2:
            return 0

        return min_score

    def get_path_length_between(self, board, from_coord, to_coord, color):
        dist, prev = self.dijkstra(board, from_coord, to_coord, color)
        return dist[to_coord]

    def dijkstra(self, board, from_coord, to_coord, color):
        opposite_color = board.get_opposite_color(color)
        q = []
        dist = {}
        prev = {}
        
        for node in board.board:
            dist[node] = math.inf
            prev[node] = None
            
        dist[from_coord] = 1 if board.get_color(from_coord) == board.EMPTY else 0
        heappush(q, (dist[from_coord], from_coord))

        while q:
            node_dist, node = heappop(q)

            for neighbor in board.get_neighbors(node):
                new_dist = node_dist + self.distance_between(board, node, neighbor, opposite_color)
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = node
                    heappush(q, (new_dist, neighbor))
        
        return (dist, prev)

    def distance_between(self, board, coord_a, coord_b, opposite_color):
        if board.get_color(coord_b) == opposite_color:
            return math.inf
        elif board.get_color(coord_b) == board.EMPTY:
            return 1
        else:
            return 0

    def evaluate_board(self, board, color):
        if board.check_draw() or (board.check_win(color) and board.check_win(board.get_opposite_color(color))): return 0
        # if board.check_win(color): return -math.inf
        # if board.check_win(board.get_opposite_color(color)): return math.inf

        if self.eval_method == 'Dijkstra':
            player_sp = self.find_shortest_path_to_border(board, color)
            opponent_sp = self.find_shortest_path_to_border(board, board.get_opposite_color(color))
            # print('Player = %d vs opponent = %d' % (player_sp, opponent_sp))

            if player_sp == math.inf: player_sp = 0
            if opponent_sp == math.inf: opponent_sp = 0

            return -(player_sp - opponent_sp)
        else:
            return np.random.uniform(0, 1)

class Node:
    dist = math.inf
    prev = None
    coord = None

    def __init__(self, coordinate):
        self.coord = coordinate