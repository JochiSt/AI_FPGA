"""
    function for generating the ANN
"""

# TensorFlow is an open source machine learning library
import tensorflow as tf
# Keras is TensorFlow's high-level API for deep learning
from tensorflow import keras

# numpy
import numpy as np

def generate_data(NSAMPLES):
    """
        generate training / validation data for the network below
    """

    # Generate some random samples
    x_values = np.random.uniform(low=0, high=(2 * np.pi), size=NSAMPLES)

    # Create a noisy sinewave with these values
    y_values = np.sin(x_values) + (0.1 * np.random.randn(x_values.shape[0]))

    return x_values, y_values

def create_model(name="sine_v0.1"):
    """
        Simple Network which approximates a sine

        y = sin(x), where sin is replaced by the network

        This approximation can be achieved by few layers and hence few
        mathematical operations.

        That's a good starting point to get HLS4ML running and to understand
        and optimise its behaviour.

        https://www.digikey.de/en/maker/projects/intro-to-tinyml-part-1-training-a-model-for-arduino-in-tensorflow/8f1fc8c0b83d417ab521c48864d2a8ec

        and

        https://gist.github.com/ShawnHymel/79237fe6aee5a3653c497d879f746c0c
    """

    inputs = keras.Input(shape=(1,), name="waveform_input")

    layer_cnt=0
    x = keras.layers.Dense(16, 
                            activation="relu",
                            name="layer_%d"%(layer_cnt))(inputs)
    layer_cnt+=1

    x = keras.layers.Dropout(0.005)(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Dense(8, 
                            activation="relu",
                            name="layer_%d"%(layer_cnt))(x)
    layer_cnt+=1

    x = keras.layers.Dropout(0.005)(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Dense(8, 
                            activation="relu",
                            name="layer_%d"%(layer_cnt))(x)
    layer_cnt+=1

    # final layer for classification
    outputs = keras.layers.Dense(1, name="output")(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name=name)
    model.summary()

    # Compile the model using the standard 'adam' optimizer and the mean squared error or 'mse' loss function for regression.
    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    return  model

if __name__ == "__main__":
    model = create_model()
