import os
import random
from collections import deque

import gym
import numpy as np
import tensorflow as tf
from tensorflow.python.client import device_lib

from dqn import fit_batch
from model import atari_model
from train import choose_best_action, get_epsilon_for_iteration, load_random_samples
from util import Namespace, preprocess, progressbar, sample_batch, transform_reward

print('Using GPU: %s' % str(tf.test.is_gpu_available()))
print('GPU devices: %s' % str([device.name for device in device_lib.list_local_devices()]))

env = gym.make('BreakoutDeterministic-v4')

model_path = 'model.h5'
if os.path.isfile(model_path): model = tf.keras.models.load_model(model_path)
else: model = atari_model(4)

args = Namespace(
    num_total_steps = 20000,
    perc_initial_random_samples = 0.005,
    gamma = 0.99,
    batch_size = 32,
    log_every_n_steps = 500,
    replay_buffer_perc = 0.10,
    overwrite_random_samples = False,
    update_frequence = 4,
    render = True
)

replay_buffer = deque(maxlen=int(args.num_total_steps * args.replay_buffer_perc))
env, replay_buffer = load_random_samples(env, replay_buffer, args)

frame = env.reset()
last_four_frames = [preprocess(frame)] * 4

is_done = False
total_game_score = 0
num_games_played = 0
current_game_score = 0
for iteration in progressbar(range(args.num_total_steps), desc="Training"):
    # Play n steps
    for _ in range(args.update_frequence):
        state = last_four_frames
        epsilon = get_epsilon_for_iteration(iteration, args.num_total_steps)

        if random.random() < epsilon: action = env.action_space.sample()
        else: action = choose_best_action(model, state)
        
        # TODO: implement no-op max

        # Play one game iteration (note: according to the next paper, you should actually play 4 times here)
        new_frame, reward, is_done, _ = env.step(action)
        replay_buffer.append((state, action, new_frame, transform_reward(reward), is_done))

        current_game_score += transform_reward(reward)

        if reward < 0.0:
            print('STOPP!!!!!!')
            print(reward)
            exit()

        if args.render: env.render()

        if is_done:
            frame = env.reset()
            last_four_frames = [preprocess(frame)] * 4

            num_games_played += 1
            print('Ended game %d with score %d' % (num_games_played, current_game_score))
            total_game_score += current_game_score
            current_game_score = 0
        else:
            last_four_frames.pop(0)
            last_four_frames.append(preprocess(new_frame))

    # Sample a minibatch and perform SGD updates
    fit_batch(model, args.gamma, sample_batch(replay_buffer, args.batch_size))

    if iteration > 0 and iteration % (args.log_every_n_steps // args.update_frequence) == 0:
        # print('Average reward: %.2f' % (total_reward / (args.log_every_n_steps // args.update_frequence)))
        # total_reward = 0

        model.save(model_path)
