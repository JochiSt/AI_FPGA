import json
import os.path
import sys
sys.path.append('../')
from convert2FPGA import convert2FPGA
from tensorflow.keras.models import load_model

import hls4ml

if __name__ == "__main__":

    for clock_ns in [24,20,18,16,14,12,10,8,6,4,2]:
        filename = 'report_%d.json'%(clock_ns)
        print("Analysing %d ns ..."%(clock_ns))

        # first check, whether the report has been already created
        if os.path.exists(filename):
            print("\tFile already exists, continue...")
            continue

        model = load_model('../storedANN/sine_v0.2.h5')

        convert2FPGA(model, clock_ns)

        report = hls4ml.report.parse_vivado_report('sinetest')

        with open(filename, 'w') as outfile:
             json.dump( report, outfile,
                        sort_keys = True,
                        indent = 4,
                        ensure_ascii = True
                        )
