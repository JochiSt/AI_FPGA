
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
            timeout = 2
            )
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
	
    # put ANN into RESET
    print("resetting ANN ...")
    serial_port.write(str.encode('R'))
    time.sleep(1)
    # get ANN from RESET
    serial_port.write(str.encode('r'))
    time.sleep(1)
    print("... done")
	
    ANN_stimul = np.array([])
    ANN_return = np.array([])
    
    TEST_SIZE = 9
    for i in range(TEST_SIZE):
        stim = np.random.rand() * 2*np.pi
        
        uint_stim = converter.forward_conversion(input_data=stim, 
                                    signed=True, 
                                    total_bits=16, 
                                    fractional_bits=10)
                                
        
        #uint_stim = 0x3132
        int_stim = int(uint_stim)
        print("Simulus %f %d %X"%(stim, uint_stim, int_stim))
        
        try:
            byte_stim = int_stim.to_bytes(2, 'little')
            #byte_stim = int(65518).to_bytes(2, 'little')
            print("\tANN byte stim U %x L %x"%(byte_stim[1], byte_stim[0]))
                       
            
            serial_port.write(str.encode('l'))
            serial_port.flush()
            
            send_data = "%02X"%(byte_stim[0])
            #serial_port.write(str.encode("%X"%(byte_stim[0])))
            serial_port.write(bytes.fromhex(send_data))
            serial_port.flush()
            
            serial_port.write(str.encode('u'))
            serial_port.flush()
            send_data = "%02X"%(byte_stim[1])
            #serial_port.write(str.encode("%X"%(byte_stim[1])))
            serial_port.write(bytes.fromhex(send_data))
            serial_port.flush()
            
            # trigger computation
            serial_port.write(str.encode('c'))
            serial_port.flush()
            
            test = input("waiting for input ...")
            #serial_port.write(str.encode('l%du%dc'%(i,i+1)))
            #serial_port.flush()
            
            time.sleep(0.2)
            # ignore previous received bytes
            serial_port.reset_input_buffer()
            
            # readout results
            serial_port.write(str.encode('U'))
            serial_port.flush()
            rawU = serial_port.read( size=1 )
            
            serial_port.write(str.encode('L'))
            serial_port.flush()
            rawL = serial_port.read( size=1 )
            
            rawU = int.from_bytes(rawU, "big")
            rawL = int.from_bytes(rawL, "big")
                        
            raw = (rawU << 8) + rawL
            print("ANN U %x L %x = %X" %(rawU, rawL, raw) )
            
            result = converter.backward_conversion(input_data=raw, 
                                total_bits=16, 
                                fractional_bits=10)[0]

            print("\tANN float %f"%(result))
            # store stimulus and result in array
            ANN_stimul = np.append(ANN_stimul, stim)
            ANN_return = np.append(ANN_return, result)
            
            #time.sleep(0.5)
        except Exception as e:
            print(e)
            serial_port.close()
            break
        
    # put ANN into reset
    serial_port.write(str.encode('R'))
    serial_port.close()
    
    plt.title("ANN output")
    plt.ylabel("ANN output")
    plt.xlabel("ANN stimulus")
    plt.scatter( ANN_stimul, ANN_return )
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