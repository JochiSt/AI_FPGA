"""
    script to evaluate the Quantized Network
"""

import tensorflow as tf
from print_dict import print_dict

import numpy as np
import matplotlib.pyplot as plt

from network import generate_data, truth_function

from qkeras import *

def evaluateQuantModel(qmodel, NSAMPLES=1000):
    # generate data for evaluation
    x_test, y_test = generate_data(NSAMPLES)

    y_truth = truth_function( x_test )
    y_quant = np.array([])
    for x in x_test:
        y_quant = np.append(y_quant, qmodel.predict( np.array(x) ))

    # compare to Keras
    fig, ax1 = plt.subplots()
    ax1.plot(x_test, y_truth, 'g.', label='Truth')
    ax1.plot(x_test, y_quant, 'r.', label='HLS4ML')

    ax1.set_xlabel('x values')
    ax1.set_ylabel('y values')
    plt.title('Performance of Quantized Network')
    fig.legend()
    plt.savefig(qmodel.name+"_perf_quant.png")
    plt.show()


if __name__ == "__main__":
    if False:
        # use the already trained model
        from tensorflow.keras.models import load_model
        from qkeras.utils import _add_supported_quantized_objects
        co = {}
        _add_supported_quantized_objects(co)
        model = load_model('storedANN/sine_v0.1_quant', custom_objects=co)
    else:
        from network import create_model
        # generate the network
        model = create_model(quantized=True)
        from training import training
        training(model)

    evaluateQuantModel(model)
