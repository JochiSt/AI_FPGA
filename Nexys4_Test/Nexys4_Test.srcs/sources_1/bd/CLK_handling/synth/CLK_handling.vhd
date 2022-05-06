--Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
----------------------------------------------------------------------------------
--Tool Version: Vivado v.2020.1 (lin64) Build 2902540 Wed May 27 19:54:35 MDT 2020
--Date        : Fri May  6 15:48:39 2022
--Host        : einstein running 64-bit Ubuntu 20.04.4 LTS
--Command     : generate_target CLK_handling.bd
--Design      : CLK_handling
--Purpose     : IP block netlist
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity CLK_handling is
  port (
    CLK100MHZ : in STD_LOGIC;
    CLK20MHZ : out STD_LOGIC;
    CLK40MHZ : out STD_LOGIC;
    locked : out STD_LOGIC;
    rst : in STD_LOGIC
  );
  attribute CORE_GENERATION_INFO : string;
  attribute CORE_GENERATION_INFO of CLK_handling : entity is "CLK_handling,IP_Integrator,{x_ipVendor=xilinx.com,x_ipLibrary=BlockDiagram,x_ipName=CLK_handling,x_ipVersion=1.00.a,x_ipLanguage=VHDL,numBlks=1,numReposBlks=1,numNonXlnxBlks=0,numHierBlks=0,maxHierDepth=0,numSysgenBlks=0,numHlsBlks=0,numHdlrefBlks=0,numPkgbdBlks=0,bdsource=USER,da_board_cnt=1,synth_mode=OOC_per_IP}";
  attribute HW_HANDOFF : string;
  attribute HW_HANDOFF of CLK_handling : entity is "CLK_handling.hwdef";
end CLK_handling;

architecture STRUCTURE of CLK_handling is
  component CLK_handling_clk_wiz_0_0 is
  port (
    reset : in STD_LOGIC;
    clk_in1 : in STD_LOGIC;
    locked : out STD_LOGIC;
    CLK20MHZ : out STD_LOGIC;
    CLK40MHZ : out STD_LOGIC
  );
  end component CLK_handling_clk_wiz_0_0;
  signal CLK100MHZ_1 : STD_LOGIC;
  signal RESET_1 : STD_LOGIC;
  signal clk_wiz_0_CLK20MHZ : STD_LOGIC;
  signal clk_wiz_0_CLK40MHZ : STD_LOGIC;
  signal clk_wiz_0_locked : STD_LOGIC;
  attribute X_INTERFACE_INFO : string;
  attribute X_INTERFACE_INFO of CLK100MHZ : signal is "xilinx.com:signal:clock:1.0 CLK.CLK100MHZ CLK";
  attribute X_INTERFACE_PARAMETER : string;
  attribute X_INTERFACE_PARAMETER of CLK100MHZ : signal is "XIL_INTERFACENAME CLK.CLK100MHZ, ASSOCIATED_RESET rst, CLK_DOMAIN CLK_handling_CLK100MHZ, FREQ_HZ 100000000, FREQ_TOLERANCE_HZ 0, INSERT_VIP 0, PHASE 0.000";
  attribute X_INTERFACE_INFO of CLK20MHZ : signal is "xilinx.com:signal:clock:1.0 CLK.CLK20MHZ CLK";
  attribute X_INTERFACE_PARAMETER of CLK20MHZ : signal is "XIL_INTERFACENAME CLK.CLK20MHZ, CLK_DOMAIN CLK_handling_clk_wiz_0_0_CLK20MHZ, FREQ_HZ 20000000, FREQ_TOLERANCE_HZ 0, INSERT_VIP 0, PHASE 0.0";
  attribute X_INTERFACE_INFO of CLK40MHZ : signal is "xilinx.com:signal:clock:1.0 CLK.CLK40MHZ CLK";
  attribute X_INTERFACE_PARAMETER of CLK40MHZ : signal is "XIL_INTERFACENAME CLK.CLK40MHZ, CLK_DOMAIN CLK_handling_clk_wiz_0_0_CLK20MHZ, FREQ_HZ 40000000, FREQ_TOLERANCE_HZ 0, INSERT_VIP 0, PHASE 0.0";
  attribute X_INTERFACE_INFO of rst : signal is "xilinx.com:signal:reset:1.0 RST.RST RST";
  attribute X_INTERFACE_PARAMETER of rst : signal is "XIL_INTERFACENAME RST.RST, INSERT_VIP 0, POLARITY ACTIVE_HIGH";
begin
  CLK100MHZ_1 <= CLK100MHZ;
  CLK20MHZ <= clk_wiz_0_CLK20MHZ;
  CLK40MHZ <= clk_wiz_0_CLK40MHZ;
  RESET_1 <= rst;
  locked <= clk_wiz_0_locked;
clk_wiz_0: component CLK_handling_clk_wiz_0_0
     port map (
      CLK20MHZ => clk_wiz_0_CLK20MHZ,
      CLK40MHZ => clk_wiz_0_CLK40MHZ,
      clk_in1 => CLK100MHZ_1,
      locked => clk_wiz_0_locked,
      reset => RESET_1
    );
end STRUCTURE;
