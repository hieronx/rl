import tensorflow as tf


def atari_model(n_actions):
    # We assume a theano backend here, so the "channels" are first.
    ATARI_SHAPE = (4, 105, 80)

    # With the functional API we need to define the inputs.
    frames_input = tf.keras.Input(ATARI_SHAPE, name='frames')
    actions_input = tf.keras.Input((n_actions,), name='mask')

    # Assuming that the input frames are still encoded from 0 to 255. Transforming to [0, 1].
    normalized = tf.keras.layers.Lambda(lambda x: x / 255.0)(frames_input)
    
    # "The first hidden layer convolves 16 8×8 filters with stride 4 with the input image and applies a rectifier nonlinearity."
    conv_1 = tf.keras.layers.Conv2D(
        filters=16, kernel_size=(8, 8), strides=4, padding='same', activation='relu'
    )(normalized)
    # "The second hidden layer convolves 32 4×4 filters with stride 2, again followed by a rectifier nonlinearity."
    conv_2 = tf.keras.layers.Conv2D(
        filters=32, kernel_size=(4, 4), strides=2, padding='same', activation='relu'
    )(conv_1)
    # Flattening the second convolutional layer.
    conv_flattened = tf.keras.layers.Flatten()(conv_2)

    # TODO: the paper uses 512 hidden units in this layer
    # "The final hidden layer is fully-connected and consists of 256 rectifier units."
    hidden = tf.keras.layers.Dense(256, activation='relu')(conv_flattened)
    # "The output layer is a fully-connected linear layer with a single output for each valid action."
    output = tf.keras.layers.Dense(n_actions)(hidden)
    # Finally, we multiply the output by the mask!
    filtered_output = tf.keras.layers.multiply([output, actions_input])

    model = tf.keras.models.Model(inputs=[frames_input, actions_input], outputs=filtered_output)
    optimizer = optimizer=tf.keras.optimizers.RMSprop(lr=0.00025, rho=0.95, epsilon=0.01)
    model.compile(optimizer, loss='mse')

    return model
