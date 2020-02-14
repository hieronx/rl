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
                path = self.get_path_between(from_coord, to_coord, color)

                # invalid or impossible path
                if len(path) < 1: 
                    continue

                score = len(path)
                if score < min_score:
                    min_score = score

        return min_score

    def get_path_between(self, from_coord, to_coord, color):
        open_list = [Node(from_coord, 0)]
        closed_list = []
        endNode = None

        while len(open_list) > 0:
            # find the node in the open_list with the lowest distance
            node = self.find_lowest_dist_node(open_list)
            open_list.remove(node)

            neighbors = board.get_traversable_neighbors(node.coord, color)
            for neighbor in neighbors:
                
                cost = self.get_cost_between(neighbor, node.coord)

                neighborNode = Node(neighbor, node.distance + cost)
                neighborNode.prevNode = node

                if neighbor == to_coord: 
                    endNode = neighborNode
                    break

                found = False
                for otherNode in open_list:
                    if otherNode.coord == neighborNode.coord:
                        if otherNode.distance > neighborNode.coord:
                            otherNode.distance = neighborNode.distance
                            otherNode.prevNode = neighborNode.prevNode
                            found = True
                # we already have an entry for this coord, so no need to continue this
                if found: continue

                found = False
                for otherNode in closed_list:
                    if otherNode.coord == neighborNode.coord:
                        if otherNode.distance > neighborNode.coord:
                            otherNode.distance = neighborNode.distance
                            otherNode.prevNode = neighborNode.prevNode
                            found = True
                if found: continue

                # if we make it this far, please add this neighbor to the open_list
                open_list.append(neighborNode)
                
            # we're done with this node, add it to the closed list
            closed_list.append(node)
        
        # return the path between these two points
        return self.get_path_from_end()

    def get_cost_between(self, coordA, coordB):
        colorA = board.get_color(coordA)
        colorB = board.get_color(coordB)
        if colorA == board.EMPTY or colorB == board.EMPTY:
            return 1
        if colorA == colorB:
            return 0
        return 1

    def get_path_from_end(self, endNode):
        if endNode == None: 
            return []
        path = []
        node = endNode
        while node.prevNode != None:
            path.append(node)
            node = node.prevNode
        return path

    def find_lowest_dist_node(self, open_list):
        record = list[0]
        for node in open_list:
            if node.distance <= record.distance:
                record = node
        return record

    def evaluate_board(self, board, color):
        if self.eval_method == 'Dijkstra':
            player_sp = self.find_shortest_path_to_border(board, color)
            opponent_sp = self.find_shortest_path_to_border(board, board.get_opposite_color(color))

            return player_sp - opponent_sp
        else:
            return np.random.uniform(0, 1)

class Node:
    prevNode = None
    distance = math.inf
    coord = None

    def __init__(self, location, dist = math.inf):
        self.coord = location
        self.distance = dist