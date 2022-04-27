export PATH="$PATH:/opt/Xilinx/Vivado/2020.1/bin/"
hls4ml build -p sinetest --simulation --synthesis --export
#--vivado-synthesis

# --co-simulation does not work
# --validation needs co-sim
