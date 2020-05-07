from functools import lru_cache

import numpy as np

from alphazero.Game import Game
from util.hexboard import HexBoard


class AZHexGame(Game):

    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        # return initial board
        return HexBoard(self.n)

    @lru_cache(maxsize=4)
    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    @lru_cache(maxsize=4)
    def getActionSize(self):
        # return number of actions
        return self.n*self.n

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        color = HexBoard.RED if player == 1 else HexBoard.BLUE

        # TODO: might need to be reversed
        y = action % self.n
        x = (action - y) / self.n
        move = (int(x), int(y))

        new_board = board.make_move(move, color)
        return (new_board, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = np.zeros(self.getActionSize())
        legalMoves = board.get_possible_moves()

        for x, y in legalMoves:
            valids[self.n*x+y] = 1
        return valids

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        winner = board.get_winner()
        if winner is None: return 0

        player_col = HexBoard.RED if player == 1 else HexBoard.BLUE
        return 1 if player_col == winner else -1

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1

        # if len(board.get_possible_moves()) < 24:
        #     board.print()
        #     mir = board.get_mirrored_board()
        #     mir.print()
        #     print('----\n')
        #     # exit()

        return board.get_mirrored_board() if player == -1 else board

    def getOriginalForm(self, board, player):
        return board.get_unmirrored_board() if player == -1 else board

    def getSymmetries(self, board, pi):
        # mirror, rotational

        # TODO: implement symmetrical board here
        # return [(board, pi)]

        board = board.as_np()
        pi_board = np.reshape(pi, (self.n, self.n))
        # print(pi)

        # From left to right
        lr_board = np.fliplr(board)
        lr_pi = np.fliplr(pi_board)

        # From top to bottom
        ud_board = np.flipud(board)
        ud_pi = np.flipud(pi_board)

        # 180 degrees rotation
        rotated_board = np.rot90(board, 2)
        rotated_pi = np.rot90(pi_board, 2)

        li = [(lr_board, lr_pi), (ud_board, ud_pi), (rotated_board, rotated_pi)]
        li = [(board, list(pi_new.ravel())) for board, pi_new in li]

        return li
        
    def stringRepresentation(self, board):
        return str(board)

    def stringRepresentationReadable(self, board):
        return str(board)

    def getScore(self, board, player):
        color = HexBoard.RED if player == 1 else HexBoard.BLUE
        
        winner = board.get_winner()
        if winner == color:
            print('Score: inf')
            return math.inf
        elif winner is not None:
            print('Score: -inf')
            return -math.inf
        else:
            print('Score: 0')
            return 0

    @staticmethod
    def display(board):
        board.print()
