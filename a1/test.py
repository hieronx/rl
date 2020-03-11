import unittest
import random
import time

from hexboard import HexBoard
from minimax import Minimax
from evaluate import Evaluate

class TestHexMinimax(unittest.TestCase):
    """All unit tests used to determine if the code we wrote is still running as intended"""

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

    def test_game_win(self):
        """Checks if the detection for gameover states is working as expected by filling all hexes with one color"""
        board = HexBoard(3)

        board.board[(1, 0)] = HexBoard.RED
        board.board[(2, 0)] = HexBoard.BLUE
        self.assertEqual(board.check_win(HexBoard.RED), False)
        self.assertEqual(board.check_win(HexBoard.BLUE), False)
        self.assertEqual(board.check_draw(), False)

    def test_source_coordinates(self):
        """Let's see if the source coordinates are all correct and as we think they should be"""
        board = HexBoard(4)
        source_coordinates = board.get_source_coordinates(HexBoard.RED)
        actual_sources = [(0, 0), (1, 0), (2, 0), (3, 0)]

        for actual_source in actual_sources:
            self.assertTrue(actual_source in source_coordinates)

    def test_target_coordinates(self):
        """Does the same thing as test_source coordinates, only checks for the target coordinates"""
        board = HexBoard(4)
        target_coordinates = board.get_target_coordinates(HexBoard.RED)
        actual_targets = [(0, 3), (1, 3), (2, 3), (3,3)]

        for actual_target in actual_targets:
            self.assertTrue(actual_target in target_coordinates)

    def test_minimax(self):
        """"Tests to see if minimax returns the expected best moves for specific board states"""
        evaluate = Evaluate('Dijkstra')
        board = HexBoard(3)

        board.board[(0, 0)] = HexBoard.RED
        board.board[(0, 1)] = HexBoard.RED

        self.assertFalse(board.game_over())

        minimax = Minimax(3, 3, None, evaluate, False)
        move = minimax.get_next_move(board, HexBoard.RED)
        self.assertEqual(move, (0, 2))

    def test_minimax_top_left(self):
        """"Another scenario which tests a specific minimax scenario"""
        evaluate = Evaluate('Dijkstra')
        board = HexBoard(4)

        board.board[(1, 0)] = HexBoard.RED
        board.board[(1, 1)] = HexBoard.RED
        board.board[(1, 2)] = HexBoard.RED
        board.board[(0, 1)] = HexBoard.BLUE
        board.board[(0, 2)] = HexBoard.BLUE
        board.board[(0, 3)] = HexBoard.BLUE

        good_board = board.make_move((1, 3), HexBoard.RED)
        eval_good_board = evaluate.evaluate_board(good_board, HexBoard.RED)

        bad_board = board.make_move((0, 0), HexBoard.RED)
        eval_bad_board = evaluate.evaluate_board(bad_board, HexBoard.RED)

        self.assertTrue(eval_good_board > eval_bad_board)

        minimax = Minimax(4, 3, None, evaluate, False)
        move = minimax.get_next_move(board, HexBoard.RED)
        self.assertEqual(move, (1, 3))

    def test_dijkstra(self):
        """First scenario to see if dijkstra returns sane data"""
        evaluate = Evaluate('Dijkstra')
        board = HexBoard(3)

        board.board[(0, 0)] = HexBoard.BLUE
        board.board[(1, 0)] = HexBoard.BLUE

        self.assertEqual(evaluate.dijkstra(board, (0,0), [(2,0)], HexBoard.BLUE, HexBoard.RED), 1)

    def test_astar_second_row(self):
        """Another test scenario to see if AStar returns the correct path length"""
        evaluate = Evaluate('AStar')
        board = HexBoard(4)

        board.board[(1, 0)] = HexBoard.RED
        board.board[(2, 0)] = HexBoard.RED
        board.board[(3, 0)] = HexBoard.RED
        board.board[(0, 2)] = HexBoard.RED

        board.board[(1, 1)] = HexBoard.BLUE
        board.board[(2, 1)] = HexBoard.BLUE
        board.board[(3, 1)] = HexBoard.BLUE

        self.assertEqual(evaluate.astar(board, (0, 1), [(3, 1)], HexBoard.BLUE, HexBoard.RED), 1)
        self.assertEqual(evaluate.astar(board, (0, 0), [(0, 3)], HexBoard.RED, HexBoard.BLUE), 3)
        self.assertEqual(evaluate.astar(board, (3, 0), [(0, 3)], HexBoard.RED, HexBoard.BLUE), 2)

        minimax = Minimax(3, 2, None, evaluate, False)
        move = minimax.get_next_move(board, HexBoard.RED)
        self.assertEqual(move, (0, 1))

    def test_board_evaluation(self):
        """Checks to see if the board evaluation returns the expected result in several synthetic board states"""
        evaluate = Evaluate('Dijkstra')
        board = HexBoard(3)
        
        board.board[(0, 0)] = HexBoard.BLUE
        board.board[(1, 0)] = HexBoard.BLUE

        self.assertTrue(evaluate.evaluate_board(board, HexBoard.BLUE) > evaluate.evaluate_board(board, HexBoard.RED))

        board = HexBoard(3)

        board.board[(0, 0)] = HexBoard.RED
        board.board[(0, 1)] = HexBoard.RED

        self.assertTrue(evaluate.evaluate_board(board, HexBoard.RED) > evaluate.evaluate_board(board, HexBoard.BLUE))

    def test_hash_code(self):
        """Makes sure the hashcode that we're generating is indeed what we expect it to be"""
        board = HexBoard(3)

        board.board[(0, 0)] = HexBoard.RED
        board.board[(1, 2)] = HexBoard.BLUE

        self.assertEqual(board.hash_code(HexBoard.BLUE), 3331333321)
        self.assertEqual(board.hash_code(HexBoard.RED), 3331333322)

    def test_tp_table(self):
        """Tests if the transposition table is working as intended"""
        evaluate = Evaluate('Dijkstra')
        board = HexBoard(3)
        minimax = Minimax(3, 3, None, evaluate, False)

        board.board[(0, 0)] = HexBoard.RED
        board.board[(0, 1)] = HexBoard.RED
        self.assertEqual(minimax.tp_table, {})
        
        move = minimax.get_next_move(board, HexBoard.RED)
        self.assertTrue(len(minimax.tp_table) > 0)
    

if __name__ == '__main__':
    unittest.main()
