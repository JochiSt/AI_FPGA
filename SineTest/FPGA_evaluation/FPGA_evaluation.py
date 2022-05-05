
import numpy as np
import matplotlib.pyplot as plt

from fxpmath import Fxp

import serial
import time

import sys
sys.path.append("PYNQ-ap_fixed-converter")
from converter import Converter

def FPGA_evaluation(tty="/dev/ttyUSB1"):
    serial_port = None
    
    try:
        # open serial port
        serial_port = serial.Serial(tty,
							baudrate= 115200,
							bytesize = serial.EIGHTBITS,
							parity = serial.PARITY_NONE,
							stopbits = serial.STOPBITS_ONE,
                            timeout = 2)
    except Exception as e:
        print(e)
        serial_port.close()
        return

    try:
        # clear input and output
        serial_port.flush()
        serial_port.flushInput()
    except Exception as e:
        print(e)
        serial_port.close()
        return

    # some debug info
    print("connected to AI test")
	
    # get ANN from reset
    serial_port.write(str.encode("r"))
	
    TEST_SIZE = 10
    
    for i in range(TEST_SIZE):
        try:
            serial_port.write(str.encode("1"))
            raw1 = serial_port.read( size=1 )

            serial_port.write(str.encode("2"))
            raw2 = serial_port.read( size=1 )
            
            if i > 1:
                print("ANN", raw2, raw1)
            
        except Exception as e:
            print(e)
            serial_port.close()
            break

    # put ANN into reset
    serial_port.write(str.encode("r"))

def testConverter():
    converter = Converter()

    uint_result = converter.forward_conversion(input_data=0.7, signed=False, total_bits=4, fractional_bits=3)
    print('Forward converted input:',uint_result)

    fractional_result = converter.backward_conversion(input_data=uint_result, total_bits=4, fractional_bits=3)
    print('Backward converted input', fractional_result)

if __name__ == "__main__":
    #FPGA_evaluation()
    testConverter()