import os
import random

import gym
import numpy as np
import tensorflow as tf

from dqn import fit_batch
from model import atari_model
from ring_buf import RingBuf
from train import choose_best_action, get_epsilon_for_iteration, load_random_samples
from util import Namespace, preprocess, progressbar, transform_reward

env = gym.make('BreakoutDeterministic-v4')

model_path = 'model.h5'
if os.path.isfile(model_path): model = tf.keras.models.load_model(model_path)
else: model = atari_model(4)

args = Namespace(
    num_total_steps = 20000,
    num_random_samples = 50000,
    gamma = 0.99,
    batch_size = 32,
    log_every_n_steps = 500,
    replay_buffer_size = 10**6
)

replay_buffer = RingBuf(args.replay_buffer_size)

env, replay_buffer = load_random_samples(env, replay_buffer)

def q_iteration(env, model, state, iteration, replay_buffer):
    # Choose epsilon based on the iteration
    epsilon = get_epsilon_for_iteration(iteration, args.num_total_steps)

    # Choose the action 
    if random.random() < epsilon:
        action = env.action_space.sample()
        # print('Random action: %d' % action)
    else:
        action = choose_best_action(model, state)
        print('Greedy action: %d' % action)

    # Play one game iteration (note: according to the next paper, you should actually play 4 times here)
    new_frame, reward, is_done, _ = env.step(action)
    replay_buffer.append((state, action, new_frame, reward, is_done))

    # Sample and fit
    batch = replay_buffer.sample_batch(args.batch_size)
    fit_batch(model, args.gamma, batch)

    return new_frame, reward, is_done

frame = env.reset()
last_four_frames = [preprocess(frame)] * 4

is_done = False
iteration = 0
total_reward = 0
for i in progressbar(range(args.num_total_steps), desc="Training"):
    state = last_four_frames

    new_frame, reward, is_done = q_iteration(env, model, state, iteration, replay_buffer)

    last_four_frames.pop(0)
    last_four_frames.append(preprocess(new_frame))

    total_reward += reward
    iteration += 1
    
    if is_done:
        frame = env.reset()
        last_four_frames = [preprocess(frame)] * 4

    if i % args.log_every_n_steps == 0:
        print('Avg reward: %.2f' % (total_reward / args.log_every_n_steps))
        total_reward = 0

        model.save(model_path)
