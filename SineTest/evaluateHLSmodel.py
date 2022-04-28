"""
    script to evaluate the HLS network
"""

import tensorflow as tf
from tensorflow.keras.models import load_model
from print_dict import print_dict
import numpy as np
import matplotlib.pyplot as plt

from network import generate_data

import hls4ml

def evaluateHLSmodel(model, NSAMPLES=1000, config=None):
    # evaluate model and make some plots
    # TODO

    if not config:
        # create basic config
        config = hls4ml.utils.config_from_keras_model(model, 
                                                        granularity='model')

    config['Model']['Precision'] = 'ap_fixed<14,6>'

    print("-----------------------------------")
    print("Configuration")
    print_dict(config)
    print("-----------------------------------")
    hls_model = hls4ml.converters.convert_from_keras_model(model,
                                hls_config=config,
                                project_name='sinetest',
                                output_dir='sinetest',
                                part='xcu250-figd2104-2L-e')

    # model is written to output dir

    # generate data for evaluation
    x_test, y_test = generate_data(NSAMPLES)
   
    # compile HLS model
    hls_model.compile()

    y_hls = np.array([])
    y_keras = np.array([])
    
    for x in x_test:
        y_hls_   = hls_model.predict(np.array(x))
        y_hls = np.append(y_hls, y_hls_)

    y_keras = model.predict( x_test )

    # compare to Keras
    fig, ax1 = plt.subplots()
    ax1.plot(x_test, y_keras, 'b.', label='Keras')
    ax1.plot(x_test, y_hls,   'r.', label='HLS4ML')

    ax1.set_xlabel('x values')
    ax1.set_ylabel('y values')
    plt.title('Comparison between Keras and HLS4ML')
    fig.legend()
    plt.savefig(model.name+"_keras_hls4ml.png")
    plt.show()


if __name__ == "__main__":
    # printout the used versions
    print('Numpy ' + np.__version__)
    print('TensorFlow ' + tf.__version__)
    print('Keras ' + tf.keras.__version__)
    print('HLS4ML ' + hls4ml.__version__)

    # use the already trained model
    model = load_model('storedANN/sine_v0.1.h5')
    evaluateHLSmodel(model)
