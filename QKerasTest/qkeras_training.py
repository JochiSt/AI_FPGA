"""
    Test the usage of QKeras
    
"""
# TensorFlow is an open source machine learning library
import tensorflow as tf
# Keras is TensorFlow's high-level API for deep learning
from tensorflow import keras

import qkeras

import sys
sys.path.append("../SineTest")
from training import training

quant_bit_param = (16,6,0)

layer_cnt = 0

inputs = keras.Input(shape=(1,), name="input")
# quantized_bits(bits=8, integer=0, symmetric=0, keep_negative=1)
x = qkeras.qlayers.QDense(16,
            kernel_quantizer= qkeras.quantizers.quantized_bits( *quant_bit_param ),
            bias_quantizer  = qkeras.quantizers.quantized_bits( *quant_bit_param ),
            name="layer_%d"%(layer_cnt))(inputs)
layer_cnt+=1
x = qkeras.qlayers.QActivation("quantized_relu(5)")(x)

x = qkeras.qlayers.QDense(16,
            kernel_quantizer= qkeras.quantizers.quantized_bits( *quant_bit_param ),
            bias_quantizer  = qkeras.quantizers.quantized_bits( *quant_bit_param ),
            name="layer_%d"%(layer_cnt))(x)
layer_cnt+=1
x = qkeras.qlayers.QActivation("quantized_relu(5)")(x)

# final layer
outputs = qkeras.qlayers.QDense(1,
            kernel_quantizer= qkeras.quantizers.quantized_bits( *quant_bit_param ),
            bias_quantizer  = qkeras.quantizers.quantized_bits( *quant_bit_param ),
            name="output")(x)

qmodel = keras.Model(inputs=inputs, outputs=outputs, name="QKerasTest")
qmodel.summary()

qmodel.compile(optimizer='adam',
        loss='mse',
        metrics=['mae', 'mse'])

qkeras.print_qstats(qmodel)

training(qmodel)
