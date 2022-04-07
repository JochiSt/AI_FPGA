"""
    function for generating the ANN
"""

# TensorFlow is an open source machine learning library
import tensorflow as tf
# Keras is TensorFlow's high-level API for deep learning
from tensorflow import keras

# number of samples for training, testing etc.
SAMPLES = 100000

def create_model(name="network_v0.5"):
    """
        
    """

    inputs = keras.Input(shape=(128,), name="waveform_input")

    layer_cnt=0
    x = keras.layers.Dense(8, 
                            activation="relu",
                            kernel_regularizer=keras.regularizers.l1(0.00001),
                            name="layer_%d"%(layer_cnt))(inputs)
    layer_cnt+=1

    x = keras.layers.Dropout(0.005)(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Dense(8, 
                            activation="relu",
                            kernel_regularizer=keras.regularizers.l1(0.00001),
                            name="layer_%d"%(layer_cnt))(x)
    layer_cnt+=1

    x = keras.layers.Dropout(0.005)(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Dense(8, 
                            activation="relu",
                            kernel_regularizer=keras.regularizers.l1(0.00001),
                            name="layer_%d"%(layer_cnt))(x)
    layer_cnt+=1

    # final layer for classification
    outputs = keras.layers.Dense(3, name="classification")(x)

    model_1 = keras.Model(inputs=inputs, outputs=outputs, name=name)
    model_1.summary()

    # Compile the model using the standard 'adam' optimizer and the mean squared error or 'mse' loss function for regression.
    model_1.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    # save an image of the ANN
    tf.keras.utils.plot_model(model_1, 
            to_file='model_1.png',        # output file name
            show_layer_activations=True,  # show activation functions
            show_layer_names=True,        # show layer names
            show_dtype=True,              # show datatype
            show_shapes=True,             # show input / output shapes
            rankdir='LR'                  # left to right image
        )

    return  model_1


def save_model(model, name=None):
    """
        Save as model.h5, model_weights.h5, and model.json

        from https://jiafulow.github.io/blog/2021/02/17/simple-fully-connected-nn-firmware-using-hls4ml/
    """

    if name is None:
        name = model.name

    model.save(name + '.h5')
    model.save_weights(name + '_weights.h5')
    with open(name + '.json', 'w') as outfile:
        outfile.write(model.to_json())
    return

if __name__ == "__main__":
    model = create_model()
