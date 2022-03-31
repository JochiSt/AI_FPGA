"""
    generate the waveform from input parameters
"""

import numpy as np

TOTAL_SAMPLES = 128
RISING_POINTS = 4

def generate_waveform(position = 0, pulse_length = 32, height=1, noise=0, offset=0):
    assert TOTAL_SAMPLES - pulse_length - position - RISING_POINTS * 2 > 0

    # zeroes at front of the pulse
    template = np.zeros(position)
    # create rising edge
    template = np.append(template, np.linspace(0,1,RISING_POINTS, endpoint=False))
    # high part of the pulse
    template = np.append(template, np.ones(pulse_length))
    # create falling edge
    template = np.append(template, np.linspace(1,0,RISING_POINTS, endpoint=False))
    # zeroes after the pulse
    template = np.append(template, np.zeros( TOTAL_SAMPLES - pulse_length - position - 2*RISING_POINTS))
    # multiply by the height to get the right amplitude
    template *= height
    # add some noise
    template  += noise * np.random.randn(*template.shape)
    # add a constant offset
    template += offset
    # clip template to range [0, 255]
    template = np.clip(template, 0, 255)
    # convert to integer
    template = template.astype(int)

    return template

