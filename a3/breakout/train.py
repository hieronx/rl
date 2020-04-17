import os
import random
import statistics

import gym
import numpy as np
import tensorflow as tf

from breakout.buffer import create_and_prefill_buffer, load_random_samples, create_last_four_frame_state
from breakout.dqn import fit_batch
from breakout.stats import Stats
from breakout.model import create_models, get_epsilon_greedy_action
from breakout.util import Namespace, copy_model, get_epsilon_for_iteration, preprocess, progressbar


def train(args):
    # Initialize environment, model, state, and replay buffer
    model_path = 'breakout/model.h5'
    env = gym.make('BreakoutDeterministic-v4')
    model, target_model = create_models(model_path)
    replay_buffer = create_and_prefill_buffer(env, args)
    state = create_last_four_frame_state(env)

    # Reset statistics and do a random spinup, idling for a random amount of time
    is_done = False
    stats = Stats()
    spinup_game(env, args)

    # Run the training loop
    for iteration in progressbar(range(args.num_total_steps), desc="Training"):
        # Play n steps, based on the update frequency
        for _ in range(args.update_frequency):
            action = get_epsilon_greedy_action(env, model, state, args, iteration)
            # Play action and store in replay buffer
            new_frame, reward, is_done, _ = env.step(action)
            replay_buffer.append((state, action, preprocess(new_frame), reward, is_done))
            stats.current_game_score += reward

            # Render the GUI
            if args.render: env.render()

            if is_done:
                # Reset the state and statistics, and do another random spinup time for the new game
                frame = env.reset()
                state = create_last_four_frame_state(env)
                stats.finished_game()
                spinup_game(env, args)

            else:
                # If the game isn't done yet, save the frame in the state (removing the first one)
                state.append(preprocess(frame))

        # Sample a minibatch and perform SGD updates
        # TODO: speed up based on https://github.com/keras-rl/keras-rl/blob/216c3145f3dc4d17877be26ca2185ce7db462bad/rl/memory.py#L30
        random_batch = [random.choice(replay_buffer) for _ in range(args.batch_size)]
        fit_batch(model, target_model, args.gamma, random_batch)

        if iteration > 0 and iteration % args.backup_target_model_every_n_steps == 0:
            target_model = copy_model(model, model_path)

def spinup_game(env, args):
    """Does a random amount of spinup with no-op actions"""
    for _ in range(random.randint(0, args.max_no_op_actions)):
        env.step(0)