import unittest
import random
import time

from util.hexboard import HexBoard
from search.minimax import Minimax
from evaluate.dijkstra import Dijkstra
from evaluate.astar import AStar

class TestUtil(unittest.TestCase):
    """All unit tests for util used to determine if the code we wrote is still running as intended"""

    def test_from_cache(self):
        board = HexBoard(3)
        board.board[(0,0)] = HexBoard.RED
        board.board[(1,1)] = HexBoard.BLUE
        board.board[(0,1)] = HexBoard.BLUE

        hash_code = board.hash_code()

        new_board = HexBoard.from_hash_code(hash_code)
        self.assertEqual(board.hash_code(), new_board.hash_code())

    def test_win_detection(self):
        """Checks if the detection for win states is working as expected by creating a win scenario"""
        for i in range(0, 2):
            winner = HexBoard.RED if i == 0 else HexBoard.BLUE
            looser = HexBoard.BLUE if i == 0 else HexBoard.RED
            board = HexBoard(3)

            board.board[(1, 1)] = looser
            board.board[(2, 1)] = looser
            board.board[(1, 2)] = looser
            board.board[(2, 2)] = looser
            board.board[(0, 0)] = winner
            board.board[(1, 0)] = winner
            board.board[(2, 0)] = winner
            board.board[(0, 1)] = winner
            board.board[(0, 2)] = winner

            self.assertEqual(board.check_win(winner), True)
            self.assertEqual(board.check_win(looser), False)

    def test_game_end(self):
        """Checks if the detection for gameover states is working as expected by filling all hexes with one color"""
        endable_board = HexBoard(4)

        while not endable_board.game_over():
            endable_board.board[(random.randint(0, 4), random.randint(0, 4))] = HexBoard.RED

        self.assertEqual(endable_board.game_over(), True)
        self.assertEqual(endable_board.check_win(HexBoard.RED), True)
        self.assertEqual(endable_board.check_win(HexBoard.BLUE), False)

    def test_weird_win_detection_edge_case(self):
        board = HexBoard(3)
        board.board[(2, 0)] = HexBoard.BLUE
        self.assertEqual(board.check_win(HexBoard.BLUE), False)

    def test_source_coordinates(self):
        """Let's see if the source coordinates are all correct and as we think they should be"""
        board = HexBoard(4)
        source_coordinates = board.source_coords[HexBoard.RED]
        actual_sources = [(0, 0), (1, 0), (2, 0), (3, 0)]

        for actual_source in actual_sources:
            self.assertTrue(actual_source in source_coordinates)

    def test_target_coordinates(self):
        """Does the same thing as test_source coordinates, only checks for the target coordinates"""
        board = HexBoard(4)
        target_coordinates = board.get_target_coordinates(HexBoard.RED, board.size)
        actual_targets = [(0, 3), (1, 3), (2, 3), (3,3)]

        for actual_target in actual_targets:
            self.assertTrue(actual_target in target_coordinates)

    def test_hash_code(self):
        """Makes sure the hashcode that we're generating is indeed what we expect it to be"""
        board = HexBoard(3)

        board.board[(0, 0)] = HexBoard.RED
        board.board[(1, 2)] = HexBoard.BLUE

        self.assertEqual(board.hash_code(HexBoard.BLUE), 3331333321)
        self.assertEqual(board.hash_code(HexBoard.RED), 3331333322)

    def test_reward(self):
        board = HexBoard(3)

        board.board[(0, 0)] = HexBoard.BLUE
        board.board[(1, 0)] = HexBoard.BLUE
        board.board[(2, 0)] = HexBoard.BLUE

        self.assertEqual(board.get_reward(HexBoard.BLUE), 1)

    def test_from_hash_code(self):
        board = HexBoard(3)

        board.board[(0, 0)] = HexBoard.RED
        board.board[(1, 2)] = HexBoard.BLUE

        self.assertEqual(board.hash_code(HexBoard.BLUE), 3331333321)

        new_board = HexBoard.from_hash_code(3331333321)
        self.assertEqual(new_board.hash_code(HexBoard.BLUE), 3331333321)

    def get_move_between_boards(self):
        board1 = HexBoard(3)
        board.board[(0, 0)] = HexBoard.RED

        board2 = HexBoard(3)
        board2.board[(0, 0)] = HexBoard.RED
        board2.board[(1, 2)] = HexBoard.BLUE

        self.assertEqual(board.get_move_between_boards(board2), (1, 2))



if __name__ == '__main__':
    unittest.main()
