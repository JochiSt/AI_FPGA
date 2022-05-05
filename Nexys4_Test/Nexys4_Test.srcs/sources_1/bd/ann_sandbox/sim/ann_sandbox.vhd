--Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
----------------------------------------------------------------------------------
--Tool Version: Vivado v.2020.1 (lin64) Build 2902540 Wed May 27 19:54:35 MDT 2020
--Date        : Thu May  5 08:00:49 2022
--Host        : einstein running 64-bit Ubuntu 20.04.4 LTS
--Command     : generate_target ann_sandbox.bd
--Design      : ann_sandbox
--Purpose     : IP block netlist
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity ann_sandbox is
  port (
    CLK100MHZ : in STD_LOGIC;
    ap_done : out STD_LOGIC;
    ap_idle : out STD_LOGIC;
    ap_ready : out STD_LOGIC;
    ap_rst : in STD_LOGIC;
    ap_start : in STD_LOGIC;
    const_size_in_1_0 : out STD_LOGIC_VECTOR ( 15 downto 0 );
    const_size_in_1_ap_vld_0 : out STD_LOGIC;
    const_size_out_1_0 : out STD_LOGIC_VECTOR ( 15 downto 0 );
    const_size_out_1_ap_vld_0 : out STD_LOGIC;
    data_in : in STD_LOGIC_VECTOR ( 15 downto 0 );
    data_in_valid : in STD_LOGIC;
    data_out : out STD_LOGIC_VECTOR ( 15 downto 0 );
    data_out_valid : out STD_LOGIC
  );
  attribute CORE_GENERATION_INFO : string;
  attribute CORE_GENERATION_INFO of ann_sandbox : entity is "ann_sandbox,IP_Integrator,{x_ipVendor=xilinx.com,x_ipLibrary=BlockDiagram,x_ipName=ann_sandbox,x_ipVersion=1.00.a,x_ipLanguage=VHDL,numBlks=1,numReposBlks=1,numNonXlnxBlks=1,numHierBlks=0,maxHierDepth=0,numSysgenBlks=0,numHlsBlks=1,numHdlrefBlks=0,numPkgbdBlks=0,bdsource=USER,da_clkrst_cnt=2,synth_mode=Global}";
  attribute HW_HANDOFF : string;
  attribute HW_HANDOFF of ann_sandbox : entity is "ann_sandbox.hwdef";
end ann_sandbox;

