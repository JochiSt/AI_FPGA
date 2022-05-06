// Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2020.1 (lin64) Build 2902540 Wed May 27 19:54:35 MDT 2020
// Date        : Fri May  6 15:50:08 2022
// Host        : einstein running 64-bit Ubuntu 20.04.4 LTS
// Command     : write_verilog -force -mode synth_stub
//               /home/jochen/sdvlp/ANN_FPGA/AI_FPGA/Nexys4_Test/Nexys4_Test.srcs/sources_1/bd/CLK_handling/ip/CLK_handling_clk_wiz_0_0/CLK_handling_clk_wiz_0_0_stub.v
// Design      : CLK_handling_clk_wiz_0_0
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7a100tcsg324-1
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
module CLK_handling_clk_wiz_0_0(CLK20MHZ, CLK40MHZ, reset, locked, clk_in1)
/* synthesis syn_black_box black_box_pad_pin="CLK20MHZ,CLK40MHZ,reset,locked,clk_in1" */;
  output CLK20MHZ;
  output CLK40MHZ;
  input reset;
  output locked;
  input clk_in1;
endmodule
