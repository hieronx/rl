import numpy as np

def get_epsilon_for_iteration(iteration, num_total_steps):
    if iteration > num_total_steps * 0.1: return 0.1
    else: return 0.9 * (1.0 - (iteration / (num_total_steps * 0.1))) + 0.1

def choose_best_action(model, state):
    # state is (4, 105, 80), should be (1, 4, 105, 80), since the first dimension is the batch size
    Q_values = model.predict([np.expand_dims(state, axis=0), np.ones((1, 4))])
    max_Q = np.argmax(Q_values)
    return max_Q
