from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import numpy as np


def build_model(input_size, output_size):
    model = Sequential()
    model.add(Dense(256, input_dim=input_size, activation="relu"))
    # model.add(Dense(256, activation="relu"))
    model.add(Dense(128, activation="relu"))
    # model.add(Dropout(0.2))
    model.add(Dense(52, activation="relu"))
    # model.add(Dropout(0.2))
    model.add(Dense(output_size, activation="linear"))
    model.compile(loss="mse", optimizer=Adam())

    return model

def get_best_action(model, observation):
    """
    Returns the index of the best action from the provided values out of the prediction.
    If for example the output of the prediction model based on the provided observation 
    was [0.45, 0.12, 0.90] this function would return 2
    """
    return np.argmax(model.predict(observation.reshape(-1, len(observation)))[0])