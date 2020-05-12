import torch
import yaml

from src.gameplay.logic import play_game, player_vs_player
from src.gameplay.players import AlphaZeroPlayer, HumanPlayer
from src.games.Hex import Hex
from src.mcts import MCTS
from src.nn.wrapper import ModelWrapper

with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Running on device: %s" % device)

game = Hex(**config['GAME'])
nn1 = ModelWrapper(game, device, **config['NN'])
nn1.load_model("tests/best_after_6_hours.pt")
nn2 = ModelWrapper(game, device, **config['NN'])
nn2.load_model("tests/best_after_29_ep.pt")

mcts1 = MCTS(**config['MCTS'])
mcts2 = MCTS(**config['MCTS'])

#play_game(game, p1 =  AlphaZeroPlayer(nn1, mcts), p2 =  HumanPlayer(), print_b = True)
player_vs_player(game, p1 =  AlphaZeroPlayer(nn1, mcts1),  p2 =  AlphaZeroPlayer(nn2, mcts2), n_games = 100, treshold = 0.5, print_b = False)
