-- Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
-- --------------------------------------------------------------------------------
-- Tool Version: Vivado v.2020.1 (lin64) Build 2902540 Wed May 27 19:54:35 MDT 2020
-- Date        : Fri May  6 15:50:08 2022
-- Host        : einstein running 64-bit Ubuntu 20.04.4 LTS
-- Command     : write_vhdl -force -mode synth_stub
--               /home/jochen/sdvlp/ANN_FPGA/AI_FPGA/Nexys4_Test/Nexys4_Test.srcs/sources_1/bd/CLK_handling/ip/CLK_handling_clk_wiz_0_0/CLK_handling_clk_wiz_0_0_stub.vhdl
-- Design      : CLK_handling_clk_wiz_0_0
-- Purpose     : Stub declaration of top-level module interface
-- Device      : xc7a100tcsg324-1
-- --------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity CLK_handling_clk_wiz_0_0 is
  Port ( 
    CLK20MHZ : out STD_LOGIC;
    CLK40MHZ : out STD_LOGIC;
    reset : in STD_LOGIC;
    locked : out STD_LOGIC;
    clk_in1 : in STD_LOGIC
  );

end CLK_handling_clk_wiz_0_0;

architecture stub of CLK_handling_clk_wiz_0_0 is
attribute syn_black_box : boolean;
attribute black_box_pad_pin : string;
attribute syn_black_box of stub : architecture is true;
attribute black_box_pad_pin of stub : architecture is "CLK20MHZ,CLK40MHZ,reset,locked,clk_in1";
begin
end;
