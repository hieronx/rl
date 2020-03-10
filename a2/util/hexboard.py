from copy import deepcopy
from functools import lru_cache
import math

class HexBoard:
    """This class holds all the data for a single board state"""

    BLUE = 1
    RED = 2
    EMPTY = 3

    def __init__(self, board_size):
        """Creates a new empty board with the provided size"""
        self.board = {}
        possible_moves = []
        self.size = board_size

        for x in range(board_size):
            for y in range(board_size):
                self.board[x, y] = HexBoard.EMPTY

    def is_empty(self, coordinates):
        """Returns if the board is empty at the provided coordinate"""
        return self.board[coordinates] == HexBoard.EMPTY

    def is_color(self, coordinates, color):
        """Returns if the board is a certain color at the provided coordinate"""
        return self.board[coordinates] == color

    def get_color(self, coordinates):
        """Returns the color at the provided board coordinate"""
        return self.board[coordinates]

    def make_move(self, coordinates, color):
        """Should return the new board without modifying the existing board"""
        new_board = deepcopy(self)
        new_board.board[coordinates] = color
        return new_board

    @lru_cache(maxsize=4)
    def get_opposite_color(self, current_color):
        """Returns the opposite color of the provided color. Returns BLUE if the color is not recognized"""
        return HexBoard.RED if current_color == HexBoard.BLUE else HexBoard.BLUE

    @lru_cache(maxsize=512) # caching this to create lower lookup times, technically can't have more than board.size ** 2 options
    def get_neighbors(self, coordinates):
        """Returns a list with the coordinates of every possible/valid neighbor."""
        (cx, cy) = coordinates
        neighbors = []

        if cx-1 >= 0:
            neighbors.append((cx-1, cy))
        if cx+1 < self.size:
            neighbors.append((cx+1, cy))
        if cx-1 >= 0 and cy+1 < self.size-1:
            neighbors.append((cx-1, cy+1))
        if cx+1 < self.size and cy-1 >= 0:
            neighbors.append((cx+1, cy-1))
        if cy+1 < self.size:
            neighbors.append((cx, cy+1))
        if cy-1 >= 0:
            neighbors.append((cx, cy-1))

        return neighbors

    def border(self, color, move):
        """Returns if we have reached the border (goal) for a specific color"""
        (nx, ny) = move
        return (color == HexBoard.BLUE and nx == self.size-1) or (color == HexBoard.RED and ny == self.size-1)

    def traverse(self, color, move, visited):
        """
        Returns true if we can reach the end of the board using this move.
        Returns false if the next move is already visited or the wrong color.
        If we did not reach the end we recursively check each of the neighbors,
        and if we reach the otherside that way we return true as well.
        """
        if not self.board[move] == color or (move in visited):
            return False

        if self.border(color, move):
            return True

        visited[move] = True
        for n in self.get_neighbors(move):
            if self.traverse(color, n, visited):
                return True
		
        return False

    def game_over(self):
        """Check if the game has ended, either by a win or by a draw"""
        return self.check_win(HexBoard.RED) or self.check_win(HexBoard.BLUE) or self.check_draw()

    def check_win(self, color):
        """Check if we have made a snake from the source side to the opposing side for the provided color"""
        for move in self.get_source_coordinates(self):			
            if self.traverse(color, move, {}):
                return True
        return False

    def check_draw(self):
        """Checks if we have any empty hexes left on the board"""
        for _, color in self.board.items():
            if color == HexBoard.EMPTY: return False
        return True

    @lru_cache(maxsize=2)
    def get_source_coordinates(self, color):
        """Returns the coordinates of the left border (for blue) or the top border (for red)"""
        if color == HexBoard.BLUE:
            return [(0, i) for i in range(self.size)]
        else:
            return [(i, 0) for i in range(self.size)]
            
    @lru_cache(maxsize=2)
    def get_target_coordinates(self, color):
        """Returns the coordinates of the right border (for blue) or the left border (for red)"""
        if color == HexBoard.BLUE:
            return [(self.size - 1, i) for i in range(self.size)]
        else:
            return [(i, self.size - 1) for i in range(self.size)]

    def print(self):
        """Outputs the board pieces to the console"""
        print("   ", end="")

        for y in range(self.size):
            print(chr(y + ord('a')), "", end="")
        print("")
        print(" -----------------------")

        for y in range(self.size):
            print(y, "|", end="")
			
            for z in range(y):
                print(" ", end="")

            for x in range(self.size):
                piece = self.board[x, y]
                if piece == HexBoard.BLUE:
                    print("\u001b[36m\u25CF\u001b[0m ", end="")
                elif piece == HexBoard.RED:
                    print("\u001b[31m\u25CF\u001b[0m ", end="")
                else:
                    if x == self.size:
                        print("-", end="")
                    else:
                        print("- ", end="")
            print("|")

        print("   -----------------------")

    def hash_code(self, color):
        """Generates a hash code that mirrors the current board state as seen by the provided player"""
        multiplier = 10
        code = color
        for _, value in self.board.items():
            code += value * multiplier
            multiplier *= 10
        return code
    
    def get_reward(self, color):
        """Returns the reward for the specified color, -1 if it loses, 1 if it wins, 0 on a draw"""
        color_won = self.check_win(color)
        other_won = self.check_win(self.get_opposite_color(color))
        if not other_won and not color_won:
            return 0
        else:
            return 1 if color_won else -1

    @classmethod
    def from_hash_code(cls, hash_code):
        color = int(str(hash_code)[-1])
        pos = str(hash_code)[:len(str(hash_code))-1][::-1]
        board_size = int(math.sqrt(len(pos)))
        board = cls(board_size)

        i = 0
        for x in range(board_size):
            for y in range(board_size):
                board.board[x, y] = int(pos[i])
                i += 1
        
        return board
    
    def get_move_between_boards(self, other_board):
        if self.size is not other_board.size:
            logger.error('Trying to get the move between two boards of different sizes.')
            return (None, None)

        for x in range(self.size):
            for y in range(self.size):
                if self.board[x, y] != other_board.board[x, y]:
                    return (x, y)
        
        return (None, None)