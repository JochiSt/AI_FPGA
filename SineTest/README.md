# Sinetest
Simple network, which generates the sine from the input (0-2pi)

## Purpose
The purpose of this network is to get the chain from Keras to the FPGA working.
The network is not designed to the very best performance, it is just "a"
network, which uses some ressources.

## How to from Keras to FPGA
The network is defined in `network.py`. This is then used in the following 
steps
```
python3 training.py
python3 evaluateHLSmodel.py
./convert2FPGA.sh
```

Now the IP core is ready for beeing used in Vivado
