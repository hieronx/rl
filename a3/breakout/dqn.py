from collections import deque

import numpy as np


def fit_batch(model, target_model, gamma, batch_idx, replay_buffer):
    """
    Fits the model to one batch. Every batch is 32 samples. Every sample consists
    of a tuple of: state, action, new_frame, reward, is_done
    """
    start_states, next_states, actions, rewards, is_dones = ([], [], [], [], [])

    for idx in batch_idx:
        start_state = replay_buffer.start_states[idx]
        action = [1 if i == replay_buffer.actions[idx] else 0 for i in range(4)]
        reward = replay_buffer.rewards[idx]
        is_done = replay_buffer.is_dones[idx]
        next_state = deque(replay_buffer.start_states[idx], maxlen=4)
        next_state.append(replay_buffer.next_frames[idx])

        next_states.append(next_state)
        start_states.append(start_state)
        rewards.append(reward)
        is_dones.append(is_done)
        actions.append(action)

    start_states = np.array(start_states)
    next_states = np.array(next_states)
    actions = np.array(actions)
    rewards = np.array(rewards)
    is_dones = np.array(is_dones)

    next_Q_values = target_model.predict([next_states, np.ones(actions.shape)])
    next_Q_values[is_dones] = 0

    Q_values = rewards + gamma * np.max(next_Q_values, axis=1)

    targets = actions * Q_values[:, None]

    # log_file = open("log.txt","w")

    # log_file.write('Start state: %s\n' % np.average(start_states[0]))
    # log_file.write('Next state: %s\n' % np.average(next_states[0]))
    # log_file.write('Actions: %s\n' % actions[0])
    # log_file.write('Rewards: %s\n' % rewards[0])
    # log_file.write('Is dones: %s\n\n' % is_dones[0])
    # log_file.write('Next Q values: %s\n' % next_Q_values[0])
    # log_file.write('Next Q values after resetting is_done states: %s\n' % next_Q_values[0])
    # log_file.write('Gamma: %.2f\n' % gamma)
    # log_file.write('Targets: %s\n\n' % targets[0])
    # log_file.close()

    model.fit([start_states, actions], targets, epochs=1, batch_size=len(start_states), verbose=0)

    return model
