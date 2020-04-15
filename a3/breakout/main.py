import os
import pickle
import random

import gym

from dqn import fit_batch
from model import atari_model
from ring_buf import RingBuf
from util import preprocess, progressbar, transform_reward

env = gym.make('BreakoutDeterministic-v4')

model = atari_model(4)
memory = RingBuf(1000000)

def load_training_data(env, memory):
    if os.path.isfile("training_data.p"):
        print("Loading training data from cache...")
        with open("training_data.p", "rb") as f:
            memory = pickle.load(f)

    else:
        frame = env.reset()
        last_four_frames = [preprocess(frame)] * 4

        for _ in progressbar(range(50000), desc="Generating training data"):
            state = last_four_frames
            action = env.action_space.sample()

            new_frame, reward, is_done, _ = env.step(action)
            memory.append((state, action, new_frame, reward, is_done))

            last_four_frames.pop(0)
            last_four_frames.append(preprocess(new_frame))

            if is_done: frame = env.reset()
        
        with open("training_data.p", "wb") as training_data_file:
            pickle.dump(memory, training_data_file)

    env.reset()
    return env, memory

env, memory = load_training_data(env, memory)

assert(len(memory) == 50000)

frame = env.reset()

def get_epsilon_for_iteration(iteration):
    if iteration > 1000000: return 0.1
    else: return 0.9 * (1.0 - (iteration / 1000000)) + 0.1

def choose_best_action(model, state):
    Q_values = model.predict([state, np.ones(actions.shape)])
    return np.max(Q_values, axis=1)

def q_iteration(env, model, state, iteration, memory):
    # Choose epsilon based on the iteration
    epsilon = get_epsilon_for_iteration(iteration)

    # Choose the action 
    if random.random() < epsilon:
        action = env.action_space.sample()
    else:
        action = choose_best_action(model, state)

    # Play one game iteration (note: according to the next paper, you should actually play 4 times here)
    new_frame, reward, is_done, _ = env.step(action)
    memory.append((state, action, new_frame, reward, is_done))

    # Sample and fit
    batch = memory.sample_batch(32)
    fit_batch(model, 0.99, batch)

    return new_frame, reward, is_done

num_training_steps = 100000
frame = env.reset()
last_four_frames = [preprocess(frame)] * 4

is_done = False
iteration = 0
total_reward = 0
for i in progressbar(range(num_training_steps), desc="Training"):
    state = last_four_frames

    new_frame, reward, is_done = q_iteration(env, model, state, iteration, memory)

    last_four_frames.pop(0)
    last_four_frames.append(preprocess(new_frame))

    total_reward += reward
    iteration += 1
    
    if is_done:
        frame = env.reset()
        last_four_frames = [preprocess(frame)] * 4
        iteration = 0

    if i % 100 == 0:
        print('Avg reward: %.2f' % (total_reward / 100))
        total_reward = 0
