"""
    script to evaluate the HLS network
"""

import tensorflow as tf
from tensorflow.keras.models import load_model
from print_dict import print_dict
import numpy as np
import matplotlib.pyplot as plt

from network import generate_data, truth_function
from convert2FPGA import convert2FPGA

import hls4ml

def evaluateHLSmodel(model, NSAMPLES=1000):
    # convert TF model into HLS4ML
    hls_model = convert2FPGA(model,
        clock_period=4, build=False, profiling=False, use_additional_cfg=True)

    # generate data for evaluation
    x_test, y_test = generate_data(NSAMPLES)

    y_truth = truth_function( x_test )
    y_hls = np.array([])
    for x in x_test:
        y_hls = np.append(y_hls, hls_model.predict( np.array(x) ))
    y_keras = model.predict( x_test )

    # compare to Keras
    fig, ax1 = plt.subplots()
    ax1.plot(x_test, y_truth, 'g.', label='Truth')
    ax1.plot(x_test, y_keras, 'b.', label='Keras')
    ax1.plot(x_test, y_hls,   'r.', label='HLS4ML')

    ax1.set_xlabel('x values')
    ax1.set_ylabel('y values')
    plt.title('Comparison between Keras and HLS4ML')
    fig.legend()
    plt.savefig(model.name+"_keras_hls4ml.png")
    plt.show()

if __name__ == "__main__":
    # use the already trained model
    model = load_model('storedANN/sine_v0.2.h5')
    evaluateHLSmodel(model)
