import argparse
import logging
import sys

import tensorflow as tf
from tensorflow.python.client import device_lib

from breakout.train import train as train_breakout
from mountaincar.train import train as train_mountain_car

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt = '%H:%M:%S',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    """Main entry point of the code. Below we describe all the different argument possibilities"""
    parser = argparse.ArgumentParser(description="Deep-Q-learning implementation for Atari games")
    commands = parser.add_subparsers(dest='command')

    train = commands.add_parser('train', help='Train the DQN algorithm')
    game_sp = train.add_subparsers(dest='game')

    breakout_train_command = game_sp.add_parser('breakout', help='Train the DQN algorithm for Breakout')
    breakout_train_command.add_argument('--num-total-steps', type=int, default=20000, help='Set the number of training iterations')
    breakout_train_command.add_argument('--backup-target-model-every-n-steps', type=int, default=1000, help='Duplicate the CNN model every n steps to create a new target network')
    breakout_train_command.add_argument('--perc-initial-random-samples', type=float, default=0.005, help='%% of initial random samples')
    breakout_train_command.add_argument('--gamma', type=float, default=0.99, help='Discount factor for Q estimation function')
    breakout_train_command.add_argument('--batch-size', type=int, default=32, help='Batch size')
    breakout_train_command.add_argument('--log-every-n-steps', type=int, default=500, help='Print statistics every n iterations')
    breakout_train_command.add_argument('--replay-buffer-perc', type=float, default=0.10, help='%% of the replay buffer compared to the total number of steps')
    breakout_train_command.add_argument('--overwrite-random-samples', action='store_true', help='Overwrite the random samples if they were already cached')
    breakout_train_command.add_argument('--update-frequency', type=int, default=4, help='Run n steps for every DQN batch fit')
    breakout_train_command.add_argument('--render', action='store_true', help='Show the GUI while training')
    breakout_train_command.add_argument('--max-no-op-actions', type=int, default=30, help='Maximum number of no-op actions to take at the start of every game')

    mountain_car_train_command = game_sp.add_parser('mountain-car', help='Train the DQN algorithm for Mountain Car')
    mountain_car_train_command.add_argument('--score-requirement', type=int, default=-198, help='Set the minimum score requirement')
    mountain_car_train_command.add_argument('--num-games-train', type=int, default=10000, help='Set the number of games played for training')
    mountain_car_train_command.add_argument('--num-games-eval', type=int, default=100, help='Set the number of games played for evaluation')
    mountain_car_train_command.add_argument('--steps-per-game-train', type=int, default=200, help='Set the number of max steps played per game during training')
    mountain_car_train_command.add_argument('--steps-per-game-eval', type=int, default=200, help='Set the number of max steps played per game during evaluation')
    mountain_car_train_command.add_argument('--num-threads', type=int, default=10, help='Set the number of threads')

    args = parser.parse_args(sys.argv[1:])

    if tf.__version__[:4] != 1.15:
        logger.critical('Requires Tensorflow 1.15')
        exit()

    # Train command
    if args.command == 'train':
        logger.info('Using GPU: %s' % str(tf.test.is_gpu_available()))
        logger.info('GPU devices: %s' % str([device.name for device in device_lib.list_local_devices()]))

        if args.game == 'breakout':
            train_breakout(args)
        elif args.game == 'mountain-car':
            train_mountain_car(args)
