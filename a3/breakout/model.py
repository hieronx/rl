import numpy as np
import tensorflow as tf
import random
from breakout.util import get_epsilon_for_iteration
from breakout.model import predict_max_q_action

def create_models(model_path):
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
    output = tf.keras.layers.Dense(n_actions)(hidden)

    filtered_output = tf.keras.layers.multiply([output, actions_input])

    model = tf.keras.models.Model(inputs=[frames_input, actions_input], outputs=filtered_output)

    optimizer = optimizer=tf.keras.optimizers.Adam(lr=0.00025 / 4, epsilon=0.00015) # From the Rainbow paper
    # optimizer = optimizer=tf.keras.optimizers.RMSprop(lr=0.00025, rho=0.95, epsilon=0.01)

    model.compile(optimizer, loss=huber_loss)

    return model

def predict_max_q_action(model, state):
    """Returns the index of the output layer that has the highest value, this is effectively the index of the best action"""
    Q_values = model.predict([np.expand_dims(state, axis=0), np.ones((1, 4))])
    return np.argmax(Q_values)

def huber_loss(a, b, in_keras=True):
    """
    Implements the Huber_Loss function, the in_keras parameter 
    can be used to test this using debug numpy arrays by setting it to false
    """
    error = a - b
    quadratic_term = error * error / 2
    linear_term = abs(error) - .5
    use_linear_term = (abs(error) > 1.0)
    
    # Keras won't let us multiply floats by booleans, so we explicitly cast the booleans to floats
    if in_keras: use_linear_term = tf.keras.backend.cast(use_linear_term, 'float32')
    
    return use_linear_term * linear_term + (1-use_linear_term) * quadratic_term

def get_epsilon_greedy_action(env, model, state, args, iteration):
    # Choose action using epsilon-greedy approach
    epsilon = get_epsilon_for_iteration(iteration, args.num_total_steps)

    if random.random() < epsilon: action = env.action_space.sample()
    else: action = predict_max_q_action(model, state)
