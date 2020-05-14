import unittest

from alphazero.src.games.hex import Hex
from util.hexboard import HexBoard

class TestHex(unittest.TestCase):
    """Have to write compulsive comments""" 

    def test_canonical_board_state(self):
       game = Hex(board_size = (7, 7))
       for i in range(5):
           game.play(i)
       game.print_board()
       
       board = HexBoard(7)
       board.from_np(game.get_canonical_board(), 7, 0).print()
        
       game.play(5)
       board.from_np(game.get_canonical_board(), 7, 0).print()
       
       game.play(6)
       board.from_np(game.get_canonical_board(), 7, 0).print()


   
if __name__ == '__main__':
    unittest.main()
