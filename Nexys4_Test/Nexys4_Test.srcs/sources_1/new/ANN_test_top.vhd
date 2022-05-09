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
use IEEE.NUMERIC_STD.ALL; -- support for signed / unsigned values

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity ANN_test_top is
    Port ( CLK100MHZ : in STD_LOGIC;
    
           LED       : out std_logic_vector(15 downto 0);
           
           RGB1_Red  : out std_logic;
           RGB1_Green: out std_logic;
           RGB1_Blue : out std_logic;
           
           RGB2_Red  : out std_logic;
           RGB2_Green: out std_logic;
           RGB2_Blue : out std_logic;
           
           RsRx      : in STD_LOGIC;
           RsTx      : out STD_LOGIC);
end ANN_test_top;

architecture Behavioral of ANN_test_top is
    ----------------------------------------------------------------------------
    -- Connections to the UART
    signal RX_DV                : std_logic := '0';
    signal RX_BYTE              : std_logic_vector(7 downto 0) := (others=>'0');
    
    signal TX_DV                : std_logic := '0';
    signal TX_BYTE              : std_logic_vector(7 downto 0) := (others=>'0');
    signal TX_ACTIVE            : std_logic := '0';
    signal TX_DONE              : std_logic := '0';
    ----------------------------------------------------------------------------
    -- number clock samples per second
    constant CLKPS              : integer := 100000000; -- 100 MHz
    constant BAUDRATE           : integer := 115200;
    
    -- Set Generic g_CLKS_PER_BIT as follows:
    -- g_CLKS_PER_BIT = (Frequency of i_Clk)/(Frequency of UART)
    -- Example: 25 MHz Clock, 115200 baud UART = (25000000)/(115200) = 217
    constant CLKS_PER_BIT       : integer := CLKPS / BAUDRATE;
    ----------------------------------------------------------------------------
    -- Signals for ANN control / status
    signal ap_done              : STD_LOGIC;    -- DONE
    signal ap_idle              : STD_LOGIC;    -- IDLE
    signal ap_ready             : STD_LOGIC;    -- READY
        
    signal ap_rst               : STD_LOGIC := '1';    -- RESET
    signal ap_start             : STD_LOGIC := '0';    -- START
    ----------------------------------------------------------------------------
    -- Signals for ANN Data IN and OUT
    signal ap_data_in           : STD_LOGIC_VECTOR(15 downto 0);
    signal ap_data_in_valid     : STD_LOGIC := '0';
    signal ap_data_out          : STD_LOGIC_VECTOR(15 downto 0);    
    signal ap_data_out_valid    : STD_LOGIC := '0';
    
    ----------------------------------------------------------------------------
    -- some constants, which are generated from Vivado HLS
    signal const_size_in_1_0         : STD_LOGIC_VECTOR (15 downto 0);
    signal const_size_in_1_ap_vld_0  : STD_LOGIC;
    signal const_size_out_1_0        : STD_LOGIC_VECTOR (15 downto 0);
    signal const_size_out_1_ap_vld_0 : STD_LOGIC;
    ----------------------------------------------------------------------------
    -- merge 2x 8 bit of the UART RX into 1x 16 bit for the ANN
    signal RX_upper_lower       : std_logic := '0';
    signal RX_valid             : std_logic := '0';
    signal RX_16bit             : std_logic_vector(15 downto 0):=(others =>'0');
    
    signal TX_upper_lower       : std_logic := '0';
    signal TX_valid             : std_logic := '0';
    signal TX_16bit             : std_logic_vector(15 downto 0):=(others =>'0');
    ----------------------------------------------------------------------------
    
    signal CLK_20MHZ            : std_logic := '0';
    signal CLK_40MHZ            : std_logic := '0';
    signal CLK_locked           : std_logic := '0';
    signal CLK_rst              : std_logic := '1';
