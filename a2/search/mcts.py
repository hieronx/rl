import logging
import random

from . import HexSearchMethod

logger = logging.getLogger(__name__)

class MCTS(HexSearchMethod):
    """This object houses all the code necessary for the MCTS implementation"""

    def __init__(self, N, Cp, size, evaluate_class, live_play = True):
        self.N = N
        self.Cp = Cp
        self.size = size
        self.evaluate_class = evaluate_class
        self.live_play = live_play

    def get_next_move(self, board, color):
        for _ in range(self.N):
            move = self.get_possible_moves(board)[0] # TODO: selection step

            new_board = board.make_move(move, color)
            self.simulate(new_board, color, board.get_opposite_color(color))

            # TODO: Backpropagation step

    def simulate(self, board, color, opposite_color):
        """Simulates a board until a terminal node is reached"""
        
        moves = self.get_possible_moves(board)
        move = None
        player = color
        while not board.game_over():
            move = random.choice(moves)
            moves.remove(move)
            
            board.board[move] = player
            player = color if player != color else opposite_color

        if board.check_draw() or (board.check_win(color) and board.check_win(opposite_color)): return 0
        if board.check_win(color): return 1
        if board.check_win(opposite_color): return -1

        logger.critical('Oops, this should not have happened.')


                
        #     Loop Forever:

        # if Si is a terminal state:

        #    return Value(Si)

        # Ai = random(available_actions(Si))

        # Si = Simulate(Si, Ai)

        # This loop will run forever until you reach a terminal state.

    