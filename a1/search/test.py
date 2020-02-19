import unittest
import numpy as np

from hexboard import HexBoard
from minimax import Minimax
from evaluate import Evaluate

class TestHexMinimax(unittest.TestCase):

    def test_win_detection(self):
        for i in range(0, 2):
            winner = HexBoard.RED if i == 0 else HexBoard.BLUE
            looser = HexBoard.BLUE if i == 0 else HexBoard.RED
            board = HexBoard(3)

            board.place((1, 1), looser)
            board.place((2, 1), looser)
            board.place((1, 2), looser)
            board.place((2, 2), looser)
            board.place((0, 0), winner)
            board.place((1, 0), winner)
            board.place((2, 0), winner)
            board.place((0, 1), winner)
            board.place((0, 2), winner)

            self.assertEqual(board.check_win(winner), True)
            self.assertEqual(board.check_win(looser), False)

    def test_game_end(self):
        endable_board = HexBoard(4)

        while not endable_board.game_over:
            endable_board.place(
                (np.random.randint(0, 4), np.random.randint(0, 4)), HexBoard.RED)

        self.assertEqual(endable_board.game_over, True)
        self.assertEqual(endable_board.check_win(HexBoard.RED), True)
        self.assertEqual(endable_board.check_win(HexBoard.BLUE), False)

    def test_source_coordinates(self):
        board_size = np.random.randint(2, 8)

        board = HexBoard(board_size)
        source_coordinates = board.get_source_coordinates(HexBoard.BLUE)

        source_coordinates_correct_len = board_size
        self.assertEqual(len(source_coordinates),
                         source_coordinates_correct_len)

    def test_target_coordinates(self):
        board_size = np.random.randint(2, 8)

        board = HexBoard(board_size)
        target_coordinates = board.get_target_coordinates(HexBoard.BLUE)

        target_coordinates_correct_len = board_size
        self.assertEqual(len(target_coordinates),
                         target_coordinates_correct_len)

    def test_possible_moves(self):
        evaluate = Evaluate('random')
        minimax = Minimax(2, 1, evaluate)

        board = HexBoard(2)
        possible_moves = minimax.get_possible_moves(board)
        possible_moves_correct_len = 4

        self.assertEqual(len(possible_moves), possible_moves_correct_len)

    def test_minimax(self):
        evaluate = Evaluate('Dijkstra')
        board = HexBoard(3)

        board.place((0, 0), HexBoard.RED)
        board.place((0, 1), HexBoard.RED)

        self.assertFalse(board.game_over)

        minimax = Minimax(3, 3, evaluate, False)
        move = minimax.get_next_move(board, HexBoard.RED)
        self.assertEqual(move, (0, 2))

    def test_board_evaluation(self):
        evaluate = Evaluate('Dijkstra')
        board = HexBoard(3)
        
        print("Empty board costs:")
        evaluate.evaluate_board(board, HexBoard.BLUE)
        board.place((0, 0), HexBoard.BLUE)
        print("First move by blue:")
        evaluate.evaluate_board(board, HexBoard.BLUE)
        board.place((1, 0), HexBoard.BLUE)
        print("Second move from blue:")
        evaluate.evaluate_board(board, HexBoard.BLUE)
        print("Final outcome")
        board.print()

        self.assertTrue(evaluate.evaluate_board(board, HexBoard.BLUE) < evaluate.evaluate_board(board, HexBoard.RED))

        board = HexBoard(3)

        board.place((0, 0), HexBoard.RED)
        board.place((0, 1), HexBoard.RED)
        board.place((0, 2), HexBoard.RED)

        self.assertTrue(evaluate.evaluate_board(board, HexBoard.RED) < evaluate.evaluate_board(board, HexBoard.BLUE))

    def test_hash_code(self):
        board = HexBoard(3)

        board.place((0, 0), HexBoard.RED)
        board.place((1, 2), HexBoard.BLUE)

        self.assertEqual(board.hash_code(), 233331333)

    def test_tp_table(self):
        evaluate = Evaluate('Dijkstra')
        board = HexBoard(3)
        minimax = Minimax(3, 3, evaluate, False)

        board.place((0, 0), HexBoard.RED)
        board.place((0, 1), HexBoard.RED)
        self.assertEqual(minimax.tp_table, {})
        
        move = minimax.get_next_move(board, HexBoard.RED)
        self.assertTrue(len(minimax.tp_table) > 0)


if __name__ == '__main__':
    unittest.main()
