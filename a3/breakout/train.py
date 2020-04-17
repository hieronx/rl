import os
import random
import statistics

import gym
import numpy as np
import tensorflow as tf

from breakout.buffer import create_and_prefill_buffer, create_last_four_frame_state
from breakout.dqn import fit_batch
from breakout.model import copy_model, create_models, get_epsilon_greedy_action
from breakout.stats import Stats
from breakout.util import get_epsilon_for_iteration, preprocess, progressbar


def train(args):
    # Initialize environment, model, state, and replay buffer
    model_path = 'breakout/model.h5'
    stats = Stats()
    env = gym.make('BreakoutDeterministic-v4')
    model, target_model = create_models(model_path)
    replay_buffer = create_and_prefill_buffer(env, args)

    state = create_last_four_frame_state(env)
    is_done = spinup_game(env, args)

    # Run the training loop
    for iteration in progressbar(range(args.num_total_steps), desc="Training"):
        # Play n steps, based on the update frequency
        for _ in range(args.update_frequency):
            action = get_epsilon_greedy_action(env, model, state, args, iteration)

            # Play action and store in replay buffer
            new_frame, reward, is_done, info = env.step(action)

            stats.current_game_score += reward

            if stats.lives > info['ale.lives']: reward = -1
            stats.lives = info['ale.lives']

            replay_buffer.append((state, action, preprocess(new_frame), reward, is_done))

            if args.render: env.render()

            if is_done:
                state = create_last_four_frame_state(env)
                stats.finished_game()
                is_done = spinup_game(env, args)
            else:
                state.append(preprocess(new_frame))

        # Sample a minibatch and perform SGD updates
        random_batch_idx = random.sample(range(1, len(replay_buffer)), args.batch_size)
        fit_batch(model, target_model, args.gamma, random_batch_idx, replay_buffer)

        if iteration > 0 and iteration % args.backup_target_model_every_n_steps == 0:
            target_model = copy_model(model, model_path)

def spinup_game(env, args):
    """Does a random amount of spinup with no-op actions"""
    for _ in range(random.randint(0, args.max_no_op_actions)):
        env.step(0)
    
    return False
