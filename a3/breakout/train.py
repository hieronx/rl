import os
import random
import statistics
from collections import deque

import gym
import numpy as np
import tensorflow as tf

from breakout.buffer import create_and_prefill_buffer, load_random_samples
from breakout.dqn import fit_batch
from breakout.model import create_models
from breakout.util import Namespace, copy_model, get_epsilon_for_iteration, preprocess, progressbar


def train(args):
    # Initialize environment, model, and replay buffer
    env = gym.make('BreakoutDeterministic-v4')

    model_path = 'breakout/model.h5'
    model, target_model = create_models(model_path)

    replay_buffer = create_and_prefill_buffer(env, args)

    # Copy the initial frame 4 times and store this as the initial state
    frame = env.reset()
    state = deque([preprocess(frame)] * 4, maxlen=4)

    # Reset statistics
    is_done = False
    running_game_scores = deque([], maxlen=int(100))
    total_game_score = 0
    num_games_played = 0
    current_game_score = 0

    # Determine number of no-op actions to take at the start of the first game,
    # which is between 0 and the max value.
    no_op_actions = random.randint(0, args.max_no_op_actions)

    # Run the training loop
    for iteration in progressbar(range(args.num_total_steps), desc="Training"):
        # Play n steps, based on the update frequency
        for _ in range(args.update_frequency):
            if no_op_actions > 0:
                # Don't do anything
                new_frame, _, is_done, _ = env.step(0)
                no_op_actions -= 1

            else:
                # Choose action using epsilon-greedy approach
                epsilon = get_epsilon_for_iteration(iteration, args.num_total_steps)

                if random.random() < epsilon: action = env.action_space.sample()
                else: action = predict_max_q_action(model, state)

                # Play action and store in replay buffer
                new_frame, reward, is_done, _ = env.step(action)
                replay_buffer.append((state, action, preprocess(new_frame), reward, is_done))

                current_game_score += reward

            # Render the GUI
            if args.render: env.render()

            if is_done:
                # Reset the state and statistics
                frame = env.reset()
                state = deque([preprocess(frame)] * 4, maxlen=4)

                num_games_played += 1
                running_game_scores.append(current_game_score)
                print('Ended game %d with score %d, running average is %.2f' % (num_games_played, current_game_score, statistics.mean(running_game_scores)))
                total_game_score += current_game_score
                current_game_score = 0

                # Re-calculate the number of no-op actions for the next game
                no_op_actions = random.randint(0, args.max_no_op_actions)
            else:
                # If the game isn't done yet, save the frame in the state (removing the first one)
                state.append(preprocess(frame))

        # Sample a minibatch and perform SGD updates
        # TODO: speed up based on https://github.com/keras-rl/keras-rl/blob/216c3145f3dc4d17877be26ca2185ce7db462bad/rl/memory.py#L30
        random_batch = [random.choice(replay_buffer) for _ in range(args.batch_size)]
        fit_batch(model, target_model, args.gamma, random_batch)

        if iteration > 0 and iteration % args.backup_target_model_every_n_steps == 0:
            target_model = copy_model(model, model_path)
