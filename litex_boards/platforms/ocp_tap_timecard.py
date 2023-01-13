#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2023 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

# TimeCard project:
# https://opencomputeproject.github.io/Time-Appliance-Project/docs/time-card/introduction

# FPGA SoM:
# http://www.alinx.vip:81/ug_en/AC7100B_User_Manual.pdf

from litex.build.generic_platform import *
from litex.build.xilinx import Xilinx7SeriesPlatform, VivadoProgrammer
from litex.build.openocd import OpenOCD

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst.
    ("clk125", 0,
        Subsignal("p", Pins("F6"), IOStandard("DIFF_SSTL15")),
        Subsignal("n", Pins("E6"), IOStandard("DIFF_SSTL15"))
    ),
    ("clk200", 0,
        Subsignal("p", Pins("R4"), IOStandard("DIFF_SSTL15")),
        Subsignal("n", Pins("T4"), IOStandard("DIFF_SSTL15"))
    ),
    ("rst_n", 0, Pins("T6"), IOStandard("LVCMOS15")),

    # Leds.
    ("user_led", 0, Pins("B13"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("C13"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("D14"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("D15"), IOStandard("LVCMOS33")),

    # Buttons.
    ("user_btn", 0, Pins("J21"), IOStandard("LVCMOS33")),
    ("user_btn", 1, Pins("E13"), IOStandard("LVCMOS33")),

    # SPIFlash.
    ("flash_cs_n", 0, Pins("T19"), IOStandard("LVCMOS33")),
    ("flash", 0,
        Subsignal("mosi", Pins("P22")),
        Subsignal("miso", Pins("R22")),
        Subsignal("wp",   Pins("P21")),
        Subsignal("hold", Pins("R21")),
        IOStandard("LVCMOS33")
    ),

    # PCIe.
    ("pcie_x1", 0,
        Subsignal("rst_n", Pins("J20"), IOStandard("LVCMOS33"), Misc("PULLUP=TRUE")),
        Subsignal("clk_p", Pins("F10")),
        Subsignal("clk_n", Pins("E10")),
        Subsignal("rx_p",  Pins("D11")),
        Subsignal("rx_n",  Pins("C11")),
        Subsignal("tx_p",  Pins("D5")),
        Subsignal("tx_n",  Pins("C5")),
    ),

    # Leds.
    ("led", 0, Pins("E21"), IOStandard("LVCMOS33")),
    ("led", 1, Pins("D21"), IOStandard("LVCMOS33")),
    ("led", 2, Pins("E22"), IOStandard("LVCMOS33")),
    ("led", 3, Pins("D22"), IOStandard("LVCMOS33")),

    # I2C.
    ("i2c", 0,
        Subsignal("scl", Pins("N17"), Misc("PULLUP=True")),
        Subsignal("sda", Pins("T16"), Misc("PULLUP=True")),
        IOStandard("LVCMOS33")
    ),

    # PMOD.
    ("pmod", 0, Pins("M22 N22 H18 H17 H22 J22 K21 K22"), IOStandard("LVCMOS33")),

    # GPS.
    ("gps", 0,
        Subsignal("rst_n", Pins("Y16")),
        Subsignal("tx",    Pins("P20")),
        Subsignal("rx",    Pins("N15")),
        Subsignal("tp",    Pins("W14 Y14")),
        IOStandard("LVCMOS33")
    ),
    ("gps", 1,
        Subsignal("rst_n", Pins("G15")),
        Subsignal("tx",    Pins("M17")),
        Subsignal("rx",    Pins("J16")),
        Subsignal("tp",    Pins("G17 G18")),
        IOStandard("LVCMOS33")
    ),

    # SMAs.
    ("sma", 0,
        Subsignal("in",     Pins("Y11"), IOStandard("LVCMOS33"), Misc("PULLDOWN=TRUE")),
        Subsignal("in_en",  Pins("H15"), IOStandard("LVCMOS33")),
        Subsignal("out",    Pins("W11"), IOStandard("LVCMOS33"), Misc("DRIVE=16")),
        Subsignal("out_en", Pins("J15"), IOStandard("LVCMOS33")),
    ),
    ("sma", 1,
        Subsignal("in",     Pins("Y12"), IOStandard("LVCMOS33"), Misc("PULLDOWN=TRUE")),
        Subsignal("in_en",  Pins("J14"), IOStandard("LVCMOS33")),
        Subsignal("out",    Pins("W12"), IOStandard("LVCMOS33"), Misc("DRIVE=16")),
        Subsignal("out_en", Pins("H14"), IOStandard("LVCMOS33")),
    ),
    ("sma", 2,
        Subsignal("in",     Pins("AA21"), IOStandard("LVCMOS33"), Misc("PULLDOWN=TRUE")),
        Subsignal("in_en",  Pins("K14"),  IOStandard("LVCMOS33")),
        Subsignal("out",    Pins("V10"),  IOStandard("LVCMOS33"), Misc("DRIVE=16")),
        Subsignal("out_en", Pins("K13"),  IOStandard("LVCMOS33")),
    ),
    ("sma", 2,
        Subsignal("in",     Pins("AA20"), IOStandard("LVCMOS33"), Misc("PULLDOWN=TRUE")),
        Subsignal("in_en",  Pins("L13"),  IOStandard("LVCMOS33")),
        Subsignal("out",    Pins("W10"),  IOStandard("LVCMOS33"), Misc("DRIVE=16")),
        Subsignal("out_en", Pins("M13"),  IOStandard("LVCMOS33")),
    ),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(Xilinx7SeriesPlatform):
    default_clk_name   = "clk200"
    default_clk_period = 1e9/200e6

    def __init__(self,toolchain="vivado"):
        Xilinx7SeriesPlatform.__init__(self, "xc7a100t-fgg484-2", _io, toolchain=toolchain)

        self.toolchain.bitstream_commands = [
            "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
            "set_property BITSTREAM.CONFIG.CONFIGRATE 16 [current_design]",
            "set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]",
            "set_property CFGBVS VCCO [current_design]",
            "set_property CONFIG_VOLTAGE 3.3 [current_design]",
        ]

        self.toolchain.additional_commands = [
            # Non-Multiboot SPI-Flash bitstream generation.
            "write_cfgmem -force -format bin -interface spix4 -size 16 -loadbit \"up 0x0 {build_name}.bit\" -file {build_name}.bin",

            # Multiboot SPI-Flash Operational bitstream generation.
            "set_property BITSTREAM.CONFIG.TIMER_CFG 0x0001fbd0 [current_design]",
            "set_property BITSTREAM.CONFIG.CONFIGFALLBACK Enable [current_design]",
            "write_bitstream -force {build_name}_operational.bit ",
            "write_cfgmem -force -format bin -interface spix4 -size 16 -loadbit \"up 0x0 {build_name}_operational.bit\" -file {build_name}_operational.bin",

            # Multiboot SPI-Flash Fallback bitstream generation.
            "set_property BITSTREAM.CONFIG.NEXT_CONFIG_ADDR 0x00400000 [current_design]",
            "write_bitstream -force {build_name}_fallback.bit ",
            "write_cfgmem -force -format bin -interface spix4 -size 16 -loadbit \"up 0x0 {build_name}_fallback.bit\" -file {build_name}_fallback.bin"
        ]

    def create_programmer(self, name='openocd'):
        if name == 'openocd':
            return OpenOCD("openocd_xc7_ft232.cfg", "bscan_spi_xc7a200t.bit")
        elif name == 'vivado':
            # TODO: some board versions may have s25fl128s
            return VivadoProgrammer(flash_part='s25fl256sxxxxxx0-spi-x1_x2_x4')

    def do_finalize(self, fragment):
        Xilinx7SeriesPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk200", loose=True), 1e9/200e6)
