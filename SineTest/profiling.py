import numpy as np
import matplotlib.pyplot as plt

import hls4ml

from convert2FPGA import convert2FPGA
from network import generate_data

def profiling_hlsmodel(model):

    hls_model = convert2FPGA(model, clock_period=4, build=False, profiling=True)
    
    NSAMPLES = 1000
    # generate data for evaluation
    x_test, y_test = generate_data(NSAMPLES)
    
    # produce an activation profile (ap)
    # and weights profile (wp)
    wp, wph, ap, aph = hls4ml.model.profiling.numerical( 
                                    model=model, hls_model=hls_model, X= np.array(x_test) )
    
    if wp is not None:
        wp.savefig( "prof_"+model.name+"_wp.png")
    if wph is not None:
        wph.savefig("prof_"+model.name+"_wph.png")
        
    if ap is not None:
        ap.savefig( "prof_"+model.name+"_ap.png")
    if aph is not None:
        aph.savefig("prof_"+model.name+"_aph.png")

    plt.show()

if __name__ == "__main__":
    # use the already trained model
    from tensorflow.keras.models import load_model
    model = load_model('storedANN/sine_v0.2.h5')
    profiling_hlsmodel(model)