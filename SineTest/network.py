"""
    function for generating the ANN
"""

# TensorFlow is an open source machine learning library
import tensorflow as tf
# Keras is TensorFlow's high-level API for deep learning
from tensorflow import keras

def create_model(name="sine_v0.1"):
    """
        Simple Network which approximates a sine

        y = sin(x), where sin is replaced by the network

        This approximation can be achieved by few layers and hence few
        mathematical operations.

        That's a good starting point to get HLS4ML running and to understand
        and optimise its behaviour.
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
