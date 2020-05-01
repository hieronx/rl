from util.hexboard import HexBoard

class HexSearchMethod:
    """TODO: This class is probably not used anymore. Should be removed?"""


    def get_next_move(self, board, color):
        """This should not be used and thus raises an error"""
        raise NotImplementedError
    
    def get_possible_moves(self, board):
        """Compiles a list of all empty hexes in the current hexboard"""
        raise DeprecationWarning
    
        if board.get_winner() is not None: return []
        return [coord for coord, color in board.board.items() if color == HexBoard.EMPTY]