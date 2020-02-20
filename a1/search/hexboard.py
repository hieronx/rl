from copy import deepcopy


class HexBoard:
    """This class holds all the data for a single board state"""

    BLUE = 1
    RED = 2
    EMPTY = 3

    def __init__(self, board_size):
        """Creates a new empty board with the provided size"""
        self.board = {}
        self.size = board_size
        self.game_over = False

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
        if coordinates == (-1, -1):
            return HexBoard.EMPTY
        return self.board[coordinates]

    def place(self, coordinates, color):
        """Places the provided color at the board coordinate. This modifies the interior board state of this object"""
        if not self.game_over and self.board[coordinates] == HexBoard.EMPTY:
            self.board[coordinates] = color
            if self.check_win(HexBoard.RED) or self.check_win(HexBoard.BLUE) or self.check_draw():
                self.game_over = True

    def make_move(self, coordinates, color):
        """Should return the new board without modifying the existing board"""
        new_board = deepcopy(self)
        new_board.place(coordinates, color)
        return new_board

    def get_opposite_color(self, current_color):
        """Returns the opposite color of the provided color. Returns BLUE if the color is not recognized"""
        if current_color == HexBoard.BLUE:
            return HexBoard.RED
        return HexBoard.BLUE

    def get_traversable_neighbors(self, coordinates, color):
        neighbors = self.get_neighbors(coordinates)
        traversable = []
        for neighbor in neighbors:
            if self.is_empty(coordinates) or self.is_color(coordinates, color):
                traversable.append(neighbor)
        return traversable

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
        if not self.is_color(move, color) or (move in visited and visited[move]):
            return False

        if self.border(color, move):
            return True

        visited[move] = True
        for n in self.get_neighbors(move):
            if self.traverse(color, n, visited):
                return True
		
        return False

    def check_win(self, color):
        """Check if we have made a snake from the source side to the opposing side for the provided color"""
        for i in range(self.size):
            if color == HexBoard.BLUE:
                move = (0, i)
            else:
                move = (i, 0)
			
            if self.traverse(color, move, {}):
                return True

        return False

    def check_draw(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[(x, y)] == HexBoard.EMPTY:
                    return False
        
        return True

    def get_source_coordinates(self, color):
        """Returns the coordinates of the left border (for blue) or the top border (for red)"""
        if color == HexBoard.BLUE:
            return [(0, i) for i in range(self.size)]
        else:
            return [(i, 0) for i in range(self.size)]
            
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
        code = str(color)
        for x in range(self.size):
            for y in range(self.size):
                code += str(self.board[x, y])
        
        return int(code)