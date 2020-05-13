import torch
import yaml

from alphazero.src.games.hex import Hex
from alphazero.src.mcts import MCTS
from alphazero.src.nn.wrapper import ModelWrapper
from alphazero.src.trainer import AlphaZeroTrainer


def train():
    with open("alphazero/config.yaml", 'r') as f:
        config = yaml.safe_load(f)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Running on device: %s" % device)

    game = Hex(**config['GAME'])
    mcts = MCTS(**config['MCTS'])
    model_wrapper = ModelWrapper(game, device, **config['NN'])

    trainer = AlphaZeroTrainer(model_wrapper, game, mcts, **config['AZ'])
    loss = trainer.train(game, device, **config['NN'])
