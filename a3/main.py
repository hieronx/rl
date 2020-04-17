import argparse
import logging
import sys

from breakout.train import train as train_breakout

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

    args = parser.parse_args(sys.argv[1:])

    # Train command
    if args.command == 'train':
        if args.game == 'breakout':
            train_breakout(args)
