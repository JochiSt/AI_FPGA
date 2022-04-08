
import numpy as np
import tensorflow as tf
from tensorflow import keras

# import waveform generation
from generate_waveform import generate_waveform

# import parameters
from parameters import *

# import network / model related functions
from network import create_model, save_model

# number of samples for training, testing etc.
SAMPLES = 100000

def generate_training_data():
    y_values = []
    x_values = []

    # generate the waveforms
    for i in range(SAMPLES):
        # use random settings
        width = np.random.randint( *P_width )       # width
        position = np.random.randint( *P_position ) # limit position into a certain window
        height = np.random.randint( *P_height )     # pulse height
        offset = np.random.randint( *P_offset )     # constant offset

        x_values.append( (width/SCALE_WIDTH, position/SCALE_POS, height/SCALE_HEIGHT) )
        y_values.append( generate_waveform(position = position, pulse_length = width, height=height, noise=noise, offset=offset) / SCALE_HEIGHT )

    return x_values, y_values

if __name__ == "__main__":

    # generate the network
    model_1 = create_model()

    # We'll use 60% of our data for training and 20% for testing. The remaining 20%
    # will be used for validation. Calculate the indices of each section.
    TRAIN_SPLIT =  int(0.6 * SAMPLES)
    TEST_SPLIT = int(0.2 * SAMPLES + TRAIN_SPLIT)
    print("using %d points for training and %d points for testing"%(TRAIN_SPLIT, TEST_SPLIT))

    # generate the training data
    x_values, y_values = generate_training_data()

    # convert data into numpy arrays
    y_values = np.array(y_values) # parameters
    x_values = np.array(x_values) # waveforms

    # Use np.split to chop our data into three parts.
    # The second argument to np.split is an array of indices where the data will be
    # split. We provide two indices, so the data will be divided into three chunks.
    x_train, x_test, x_validate = np.split(x_values, [TRAIN_SPLIT, TEST_SPLIT])
    y_train, y_test, y_validate = np.split(y_values, [TRAIN_SPLIT, TEST_SPLIT])

    # Double check that our splits add up correctly
    assert (len(x_train) + len(x_validate) + len(x_test) ) ==  SAMPLES

    # fully train the network
    history_1 = model_1.fit(y_train, x_train, epochs=50, batch_size=333, validation_data=(y_validate, x_validate))

    save_model(model_1)

    # pruning + quantisation



