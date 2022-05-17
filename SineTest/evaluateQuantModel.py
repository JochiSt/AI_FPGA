"""
    script to evaluate the Quantized Network
"""

import tensorflow as tf
from print_dict import print_dict

import numpy as np
import matplotlib.pyplot as plt

from qkeras import *

from network import generate_data, truth_function
from compareModel import meanAbsDistance, getDistances

def evaluateQuantModel(qmodel, NSAMPLES=1000):
    # generate data for evaluation
    x_test, y_test = generate_data(NSAMPLES)

    y_truth = truth_function( x_test )
    y_quant = np.array([])
#    for x in x_test:
#        y_quant = np.append(y_quant, qmodel.predict( x ))
    y_quant = qmodel.predict( x_test )

    mad = meanAbsDistance( y_truth, y_quant )
    print("Quantisated Model :", mad)

    # compare to Keras
    fig, ax1 = plt.subplots()
    ax1.plot(x_test, y_truth, 'g.', label='Truth')
    ax1.plot(x_test, y_quant, 'r.', label='HLS4ML')

    ax1.set_xlabel('x values')
    ax1.set_ylabel('y values')
    plt.title('Performance of Quantized Network')
    fig.legend()
    plt.savefig("plots/"+qmodel.name+"_perf_quant.png")
    plt.show()


if __name__ == "__main__":
    if True:
        # use the already trained model
        from AI_TF_helpers import load_quant_model
        model = load_quant_model("sine_v0.2_quant")
        
    else:
        from network import create_model
        # generate the network
        model = create_model(quantized=True)
        from training import training
        training(model)

    evaluateQuantModel(model)
