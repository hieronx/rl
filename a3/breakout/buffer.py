import os
import pickle
from collections import deque

import numpy as np

from breakout.util import preprocess, progressbar


def create_and_prefill_buffer(env, args):
    """Create the deque and prefill the buffer either from disk or by creating random samples"""
    replay_buffer = ReplayBuffer(int(args.num_total_steps * args.replay_buffer_perc))
    replay_buffer = load_random_samples(env, replay_buffer, args)
    return replay_buffer

def load_random_samples(env, replay_buffer, args):
    """
    Loads the random samples. Depending on the arguments this will either generate/overwrite
    new random samples and pickle them, or it will load the pickled random samples.

    The environment is also given to this function because it needs it to generate random sample data.
    """
    random_samples_path = 'breakout/random_samples.p'
   
    if not args.overwrite_random_samples and os.path.isfile(random_samples_path):
        print("Loading random samples from cache...")
        with open(random_samples_path, "rb") as f:
            replay_buffer = pickle.load(f)

    else:
        state = create_play_history(env)

        for _ in progressbar(range(int(args.num_total_steps * args.perc_initial_random_samples)), desc="Generating random samples"):
            action = env.action_space.sample()

            new_frame, reward, is_done, _ = env.step(action)
            proc_frame = preprocess(new_frame)
            replay_buffer.append(state, action, proc_frame, reward, is_done)

            state.append(proc_frame)

            if is_done: frame = env.reset()
        
        with open(random_samples_path, "wb") as training_data_file:
            pickle.dump(replay_buffer, training_data_file, protocol=pickle.HIGHEST_PROTOCOL)

    env.reset()
    return replay_buffer


def create_play_history(env):
    """Creates a simple queue of the last four frames"""
    frame = env.reset()
    return deque([preprocess(frame)] * 4, maxlen=4)

class ReplayBuffer:

    def __init__(self, size):
        self.start_states = deque([], maxlen=size)
        self.actions = deque([], maxlen=size)
        self.next_frames = deque([], maxlen=size)
        self.rewards = deque([], maxlen=size)
        self.is_dones = deque([], maxlen=size)
        self.size = 0

    def append(self, state, action, proc_frame, reward, is_done):
        self.start_states.append(state)
        self.actions.append(action)
        self.next_frames.append(proc_frame)
        self.rewards.append(reward)
        self.is_dones.append(is_done)
        self.size = len(self.actions)
