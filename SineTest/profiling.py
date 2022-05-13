import numpy as np
import matplotlib.pyplot as plt

import hls4ml

from convert2FPGA import convert2FPGA
from network import generate_data

from collections import defaultdict
# from https://stackoverflow.com/questions/29348345/declaring-a-multi-dimensional-dictionary-in-python
def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))

def profiling_hlsmodel(model):
    
    # create blank cfg
    add_cfg = hls4ml.utils.config_from_keras_model(model, granularity='name')
    
    add_cfg['LayerName']['layer_0']['Precision']['weight'] = 'ap_fixed<6,1>'
    add_cfg['LayerName']['layer_0']['Precision']['bias']   = 'ap_fixed<11,2>'
    add_cfg['LayerName']['layer_0']['Precision']['result'] = 'ap_fixed<11,2>'
    add_cfg['LayerName']['layer_0_linear']['Precision'] = add_cfg['LayerName']['layer_0']['Precision']['result']
        
    add_cfg['LayerName']['layer_1']['Precision']['weight'] = 'ap_fixed<11,2>'
    add_cfg['LayerName']['layer_1']['Precision']['bias']   = 'ap_fixed<9,1>'
    add_cfg['LayerName']['layer_1']['Precision']['result'] = 'ap_fixed<11,2>'
    add_cfg['LayerName']['layer_1_linear']['Precision'] = add_cfg['LayerName']['layer_1']['Precision']['result']    
    
    add_cfg['LayerName']['output']['Precision']['weight']  = 'ap_fixed<7,2>'
    add_cfg['LayerName']['output']['Precision']['bias']    = 'ap_fixed<4,1>'
    add_cfg['LayerName']['output']['Precision']['result']  = 'ap_fixed<8,1>'
    add_cfg['LayerName']['output_linear']['Precision'] = add_cfg['LayerName']['output']['Precision']['result']
    
    add_cfg['LayerName']['activation']  ['Precision'] = 'ap_fixed<11,2>'
    add_cfg['LayerName']['activation_1']['Precision'] = 'ap_fixed<12,2>'

    print(add_cfg)

    hls_model = convert2FPGA(model, 
                    clock_period=4, 
                    build=False, 
                    profiling=True, 
                    additional_cfg = add_cfg
                    )
    
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