--Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
----------------------------------------------------------------------------------
--Tool Version: Vivado v.2020.1 (lin64) Build 2902540 Wed May 27 19:54:35 MDT 2020
--Date        : Fri May  6 15:48:39 2022
--Host        : einstein running 64-bit Ubuntu 20.04.4 LTS
--Command     : generate_target CLK_handling_wrapper.bd
--Design      : CLK_handling_wrapper
--Purpose     : IP block netlist
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity CLK_handling_wrapper is
  port (
    CLK100MHZ : in STD_LOGIC;
    CLK20MHZ : out STD_LOGIC;
    CLK40MHZ : out STD_LOGIC;
    locked : out STD_LOGIC;
    rst : in STD_LOGIC
  );
end CLK_handling_wrapper;

architecture STRUCTURE of CLK_handling_wrapper is
  component CLK_handling is
  port (
    CLK100MHZ : in STD_LOGIC;
    CLK20MHZ : out STD_LOGIC;
    CLK40MHZ : out STD_LOGIC;
    locked : out STD_LOGIC;
    rst : in STD_LOGIC
  );
  end component CLK_handling;
begin
CLK_handling_i: component CLK_handling
     port map (
      CLK100MHZ => CLK100MHZ,
      CLK20MHZ => CLK20MHZ,
      CLK40MHZ => CLK40MHZ,
      locked => locked,
      rst => rst
    );
end STRUCTURE;
