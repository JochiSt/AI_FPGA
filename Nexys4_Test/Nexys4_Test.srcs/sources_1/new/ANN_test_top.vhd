----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 05/02/2022 04:46:56 PM
-- Design Name: 
-- Module Name: ANN_test_top - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity ANN_test_top is
    Port ( CLK100MHZ : in STD_LOGIC;
           LED       : out std_logic_vector(15 downto 0);
           RsRx      : in STD_LOGIC;
           RsTx      : out STD_LOGIC);
end ANN_test_top;

architecture Behavioral of ANN_test_top is
    signal RX_DV    : std_logic := '0';
    signal RX_BYTE  : std_logic_vector(7 downto 0) := (others => '0');
    
    signal TX_DV    : std_logic := '0';
    signal TX_BYTE  : std_logic_vector(7 downto 0) := (others => '0');
    signal TX_ACTIVE: std_logic := '0';
    signal TX_DONE  : std_logic := '0';
    
    
    -- number clock samples per second
    constant CLKPS : integer := 100000000; -- 100 MHz
    constant BAUDRATE : integer := 115200;
    
    -- Set Generic g_CLKS_PER_BIT as follows:
    -- g_CLKS_PER_BIT = (Frequency of i_Clk)/(Frequency of UART)
    -- Example: 25 MHz Clock, 115200 baud UART = (25000000)/(115200) = 217
    constant CLKS_PER_BIT : integer := CLKPS / BAUDRATE;
begin   
 
    -- instantiate RX core
    uartrx : entity Work.UART_RX
    GENERIC MAP (
        g_CLKS_PER_BIT => CLKS_PER_BIT
    )
    PORT MAP(
        i_Clk => CLK100MHZ,
        i_RX_Serial => RsRx,
        o_RX_DV => RX_DV,
        o_RX_Byte => RX_BYTE
    );
    
    -- instantiate TX core
    uarttx : entity Work.UART_TX    
    GENERIC MAP (
        g_CLKS_PER_BIT => CLKS_PER_BIT
    )
    PORT MAP(
        i_Clk       => CLK100MHZ,
        i_TX_DV     => TX_DV,
        i_TX_Byte   => TX_BYTE,
        o_TX_Active => TX_ACTIVE,
        o_TX_Serial => RsTx,
        o_TX_Done   => TX_DONE
    );
    
    -- use the block design as a wrapper for the ANN IP core
    ann : entity Work.ANN_sandbox_wrapper
    PORT MAP (
        data_in  => RX_BYTE,
        data_out => TX_BYTE
    );

    -- simple feedthrough
    --TX_BYTE <= RX_BYTE;
    TX_DV <= RX_DV;

    LED(0) <= TX_DV;
    LED(1) <= TX_ACTIVE;
    LED(2) <= TX_DONE;
    LED(7 downto 3) <= "00000";
    LED(15 downto 8) <= TX_BYTE;
    
end Behavioral;
