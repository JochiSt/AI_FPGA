from print_dict import print_dict

# import own helper functions
import AI_TF_helpers as helpers

# QKeras
from qkeras.autoqkeras import *
from qkeras import *
from qkeras.utils import model_quantize
from qkeras.qtools import run_qtools
from qkeras.qtools import settings as qtools_settings

from network import create_model
from training import training, create_datasets

def get_computing_costs(model):
    reference_internal = "fp32"
    reference_accumulator = "fp32"
    q = run_qtools.QTools(
            model,
            # energy calculation using a given process
            # "horowitz" refers to 45nm process published at  M. Horowitz,
            # "1.1 Computing's energy problem (and what we can do about it),
            # "2014 IEEE International Solid-State Circuits Conference Digest
            # of Technical Papers (ISSCC), San Francisco, CA, 2014, pp. 10-14,
            # doi: 10.1109/ISSCC.2014.6757323.
            process="horowitz",
            # quantizers for model input
            source_quantizers=[quantized_bits(8, 0, 1)],
            is_inference=False,
            # absolute path (including filename) of the model weights
            # in the future, we will attempt to optimize the power model
            # by using weight information, although it can be used to further
            # optimize QBatchNormalization.
            weights_path=None,
            # keras_quantizer to quantize weight/bias in un-quantized keras layers
            keras_quantizer=reference_internal,
            # keras_quantizer to quantize MAC in un-quantized keras layers
            keras_accumulator=reference_accumulator,
            # whether calculate baseline energy
            for_reference=True
            )

    # caculate energy of the derived data type map.
    energy_dict = q.pe(
            # whether to store parameters in dram, sram, or fixed
            weights_on_memory="fixed",
            # store activations in dram or sram
            activations_on_memory="dram",
            # minimum sram size in number of bits. Let's assume a 16MB SRAM.
            min_sram_size=8*16*1024*1024,
            # whether load data from dram to sram (consider sram as a cache
            # for dram. If false, we will assume data will be already in SRAM
            rd_wr_on_io=False
            )

    # get stats of energy distribution in each layer
    energy_profile = q.extract_energy_profile(
                                qtools_settings.cfg.include_energy, energy_dict)

    # extract sum of energy of each layer according to the rule specified in
    # qtools_settings.cfg.include_energy
    total_energy = q.extract_energy_sum(
                                qtools_settings.cfg.include_energy, energy_dict)

    #print("Total energy: {:.2f} uJ".format(total_energy / 1000000.0))

    return total_energy, energy_profile

def quantize_model(model):
    # following 
    # https://github.com/google/qkeras/blob/master/notebook/AutoQKeras.ipynb

    # definition, which quantization is allowed
    # and their forgiving factors
    
    # alpha=1 for setting the scale factor of the number
    # from https://github.com/google/qkeras/issues/60#issuecomment-840609502
    quantization_config = {
        "kernel": {
#            "binary": 1,
#            "stochastic_binary": 1,
#            "ternary": 2,
#            "stochastic_ternary": 2,
            "quantized_bits(2,1,1,alpha=1)": 2,
            "quantized_bits(4,0,1,alpha=1)": 4,
            "quantized_bits(8,0,1,alpha=1)": 8,
#            "quantized_po2(4,1)": 4
        },
        "bias": {
            "quantized_bits(4,0,1,alpha=1)": 4,
            "quantized_bits(8,3,1,alpha=1)": 8,
#            "quantized_po2(4,8)": 4
        },
        "activation": {
#            "binary": 1,
#            "ternary": 2,
#            "quantized_relu_po2(4,4)": 4,
            "quantized_relu(3,1)": 3,
            "quantized_relu(4,2)": 4,
            "quantized_relu(8,2)": 8,
            "quantized_relu(8,4)": 8,
            "quantized_relu(16,8)": 16
        },
        "linear": {
#            "binary": 1,
#            "ternary": 2,
            "quantized_bits(4,1,alpha=1)": 4,
            "quantized_bits(8,2,alpha=1)": 8,
            "quantized_bits(16,10,alpha=1)": 16
        }
    }

    # Limits of the Quantisation
    # n.b. a Flatten layer does not change the datatype
    limit = {
        "Dense": [8, 8, 4],
        "Conv2D": [4, 8, 4],
        "DepthwiseConv2D": [4, 8, 4],
        "Activation": [4],
        "BatchNormalization": []
    }


    goal = {
        "type": "energy",   #
        "params": {
            "delta_p": 8.0,
            "delta_n": 8.0,
            "rate": 2.0,
            "stress": 1.0,
            "process": "horowitz",
            "parameters_on_memory": ["sram", "sram"],
            "activations_on_memory": ["sram", "sram"],
            "rd_wr_on_io": [False, False],
            "min_sram_size": [0, 0],
            "source_quantizers": ["int8"],
            "reference_internal": "int8",
            "reference_accumulator": "int32"
        }
    }

    cur_strategy = tf.distribute.get_strategy()
    custom_objects = {}

    run_config = {
        "output_dir": model.name+"_quant",
        "goal": goal,
        "quantization_config": quantization_config,
        "learning_rate_optimizer": False,
        # Do not transfer the weights, because the trainable parameters will
        # have different shapes
        "transfer_weights": False,
        # Operation modes
        # random, bayesian and hyperband
        # look at https://keras.io/keras_tuner/
        "mode": "random",
        "seed": 42,
        "limit": limit,
        "tune_filters": "layer",
        "tune_filters_exceptions": "",
        #"tune_filters_exceptions": "^dense",
        "distribution_strategy": cur_strategy,
        # first layer is input, last layer is output
        "layer_indexes": range(1, len(model.layers) - 1),
        # how many optimisation trials should be done?
        "max_trials": 4,
    }

    print("quantizing layers:",\
            [model.layers[i].name for i in run_config["layer_indexes"]]
            )

    autoqk = AutoQKeras(model, metrics=["mse"], 
                    custom_objects=custom_objects, **run_config)

    x_train, x_test, x_validate,\
    y_train, y_test, y_validate = create_datasets(10000)

    autoqk.fit(x_train, y_train, validation_data=(x_test, y_test),
                                batch_size=50,
                                epochs=50
                        )

    print("\n"*4)
    print("#"*80)
    print("Train Best Model")
    
    qmodel = autoqk.get_best_model()

    qmodel.fit(x_train, y_train, 
                validation_data=(x_test, y_test),
                batch_size=50,
                epochs=50
                )

    print("#"*80)
    print("Model Summary:")
    qmodel.summary()

    print("#"*80)
    print("Qstats:")
    print_qstats(qmodel)

    print("#"*80)
    qmodel._name = qmodel.name + "_quant"
    return qmodel

if __name__ == "__main__":
    # use the already trained model
    from tensorflow.keras.models import load_model
    model = load_model('storedANN/sine_v0.2.h5')

    # unfortunately, saving this model does not work
    #model = create_model(quantized=False)
    #model = training(model, store=False)

    qmodel = quantize_model(model)
    
    #training(qmodel)
        
    helpers.save_model(qmodel)
