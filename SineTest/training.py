import numpy as np
import tensorflow as tf
from tensorflow import keras

# import matplotlib
import matplotlib.pyplot as plt

# import own helper functions
import AI_TF_helpers as helpers

def create_datasets(SAMPLES):
    # import network / model related functions
    from network import generate_data

    # We'll use 60% of our data for training and 20% for testing.
    # The remaining 20% will be used for validation. Calculate the indices of
    # each section.
    TRAIN_SPLIT = int(0.6 * SAMPLES)
    TEST_SPLIT =  int(0.2 * SAMPLES + TRAIN_SPLIT)

    # generate the training data
    x_values, y_values = generate_data(SAMPLES)

    # convert data into numpy arrays
    x_values = np.array(x_values) # waveforms
    y_values = np.array(y_values) # parameters

    # Use np.split to chop our data into three parts.
    # The second argument to np.split is an array of indices where the data
    # will be split. We provide two indices, so the data will be divided into
    # three chunks.
    x_train, x_test, x_validate = np.split(x_values, [TRAIN_SPLIT, TEST_SPLIT])
    y_train, y_test, y_validate = np.split(y_values, [TRAIN_SPLIT, TEST_SPLIT])

    return x_train, x_test, x_validate, y_train, y_test, y_validate

def training(model, SAMPLES=100000):
    x_train, x_test, x_validate,\
    y_train, y_test, y_validate = create_datasets(SAMPLES)

    # Double check that our splits add up correctly
    assert (len(x_train) + len(x_validate) + len(x_test) ) ==  SAMPLES

    print("Points using for:")
    print(" - Training:  ", len(x_train) )
    print(" - Validation:", len(x_validate) )
    print(" - Testing:   ", len(x_test) )
    print("in total:     ", SAMPLES)

    ###########################################################################
    # Train the network
    # fully train the network
    history = model.fit(x_train, y_train,
                            epochs=50,          # how long do we want to train 
                            batch_size=333,     # how large is one batch
                            shuffle=True,
                            validation_data=(x_validate, y_validate))

    ###########################################################################
    # create typical deep learning performance plots
    # Plot the training history
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    # the MAE mean absolute error is a good quantity, which gives the 
    # 'accuracy' of our model.
    mae = history.history['mae']
    val_mae = history.history['val_mae']

    # create x-axis
    epochs = range(1, len(loss) + 1)

    # create plots
    fig, ax1 = plt.subplots()
    ax1.plot(epochs, loss,     'b', label='Training loss')
    ax1.plot(epochs, val_loss, 'b--', label='Validation loss')

    ax2 = ax1.twinx()
    ax2.plot(epochs, mae,     'r', label='Training MAE')
    ax2.plot(epochs, val_mae, 'r--', label='Validation MAE')

    ax1.set_xlabel('epochs')
    ax1.set_ylabel('loss', color='b')
    ax2.set_ylabel('MAE', color='r')
    plt.title('Training and validation Performance')
    fig.legend()
    plt.savefig(model.name+"_train_perf.png")
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

if __name__ == "__main__":
    # printout the used versions
    print('Numpy ' + np.__version__)
    print('TensorFlow ' + tf.__version__)
    print('Keras ' + tf.keras.__version__)

    from network import create_model
    # generate the network
    model = create_model()

    training(model)
