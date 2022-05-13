"""
    script to convert the network using HLS4ML in HDL code
"""

import os
#os.environ['PATH'] = '/opt/Xilinx/Vivado/2019.2/bin:' + os.environ['PATH']
os.environ['PATH'] = '/opt/Xilinx/Vivado/2020.1/bin:' + os.environ['PATH']

# Convert the model to FPGA firmware with hls4ml
# Make an hls4ml config & model
import hls4ml
from print_dict import print_dict

import json

# import own helper functions
import AI_TF_helpers as helpers

# some basic config
#hls4ml.model.optimizer.OutputRoundingSaturationMode.layers = ['Activation']
#hls4ml.model.optimizer.OutputRoundingSaturationMode.rounding_mode = 'AP_RND'
#hls4ml.model.optimizer.OutputRoundingSaturationMode.saturation_mode = 'AP_SAT'

def convert2FPGA(model, clock_period=4, build=True, profiling=False, use_additional_cfg=True):
    # create basic config
    if not profiling:
        model_cfg = hls4ml.utils.config_from_keras_model(model, granularity='model')
    else:
        model_cfg = hls4ml.utils.config_from_keras_model(model, granularity='name')

    model_cfg['Model'] = {}
    model_cfg['Model']['ReuseFactor'] = 1
    #model_cfg['Model']['Strategy'] = 'Resource'
    model_cfg['Model']['Strategy'] = 'Latency'
    model_cfg['Model']['Precision'] = 'ap_fixed<16,6>'
    model_cfg['Model']['Precision'] = 'ap_fixed<16,6>'
    
    # include external configuration
    if use_additional_cfg:
        try:
            with open(model.name+'_layer_cfg.json') as data_file:
                additional_cfg = json.load(data_file)
            model_cfg = helpers.merge_dicts(model_cfg, additional_cfg)
        except Exception as e:
            print(e)
            pass
    
    if profiling:
        for layer in model_cfg['LayerName'].keys():
            model_cfg['LayerName'][layer]['Trace'] = True

    # load Project config from 'project_cfg.json'
    with open('project_cfg.json') as data_file:
        cfg = json.load(data_file)
        
    # there are some leftovers, which have to be set in this special way        
    cfg['Part'] = cfg['XilinxPart']
    cfg['HLSConfig'] = model_cfg
    cfg['KerasModel'] = model
    
    print("-----------------------------------")
    print("Configuration")
    print_dict(cfg)
    print("-----------------------------------")
    hls_model = hls4ml.converters.keras_to_hls(cfg)

    # Let's visualise what we created. The model architecture is shown,
    # annotated with the shape and data types
    hls4ml.utils.plot_model(hls_model,
                            show_shapes=True,
                            show_precision=True,
                            to_file=model.name+"_hls4ml.png"
                            )

    # Compile
    print("Compiling HLS model")
    hls_model.compile()

    # Synthesize
    if build:
        print("Building the model ....")
        print("This can take several minutes.")
        hls_model.build(
                        csim=True,  #
                        export=True # this fails, unless you use faketime
                        )

    return hls_model

if __name__ == "__main__":
    # use the already trained model
    from tensorflow.keras.models import load_model
    model = load_model('storedANN/sine_v0.2.h5')
    
    convert2FPGA(model)

    # Check the reports
    hls4ml.report.read_vivado_report('sinetest')
    
