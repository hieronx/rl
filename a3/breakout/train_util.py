import numpy as np


def choose_best_action(model, state):
    # state is (4, 105, 80), should be (1, 4, 105, 80), since the first dimension is the batch size
    Q_values = model.predict([np.expand_dims(state, axis=0), np.ones((1, 4))])
    max_Q = np.argmax(Q_values)
    return max_Q
