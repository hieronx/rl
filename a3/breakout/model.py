import random

import numpy as np
import tensorflow as tf

from breakout.util import get_epsilon_for_iteration


def create_models(model_path):
    """Creates the model and the target model, returning both"""
    model = create_dqn_model(4)
    target_model = copy_model(model, model_path)
    return model, target_model

def create_dqn_model(n_actions):
    """Creates and returns the ATARI model with the specified amount of actions that are possible"""
    ATARI_SHAPE = (4, 105, 80) # TODO: maybe make these NONE-magic numbers?

    frames_input = tf.keras.Input(ATARI_SHAPE, name='frames')
    actions_input = tf.keras.Input((n_actions,), name='mask')

    normalized = tf.keras.layers.Lambda(lambda x: x / 255.0)(frames_input)
    
    conv_1 = tf.keras.layers.Conv2D(
        filters=16, kernel_size=(8, 8), strides=4, padding='same', activation='relu'
    )(normalized)
    conv_2 = tf.keras.layers.Conv2D(
        filters=32, kernel_size=(4, 4), strides=2, padding='same', activation='relu'
    )(conv_1)
    conv_flattened = tf.keras.layers.Flatten()(conv_2)

    hidden = tf.keras.layers.Dense(256, activation='relu')(conv_flattened)
    regularized_hidden = tf.keras.layers.Dropout(0.2)(hidden)
    output = tf.keras.layers.Dense(n_actions)(regularized_hidden)

    filtered_output = tf.keras.layers.multiply([output, actions_input])

    model = tf.keras.models.Model(inputs=[frames_input, actions_input], outputs=filtered_output)

    optimizer = tf.keras.optimizers.Adam(lr=0.00025 / 4, epsilon=0.00015) # From the Rainbow paper
    # optimizer = tf.keras.optimizers.RMSprop(lr=0.00025, rho=0.95, epsilon=0.01)

    model.compile(optimizer, loss=tf.keras.losses.Huber())

    return model

def predict_max_q_action(model, state):
    """Returns the index of the output layer that has the highest value, this is effectively the index of the best action"""
    Q_values = model.predict([np.expand_dims(state, axis=0), np.ones((1, 4))])
    return np.argmax(Q_values)

def get_epsilon_greedy_action(env, model, state, args, iteration):
    # Choose action using epsilon-greedy approach
    epsilon = get_epsilon_for_iteration(iteration, args.num_total_steps)

    if random.random() < epsilon: action = env.action_space.sample()
    else: action = predict_max_q_action(model, state)

    return action, epsilon

def copy_model(model, path):
    """Copies the neural network model by saving it to disk and loading a new model from the saved copy"""
    model.save(path)
    return tf.keras.models.load_model(path)
