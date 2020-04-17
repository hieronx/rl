import numpy as np

from breakout.util import preprocess


def fit_batch(model, target_model, gamma, batch):
    # batch = 32 * (state, action, new_frame, reward, is_done)
    try:
        start_states = np.array([sample[0] for sample in batch])
    except:
        print(batch)

    actions = np.array([[1 if i == sample[1] else 0 for i in range(4)] for sample in batch])
    
    next_states = []
    for sample in batch:
        next_state = sample[0]
        next_state.pop(0)
        next_state.append(preprocess(sample[2]))
        next_states.append(next_state)
    next_states = np.array(next_states)

    rewards = np.array([sample[3] for sample in batch])
    is_dones = np.array([sample[4] for sample in batch])

    next_Q_values = target_model.predict([next_states, actions])
    next_Q_values[is_dones] = 0

    Q_values = rewards + gamma * np.max(next_Q_values, axis=1)

    model.fit([start_states, actions], actions * Q_values[:, None], epochs=1, batch_size=len(start_states), verbose=0)

    return model
