from copy import deepcopy
from functools import lru_cache
import math

class HexBoard:
    """This class holds all the data for a single board state"""

    BLUE = 1
    RED = 2
    EMPTY = 3
    POSSIBLE_NEIGHBORS = ((-1, 0), (1, 0), (-1, 1), (1, -1), (0, 1), (0, -1))

    def __init__(self, board_size):
        """Creates a new empty board with the provided size"""
        self.board = {}
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
        new_board = self.copy()
        new_board.board[coordinates] = color
        return new_board
    
    def copy(self):
        """Returns an exact deep copy of itself"""
        return HexBoard.from_hash_code(self.hash_code())

    @classmethod
    @lru_cache(maxsize=512) # caching this to create lower lookup times, technically can't have more than board.size ** 2 options
    def get_neighbors(cls, coordinates, size):
        """Returns a list with the coordinates of every possible/valid neighbor."""
        (cx, cy) = coordinates
        neighbors = [(x + cx, y + cy) for x, y in HexBoard.POSSIBLE_NEIGHBORS if HexBoard.in_bounds(cx + x, cy + y, size)]
        return neighbors

    def traverse(self, color, move, visited):
        """
        Returns true if we can reach the end of the board using this move.
        Returns false if the next move is already visited or the wrong color.
        If we did not reach the end we recursively check each of the neighbors,
        and if we reach the otherside that way we return true as well.
        """
        # if we have reached the border (target) for a specific color
        if (color == HexBoard.BLUE and move[0] == self.size-1) or (color == HexBoard.RED and move[1] == self.size-1):
            return True

        visited[move] = True
        for n in HexBoard.get_neighbors(move, self.size):
            if self.board[n] != color or n in visited: continue

            if self.traverse(color, n, visited):
                return True
		
        return False

    def game_over(self):
        """Check if the game has ended, either by a win or by a draw"""
        return self.check_win(HexBoard.RED) or self.check_win(HexBoard.BLUE) or self.check_draw()

    def check_win(self, color):
        """Check if we have made a snake from the source side to the opposing side for the provided color"""
        useful_to_check = False
        for move in HexBoard.get_target_coordinates(color, self.size):
            if self.board[move] == color:
                useful_to_check = True
                break
        if not useful_to_check: return False

        for move in HexBoard.get_source_coordinates(color, self.size):
            if self.board[move] != color: continue
            if self.traverse(color, move, {}):
                return True        
        return False

    def check_draw(self):
        """Checks if we have any empty hexes left on the board"""
        for _, color in self.board.items():
            if color == HexBoard.EMPTY: return False
        return True

    def get_possible_moves(self):
        """Compiles a list of all empty hexes in the current hexboard"""
        if self.game_over(): return []
        return [coord for coord, color in self.board.items() if color == HexBoard.EMPTY]

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

    def __str__(self):
        """Outputs the board pieces to the console"""
        output = "["

        for y in range(self.size):
            output += ""
			
            for x in range(self.size):
                piece = self.board[x, y]
                if piece == HexBoard.BLUE:
                    output += "b"
                elif piece == HexBoard.RED:
                    output += "r"
                else:
                    output += "."
            
            if y is not self.size - 1: output += " "

        output += "]"
        return output

    def hash_code(self, color=3):
        """Generates a hash code that mirrors the current board state as seen by the provided player"""
        multiplier = 10
        code = color
        for _, value in self.board.items():
            code += value * multiplier
            multiplier *= 10
        return code
    
    def get_reward(self, color):
        """Returns the reward for the specified color, -1 if it loses, 1 if it wins, 0 on a draw"""
        if not self.game_over():
            print('get_reward() called on a board that hasn\'t ended yet.')

        if self.check_win(color):
            return 1
        elif self.check_win(HexBoard.get_opposite_color(color)):
            return -1
        else:
            return 0

    @classmethod          
    @lru_cache(maxsize=32)
    def get_target_coordinates(cls, color, size):
        """Returns the coordinates of the right border (for blue) or the left border (for red)"""
        if color == HexBoard.BLUE:
            return [(size - 1, i) for i in range(size)]
        else:
            return [(i, size - 1) for i in range(size)] 

    @classmethod
    @lru_cache(maxsize=32)
    def get_source_coordinates(cls, color, size):
        """Returns the coordinates of the left border (for blue) or the top border (for red)"""
        if color == HexBoard.BLUE:
            return [(0, i) for i in range(size)]
        else:
            return [(i, 0) for i in range(size)]

    @classmethod
    def from_hash_code(cls, hash_code):
        pos = str(hash_code)[:-1][::-1]
        board_size = int(math.sqrt(len(pos)))
        board = cls(board_size)

        i = 0
        for x in range(board_size):
            for y in range(board_size):
                board.board[x, y] = int(pos[i])
                i += 1
        
        return board

    @classmethod
    @lru_cache(maxsize=2)
    def get_opposite_color(cls, color):
        """Returns the opposite color of the provided color. Returns BLUE if the color is not recognized"""
        return HexBoard.RED if color == HexBoard.BLUE else HexBoard.BLUE
    
    def get_move_between_boards(self, other_board):
        if self.size is not other_board.size:
            print('Trying to get the move between two boards of different sizes.')
            return (None, None)

        for x in range(self.size):
            for y in range(self.size):
                if self.board[x, y] != other_board.board[x, y]:
                    return (x, y)
        
        return (None, None)

    @classmethod
    @lru_cache(maxsize=512)
    def in_bounds(cls, numx, numy, size):
        """Returns if a number is still within the required constraints for the board size"""
        return numx >= 0 and numx < size and numy >= 0 and numy < size