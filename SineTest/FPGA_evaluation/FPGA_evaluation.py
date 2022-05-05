
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

    # instantiate float ap_fixed converter
    converter = Converter()

    # some debug info
    print("connected to AI test")
	
    # get ANN from reset
    serial_port.write(str.encode("r"))
	
    ANN_stimul = np.array([])
    ANN_return = np.array([])
    
    TEST_SIZE = 10
    for i in range(TEST_SIZE):
        stim = np.random.rand() * 2*np.pi
        ANN_stimul = np.append(ANN_stimul, stim)
        
        uint_stim = converter.forward_conversion(input_data=stim, 
                                    signed=True, total_bits=16, fractional_bits=10)
                                
        
        #uint_stim = 0x3132
        int_stim = int(uint_stim)
        print("Simulus %f %d %X"%(stim, uint_stim, int_stim))
        """
        try:
            byte_stim = uint_stim.to_bytes(2, 'big')
            print("%x %x"%(byte_stim[0], byte_stim[1]))
            
            serial_port.write(byte_stim[0])
            time.sleep(0.1)
            raw1 = serial_port.read( size=1 )
            print(raw1)
            
            time.sleep(0.2)
            
            serial_port.write(byte_stim[1])
            time.sleep(0.1)
            raw2 = serial_port.read( size=1 )
            print(raw2)
            
            if i > 0:
                raw1 = int.from_bytes(raw1, "big")
                raw2 = int.from_bytes(raw2, "big")
                
                raw = (raw2 << 8) + raw1

                print("ANN %x %x = %X" %(raw1, raw2, raw) )
                
                result = converter.backward_conversion(input_data=raw, 
                                    total_bits=16, fractional_bits=10)[0]
                        
                ANN_return = np.append(ANN_return, result)
            
            time.sleep(0.5)
        except Exception as e:
            print(e)
            serial_port.close()
            break
        """
    # put ANN into reset
    serial_port.write(str.encode("r"))
    serial_port.close()
    
    plt.title("ANN output")
    plt.ylabel("ANN output")
    plt.xlabel("ANN stimulus")
    plt.scatter( ANN_stimul[:-1], ANN_return )
    plt.savefig("FPGA_evaluation.png")
    plt.show()

def testConverter():
    converter = Converter()

    uint_result = converter.forward_conversion(input_data=0.7, signed=False, total_bits=4, fractional_bits=3)
    print('Forward converted input:',uint_result)

    fractional_result = converter.backward_conversion(input_data=uint_result, total_bits=4, fractional_bits=3)
    print('Backward converted input', fractional_result)

if __name__ == "__main__":
    FPGA_evaluation()
    #testConverter()