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
If the installation seems to be on hold, fake `/etc/os-releases` to a version, which is officially supported by Xilinx. (see this answer record)[https://support.xilinx.com/s/question/0D52E00006iHj2dSAC/xilinx-unified-installer-20201-exception-in-thread-splashloadmessage-ubuntu?language=en_US]
