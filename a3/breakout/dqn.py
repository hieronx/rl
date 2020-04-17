from collections import deque

import numpy as np


def fit_batch(model, target_model, gamma, batch_idx, replay_buffer):
    """
    Fits the model to one batch. Every batch is 32 samples. Every sample consists
    of a tuple of: state, action, new_frame, reward, is_done
    """
    start_states, next_states, actions, rewards, is_dones = ([], [], [], [], [])

    for idx in batch_idx:
        sample = replay_buffer[idx]

        start_state = sample[0]
        action = [1 if i == sample[1] else 0 for i in range(4)]
        reward = sample[3]
        is_done = sample[4]
        next_state = deque(sample[0], maxlen=4)
        next_state.append(sample[2])

        next_states.append(next_state)
        start_states.append(start_state)
        rewards.append(reward)
        is_dones.append(is_done)
        actions.append(action)

    next_states = np.array(next_states)
    start_states = np.array(start_states)
    actions = np.array(actions)
    rewards = np.array(rewards)
    is_dones = np.array(is_dones)

    next_Q_values = target_model.predict([next_states, np.ones(actions.shape)])
    next_Q_values[is_dones] = 0

    Q_values = rewards + gamma * np.max(next_Q_values, axis=1)

    model.fit([start_states, actions], actions * Q_values[:, None], epochs=1, batch_size=len(start_states), verbose=0)

    return model
