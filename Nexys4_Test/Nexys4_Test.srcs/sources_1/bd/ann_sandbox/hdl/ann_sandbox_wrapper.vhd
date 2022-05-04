--Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
----------------------------------------------------------------------------------
--Tool Version: Vivado v.2020.1 (lin64) Build 2902540 Wed May 27 19:54:35 MDT 2020
--Date        : Wed May  4 15:59:20 2022
--Host        : einstein running 64-bit Ubuntu 20.04.4 LTS
--Command     : generate_target ann_sandbox_wrapper.bd
--Design      : ann_sandbox_wrapper
--Purpose     : IP block netlist
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity ann_sandbox_wrapper is
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
end ann_sandbox_wrapper;

architecture STRUCTURE of ann_sandbox_wrapper is
  component ann_sandbox is
  port (
    CLK100MHZ : in STD_LOGIC;
    ap_rst : in STD_LOGIC;
    const_size_in_1_0 : out STD_LOGIC_VECTOR ( 15 downto 0 );
    const_size_in_1_ap_vld_0 : out STD_LOGIC;
    const_size_out_1_0 : out STD_LOGIC_VECTOR ( 15 downto 0 );
    const_size_out_1_ap_vld_0 : out STD_LOGIC;
    data_in : in STD_LOGIC_VECTOR ( 15 downto 0 );
    data_in_valid : in STD_LOGIC;
    data_out : out STD_LOGIC_VECTOR ( 15 downto 0 );
    data_out_valid : out STD_LOGIC;
    ap_start : in STD_LOGIC;
    ap_done : out STD_LOGIC;
    ap_ready : out STD_LOGIC;
    ap_idle : out STD_LOGIC
  );
  end component ann_sandbox;
begin
ann_sandbox_i: component ann_sandbox
     port map (
      CLK100MHZ => CLK100MHZ,
      ap_done => ap_done,
      ap_idle => ap_idle,
      ap_ready => ap_ready,
      ap_rst => ap_rst,
      ap_start => ap_start,
      const_size_in_1_0(15 downto 0) => const_size_in_1_0(15 downto 0),
      const_size_in_1_ap_vld_0 => const_size_in_1_ap_vld_0,
      const_size_out_1_0(15 downto 0) => const_size_out_1_0(15 downto 0),
      const_size_out_1_ap_vld_0 => const_size_out_1_ap_vld_0,
      data_in(15 downto 0) => data_in(15 downto 0),
      data_in_valid => data_in_valid,
      data_out(15 downto 0) => data_out(15 downto 0),
      data_out_valid => data_out_valid
    );
end STRUCTURE;
