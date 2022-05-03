"""
    script to convert the network using HLS4ML in HDL code
"""

import os
#os.environ['PATH'] = '/opt/Xilinx/Vivado/2019.2/bin:' + os.environ['PATH']
os.environ['PATH'] = '/opt/Xilinx/Vivado/2020.1/bin:' + os.environ['PATH']

# use the already trained model
from tensorflow.keras.models import load_model
model = load_model('storedANN/sine_v0.1.h5')

# Convert the model to FPGA firmware with hls4ml
# Make an hls4ml config & model

import hls4ml
from print_dict import print_dict
# create basic config
config = hls4ml.utils.config_from_keras_model(model, granularity='model')

# set the reuse factor
config['Model']['ReuseFactor'] = 2
# set clock frequency
config['ClockPeriod'] = 10 # ns => 100MHz
# use parallel IO
config['IOType'] = 'io_parallel'

print("-----------------------------------")
print("Configuration")
print_dict(config)
print("-----------------------------------")
hls_model = hls4ml.converters.convert_from_keras_model(model,
                            hls_config=config,
                            project_name='sinetest',
                            output_dir='sinetest',
                            part='xc7a100tcsg324-1' # Nexys 4
                            )

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
