import numpy as np
import tensorflow as tf
from tensorflow import keras

# import matplotlib
import matplotlib.pyplot as plt

# import own helper functions
import AI_TF_helpers as helpers

# import network / model related functions
from network import create_model
from network import generate_data

# number of samples for training, testing etc.
SAMPLES = 100000

if __name__ == "__main__":
    # printout the used versions
    print('Numpy ' + np.__version__)
    print('TensorFlow ' + tf.__version__)
    print('Keras ' + tf.keras.__version__)

    # generate the network
    model = create_model()

    # We'll use 60% of our data for training and 20% for testing.
    # The remaining 20% will be used for validation. Calculate the indices of
    # each section.
    TRAIN_SPLIT =  int(0.6 * SAMPLES)
    TEST_SPLIT = int(0.2 * SAMPLES + TRAIN_SPLIT)
    print("using %d points for training and %d points for testing"%(
                                                    TRAIN_SPLIT, TEST_SPLIT))

    # generate the training data
    x_values, y_values = generate_data(SAMPLES)

    # convert data into numpy arrays
    y_values = np.array(y_values) # parameters
    x_values = np.array(x_values) # waveforms

    # Use np.split to chop our data into three parts.
    # The second argument to np.split is an array of indices where the data
    # will be split. We provide two indices, so the data will be divided into
    # three chunks.
    x_train, x_test, x_validate = np.split(x_values, [TRAIN_SPLIT, TEST_SPLIT])
    y_train, y_test, y_validate = np.split(y_values, [TRAIN_SPLIT, TEST_SPLIT])

    # Double check that our splits add up correctly
    assert (len(x_train) + len(x_validate) + len(x_test) ) ==  SAMPLES

    ###########################################################################
    # Train the network
    # fully train the network
    history = model.fit(x_train, y_train,
                            epochs=50, batch_size=333,
                            validation_data=(y_validate, x_validate))

    ###########################################################################
    # create typical deep learning performance plots
    # Plot the training history
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(1, len(loss) + 1)

    plt.plot(epochs, loss, 'b', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()

    # save network
    helpers.save_model(model)

    ###########################################################################
    # Test the network
    # Plot predictions against actual values
    predictions = model.predict(x_test)

    plt.clf()
    plt.title("Comparison of predictions to actual values")
    plt.plot(x_test, y_test, 'b.', label='Actual')
    plt.plot(x_test, predictions, 'r.', label='Prediction')
    plt.legend()
    plt.show()

    # pruning + quantisation



