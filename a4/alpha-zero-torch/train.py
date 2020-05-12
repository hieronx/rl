import torch
import yaml

from src.games.Hex import Hex
from src.mcts import MCTS
from src.nn.wrapper import ModelWrapper
from src.trainer import AlphaZeroTrainer

with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Running on device: %s" % device)

game = Hex(**config['GAME'])
mcts = MCTS(**config['MCTS'])
model_wrapper = ModelWrapper(game, device, **config['NN'])

trainer = AlphaZeroTrainer(model_wrapper, game, mcts, **config['AZ'])
loss = trainer.train(game, device, **config['NN'])
