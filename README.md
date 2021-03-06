# AI_FPGA
Goal is to run a Tensorflow / Keras ANN on an FPGA using HLS4ML.

# Setup
create virtual environment
```
python3 -m venv HLS4ML
. HLS4ML/bin/activate
```

install hls4ml and tensorflow
```
pip install hls4ml
pip install tensorflow
```

## Installation Xilinx Vivado 2020.1
If the installation seems to be on hold, fake `/etc/os-releases` to a version, which is officially supported by Xilinx [see this answer record](https://support.xilinx.com/s/question/0D52E00006iHj2dSAC/xilinx-unified-installer-20201-exception-in-thread-splashloadmessage-ubuntu?language=en_US)

If the installation stops on generating the installed hardware list - [this answer records helped me](https://support.xilinx.com/s/question/0D52E00006iHjbcSAC/vivado-20211-installation-hangs-at-generating-installed-device-list?language=en_US) - and I generated this list manually after the installer exits.


### Install Digilent Board files
This [manual](https://digilent.com/reference/programmable-logic/guides/installing-vivado-and-vitis) from Digilent helped me to install the Board Files from Digilent.

# HLS4ML Tutorial
There is a HLS4ML tutorial at https://github.com/fastmachinelearning/hls4ml-tutorial focusing on HEP.
This is based on: `Vivado(TM) HLS - High-Level Synthesis from C, C++ and SystemC v2019.2 (64-bit)`

# References
[1] https://fastmachinelearning.org/hls4ml/
[2] https://jiafulow.github.io/blog/2021/02/17/simple-fully-connected-nn-firmware-using-hls4ml/
