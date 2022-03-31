

from generate_waveform import generate_waveform
from parameters import *

from network import generate_network

if __name__ == "__main__":

    model_1 = generate_network()

    model_1.summary()
