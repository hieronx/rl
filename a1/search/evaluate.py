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
        
        min_score = math.inf

        #For every combination of target and source coord
        for from_coord in source_coords:
            for to_coord in target_coords:
                # Only count nodes without placed positions of this color
                score = self.get_path_between(board, from_coord, to_coord, color)

                if score < min_score:
                    min_score = score

        return min_score

    def get_path_between(self, board, from_coord, to_coord, color):
        open_list = [Node(from_coord, 0)]
        closed_list = []
        end_node = None

        while len(open_list) > 0:
            # find the node in the open_list with the lowest distance
            node = self.find_lowest_dist_node(open_list)
            open_list.remove(node)

            neighbors = board.get_traversable_neighbors(node.coord, color)
            for neighbor in neighbors:
                
                cost = self.get_cost_between(board, neighbor, node.coord)

                neighbor_node = Node(neighbor, node.distance + cost)
                neighbor_node.prev_node = node

                found = False
                for other_node in open_list:
                    if other_node.coord == neighbor_node.coord:
                        found = True
                        if other_node.distance > neighbor_node.distance:
                            other_node.distance = neighbor_node.distance
                            other_node.prev_node = neighbor_node.prev_node
                            
                
                # we already have an entry for this coord, so no need to continue this
                
                for other_node in closed_list:
                    if other_node.coord == neighbor_node.coord:
                        found = True
                        if other_node.distance > neighbor_node.distance:
                            other_node.distance = neighbor_node.distance
                            other_node.prev_node = neighbor_node.prev_node
                            
                
                # if we make it this far, please add this neighbor to the open_list
                if not found: 
                    open_list.append(neighbor_node)
                
            # we're done with this node, add it to the closed list
            closed_list.append(node)
        
        for node in closed_list:
            if node.coord == to_coord:
                end_node = node
        for node in open_list:
            if node.coord == to_coord:
                end_node = node

        # return the path between these two points
        if end_node == None: return math.inf
        return end_node.distance

    def get_cost_between(self, board, coordA, coordB):
        colorA = board.get_color(coordA)
        if colorA == board.EMPTY: 
            return 1
        else:
            return 0

    def find_lowest_dist_node(self, open_list):
        record = open_list[0]
        for node in open_list:
            if node.distance <= record.distance:
                record = node
        return record

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
    prev_node = None
    distance = math.inf
    coord = None

    def __init__(self, location, dist = math.inf):
        self.coord = location
        self.distance = dist