
################################################################
# This is a generated script based on design: ann_sandbox
#
# Though there are limitations about the generated script,
# the main purpose of this utility is to make learning
# IP Integrator Tcl commands easier.
################################################################

namespace eval _tcl {
proc get_script_folder {} {
   set script_path [file normalize [info script]]
   set script_folder [file dirname $script_path]
   return $script_folder
}
}
variable script_folder
set script_folder [_tcl::get_script_folder]

################################################################
# Check if script is running in correct Vivado version.
################################################################
set scripts_vivado_version 2020.1
set current_vivado_version [version -short]

if { [string first $scripts_vivado_version $current_vivado_version] == -1 } {
   puts ""
   catch {common::send_gid_msg -ssname BD::TCL -id 2041 -severity "ERROR" "This script was generated using Vivado <$scripts_vivado_version> and is being run in <$current_vivado_version> of Vivado. Please run the script in Vivado <$scripts_vivado_version> then open the design in Vivado <$current_vivado_version>. Upgrade the design by running \"Tools => Report => Report IP Status...\", then run write_bd_tcl to create an updated script."}

   return 1
}

################################################################
# START
################################################################

# To test this script, run the following commands from Vivado Tcl console:
# source ann_sandbox_script.tcl

# If there is no project opened, this script will create a
# project, but make sure you do not have an existing project
# <./myproj/project_1.xpr> in the current working folder.

set list_projs [get_projects -quiet]
if { $list_projs eq "" } {
   create_project project_1 myproj -part xc7a100tcsg324-1
   set_property BOARD_PART digilentinc.com:nexys4:part0:1.1 [current_project]
}


# CHANGE DESIGN NAME HERE
variable design_name
set design_name ann_sandbox

# If you do not already have an existing IP Integrator design open,
# you can create a design using the following command:
#    create_bd_design $design_name

# Creating design if needed
set errMsg ""
set nRet 0

set cur_design [current_bd_design -quiet]
set list_cells [get_bd_cells -quiet]

if { ${design_name} eq "" } {
   # USE CASES:
   #    1) Design_name not set

   set errMsg "Please set the variable <design_name> to a non-empty value."
   set nRet 1

} elseif { ${cur_design} ne "" && ${list_cells} eq "" } {
   # USE CASES:
   #    2): Current design opened AND is empty AND names same.
   #    3): Current design opened AND is empty AND names diff; design_name NOT in project.
   #    4): Current design opened AND is empty AND names diff; design_name exists in project.

   if { $cur_design ne $design_name } {
      common::send_gid_msg -ssname BD::TCL -id 2001 -severity "INFO" "Changing value of <design_name> from <$design_name> to <$cur_design> since current design is empty."
      set design_name [get_property NAME $cur_design]
   }
   common::send_gid_msg -ssname BD::TCL -id 2002 -severity "INFO" "Constructing design in IPI design <$cur_design>..."

} elseif { ${cur_design} ne "" && $list_cells ne "" && $cur_design eq $design_name } {
   # USE CASES:
   #    5) Current design opened AND has components AND same names.

   set errMsg "Design <$design_name> already exists in your project, please set the variable <design_name> to another value."
   set nRet 1
} elseif { [get_files -quiet ${design_name}.bd] ne "" } {
   # USE CASES: 
   #    6) Current opened design, has components, but diff names, design_name exists in project.
   #    7) No opened design, design_name exists in project.

   set errMsg "Design <$design_name> already exists in your project, please set the variable <design_name> to another value."
   set nRet 2

} else {
   # USE CASES:
   #    8) No opened design, design_name not in project.
   #    9) Current opened design, has components, but diff names, design_name not in project.

   common::send_gid_msg -ssname BD::TCL -id 2003 -severity "INFO" "Currently there is no design <$design_name> in project, so creating one..."

   create_bd_design $design_name

   common::send_gid_msg -ssname BD::TCL -id 2004 -severity "INFO" "Making design <$design_name> as current_bd_design."
   current_bd_design $design_name

}

common::send_gid_msg -ssname BD::TCL -id 2005 -severity "INFO" "Currently the variable <design_name> is equal to \"$design_name\"."

if { $nRet != 0 } {
   catch {common::send_gid_msg -ssname BD::TCL -id 2006 -severity "ERROR" $errMsg}
   return $nRet
}

##################################################################
# DESIGN PROCs
##################################################################



