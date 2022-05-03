--Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
----------------------------------------------------------------------------------
--Tool Version: Vivado v.2020.1 (lin64) Build 2902540 Wed May 27 19:54:35 MDT 2020
--Date        : Tue May  3 09:33:32 2022
--Host        : einstein running 64-bit Ubuntu 20.04.4 LTS
--Command     : generate_target ANN_sandbox_wrapper.bd
--Design      : ANN_sandbox_wrapper
--Purpose     : IP block netlist
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity ANN_sandbox_wrapper is
  port (
    data_in : in STD_LOGIC_VECTOR ( 7 downto 0 );
    data_out : out STD_LOGIC_VECTOR ( 7 downto 0 )
  );
end ANN_sandbox_wrapper;

architecture STRUCTURE of ANN_sandbox_wrapper is
  component ANN_sandbox is
  port (
    data_in : in STD_LOGIC_VECTOR ( 7 downto 0 );
    data_out : out STD_LOGIC_VECTOR ( 7 downto 0 )
  );
  end component ANN_sandbox;
begin
ANN_sandbox_i: component ANN_sandbox
     port map (
      data_in(7 downto 0) => data_in(7 downto 0),
      data_out(7 downto 0) => data_out(7 downto 0)
    );
end STRUCTURE;
