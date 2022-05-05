
import numpy as np
import matplotlib.pyplot as plt

from fxpmath import Fxp

import time

import sys
sys.path.append("PYNQ-ap_fixed-converter")
from converter import Converter

stimulus = np.array([])
ANN_raw = np.array([])

with open('manual_test.txt') as f:
    lines = f.readlines()  
    for line in lines:
        try:
            stim, raw = line.split(' ')
            stim = stim.replace(',','.')
            stimulus  = np.append( stimulus,  float(stim) )
            ANN_raw = np.append( ANN_raw, int(raw[:-1], 16) )
        except Exception as e:
            print(e)
            print(line)
            pass

# instantiate float ap_fixed converter
converter = Converter()
ANN_float = np.array([])
for ANN in ANN_raw:
    print(int(ANN))
    result = converter.backward_conversion(input_data=int(ANN),
                                total_bits=16, fractional_bits=15)[0]
    print(ANN, result)
    ANN_float = np.append(ANN_float, result)
                    

plt.title("ANN output")
plt.ylabel("ANN output")
plt.xlabel("ANN stimulus")
plt.scatter( stimulus, ANN_float )
plt.savefig("FPGA_manual_evaluation.png")
plt.show()
