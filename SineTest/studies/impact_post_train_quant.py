"""
    evaluate the impact of post training quantisation
"""
import numpy as np
import matplotlib.pyplot as plt

from print_dict import print_dict

import tensorflow as tf
from tensorflow.keras.models import load_model
import hls4ml

import sys
import sys
sys.path.append('../')
from network import generate_data, truth_function
from evaluateHLSmodel import convert2HLS, createKerasConfig
from compareModel import meanAbsDistance, getDistances

def impact_post_train_quant(modelfilename, NSAMPLES=1000):

    quantisations = [
        'ap_fixed<18,6>',
        'ap_fixed<17,6>',
        'ap_fixed<16,6>',
        'ap_fixed<15,6>',

        'ap_fixed<14,6>',
        'ap_fixed<14,5>',
        'ap_fixed<14,4>',
        'ap_fixed<14,3>',

        'ap_fixed<13,6>',
        'ap_fixed<12,6>',
        'ap_fixed<11,6>',
        'ap_fixed<10,6>',
        ]

    # generate data for evaluation
    x_test, y_test = generate_data(NSAMPLES)
    y_truth = truth_function( x_test )

    distances = np.array([])

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(4,8))
    fig.suptitle('Comparison of KERAS and HLS4ML')

    ax1.set_title("Model prediction")
    ax1.set_title("distance to truth")

    ax1.plot(x_test, y_truth, '.', label='Truth', markersize=5)

    # load Keras Model
    model = load_model(modelfilename)
    y_keras = model.predict( x_test )
    y_keras = y_keras.flatten()


    mad_keras = meanAbsDistance( y_truth, y_keras )

    ax1.plot(x_test, y_keras, '.', label='Keras', markersize=5)
    ax2.plot( x_test, getDistances(y_truth, y_keras), '.', label="Keras",
                                                                markersize=5 )

    del model

    for quant in quantisations:
        # load Keras Model
        model = load_model(modelfilename)

        # create HLS4ML config
        config = createKerasConfig(model)
        config['Model']['Precision'] = quant

        # convert model 2 HLS4ML
        hls_model = convert2HLS(model, config)

        # evaluate model with given config
        y_hls = np.array([])
        for x in x_test:
            y_hls = np.append(y_hls, hls_model.predict( np.array(x) ))

        ax1.plot( x_test, y_hls, '.', label=quant, markersize=5 )

        ax2.plot( x_test, getDistances(y_truth, y_hls), '.',
                                                label=quant, markersize=5 )

        distances = np.append( distances, meanAbsDistance( y_truth, y_hls ) )

    print("KERAS ", mad_keras)
    print("HLS4ML", distances )

    ax1.set_ylabel('y values')
    ax2.set_ylabel('distance')
    ax2.set_xlabel('x values')

    ax1.set_ylim([-1.5, 1.5])
#    ax1.legend(loc='best')

    #plt.set_title('Comparison between Keras and HLS4ML')

    plt.savefig(model.name+"_PostQuantEffect_CMP.png")
    plt.show()

    fig, ax1 = plt.subplots()

    x = np.arange(0, len(quantisations))
    ax1.plot( x, '.-', distances, label='Mean Absolute Distance')

    # plot the comparison to keras
    ax1.axhline(y=mad_keras, color='r', linestyle='-', label="Keras")

    # Set number of ticks for x-axis
    ax1.set_xticks(x)
    # Set ticks labels for x-axis
    ax1.set_xticklabels( quantisations, fontsize=11, rotation = -45)
    ax1.set_ylabel('Mean Absolute Difference')

    ax1.set_yscale('log')
    ax1.legend(loc='best')

    plt.title('Impact of Post Training Quantisation HLS4ML')

    plt.tight_layout()
    plt.savefig(model.name+"_PostQuantEffect.png")
    plt.show()


if __name__ == "__main__":
    impact_post_train_quant('../storedANN/sine_v0.1.h5')
