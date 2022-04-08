#!/bin/python3

from hls4ml.model.profiling import numerical
from hls4ml.converters import keras_to_hls
import matplotlib.pyplot as plt
import yaml

# for import of keras model
from tensorflow import keras

# for generating the test data
from generate_waveform import generate_waveform
from parameters import *
import numpy as np

# how many waveforms should be used for profiling
PROFILE_SAMPLES = 1000
labels = []
X = []

for i in range(PROFILE_SAMPLES):
    # use random settings
    width = np.random.randint( *P_width )       # width
    position = np.random.randint( *P_position ) # limit position into a certain window
    height = np.random.randint( *P_height )     # pulse height
    offset = np.random.randint( *P_offset )     # constant offset

    labels.append( (width/SCALE_WIDTH, position/SCALE_POS, height/SCALE_HEIGHT) )
    X.append( generate_waveform(position = position, pulse_length = width, height=height, noise=noise, offset=offset) / SCALE_HEIGHT )

X = np.array(X) # waveforms

# load your hls4ml .yml config file with yaml
with open("generated_keras-config.yml", 'r') as ymlfile:
    config = yaml.safe_load(ymlfile)

print(config)
# load keras model from yml file
print(config['KerasH5'])
model = keras.models.load_model(config['KerasH5'].replace('_weights','') )

hls_model = keras_to_hls(config)

# produce an activation profile (ap)
# and weights profile (wp)
ap, wp = numerical(model=model, hls_model = hls_model, X=X)
plt.show()
