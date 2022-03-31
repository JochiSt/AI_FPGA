"""
    function for generating the ANN
"""

# TensorFlow is an open source machine learning library
import tensorflow as tf
# Keras is TensorFlow's high-level API for deep learning
from tensorflow import keras

# number of samples for training, testing etc.
SAMPLES = 100000

def generate_network(name="network_v0.4"):

    inputs = keras.Input(shape=(128,), name="waveform_input")

    layer_cnt=0
    x = keras.layers.Dense(32, 
    kernel_regularizer=keras.regularizers.l1(0.00001),                       
    name="layer_%d"%(layer_cnt))(inputs)
    layer_cnt+=1

    x = keras.layers.Dropout(0.005)(x)

    x = keras.layers.Dense(32, 
    kernel_regularizer=keras.regularizers.l1(0.00001),
    name="layer_%d"%(layer_cnt))(x)
    layer_cnt+=1

    x = keras.layers.Dropout(0.005)(x)

    x = keras.layers.Dense(32, 
    kernel_regularizer=keras.regularizers.l1(0.00001), 
    name="layer_%d"%(layer_cnt) )(x)
    layer_cnt+=1

    x = keras.layers.Dense(32, 
    kernel_regularizer=keras.regularizers.l1(0.00001), 
    name="layer_%d"%(layer_cnt) )(x)
    layer_cnt+=1

    x = keras.layers.Dense(32, 
    activation="relu",                       
    kernel_regularizer=keras.regularizers.l1(0.00001), 
    name="layer_%d"%(layer_cnt) )(x)
    layer_cnt+=1

    x = keras.layers.Dense(32,
    activation="relu",                       
    kernel_regularizer=keras.regularizers.l1(0.00001), 
    name="layer_%d"%(layer_cnt))(x)
    layer_cnt+=1

    x = keras.layers.Dense(16, 
    activation="relu",                       
    kernel_regularizer=keras.regularizers.l1(0.00001), 
    name="layer_%d"%(layer_cnt))(x)
    layer_cnt+=1

    x = keras.layers.Dense(16, 
    activation="relu",
    kernel_regularizer=keras.regularizers.l1(0.00001), 
    name="layer_%d"%(layer_cnt))(x)
    layer_cnt+=1

    # final layer for classification
    outputs = keras.layers.Dense(3, 
    name="classification")(x)

    model_1 = keras.Model(inputs=inputs, outputs=outputs, name=name)
    model_1.summary()

    # Compile the model using the standard 'adam' optimizer and the mean squared error or 'mse' loss function for regression.
    model_1.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    return  model_1
