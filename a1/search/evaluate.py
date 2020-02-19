import math
import numpy as np

from util import cls
from hexboard import HexBoard
from minimax import Minimax

class Evaluate:

    def __init__(self, eval_method):
        self.eval_method = eval_method

    def find_shortest_path_to_border(self, board, color):
        source_coords = board.get_source_coordinates(color)
        target_coords = board.get_target_coordinates(color)
        opposite_color = board.get_opposite_color(color)
        
        min_score = math.inf

        #For every combination of target and source coord
        for from_coord in source_coords:
            for to_coord in target_coords:
                # skip if the target or destination coord is already taken by the enemy team
                if board.get_color(from_coord) == opposite_color or board.get_color(to_coord) == opposite_color:
                    continue
                # Only count nodes without placed positions of this color
                score = self.get_path_length_between(board, from_coord, to_coord, color)

                if score < min_score:
                    min_score = score

        return min_score

    def get_path_length_between(self, board, from_coord, to_coord, color):
        dist, prev = self.dijkstra(board, from_coord, to_coord, color)
        path = []
        node = to_coord

        while node != None:
            path.append(node)
            node = prev[node]

        return len(path)

    def dijkstra(self, board, from_coord, to_coord, color):
        opposite_color = board.get_opposite_color(color)
        q = []
        dist = {}
        prev = {}
        
        for node in board.board:
            # don't add this node to the list, since we can basically see it as a wall
            if board.get_color(node) == opposite_color:
                continue
            # otherwise initialize node as normal
            dist[node] = math.inf
            prev[node] = None
            q.append(node)
        dist[from_coord] = 0

        while len(q) > 0:
            node = min(q, key=lambda x: dist[x])
            q.remove(node)

            for neighbor in board.get_traversable_neighbors(node, color):
                if neighbor not in dist: continue
                
                new_dist = dist[node] + self.distance_between(board, node, neighbor)
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = node
        
        return (dist, prev)

    def distance_between(self, board, coord_a, coord_b):
        color_a = board.get_color(coord_a)
        color_b = board.get_color(coord_b)
        is_identical = color_a == color_b

        if color_a != board.EMPTY and is_identical:
            return 0
        else:
            return 1
        

    def evaluate_board(self, board, color):
        if board.check_draw(): return 0
        if board.check_win(color): return math.inf
        if board.check_win(board.get_opposite_color(color)): return -math.inf

        if self.eval_method == 'Dijkstra':
            player_sp = self.find_shortest_path_to_border(board, color)
            opponent_sp = self.find_shortest_path_to_border(board, board.get_opposite_color(color))

            print("Found %d for player and %d for opponent" % (player_sp, opponent_sp))
            return player_sp - opponent_sp
        else:
            return np.random.uniform(0, 1)

class Node:
    dist = math.inf
    prev = None
    coord = None

    def __init__(self, coordinate):
        self.coord = coordinate