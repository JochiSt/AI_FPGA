"""
    script to convert the network using HLS4ML in HDL code
"""

import os
#os.environ['PATH'] = '/opt/Xilinx/Vivado/2019.2/bin:' + os.environ['PATH']
os.environ['PATH'] = '/opt/Xilinx/Vivado/2020.1/bin:' + os.environ['PATH']

# use the already trained model
from tensorflow.keras.models import load_model
model = load_model('storedANN/sine_v0.2.h5')

# Convert the model to FPGA firmware with hls4ml
# Make an hls4ml config & model

import hls4ml
from print_dict import print_dict

# some basic config
#hls4ml.model.optimizer.OutputRoundingSaturationMode.layers = ['Activation']
#hls4ml.model.optimizer.OutputRoundingSaturationMode.rounding_mode = 'AP_RND'
#hls4ml.model.optimizer.OutputRoundingSaturationMode.saturation_mode = 'AP_SAT'

# create basic config
model_cfg = hls4ml.utils.config_from_keras_model(model, granularity='model')
model_cfg['Model'] = {}
model_cfg['Model']['ReuseFactor'] = 1
#model_cfg['Model']['Strategy'] = 'Resource'
model_cfg['Model']['Strategy'] = 'Latency'
model_cfg['Model']['Precision'] = 'ap_fixed<16,6>'
model_cfg['Model']['Precision'] = 'ap_fixed<16,6>'

cfg = hls4ml.converters.create_config()
cfg['Backend'] = 'Vivado'               # alt: VivadoAccelerator
cfg['IOType'] = 'io_parallel'
cfg['XilinxPart'] = 'xc7a100tcsg324-1'  # Nexys 4
cfg['Part'] = cfg['XilinxPart']
cfg['HLSConfig'] = model_cfg
cfg['KerasModel'] = model
cfg['OutputDir'] = 'sinetest'
cfg['ProjectName'] = 'sinetest'
#cfg['ClockPeriod'] = 10                 # 10 ns => 100MHz
cfg['ClockPeriod'] = 4                 # 4 ns => 125MHz

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
hls_model.compile()

# Synthesize
print("Building the model ....")
print("This can take several minutes.")
hls_model.build(
                csim=True,  #
                export=True # this fails, unless you use faketime
                )

# Check the reports
hls4ml.report.read_vivado_report('sinetest')