# Procedure to create entire design; Provide argument to make
# procedure reusable. If parentCell is "", will use root.
proc create_root_design { parentCell } {

  variable script_folder
  variable design_name

  if { $parentCell eq "" } {
     set parentCell [get_bd_cells /]
  }

  # Get object for parentCell
  set parentObj [get_bd_cells $parentCell]
  if { $parentObj == "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2090 -severity "ERROR" "Unable to find parent cell <$parentCell>!"}
     return
  }

  # Make sure parentObj is hier blk
  set parentType [get_property TYPE $parentObj]
  if { $parentType ne "hier" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2091 -severity "ERROR" "Parent <$parentObj> has TYPE = <$parentType>. Expected to be <hier>."}
     return
  }

  # Save current instance; Restore later
  set oldCurInst [current_bd_instance .]

  # Set parent object as current
  current_bd_instance $parentObj


  # Create interface ports

  # Create ports
  set CLK100MHZ [ create_bd_port -dir I -type clk CLK100MHZ ]
  set ap_done [ create_bd_port -dir O ap_done ]
  set ap_idle [ create_bd_port -dir O ap_idle ]
  set ap_ready [ create_bd_port -dir O ap_ready ]
  set ap_rst [ create_bd_port -dir I -type rst ap_rst ]
  set_property -dict [ list \
   CONFIG.POLARITY {ACTIVE_HIGH} \
 ] $ap_rst
  set ap_start [ create_bd_port -dir I ap_start ]
  set const_size_in_1_0 [ create_bd_port -dir O -from 15 -to 0 -type data const_size_in_1_0 ]
  set const_size_in_1_ap_vld_0 [ create_bd_port -dir O const_size_in_1_ap_vld_0 ]
  set const_size_out_1_0 [ create_bd_port -dir O -from 15 -to 0 -type data const_size_out_1_0 ]
  set const_size_out_1_ap_vld_0 [ create_bd_port -dir O const_size_out_1_ap_vld_0 ]
  set data_in [ create_bd_port -dir I -from 15 -to 0 -type data data_in ]
  set data_in_valid [ create_bd_port -dir I data_in_valid ]
  set data_out [ create_bd_port -dir O -from 15 -to 0 -type data data_out ]
  set data_out_valid [ create_bd_port -dir O data_out_valid ]

  # Create instance: sinetest_0, and set properties
  set sinetest_0 [ create_bd_cell -type ip -vlnv JochiSt:SineTest:sinetest:0.1 sinetest_0 ]

  # Create port connections
  connect_bd_net -net ap_clk_0_1 [get_bd_ports CLK100MHZ] [get_bd_pins sinetest_0/ap_clk]
  connect_bd_net -net ap_rst_0_1 [get_bd_ports ap_rst] [get_bd_pins sinetest_0/ap_rst]
  connect_bd_net -net ap_start_1 [get_bd_ports ap_start] [get_bd_pins sinetest_0/ap_start]
  connect_bd_net -net input_V_0_1 [get_bd_ports data_in] [get_bd_pins sinetest_0/input_V]
  connect_bd_net -net input_V_ap_vld_0_1 [get_bd_ports data_in_valid] [get_bd_pins sinetest_0/input_V_ap_vld]
  connect_bd_net -net sinetest_0_ap_done [get_bd_ports ap_done] [get_bd_pins sinetest_0/ap_done]
  connect_bd_net -net sinetest_0_ap_idle [get_bd_ports ap_idle] [get_bd_pins sinetest_0/ap_idle]
  connect_bd_net -net sinetest_0_ap_ready [get_bd_ports ap_ready] [get_bd_pins sinetest_0/ap_ready]
  connect_bd_net -net sinetest_0_const_size_in_1 [get_bd_ports const_size_in_1_0] [get_bd_pins sinetest_0/const_size_in_1]
  connect_bd_net -net sinetest_0_const_size_in_1_ap_vld [get_bd_ports const_size_in_1_ap_vld_0] [get_bd_pins sinetest_0/const_size_in_1_ap_vld]
  connect_bd_net -net sinetest_0_const_size_out_1 [get_bd_ports const_size_out_1_0] [get_bd_pins sinetest_0/const_size_out_1]
  connect_bd_net -net sinetest_0_const_size_out_1_ap_vld [get_bd_ports const_size_out_1_ap_vld_0] [get_bd_pins sinetest_0/const_size_out_1_ap_vld]
  connect_bd_net -net sinetest_0_layer16_out_0_V [get_bd_ports data_out] [get_bd_pins sinetest_0/layer8_out_0_V]
  connect_bd_net -net sinetest_0_layer16_out_0_V_ap_vld [get_bd_ports data_out_valid] [get_bd_pins sinetest_0/layer8_out_0_V_ap_vld]

  # Create address segments


  # Restore current instance
  current_bd_instance $oldCurInst

  validate_bd_design
  save_bd_design
}
# End of create_root_design()


##################################################################
# MAIN FLOW
##################################################################

create_root_design ""