architecture STRUCTURE of ann_sandbox is
  component ann_sandbox_sinetest_0_0 is
  port (
    input_V_ap_vld : in STD_LOGIC;
    const_size_in_1_ap_vld : out STD_LOGIC;
    const_size_out_1_ap_vld : out STD_LOGIC;
    layer16_out_0_V_ap_vld : out STD_LOGIC;
    input_V : in STD_LOGIC_VECTOR ( 15 downto 0 );
    layer16_out_0_V : out STD_LOGIC_VECTOR ( 15 downto 0 );
    const_size_in_1 : out STD_LOGIC_VECTOR ( 15 downto 0 );
    const_size_out_1 : out STD_LOGIC_VECTOR ( 15 downto 0 );
    ap_clk : in STD_LOGIC;
    ap_rst : in STD_LOGIC;
    ap_start : in STD_LOGIC;
    ap_done : out STD_LOGIC;
    ap_ready : out STD_LOGIC;
    ap_idle : out STD_LOGIC
  );
  end component ann_sandbox_sinetest_0_0;
  signal ap_clk_0_1 : STD_LOGIC;
  signal ap_rst_0_1 : STD_LOGIC;
  signal ap_start_1 : STD_LOGIC;
  signal input_V_0_1 : STD_LOGIC_VECTOR ( 15 downto 0 );
  signal input_V_ap_vld_0_1 : STD_LOGIC;
  signal sinetest_0_ap_done : STD_LOGIC;
  signal sinetest_0_ap_idle : STD_LOGIC;
  signal sinetest_0_ap_ready : STD_LOGIC;
  signal sinetest_0_const_size_in_1 : STD_LOGIC_VECTOR ( 15 downto 0 );
  signal sinetest_0_const_size_in_1_ap_vld : STD_LOGIC;
  signal sinetest_0_const_size_out_1 : STD_LOGIC_VECTOR ( 15 downto 0 );
  signal sinetest_0_const_size_out_1_ap_vld : STD_LOGIC;
  signal sinetest_0_layer16_out_0_V : STD_LOGIC_VECTOR ( 15 downto 0 );
  signal sinetest_0_layer16_out_0_V_ap_vld : STD_LOGIC;
  attribute X_INTERFACE_INFO : string;
  attribute X_INTERFACE_INFO of CLK100MHZ : signal is "xilinx.com:signal:clock:1.0 CLK.CLK100MHZ CLK";
  attribute X_INTERFACE_PARAMETER : string;
  attribute X_INTERFACE_PARAMETER of CLK100MHZ : signal is "XIL_INTERFACENAME CLK.CLK100MHZ, ASSOCIATED_RESET ap_rst, CLK_DOMAIN ann_sandbox_CLK100MHZ, FREQ_HZ 100000000, FREQ_TOLERANCE_HZ 0, INSERT_VIP 0, PHASE 0.000";
  attribute X_INTERFACE_INFO of ap_rst : signal is "xilinx.com:signal:reset:1.0 RST.AP_RST RST";
  attribute X_INTERFACE_PARAMETER of ap_rst : signal is "XIL_INTERFACENAME RST.AP_RST, INSERT_VIP 0, POLARITY ACTIVE_HIGH";
  attribute X_INTERFACE_INFO of const_size_in_1_0 : signal is "xilinx.com:signal:data:1.0 DATA.CONST_SIZE_IN_1_0 DATA";
  attribute X_INTERFACE_PARAMETER of const_size_in_1_0 : signal is "XIL_INTERFACENAME DATA.CONST_SIZE_IN_1_0, LAYERED_METADATA undef";
  attribute X_INTERFACE_INFO of const_size_out_1_0 : signal is "xilinx.com:signal:data:1.0 DATA.CONST_SIZE_OUT_1_0 DATA";
  attribute X_INTERFACE_PARAMETER of const_size_out_1_0 : signal is "XIL_INTERFACENAME DATA.CONST_SIZE_OUT_1_0, LAYERED_METADATA undef";
  attribute X_INTERFACE_INFO of data_in : signal is "xilinx.com:signal:data:1.0 DATA.DATA_IN DATA";
  attribute X_INTERFACE_PARAMETER of data_in : signal is "XIL_INTERFACENAME DATA.DATA_IN, LAYERED_METADATA undef";
  attribute X_INTERFACE_INFO of data_out : signal is "xilinx.com:signal:data:1.0 DATA.DATA_OUT DATA";
  attribute X_INTERFACE_PARAMETER of data_out : signal is "XIL_INTERFACENAME DATA.DATA_OUT, LAYERED_METADATA undef";
begin
  ap_clk_0_1 <= CLK100MHZ;
  ap_done <= sinetest_0_ap_done;
  ap_idle <= sinetest_0_ap_idle;
  ap_ready <= sinetest_0_ap_ready;
  ap_rst_0_1 <= ap_rst;
  ap_start_1 <= ap_start;
  const_size_in_1_0(15 downto 0) <= sinetest_0_const_size_in_1(15 downto 0);
  const_size_in_1_ap_vld_0 <= sinetest_0_const_size_in_1_ap_vld;
  const_size_out_1_0(15 downto 0) <= sinetest_0_const_size_out_1(15 downto 0);
  const_size_out_1_ap_vld_0 <= sinetest_0_const_size_out_1_ap_vld;
  data_out(15 downto 0) <= sinetest_0_layer16_out_0_V(15 downto 0);
  data_out_valid <= sinetest_0_layer16_out_0_V_ap_vld;
  input_V_0_1(15 downto 0) <= data_in(15 downto 0);
  input_V_ap_vld_0_1 <= data_in_valid;
sinetest_0: component ann_sandbox_sinetest_0_0
     port map (
      ap_clk => ap_clk_0_1,
      ap_done => sinetest_0_ap_done,
      ap_idle => sinetest_0_ap_idle,
      ap_ready => sinetest_0_ap_ready,
      ap_rst => ap_rst_0_1,
      ap_start => ap_start_1,
      const_size_in_1(15 downto 0) => sinetest_0_const_size_in_1(15 downto 0),
      const_size_in_1_ap_vld => sinetest_0_const_size_in_1_ap_vld,
      const_size_out_1(15 downto 0) => sinetest_0_const_size_out_1(15 downto 0),
      const_size_out_1_ap_vld => sinetest_0_const_size_out_1_ap_vld,
      input_V(15 downto 0) => input_V_0_1(15 downto 0),
      input_V_ap_vld => input_V_ap_vld_0_1,
      layer16_out_0_V(15 downto 0) => sinetest_0_layer16_out_0_V(15 downto 0),
      layer16_out_0_V_ap_vld => sinetest_0_layer16_out_0_V_ap_vld
    );
end STRUCTURE;
