import tensorflow as tf


def atari_model(n_actions):
    ATARI_SHAPE = (4, 105, 80)

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

    model.compile(optimizer, loss='mse')

    return model
