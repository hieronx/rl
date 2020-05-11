import torch
import yaml

from src.games.Hex import Hex
from src.MCTS import MCTS
from src.NN import NetWrapper
from src.Player import *

with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Running on device: %s" % device)

game = Hex(**config['GAME'])
nn1 = NetWrapper(game, device, lr=0.01, wd=0.015, **config['NN'])
nn1.load_model("models/1589203166.pt")

mcts = MCTS(**config['MCTS'])

play_game(game, p1 =  AlphaZeroPlayer(nn1, mcts), p2 =  HumanPlayer(), print_b = True)
#player_vs_player(game, p1 =  AlphaZeroPlayer(nn, mcts),  p2 =  AlphaZeroPlayer(nn1, mcts), n_games = 100, treshold = 0.5, print_b = False)
