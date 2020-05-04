import numpy as np

from alphazero import Arena
from alphazero.hex.HexGame import AZHexGame
from alphazero.hex.HexPlayers import *
from alphazero.hex.NNet import NNetWrapper as NNet
from alphazero.MCTS import MCTS
from alphazero.utils import *


"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

def play():
    human_vs_cpu = True

    g = AZHexGame(7)

    # all players
    rp = RandomPlayer(g).play
    gp = GreedyHexPlayer(g).play
    hp = HumanHexPlayer(g).play

    checkpoint_filename = "best_backup.pth.tar"

    # nnet players
    n1 = NNet(g)
    n1.load_checkpoint("./temp", checkpoint_filename)

    args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
    mcts1 = MCTS(g, n1, args1)
    n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

    if human_vs_cpu:
        player2 = hp
    else:
        n2 = NNet(g)
        n2.load_checkpoint("./temp" , checkpoint_filename)


        args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
        mcts2 = MCTS(g, n2, args2)
        n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

        player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

    arena = Arena.Arena(n1p, player2, g, display=AZHexGame.display)

    print(arena.playGames(2, verbose=True))