begin  

    clk_handling : entity Work.CLK_handling_wrapper
    port map(
        CLK100MHZ => CLK100MHZ,
        CLK20MHZ => CLK_20MHZ,
        CLK40MHZ => CLK_40MHZ,
        locked => CLK_locked,
        rst => CLK_rst
    );
 
    ----------------------------------------------------------------------------
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
    ----------------------------------------------------------------------------
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
    ----------------------------------------------------------------------------

    ----------------------------------------------------------------------------
    -- use the block design as a wrapper for the ANN IP core
    ann : entity Work.ANN_sandbox_wrapper
    PORT MAP (
        -- clock
        CLK100MHZ => CLK100MHZ,
        
        -- control signals 
        -- have a look at UG902 page 80
        -- inputs
        ap_rst => ap_rst,
        ap_start => ap_start,
        -- outputs
        ap_done => ap_done,
        ap_idle => ap_idle,
        ap_ready => ap_ready,
                
        -- ignore these values for the moment
        const_size_in_1_0 => const_size_in_1_0,
        const_size_in_1_ap_vld_0 => const_size_in_1_ap_vld_0,
        const_size_out_1_0 => const_size_out_1_0,
        const_size_out_1_ap_vld_0 => const_size_out_1_ap_vld_0,
        
        -- data input (from FPGA to ANN)
        data_in  => ap_data_in,   -- 15 downto 0
        data_in_valid => ap_data_in_valid,
        
        -- data output (from ANN to FPGA)
        data_out => ap_data_out,  -- 15 downto 0
        data_out_valid => ap_data_out_valid
    );
    ----------------------------------------------------------------------------
    -- Receive 2x8bit and put it into 1x16bit
    receive_16bit : process(CLK100MHZ)
    begin
        if rising_edge(CLK100MHZ) then
        
            -- data is just valid for a single clock cycle
            if RX_valid = '1' then
                RX_valid <= '0';
            end if;
            
            -- we send one byte and receive one byte
            if TX_DONE = '1' then
                if TX_DV = '1' then
                    TX_DV <= '0';
                end if;
            end if;
            
            if RX_DV = '1' then
                -- reset
                if RX_BYTE = std_logic_vector(to_unsigned(character'pos('r'),8)) then
                    ap_rst <= '0';
                elsif RX_BYTE = std_logic_vector(to_unsigned(character'pos('R'),8)) then
                    ap_rst <= '1';

                -- set upper / lower part of the 16bit input, which is fed to 
                -- the ANN
                elsif RX_BYTE = std_logic_vector(to_unsigned(character'pos('u'),8)) then
                    RX_upper_lower <= '1';
                elsif RX_BYTE = std_logic_vector(to_unsigned(character'pos('l'),8)) then
                    RX_upper_lower <= '0';
                
                -- get the result of the ANN
                elsif RX_BYTE = std_logic_vector(to_unsigned(character'pos('U'),8)) then
                    TX_BYTE <= TX_16bit(15 downto 8);
                    TX_DV <= '1';
                elsif RX_BYTE = std_logic_vector(to_unsigned(character'pos('L'),8)) then
                    TX_BYTE <= TX_16bit(7 downto 0);
                    TX_DV <= '1';
                    
                -- trigger the computation of the ANN
                elsif RX_BYTE = std_logic_vector(to_unsigned(character'pos('c'),8)) then
                    TX_16bit <= ap_data_out;
                    
                elsif RX_BYTE = std_logic_vector(to_unsigned(character'pos('C'),8)) then
                    TX_16bit <= RX_16bit;  -- simple feed through just for debug
                    
                else -- ignore characters, which are needed somewhere else
                    -- fill 16bit alternating
                    if RX_upper_lower = '0' then
                        RX_16bit( 7 downto 0) <= RX_BYTE;
                    else
                        RX_16bit(15 downto 8) <= RX_BYTE;
                        RX_valid <= '1';
                    end if;
                end if;
            end if;
            
            -- ap_start can be just the inverse of ap_rst
            ap_start <= not ap_rst;

            -- we send one byte and receive one byte
            TX_DV <= RX_DV;
        end if;
    end process receive_16bit;
        
    -- foward the data to the ANN
    -- own process for possible future extensions
    foward_data_ann : process(CLK100MHZ)
    begin
        if rising_edge(CLK100MHZ) then
        
            if RX_valid = '1' then
                ap_data_in <= RX_16bit;
            end if;
            
            ap_data_in_valid <= RX_valid;
            
            -- if ap_rst = '1' then
                -- TX_16bit <= (others => '0');
            -- elsif ap_data_out_valid = '1' then
                -- TX_16bit <= ap_data_out;
            -- end if;
            
        end if;
    end process foward_data_ann;
    
    ---------------------------------------------------------------------------
    -- connections to the LEDs
    -- normal operation
    -- LED(0) <= ap_rst;
    -- LED(1) <= ap_start;
    
    -- LED(2) <= ap_idle;
    -- LED(3) <= ap_ready;
    -- LED(4) <= ap_done;
    
    -- LED(7 downto 5) <= (others => '0');
    
    -- -- upper 8 LEDs are ANN output data, just something, not really meaningful
    -- LED(15 downto 8) <= ap_data_out(15 downto 8);
    
    --LED <= ap_data_out;
    LED <= TX_16bit;
    
    RGB1_Red    <= RX_upper_lower;
    RGB1_Blue   <= TX_upper_lower;
    RGB1_Green  <= ap_rst;
    
    RGB2_Red    <= ap_start;
    RGB2_Blue   <= ap_ready;
    RGB2_Green  <= ap_idle;
        
end Behavioral;
