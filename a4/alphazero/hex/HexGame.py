import numpy as np

from alphazero.Game import Game
from util.hexboard import HexBoard


class AZHexGame(Game):

    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        # return initial board
        return HexBoard(self.n)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        player = HexBoard.RED if player == 1 else HexBoard.BLUE

        # TODO: might need to be reversed
        y = action % self.n
        x = (action - y) / self.n
        move = (int(x), int(y))

        new_board = board.make_move(move, player)
        return (new_board, HexBoard.get_opposite_color(player))

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        player = HexBoard.RED if player == 1 else HexBoard.BLUE

        valids = [0]*self.getActionSize()
        
        legalMoves = board.get_possible_moves()

        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        
        for x, y in legalMoves:
            valids[self.n*x+y] = 1
        
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        player = HexBoard.RED if player == 1 else HexBoard.BLUE

        winner = board.get_winner()
        if winner == HexBoard.RED:
            return 1
        elif winner == HexBoard.BLUE:
            return -1
        else:
            return 0

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return board

    def getSymmetries(self, board, pi):
        # mirror, rotational

        # TODO: implement symmetrical board here
        return [(board, pi)]

        # board = board.as_np()

        # assert(len(pi) == self.n**2+1)  # 1 for pass
        # pi_board = np.reshape(pi[:-1], (self.n, self.n))
        # l = []

        # for i in range(1, 5):
        #     for j in [True, False]:
        #         newB = np.rot90(board, i)
        #         newPi = np.rot90(pi_board, i)
        #         if j:
        #             newB = np.fliplr(newB)
        #             newPi = np.fliplr(newPi)
        #         l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        # return l

    def stringRepresentation(self, board):
        return str(board)

    def stringRepresentationReadable(self, board):
        return str(board)

    def getScore(self, board, player):
        player = HexBoard.RED if player == 1 else HexBoard.BLUE
        
        if winner == player:
            return math.inf
        elif winner is not None:
            return -math.inf
        else:
            return 0

    @staticmethod
    def display(board):
        board.print()
