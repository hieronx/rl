import optuna
import torch
import yaml

from src.AlphaZeroTrainer import AlphaZeroTrainer as az
from src.games.Hex import Hex
from src.MCTS import MCTS
from src.NN import NetWrapper
from src.Player import *

#{'lr': 0.012486799182525229, 'wd': 0.015010724465999522}.

with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Running on device: %s" % device)

game = Hex(**config['GAME'])
mcts = MCTS(**config['MCTS'])
nn = NetWrapper(game, device, lr=0.01, wd=0.015, **config['NN'])
#nn.load_model()


alphat = az(nn, game, mcts, **config['AZ'])
loss = alphat.train(game, device, lr=0.01, wd=0.015, **config['NN'])
