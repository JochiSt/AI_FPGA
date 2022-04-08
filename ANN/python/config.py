#!/bin/python3
import hls4ml

import yaml
# for import of keras model
from tensorflow import keras

def merge_config(start, add):
    z = start.copy()   # start with keys and values of x
    z.update(add)    # modifies z with keys and values of y
    return z

def generate_config(filename="keras-config.yml"):
    # load your hls4ml .yml config file with yaml
    with open(filename, 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)

    # load keras model from yml file
    model = keras.models.load_model(config['KerasH5'].replace('_weights','') )

    keras_config = hls4ml.utils.config_from_keras_model(model, granularity='name')
    for layer in keras_config['LayerName'].keys():
        keras_config['LayerName'][layer]['Trace'] = True

    print(keras_config)

    combined_cfg = merge_config(keras_config, config)

    print(combined_cfg)

    with open('generated_'+filename, 'w') as outfile:
        yaml.dump(combined_cfg, outfile, default_flow_style=False)

if __name__ == "__main__":
    generate_config()
