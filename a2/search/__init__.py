from util.hexboard import HexBoard

class HexSearchMethod:
        
    def get_next_move(self, board, color):
        raise NotImplementedError
    
    def get_possible_moves(self, board):
        """Compiles a list of all empty hexes in the current hexboard"""
        raise DeprecationWarning
    
        if board.get_winner() is not None: return []
        return [coord for coord, color in board.board.items() if color == HexBoard.EMPTY]