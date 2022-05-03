--Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
----------------------------------------------------------------------------------
--Tool Version: Vivado v.2020.1 (lin64) Build 2902540 Wed May 27 19:54:35 MDT 2020
--Date        : Tue May  3 09:33:31 2022
--Host        : einstein running 64-bit Ubuntu 20.04.4 LTS
--Command     : generate_target ANN_sandbox.bd
--Design      : ANN_sandbox
--Purpose     : IP block netlist
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity ANN_sandbox is
  port (
    data_in : in STD_LOGIC_VECTOR ( 7 downto 0 );
    data_out : out STD_LOGIC_VECTOR ( 7 downto 0 )
  );
  attribute CORE_GENERATION_INFO : string;
  attribute CORE_GENERATION_INFO of ANN_sandbox : entity is "ANN_sandbox,IP_Integrator,{x_ipVendor=xilinx.com,x_ipLibrary=BlockDiagram,x_ipName=ANN_sandbox,x_ipVersion=1.00.a,x_ipLanguage=VHDL,numBlks=0,numReposBlks=0,numNonXlnxBlks=0,numHierBlks=0,maxHierDepth=0,numSysgenBlks=0,numHlsBlks=0,numHdlrefBlks=0,numPkgbdBlks=0,bdsource=USER,synth_mode=OOC_per_IP}";
  attribute HW_HANDOFF : string;
  attribute HW_HANDOFF of ANN_sandbox : entity is "ANN_sandbox.hwdef";
end ANN_sandbox;

architecture STRUCTURE of ANN_sandbox is
  signal data_in_1 : STD_LOGIC_VECTOR ( 7 downto 0 );
  attribute X_INTERFACE_INFO : string;
  attribute X_INTERFACE_INFO of data_in : signal is "xilinx.com:signal:data:1.0 DATA.DATA_IN DATA";
  attribute X_INTERFACE_PARAMETER : string;
  attribute X_INTERFACE_PARAMETER of data_in : signal is "XIL_INTERFACENAME DATA.DATA_IN, LAYERED_METADATA undef";
  attribute X_INTERFACE_INFO of data_out : signal is "xilinx.com:signal:data:1.0 DATA.DATA_OUT DATA";
  attribute X_INTERFACE_PARAMETER of data_out : signal is "XIL_INTERFACENAME DATA.DATA_OUT, LAYERED_METADATA undef";
begin
  data_in_1(7 downto 0) <= data_in(7 downto 0);
  data_out(7 downto 0) <= data_in_1(7 downto 0);
end STRUCTURE;
