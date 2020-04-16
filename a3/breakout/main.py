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
from util import Namespace, copy_model, preprocess, progressbar

print('Using GPU: %s' % str(tf.test.is_gpu_available()))
print('GPU devices: %s' % str([device.name for device in device_lib.list_local_devices()]))

env = gym.make('BreakoutDeterministic-v4')

model_path = 'model.h5'
if os.path.isfile(model_path): model = tf.keras.models.load_model(model_path)
else: model = atari_model(4)
target_model = copy_model(model, 'model.h5')

args = Namespace(
    num_total_steps = 20000,
    backup_target_model_every_n_steps = 1000,
    perc_initial_random_samples = 0.005,
    gamma = 0.99,
    batch_size = 32,
    log_every_n_steps = 500,
    replay_buffer_perc = 0.10,
    overwrite_random_samples = True,
    update_frequence = 4,
    render = False,
    max_no_op_actions = 30
)

replay_buffer = deque(maxlen=int(args.num_total_steps * args.replay_buffer_perc))
env, replay_buffer = load_random_samples(env, replay_buffer, args)

frame = env.reset()
last_four_frames = [preprocess(frame)] * 4

is_done = False
total_game_score = 0
num_games_played = 0
current_game_score = 0
no_op_actions = random.randint(0, args.max_no_op_actions)
for iteration in progressbar(range(args.num_total_steps), desc="Training"):
    # Play n steps
    for _ in range(args.update_frequence):
        state = last_four_frames

        if no_op_actions > 0:
            new_frame, _, is_done, _ = env.step(0)
            no_op_actions -= 1

        else:
            epsilon = get_epsilon_for_iteration(iteration, args.num_total_steps)

            if random.random() < epsilon: action = env.action_space.sample()
            else: action = choose_best_action(model, state)

            new_frame, reward, is_done, _ = env.step(action)
            replay_buffer.append((state, action, new_frame, reward, is_done))

            current_game_score += reward

        if args.render: env.render()

        if is_done:
            frame = env.reset()
            last_four_frames = [preprocess(frame)] * 4

            num_games_played += 1
            print('Ended game %d with score %d' % (num_games_played, current_game_score))
            total_game_score += current_game_score
            current_game_score = 0

            no_op_actions = random.randint(0, args.max_no_op_actions)
        else:
            last_four_frames.pop(0)
            last_four_frames.append(preprocess(new_frame))

    # Sample a minibatch and perform SGD updates
    random_batch = [random.choice(replay_buffer) for _ in range(args.batch_size)]
    fit_batch(model, target_model, args.gamma, random_batch)

    if iteration > 0 and iteration % args.backup_target_model_every_n_steps == 0:
        target_model = copy_model(model, 'model.h5')

    if iteration > 0 and iteration % (args.log_every_n_steps // args.update_frequence) == 0:
        # print('Average reward: %.2f' % (total_reward / (args.log_every_n_steps // args.update_frequence)))
        # total_reward = 0

        model.save(model_path)
