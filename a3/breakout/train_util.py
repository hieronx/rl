import os
import pickle

import numpy as np

from breakout.util import preprocess, progressbar

random_samples_path = 'breakout/random_samples.p'

def load_random_samples(env, replay_buffer, args):
    if not args.overwrite_random_samples and os.path.isfile(random_samples_path):
        print("Loading random samples from cache...")
        with open(random_samples_path, "rb") as f:
            replay_buffer = pickle.load(f)

    else:
        frame = env.reset()
        last_four_frames = [preprocess(frame)] * 4

        for _ in progressbar(range(int(args.num_total_steps * args.perc_initial_random_samples)), desc="Generating random samples"):
            state = last_four_frames
            action = env.action_space.sample()

            new_frame, reward, is_done, _ = env.step(action)
            replay_buffer.append((state, action, new_frame, reward, is_done))

            last_four_frames.pop(0)
            last_four_frames.append(preprocess(new_frame))

            if is_done: frame = env.reset()
        
        with open(random_samples_path, "wb") as training_data_file:
            pickle.dump(replay_buffer, training_data_file)

    env.reset()
    return env, replay_buffer

def get_epsilon_for_iteration(iteration, num_total_steps):
    if iteration > num_total_steps * 0.1: return 0.1
    else: return 0.9 * (1.0 - (iteration / (num_total_steps * 0.1))) + 0.1

def choose_best_action(model, state):
    # state is (4, 105, 80), should be (1, 4, 105, 80), since the first dimension is the batch size
    Q_values = model.predict([np.expand_dims(state, axis=0), np.ones((1, 4))])
    max_Q = np.argmax(Q_values)
    return max_Q
