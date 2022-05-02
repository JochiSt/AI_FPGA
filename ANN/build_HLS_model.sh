export PATH="$PATH:/opt/Xilinx/Vivado/2020.1/bin/"
faketime -f -1y hls4ml build -p ann-hls-test --simulation --synthesis --export
#--vivado-synthesis

# --co-simulation does not work
# --validation needs co-sim
