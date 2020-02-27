import math
import random

from functools import lru_cache
from hexboard import HexBoard
from minimax import Minimax
from heapq import heappop, heappush

class Evaluate:
    """This class holds all the logic needed to evaluate a single board state, such as Dijkstra's shortest
    path algorithm"""

    def __init__(self, eval_method):
        """Stores the eval method that will be used for this evaluate class"""
        self.eval_method = eval_method

    def find_shortest_path_to_border(self, board, color):
        """Returns the length of the shortest possible path to the border for the specified color"""
        source_coords = board.get_source_coordinates(color)
        target_coords = board.get_target_coordinates(color)
        opposite_color = board.get_opposite_color(color)
        
        min_score = board.size**2

        # For every combination of target and source coord
        for from_coord in source_coords:
            # skip if the start coord is already taken by the enemy team
            if board.get_color(from_coord) == opposite_color:
                continue

            # Only count nodes without placed positions of this color
            if self.eval_method == 'Dijkstra': 
                score = self.dijkstra(board, from_coord, target_coords, color, opposite_color)
            elif self.eval_method == 'AStar':
                score = self.astar(board, from_coord, target_coords, color, opposite_color, self.heuristic)

            if score < min_score:
                min_score = score

        return min_score

    def astar(self, board, from_coord, target_coords, color, opposite_color, h):
        """Runs the AStar pathfinding algorithm and returns the length of the shortest path to the target coordinate"""
        q = []
        checked = set()

        checked.add(from_coord)
        f = h(from_coord, target_coords)
        heappush(q, (f, 0, from_coord))

        while q:
            node_f, node_g, node = heappop(q)

            if node in target_coords:
                return node_f

            for neighbor in board.get_neighbors(node):
                new_g = node_g + self.distance_to(board.board[neighbor], opposite_color)

                if neighbor not in checked:
                    checked.add(neighbor)
                    f = new_g + h(neighbor, target_coords)
                    heappush(q, (f, new_g, neighbor))
        
        return math.inf

    @lru_cache(maxsize = 1024)
    def heuristic(self, source, targets):
        """Returns the shortest euclidian distance to one of the target coordinates"""
        return min([math.sqrt((source[0] - target[0]) ** 2 + (source[1] - target[1]) ** 2) for target in targets])

    def dijkstra(self, board, from_coord, target_coords, color, opposite_color):
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
        
    @lru_cache(maxsize=8)
    def distance_to(self, color_b, opposite_color):
        """Returns the distance between the two provided colors, this is the vertex cost for Dijkstra"""
        if color_b == opposite_color:
            return math.inf
        elif color_b == HexBoard.EMPTY:
            return 1
        else:
            return 0

    def evaluate_board(self, board, color):
        """Returns a number that corresponds to a board evaluation. Higher numbers mean better numbers for the provided color"""
        if self.eval_method == 'random':
            return random.random()

        elif self.eval_method in ('Dijkstra', 'AStar'):
            if board.check_draw() or (board.check_win(color) and board.check_win(board.get_opposite_color(color))): return 0
            if board.check_win(color): return 1000
            if board.check_win(board.get_opposite_color(color)): return -1000
            
            player_sp = self.find_shortest_path_to_border(board, color)
            opponent_sp = self.find_shortest_path_to_border(board, board.get_opposite_color(color))

            if player_sp == math.inf: player_sp = 0
            if opponent_sp == math.inf: opponent_sp = 0

            return -(player_sp - opponent_sp)
        
        else:
            print('This should not have happened, since we should have provided a valid eval method...')
            return 0