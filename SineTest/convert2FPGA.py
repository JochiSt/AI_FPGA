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

from create_JSON_config import createModelConfig, createLayerConfig, createProjectConfig

def convert2FPGA(model, clock_period=4, build=True, profiling=False, use_additional_cfg=True):

    if not os.path.exists(model.name+'_model_cfg.json'):
        print("Model Config does not exists - it is created now...")
        createModelConfig(model)

    try:
        with open(model.name+'_model_cfg.json') as data_file:
            model_cfg = json.load(data_file)
    except Exception as e:
        print(e)
        pass
    
    # include external configuration
    if use_additional_cfg:
        if not os.path.exists(model.name+'_layer_cfg.json'):
            print("Layer Config does not exists - it is created now...")
            createLayerConfig(model) 
            
        try:
            with open(model.name+'_layer_cfg.json') as data_file:
                additional_cfg = json.load(data_file)
            model_cfg = helpers.merge_dicts(model_cfg, additional_cfg)
        except Exception as e:
            print(e)
            pass
    
    # if profiling is used, we have to enable the Trace mode
    if profiling:
        for layer in model_cfg['LayerName'].keys():
            model_cfg['LayerName'][layer]['Trace'] = True

    # check, whether the project configuration exists
    if not os.path.exists('project_cfg.json'):
        print("Project Config does not exists - it is created now...")
        createProjectConfig()

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
    
