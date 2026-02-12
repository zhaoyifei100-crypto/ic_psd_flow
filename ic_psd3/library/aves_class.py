"""
AVESChipConfig - AVES script configuration class
Auto-generated from: gsu1001_2025_nto_scripts.txt
"""

from typing import Optional
from hw_bridge import DeviceManager

from .GSU1K1_NTO_reg_def import *


class AVESChipConfig:
    """
    AVES script configuration for chip initialization.
    
    This class provides methods to configure the chip using I2C commands
    converted from AVES scripts. It supports DeviceManager for centralized
    device management, enabling multi-device configurations (e.g., TX/RX boards).
    
    Usage (DeviceManager mode - recommended):
        >>> from hw_bridge import DeviceManager
        >>> dm = DeviceManager(auto_open=True)
        >>> dm.register("tx", "ftdi", i2c_port=0, chip_addr=0x58)
        >>> dm.register("rx", "ftdi", i2c_port=1, chip_addr=0x58)
        >>> tx_config = AVESChipConfig(device_manager=dm, device_name="tx")
        >>> rx_config = AVESChipConfig(device_manager=dm, device_name="rx")
        >>> tx_config.func_01_01_Chip_Power_Up()
    """

    def __init__(
        self,
        device_manager: Optional[DeviceManager] = None,
        device_name: str = "chip"
    ):
        """
        Initialize the AVES chip configuration.

        Args:
            device_manager: DeviceManager instance for device access.
                           If None, you must set it before calling methods.
            device_name: Name of the device in the DeviceManager.
        """
        self._device_manager = device_manager
        self._device_name = device_name

    def _get_device(self):
        """Get the device instance from DeviceManager."""
        if self._device_manager is None:
            raise RuntimeError("DeviceManager not set. Initialize with device_manager parameter.")
        return self._device_manager[self._device_name]

    def set_device_manager(self, device_manager: DeviceManager, device_name: str = None):
        """
        Set or update the DeviceManager.

        Args:
            device_manager: DeviceManager instance
            device_name: Optional new device name
        """
        self._device_manager = device_manager
        if device_name:
            self._device_name = device_name

    def func_01_01_Chip_Power_Up(self):
        """01-01 Chip Power Up"""
        print("Cfg func_01_01_Chip_Power_Up...")
        device = self._get_device()
        device.write_reg(0x09, 0x02, 0x13)  # I2c set
        device.write_reg(0x05, 0x39, 0x80)  # auclk_count[2:0] MUST be 0
        device.write_reg(0x09, 0x33, 0x6C)  # vbg12=1.193v

    def func_01_01_01_RESET_ALL(self):
        """01-01-01 RESET ALL"""
        print("Cfg func_01_01_01_RESET_ALL...")
        device = self._get_device()
        device.write_reg(0x00, 0xFF, 0xFF)

    def func_01_01_02_PLL_no_ssc_init(self):
        """01-01-02 PLL no ssc init"""
        print("Cfg func_01_01_02_PLL_no_ssc_init...")
        device = self._get_device()
        device.write_reg(0x05, 0xF0, 0x0A)  # mpll disable
        device.write_reg(0x05, 0xF5, 0x06)  # rxa pll disable
        device.write_reg(0x05, 0x30, 0x8F)  # clk ref from xtal
        device.write_reg(0x05, 0x31, 0x26)
        device.write_reg(0x05, 0x32, 0x38)
        device.write_reg(0x05, 0x33, 0xA0)
        device.write_reg(0x05, 0x34, 0x1E)
        device.write_reg(0x05, 0x35, 0xD8)
        device.write_reg(0x05, 0x36, 0x99)
        device.write_reg(0x05, 0x37, 0xFF)
        device.write_reg(0x05, 0x38, 0xFE)
        device.write_reg(0x05, 0x39, 0x00)  # dctest=0
        device.write_reg(0x05, 0x60, 0x8F)  # clk ref from xtal
        device.write_reg(0x05, 0x61, 0x26)
        device.write_reg(0x05, 0x62, 0x38)
        device.write_reg(0x05, 0x63, 0xA0)
        device.write_reg(0x05, 0x64, 0x1E)
        device.write_reg(0x05, 0x65, 0xD8)
        device.write_reg(0x05, 0x66, 0x99)
        device.write_reg(0x05, 0x67, 0xFF)
        device.write_reg(0x05, 0x68, 0xFE)
        device.write_reg(0x05, 0x69, 0x00)  # dctest=0
        device.write_reg(0x05, 0xB0, 0x8F)  # clk ref from xtal
        device.write_reg(0x05, 0xB1, 0x26)
        device.write_reg(0x05, 0xB2, 0x38)
        device.write_reg(0x05, 0xB3, 0xA0)
        device.write_reg(0x05, 0xB4, 0x1E)
        device.write_reg(0x05, 0xB5, 0xD8)
        device.write_reg(0x05, 0xB6, 0x99)
        device.write_reg(0x05, 0xB7, 0xFF)
        device.write_reg(0x05, 0xB8, 0xFE)
        device.write_reg(0x05, 0xB9, 0x00)  # dctest=0
        device.write_reg(0x05, 0xF0, 0x0A)  # U2 PLL disable
        device.write_reg(0x05, 0x34, 0x1E)  # U2 PLL LDO EN
        device.write_reg(0x05, 0x35, 0x58)  # U2 PLL RSV 00
        device.write_reg(0x05, 0xF1, 0x60)  # U2 LOOPDIV 2.4G
        device.write_reg(0x05, 0xF0, 0x0B)  # U2 PLL enable
        device.write_reg(0x05, 0x64, 0x1E)  # U3 PLL RSV
        device.write_reg(0x05, 0x65, 0x58)  # U3 PLL RSV
        device.write_reg(0x05, 0xB4, 0x1E)  # RXCPLL RSV
        device.write_reg(0x05, 0xB5, 0x58)  # RXCPLL RSV
        device.write_reg(0x05, 0xB0, 0x8F)  # rxcref clk to xtal
        device.write_reg(0x04, 0x1F, 0x81)  # loopdiv manen
        device.write_reg(0x04, 0x20, 0x00)  # postdiv=100
        device.write_reg(0x04, 0x21, 0x64)
        device.write_reg(0x04, 0x22, 0x00)
        device.write_reg(0x04, 0x23, 0x41)  # rxcpll off
        device.write_reg(0x09, 0x00, 0x08)  # usb2 480m_domain_rst
        device.write_reg(0x09, 0x00, 0x00)  # usb2 480m_domain_rst
        device.write_reg(0x05, 0xF0, 0x0B)  # mpll enable
        device.write_reg(0x05, 0xF5, 0x07)  # rxa pll enable

    def func_00_00_01_01_02_02_MPLL_with_2000ppm(self):
        """00-00 01-01-02-02 MPLL with +2000ppm"""
        print("Cfg func_00_00_01_01_02_02_MPLL_with_2000ppm...")
        device = self._get_device()
        device.write_reg(0x05, 0xF0, 0x0A)  # U2 PLL disable
        device.write_reg(0x05, 0x34, 0x1E)  # U2 PLL LDO EN
        device.write_reg(0x05, 0x35, 0x58)  # U2 PLL RSV 00
        device.write_reg(0x05, 0xF1, 0x41)  # U2 LOOPDIV 577
        device.write_reg(0x05, 0xF2, 0x02)  # U2 LOOPDIV 577
        device.write_reg(0x05, 0xF0, 0x32)  # U2 PLL refdiv 6
        device.write_reg(0x05, 0xF0, 0x33)  # U2 PLL enable
        device.write_reg(0x09, 0x00, 0x08)  # usb2 480m_domain_rst
        device.write_reg(0x09, 0x00, 0x00)  # usb2 480m_domain_rst

    def func_00_00_01_01_002_Hub_remove_reset(self):
        """00-00 01-01-002 Hub_remove_reset"""
        print("Cfg func_00_00_01_01_002_Hub_remove_reset...")
        device = self._get_device()
        device.write_reg(0x09, 0x64, 0x07)  # hub_2_rstn & hub_ss_rstn

    def func_01_01_03_ADC_test(self):
        """01-01-03 ADC test"""
        print("Cfg func_01_01_03_ADC_test...")
        device = self._get_device()
        device.write_reg(0x09, 0x20, 0x08)  # ADC clkdiv ctrl
        device.write_reg(0x09, 0x21, 0x1F)  # ADC power on
        device.write_reg(0x09, 0x24, 0x0F)  # ADC sample ctrl

    def func_01_01_04_PLL_with_ssc_init(self):
        """01-01-04 PLL with ssc init"""
        print("Cfg func_01_01_04_PLL_with_ssc_init...")
        device = self._get_device()
        self.func_01_01_02_PLL_no_ssc_init()
        device.write_reg(0x05, 0xF8, 0x10)
        device.write_reg(0x05, 0xF5, 0x05)
        device.write_reg(0x05, 0xF6, 0x19)
        device.write_reg(0x05, 0xF7, 0x00)
        device.write_reg(0x06, 0xB6, 0x00)
        device.write_reg(0x06, 0xB7, 0x00)
        device.write_reg(0x06, 0xB8, 0x00)
        device.write_reg(0x06, 0xB9, 0x80)
        device.write_reg(0x06, 0xB1, 0xFA)
        device.write_reg(0x06, 0xB2, 0xDB)
        device.write_reg(0x06, 0xB3, 0x03)
        device.write_reg(0x06, 0xB4, 0x00)
        device.write_reg(0x06, 0xB5, 0x09)
        device.write_reg(0x06, 0xC0, 0x1F)

    def func_01_01_04_PLL_with_ssc_rxc_mode(self):
        """01-01-04 PLL with ssc rxc mode"""
        print("Cfg func_01_01_04_PLL_with_ssc_rxc_mode...")
        device = self._get_device()
        self.func_01_01_02_PLL_no_ssc_init()
        device.write_reg(0x05, 0xB0, 0x88)
        device.write_reg(0x05, 0xF5, 0x05)
        device.write_reg(0x04, 0x1F, 0x81)  # rxc prediv man=1
        device.write_reg(0x04, 0x20, 0x00)  # rxc postdiv25
        device.write_reg(0x04, 0x21, 0x19)  # rxc postdiv25
        device.write_reg(0x06, 0xB6, 0x00)
        device.write_reg(0x06, 0xB7, 0x00)
        device.write_reg(0x06, 0xB8, 0x00)
        device.write_reg(0x06, 0xB9, 0x80)
        device.write_reg(0x06, 0xB1, 0xFA)
        device.write_reg(0x06, 0xB2, 0xDB)
        device.write_reg(0x06, 0xB3, 0x03)
        device.write_reg(0x06, 0xB4, 0x00)
        device.write_reg(0x06, 0xB5, 0x09)
        device.write_reg(0x06, 0xC0, 0x1F)
        device.write_reg(0x04, 0x23, 0x43)  # rxcpll on
        device.write_reg(0x09, 0x02, 0x33)  # dig clk sel to RXc
        device.write_reg(0x09, 0xCC, 0x1F)  # phy tx clksel=rxc

    def func_01_01_04_PLL_with_ssc_init_lpmode(self):
        """01-01-04 PLL with ssc init lpmode"""
        print("Cfg func_01_01_04_PLL_with_ssc_init_lpmode...")
        device = self._get_device()
        self.func_01_01_02_PLL_no_ssc_init()
        device.write_reg(0x09, 0x02, 0x33)  # dig clk sel to RXc
        device.write_reg(0x09, 0xCC, 0x1F)  # phy tx clksel=rxc
        device.write_reg(0x05, 0xF5, 0x07)  # SET RXCrpll dpll out to cpp path
        device.write_reg(0x05, 0xF0, 0x0F)
        device.write_reg(0x05, 0xB5, 0x59)
        device.write_reg(0x06, 0xC0, 0x0D)  # ssc_en=0, mplldpll rst for lowpower
        device.write_reg(0x06, 0xB5, 0x31)  # man_en=1, man=24, pll=2.4GHz
        device.write_reg(0x06, 0xB6, 0x7C)
        device.write_reg(0x06, 0xB7, 0x86)
        device.write_reg(0x06, 0xB8, 0x5D)
        device.write_reg(0x06, 0xB9, 0x09)
        device.write_reg(0x06, 0xB1, 0xFA)
        device.write_reg(0x06, 0xB2, 0x8B)
        device.write_reg(0x06, 0xB3, 0x02)
        device.write_reg(0x06, 0xB4, 0x00)
        device.write_reg(0x06, 0xC0, 0x1D)  # ssc_en=1, mplldpll rst for lowpower
        device.write_reg(0x04, 0x23, 0x43)  # rxcpll on

    def func_01_01_05_ANA_Rx_RAM_EQ(self):
        """01-01-05 ANA Rx RAM EQ"""
        print("Cfg func_01_01_05_ANA_Rx_RAM_EQ...")
        device = self._get_device()
        device.write_reg(0x09, 0x05, 0x05)
        device.write_reg(0x15, 0x00, 0x00)
        device.write_reg(0x15, 0x01, 0x40)
        device.write_reg(0x15, 0x02, 0x00)
        device.write_reg(0x15, 0x03, 0x00)
        device.write_reg(0x15, 0x04, 0x00)
        device.write_reg(0x15, 0x05, 0x01)
        device.write_reg(0x15, 0x06, 0x00)
        device.write_reg(0x15, 0x07, 0x00)
        device.write_reg(0x15, 0x08, 0x00)
        device.write_reg(0x15, 0x09, 0x00)
        device.write_reg(0x15, 0x0A, 0x00)
        device.write_reg(0x15, 0x0B, 0x00)
        device.write_reg(0x15, 0x0C, 0xC0)
        device.write_reg(0x15, 0x0D, 0x00)
        device.write_reg(0x15, 0x0E, 0x00)
        device.write_reg(0x15, 0x0F, 0x00)
        device.write_reg(0x15, 0x10, 0x01)
        device.write_reg(0x15, 0x11, 0x00)
        device.write_reg(0x15, 0x12, 0x00)
        device.write_reg(0x15, 0x13, 0x00)
        device.write_reg(0x15, 0x14, 0x00)
        device.write_reg(0x15, 0x15, 0x00)
        device.write_reg(0x15, 0x16, 0x00)
        device.write_reg(0x15, 0x17, 0xC0)
        device.write_reg(0x15, 0x18, 0x03)
        device.write_reg(0x15, 0x19, 0x00)
        device.write_reg(0x15, 0x1A, 0x00)
        device.write_reg(0x15, 0x1B, 0x01)
        device.write_reg(0x15, 0x1C, 0x00)
        device.write_reg(0x15, 0x1D, 0x00)
        device.write_reg(0x15, 0x1E, 0x00)
        device.write_reg(0x15, 0x1F, 0x00)
        device.write_reg(0x15, 0x20, 0x00)
        device.write_reg(0x15, 0x21, 0x00)
        device.write_reg(0x15, 0x22, 0x00)
        device.write_reg(0x15, 0x23, 0x00)
        device.write_reg(0x15, 0x24, 0x00)
        device.write_reg(0x15, 0x25, 0x00)
        device.write_reg(0x15, 0x26, 0x00)
        device.write_reg(0x15, 0x27, 0x00)
        device.write_reg(0x15, 0x28, 0x00)
        device.write_reg(0x15, 0x29, 0x00)
        device.write_reg(0x15, 0x2A, 0x00)
        device.write_reg(0x15, 0x2B, 0x00)
        device.write_reg(0x15, 0x2C, 0x00)
        device.write_reg(0x15, 0x2D, 0x00)
        device.write_reg(0x15, 0x2E, 0x00)
        device.write_reg(0x15, 0x2F, 0x00)
        device.write_reg(0x15, 0x30, 0x00)
        device.write_reg(0x15, 0x31, 0x00)
        device.write_reg(0x15, 0x32, 0x00)
        device.write_reg(0x15, 0x33, 0x00)
        device.write_reg(0x15, 0x34, 0x00)
        device.write_reg(0x15, 0x35, 0x00)
        device.write_reg(0x15, 0x36, 0x00)
        device.write_reg(0x15, 0x37, 0x00)
        device.write_reg(0x15, 0x38, 0x00)
        device.write_reg(0x15, 0x39, 0x00)
        device.write_reg(0x15, 0x3A, 0x00)
        device.write_reg(0x15, 0x3B, 0x00)
        device.write_reg(0x15, 0x3C, 0x00)
        device.write_reg(0x15, 0x3D, 0x00)
        device.write_reg(0x15, 0x3E, 0x00)
        device.write_reg(0x15, 0x3F, 0x00)
        device.write_reg(0x15, 0x40, 0x00)
        device.write_reg(0x15, 0x41, 0x00)
        device.write_reg(0x15, 0x42, 0x00)
        device.write_reg(0x15, 0x43, 0x00)
        device.write_reg(0x15, 0x44, 0x00)
        device.write_reg(0x15, 0x45, 0x00)
        device.write_reg(0x15, 0x46, 0x00)
        device.write_reg(0x15, 0x47, 0x00)
        device.write_reg(0x15, 0x48, 0x00)
        device.write_reg(0x15, 0x49, 0x00)
        device.write_reg(0x15, 0x4A, 0x00)
        device.write_reg(0x15, 0x4B, 0x00)
        device.write_reg(0x15, 0x4C, 0x00)
        device.write_reg(0x15, 0x4D, 0x00)
        device.write_reg(0x15, 0x4E, 0x00)
        device.write_reg(0x15, 0x4F, 0x00)
        device.write_reg(0x15, 0x50, 0x00)
        device.write_reg(0x15, 0x51, 0x00)
        device.write_reg(0x15, 0x52, 0x00)
        device.write_reg(0x15, 0x53, 0x00)
        device.write_reg(0x15, 0x54, 0x00)
        device.write_reg(0x15, 0x55, 0x00)
        device.write_reg(0x15, 0x56, 0x00)
        device.write_reg(0x15, 0x57, 0x00)
        device.write_reg(0x09, 0x05, 0x00)

    def func_01_01_07_Reset_PRBS(self):
        """01-01-07 Reset PRBS"""
        print("Cfg func_01_01_07_Reset_PRBS...")
        device = self._get_device()
        device.write_reg(0x31, 0x63, 0x20)
        device.write_reg(0x31, 0x64, 0x30)
        device.write_reg(0x31, 0x64, 0xB0)
        device.write_reg(0x31, 0x64, 0x30)
        device.write_reg(0x31, 0x63, 0x30)
        device.write_reg(0x31, 0x63, 0x20)
        device.write_reg(0x31, 0x63, 0x30)
        device.write_reg(0x31, 0x64, 0xB0)
        device.write_reg(0x32, 0x63, 0x20)
        device.write_reg(0x32, 0x64, 0x30)
        device.write_reg(0x32, 0x64, 0xB0)
        device.write_reg(0x32, 0x64, 0x30)
        device.write_reg(0x32, 0x63, 0x30)
        device.write_reg(0x32, 0x63, 0x20)
        device.write_reg(0x32, 0x63, 0x30)
        device.write_reg(0x32, 0x64, 0xB0)
        device.write_reg(0x33, 0x63, 0x20)
        device.write_reg(0x33, 0x64, 0x30)
        device.write_reg(0x33, 0x64, 0xB0)
        device.write_reg(0x33, 0x64, 0x30)
        device.write_reg(0x33, 0x63, 0x30)
        device.write_reg(0x33, 0x63, 0x20)
        device.write_reg(0x33, 0x63, 0x30)
        device.write_reg(0x33, 0x64, 0xB0)
        device.write_reg(0x34, 0x63, 0x20)
        device.write_reg(0x34, 0x64, 0x30)
        device.write_reg(0x34, 0x64, 0xB0)
        device.write_reg(0x34, 0x64, 0x30)
        device.write_reg(0x34, 0x63, 0x30)
        device.write_reg(0x34, 0x63, 0x20)
        device.write_reg(0x34, 0x63, 0x30)
        device.write_reg(0x34, 0x64, 0xB0)
        device.write_reg(0x35, 0x63, 0x20)
        device.write_reg(0x35, 0x64, 0x30)
        device.write_reg(0x35, 0x64, 0xB0)
        device.write_reg(0x35, 0x64, 0x30)
        device.write_reg(0x35, 0x63, 0x30)
        device.write_reg(0x35, 0x63, 0x20)
        device.write_reg(0x35, 0x63, 0x30)
        device.write_reg(0x35, 0x64, 0xB0)

    def func_01_01_08_USB2_FSLS(self):
        """01-01-08 USB2_FSLS"""
        print("Cfg func_01_01_08_USB2_FSLS...")
        device = self._get_device()
        device.write_reg(0x0D, 0x0B, 0xFF)  # rftime max
        device.write_reg(0x0D, 0x0C, 0xFF)  # rftime max
        device.write_reg(0x0D, 0x0D, 0xFF)  # rftime max
        device.write_reg(0x0D, 0x0E, 0xFF)  # rftime max
        device.write_reg(0x0D, 0x0A, 0xF3)  # id max
        device.write_reg(0x0D, 0x0F, 0x9F)  # bias max
        device.write_reg(0x0E, 0x0B, 0xFF)  # rftime max
        device.write_reg(0x0E, 0x0C, 0xFF)  # rftime max
        device.write_reg(0x0E, 0x0D, 0xFF)  # rftime max
        device.write_reg(0x0E, 0x0E, 0xFF)  # rftime max
        device.write_reg(0x0E, 0x0A, 0xF3)  # id max
        device.write_reg(0x0E, 0x0F, 0x9F)  # bias max
        device.write_reg(0x0C, 0x0B, 0xFF)  # rftime max
        device.write_reg(0x0C, 0x0C, 0xFF)  # rftime max
        device.write_reg(0x0C, 0x0D, 0xFF)  # rftime max
        device.write_reg(0x0C, 0x0E, 0xFF)  # rftime max
        device.write_reg(0x0C, 0x0A, 0xF3)  # id max
        device.write_reg(0x0C, 0x0F, 0x9F)  # bias max
        device.write_reg(0x0B, 0x0B, 0xFF)  # rftime max
        device.write_reg(0x0B, 0x0C, 0xFF)  # rftime max
        device.write_reg(0x0B, 0x0D, 0xFF)  # rftime max
        device.write_reg(0x0B, 0x0E, 0xFF)  # rftime max
        device.write_reg(0x0B, 0x0A, 0xF3)  # id max
        device.write_reg(0x0B, 0x0F, 0x9F)  # bias max
        device.write_reg(0x0A, 0x0B, 0xFF)  # rftime max
        device.write_reg(0x0A, 0x0C, 0xFF)  # rftime max
        device.write_reg(0x0A, 0x0D, 0xFF)  # rftime max
        device.write_reg(0x0A, 0x0E, 0xFF)  # rftime max
        device.write_reg(0x0A, 0x0A, 0xF3)  # id max
        device.write_reg(0x0A, 0x0F, 0x9F)  # bias max

    def func_01_01_09_SSC_set_10000ppm(self):
        """01-01-09 SSC set 10000ppm"""
        print("Cfg func_01_01_09_SSC_set_10000ppm...")
        device = self._get_device()
        device.write_reg(0x06, 0xB1, 0x00)
        device.write_reg(0x06, 0xB2, 0x07)
        device.write_reg(0x06, 0xB3, 0xB7)
        device.write_reg(0x06, 0xB4, 0xF4)

    def func_01_01_12_USB3_Upcdr_adaptive_param(self):
        """01-01-12 USB3 Upcdr adaptive param"""
        print("Cfg func_01_01_12_USB3_Upcdr_adaptive_param...")
        device = self._get_device()
        self.func_01_07_01_USB3_UP_Rx_ANA()
        device.write_reg(0x10, 0x4B, 0x00)  # khp_t man_en=0
        device.write_reg(0x10, 0x69, 0x1F)  # khp_t seg_en=1
        device.write_reg(0x10, 0x6A, 0xEC)  # prevga_gian man_en=0, when man=0, use seg
        device.write_reg(0x10, 0x09, 0x0E)  # dfe mode=0,decheck en=1,only meas init eq cfg=1,seg en=1,init_sel=0
        device.write_reg(0x10, 0x5B, 0x11)  # meh use i2c
        device.write_reg(0x10, 0x60, 0x00)  # meh cycle set 5,000
        device.write_reg(0x10, 0x61, 0x13)
        device.write_reg(0x10, 0x62, 0x88)
        device.write_reg(0x10, 0xA0, 0x00)  # loop off
        device.write_reg(0x10, 0xA1, 0x00)  # loop off
        device.write_reg(0x10, 0xA2, 0x00)  # loop off
        device.write_reg(0x10, 0xA3, 0x00)  # loop off
        device.write_reg(0x10, 0xA4, 0x00)  # loop off
        device.write_reg(0x10, 0xA5, 0x00)  # loop off
        device.write_reg(0x10, 0xA6, 0x00)  # loop off

    def func_01_01_13_Set_pipe_dp1_send_clkdiv10(self):
        """01-01-13 Set pipe_dp1 send clkdiv10"""
        print("Cfg func_01_01_13_Set_pipe_dp1_send_clkdiv10...")
        device = self._get_device()
        self.func_03_02_PIPE_dp1_Tx_Rx_PRBS()
        device.write_reg(0x32, 0x1C, 0x20)
        device.write_reg(0x32, 0x21, 0x9F)
        device.write_reg(0x32, 0x22, 0xFF)
        device.write_reg(0x32, 0x26, 0x80)
        device.write_reg(0x32, 0x27, 0x00)

    def func_01_01_14_ANA_Tx_SET_USB3(self):
        """01-01-14 ANA Tx SET, USB3"""
        print("Cfg func_01_01_14_ANA_Tx_SET_USB3...")
        device = self._get_device()
        device.write_reg(0x31, 0xEA, 0xC0)
        device.write_reg(0x31, 0x3A, 0x52)
        device.write_reg(0x31, 0x3A, 0x52)
        device.write_reg(0x31, 0x3B, 0x94)
        device.write_reg(0x31, 0x3B, 0x94)
        device.write_reg(0x31, 0x3B, 0x94)
        device.write_reg(0x31, 0x3C, 0xA5)
        device.write_reg(0x31, 0x3C, 0xA5)
        device.write_reg(0x31, 0x3D, 0x29)
        device.write_reg(0x31, 0x3D, 0x29)
        device.write_reg(0x31, 0x3D, 0x29)
        device.write_reg(0x31, 0x3E, 0x4A)
        device.write_reg(0x31, 0x3E, 0x4A)
        device.write_reg(0x31, 0x3F, 0x52)
        device.write_reg(0x31, 0x3F, 0x52)
        device.write_reg(0x31, 0x40, 0x94)
        device.write_reg(0x31, 0x40, 0x94)
        device.write_reg(0x31, 0x40, 0x94)
        device.write_reg(0x31, 0x41, 0xA0)
        device.write_reg(0x31, 0xF0, 0x00)
        device.write_reg(0x31, 0xEA, 0xC0)
        device.write_reg(0x31, 0xF6, 0x0E)
        device.write_reg(0x31, 0xF7, 0x00)
        device.write_reg(0x31, 0x0E, 0x40)
        device.write_reg(0x31, 0xED, 0x1F)
        device.write_reg(0x31, 0xEE, 0xF7)
        device.write_reg(0x32, 0xEA, 0xC0)
        device.write_reg(0x32, 0x3A, 0x52)
        device.write_reg(0x32, 0x3A, 0x52)
        device.write_reg(0x32, 0x3B, 0x94)
        device.write_reg(0x32, 0x3B, 0x94)
        device.write_reg(0x32, 0x3B, 0x94)
        device.write_reg(0x32, 0x3C, 0xA5)
        device.write_reg(0x32, 0x3C, 0xA5)
        device.write_reg(0x32, 0x3D, 0x29)
        device.write_reg(0x32, 0x3D, 0x29)
        device.write_reg(0x32, 0x3D, 0x29)
        device.write_reg(0x32, 0x3E, 0x4A)
        device.write_reg(0x32, 0x3E, 0x4A)
        device.write_reg(0x32, 0x3F, 0x52)
        device.write_reg(0x32, 0x3F, 0x52)
        device.write_reg(0x32, 0x40, 0x94)
        device.write_reg(0x32, 0x40, 0x94)
        device.write_reg(0x32, 0x40, 0x94)
        device.write_reg(0x32, 0x41, 0xA0)
        device.write_reg(0x32, 0xF0, 0x00)
        device.write_reg(0x32, 0xEA, 0xC0)
        device.write_reg(0x32, 0xF6, 0x0E)
        device.write_reg(0x32, 0xF7, 0x00)
        device.write_reg(0x32, 0x0E, 0x40)
        device.write_reg(0x32, 0xED, 0x1F)
        device.write_reg(0x32, 0xEE, 0xF7)
        device.write_reg(0x33, 0xEA, 0xC0)
        device.write_reg(0x33, 0x3A, 0x52)
        device.write_reg(0x33, 0x3A, 0x52)
        device.write_reg(0x33, 0x3B, 0x94)
        device.write_reg(0x33, 0x3B, 0x94)
        device.write_reg(0x33, 0x3B, 0x94)
        device.write_reg(0x33, 0x3C, 0xA5)
        device.write_reg(0x33, 0x3C, 0xA5)
        device.write_reg(0x33, 0x3D, 0x29)
        device.write_reg(0x33, 0x3D, 0x29)
        device.write_reg(0x33, 0x3D, 0x29)
        device.write_reg(0x33, 0x3E, 0x4A)
        device.write_reg(0x33, 0x3E, 0x4A)
        device.write_reg(0x33, 0x3F, 0x52)
        device.write_reg(0x33, 0x3F, 0x52)
        device.write_reg(0x33, 0x40, 0x94)
        device.write_reg(0x33, 0x40, 0x94)
        device.write_reg(0x33, 0x40, 0x94)
        device.write_reg(0x33, 0x41, 0xA0)
        device.write_reg(0x33, 0xF0, 0x00)
        device.write_reg(0x33, 0xEA, 0xC0)
        device.write_reg(0x33, 0xF6, 0x0E)
        device.write_reg(0x33, 0xF7, 0x00)
        device.write_reg(0x33, 0x0E, 0x40)
        device.write_reg(0x33, 0xED, 0x1F)
        device.write_reg(0x33, 0xEE, 0xF7)
        device.write_reg(0x34, 0xEA, 0xC0)
        device.write_reg(0x34, 0x3A, 0x52)
        device.write_reg(0x34, 0x3A, 0x52)
        device.write_reg(0x34, 0x3B, 0x94)
        device.write_reg(0x34, 0x3B, 0x94)
        device.write_reg(0x34, 0x3B, 0x94)
        device.write_reg(0x34, 0x3C, 0xA5)
        device.write_reg(0x34, 0x3C, 0xA5)
        device.write_reg(0x34, 0x3D, 0x29)
        device.write_reg(0x34, 0x3D, 0x29)
        device.write_reg(0x34, 0x3D, 0x29)
        device.write_reg(0x34, 0x3E, 0x4A)
        device.write_reg(0x34, 0x3E, 0x4A)
        device.write_reg(0x34, 0x3F, 0x52)
        device.write_reg(0x34, 0x3F, 0x52)
        device.write_reg(0x34, 0x40, 0x94)
        device.write_reg(0x34, 0x40, 0x94)
        device.write_reg(0x34, 0x40, 0x94)
        device.write_reg(0x34, 0x41, 0xA0)
        device.write_reg(0x34, 0xF0, 0x00)
        device.write_reg(0x34, 0xEA, 0xC0)
        device.write_reg(0x34, 0xF6, 0x0E)
        device.write_reg(0x34, 0xF7, 0x00)
        device.write_reg(0x34, 0x0E, 0x40)
        device.write_reg(0x34, 0xED, 0x1F)
        device.write_reg(0x34, 0xEE, 0xF7)
        device.write_reg(0x35, 0xEA, 0xC0)
        device.write_reg(0x35, 0x3A, 0x52)
        device.write_reg(0x35, 0x3A, 0x52)
        device.write_reg(0x35, 0x3B, 0x94)
        device.write_reg(0x35, 0x3B, 0x94)
        device.write_reg(0x35, 0x3B, 0x94)
        device.write_reg(0x35, 0x3C, 0xA5)
        device.write_reg(0x35, 0x3C, 0xA5)
        device.write_reg(0x35, 0x3D, 0x29)
        device.write_reg(0x35, 0x3D, 0x29)
        device.write_reg(0x35, 0x3D, 0x29)
        device.write_reg(0x35, 0x3E, 0x4A)
        device.write_reg(0x35, 0x3E, 0x4A)
        device.write_reg(0x35, 0x3F, 0x52)
        device.write_reg(0x35, 0x3F, 0x52)
        device.write_reg(0x35, 0x40, 0x94)
        device.write_reg(0x35, 0x40, 0x94)
        device.write_reg(0x35, 0x40, 0x94)
        device.write_reg(0x35, 0x41, 0xA0)
        device.write_reg(0x35, 0xF0, 0x00)
        device.write_reg(0x35, 0xEA, 0xC0)
        device.write_reg(0x35, 0xF6, 0x0E)
        device.write_reg(0x35, 0xF7, 0x00)
        device.write_reg(0x35, 0x0E, 0x40)
        device.write_reg(0x35, 0xED, 0x1F)
        device.write_reg(0x35, 0xEE, 0xF7)

    def func_01_05_04_USB2v2_UP_ANA(self):
        """01-05-04 USB2v2 UP ANA"""
        print("Cfg func_01_05_04_USB2v2_UP_ANA...")
        device = self._get_device()
        device.write_reg(0x42, 0x16, 0x20)  # disc mode sel
        device.write_reg(0x42, 0x19, 0x39)  # utmi_en=1
        device.write_reg(0x42, 0x1A, 0x0C)  # utmi_en=1
        device.write_reg(0x42, 0x1B, 0x00)  # man=0
        device.write_reg(0x42, 0x1C, 0x00)  # sql_sel=0
        device.write_reg(0x42, 0x25, 0x08)  # clrcnt=08
        device.write_reg(0x42, 0x26, 0x08)  # oneshot_acc=08
        device.write_reg(0x42, 0x27, 0x04)  # date_buf=0
        device.write_reg(0x42, 0x28, 0x00)  # qc3.0 clk_div=0
        device.write_reg(0x42, 0x29, 0x09)  # dsel_mode=1 mvth=4
        device.write_reg(0x42, 0x2A, 0x04)  # clr_mode=0 date_buf_sel=0
        device.write_reg(0x42, 0x2B, 0x50)  # valid_drop_sel=2 calib_swing_int=16
        device.write_reg(0x42, 0x2C, 0x02)  # swing_man=0 acc_valid=2
        device.write_reg(0x42, 0x2D, 0x08)  # loopf_bw=08
        device.write_reg(0x42, 0x08, 0xF4)  # Tx Swing bias ctrl, sql_ref=120m
        device.write_reg(0x42, 0x10, 0x63)  # Tx Swing
        device.write_reg(0x42, 0x04, 0xCF)  # disc ref 650mV, se_sql_ref>100m
        device.write_reg(0x42, 0x07, 0x9A)  # rx half gain
        device.write_reg(0x42, 0x05, 0x0C)  # 0pole

    def func_01_05_05_USB2v2_DP1_ANA(self):
        """01-05-05 USB2v2 DP1 ANA"""
        print("Cfg func_01_05_05_USB2v2_DP1_ANA...")
        device = self._get_device()
        device.write_reg(0x43, 0x16, 0x20)  # disc mode sel
        device.write_reg(0x43, 0x19, 0x39)  # utmi_en=1
        device.write_reg(0x43, 0x1A, 0x0C)  # utmi_en=1
        device.write_reg(0x43, 0x1B, 0x00)  # man=0
        device.write_reg(0x43, 0x1C, 0x00)  # sql_sel=0
        device.write_reg(0x43, 0x25, 0x08)  # clrcnt=08
        device.write_reg(0x43, 0x26, 0x08)  # oneshot_acc=08
        device.write_reg(0x43, 0x27, 0x04)  # date_buf=0
        device.write_reg(0x43, 0x28, 0x00)  # qc3.0 clk_div=0
        device.write_reg(0x43, 0x29, 0x09)  # dsel_mode=1 mvth=4
        device.write_reg(0x43, 0x2A, 0x04)  # clr_mode=0 date_buf_sel=0
        device.write_reg(0x43, 0x2B, 0x50)  # valid_drop_sel=2 calib_swing_int=16
        device.write_reg(0x43, 0x2C, 0x02)  # swing_man=0 acc_valid=2
        device.write_reg(0x43, 0x2D, 0x08)  # loopf_bw=08
        device.write_reg(0x43, 0x08, 0xF4)  # Tx Swing bias ctrl, sql_ref=120m
        device.write_reg(0x43, 0x10, 0x63)  # Tx Swing
        device.write_reg(0x43, 0x04, 0xCF)  # disc ref 650mV, se_sql_ref>100m
        device.write_reg(0x43, 0x07, 0x9A)  # rx half gain
        device.write_reg(0x43, 0x05, 0x0C)  # 0pole

    def func_01_05_06_USB2v2_DP2_ANA(self):
        """01-05-06 USB2v2 DP2 ANA"""
        print("Cfg func_01_05_06_USB2v2_DP2_ANA...")
        device = self._get_device()
        device.write_reg(0x44, 0x16, 0x20)  # disc mode sel
        device.write_reg(0x44, 0x19, 0x39)  # utmi_en=1
        device.write_reg(0x44, 0x1A, 0x0C)  # utmi_en=1
        device.write_reg(0x44, 0x1B, 0x00)  # man=0
        device.write_reg(0x44, 0x1C, 0x00)  # sql_sel=0
        device.write_reg(0x44, 0x25, 0x08)  # clrcnt=08
        device.write_reg(0x44, 0x26, 0x08)  # oneshot_acc=08
        device.write_reg(0x44, 0x27, 0x04)  # date_buf=0
        device.write_reg(0x44, 0x28, 0x00)  # qc3.0 clk_div=0
        device.write_reg(0x44, 0x29, 0x09)  # dsel_mode=1 mvth=4
        device.write_reg(0x44, 0x2A, 0x04)  # clr_mode=0 date_buf_sel=0
        device.write_reg(0x44, 0x2B, 0x50)  # valid_drop_sel=2 calib_swing_int=16
        device.write_reg(0x44, 0x2C, 0x02)  # swing_man=0 acc_valid=2
        device.write_reg(0x44, 0x2D, 0x08)  # loopf_bw=08
        device.write_reg(0x44, 0x08, 0xF4)  # Tx Swing bias ctrl, sql_ref=120m
        device.write_reg(0x44, 0x10, 0x63)  # Tx Swing
        device.write_reg(0x44, 0x04, 0xCF)  # disc ref 650mV, se_sql_ref>100m
        device.write_reg(0x44, 0x07, 0x9A)  # rx half gain
        device.write_reg(0x44, 0x05, 0x0C)  # 0pole

    def func_01_05_07_USB2v2_DP3_ANA(self):
        """01-05-07 USB2v2 DP3 ANA"""
        print("Cfg func_01_05_07_USB2v2_DP3_ANA...")
        device = self._get_device()
        device.write_reg(0x45, 0x16, 0x20)  # disc mode sel
        device.write_reg(0x45, 0x19, 0x39)  # utmi_en=1
        device.write_reg(0x45, 0x1A, 0x0C)  # utmi_en=1
        device.write_reg(0x45, 0x1B, 0x00)  # man=0
        device.write_reg(0x45, 0x1C, 0x00)  # sql_sel=0
        device.write_reg(0x45, 0x25, 0x08)  # clrcnt=08
        device.write_reg(0x45, 0x26, 0x08)  # oneshot_acc=08
        device.write_reg(0x45, 0x27, 0x04)  # date_buf=0
        device.write_reg(0x45, 0x28, 0x00)  # qc3.0 clk_div=0
        device.write_reg(0x45, 0x29, 0x09)  # dsel_mode=1 mvth=4
        device.write_reg(0x45, 0x2A, 0x04)  # clr_mode=0 date_buf_sel=0
        device.write_reg(0x45, 0x2B, 0x50)  # valid_drop_sel=2 calib_swing_int=16
        device.write_reg(0x45, 0x2C, 0x02)  # swing_man=0 acc_valid=2
        device.write_reg(0x45, 0x2D, 0x08)  # loopf_bw=08
        device.write_reg(0x45, 0x08, 0xF4)  # Tx Swing bias ctrl, sql_ref=120m
        device.write_reg(0x45, 0x10, 0x63)  # Tx Swing
        device.write_reg(0x45, 0x04, 0xCF)  # disc ref 650mV, se_sql_ref>100m
        device.write_reg(0x45, 0x07, 0x9A)  # rx half gain
        device.write_reg(0x45, 0x05, 0x0C)  # 0pole

    def func_01_05_08_USB2v2_DP4_ANA(self):
        """01-05-08 USB2v2 DP4 ANA"""
        print("Cfg func_01_05_08_USB2v2_DP4_ANA...")
        device = self._get_device()
        device.write_reg(0x46, 0x16, 0x20)  # disc mode sel
        device.write_reg(0x46, 0x19, 0x39)  # utmi_en=1
        device.write_reg(0x46, 0x1A, 0x0C)  # utmi_en=1
        device.write_reg(0x46, 0x1B, 0x00)  # man=0
        device.write_reg(0x46, 0x1C, 0x00)  # sql_sel=0
        device.write_reg(0x46, 0x25, 0x08)  # clrcnt=08
        device.write_reg(0x46, 0x26, 0x08)  # oneshot_acc=08
        device.write_reg(0x46, 0x27, 0x04)  # date_buf=0
        device.write_reg(0x46, 0x28, 0x00)  # qc3.0 clk_div=0
        device.write_reg(0x46, 0x29, 0x09)  # dsel_mode=1 mvth=4
        device.write_reg(0x46, 0x2A, 0x04)  # clr_mode=0 date_buf_sel=0
        device.write_reg(0x46, 0x2B, 0x50)  # valid_drop_sel=2 calib_swing_int=16
        device.write_reg(0x46, 0x2C, 0x02)  # swing_man=0 acc_valid=2
        device.write_reg(0x46, 0x2D, 0x08)  # loopf_bw=08
        device.write_reg(0x46, 0x08, 0xF4)  # Tx Swing bias ctrl, sql_ref=120m
        device.write_reg(0x46, 0x10, 0x63)  # Tx Swing
        device.write_reg(0x46, 0x04, 0xCF)  # disc ref 650mV, se_sql_ref>100m
        device.write_reg(0x46, 0x07, 0x9A)  # rx half gain
        device.write_reg(0x46, 0x05, 0x0C)  # 0pole

    def func_01_05_09_USB2v2_MODE2(self):
        """01-05-09 USB2v2 MODE2"""
        print("Cfg func_01_05_09_USB2v2_MODE2...")
        device = self._get_device()
        device.write_reg(0x42, 0x29, 0x0A)  # dsel_mode=2
        device.write_reg(0x42, 0x2A, 0x0C)  # date_buf_sel=12
        device.write_reg(0x47, 0x6A, 0x01)  # utm_eop_cnt=1
        device.write_reg(0x43, 0x29, 0x0A)  # dsel_mode=2
        device.write_reg(0x43, 0x2A, 0x0C)  # date_buf_sel=12
        device.write_reg(0x48, 0x6A, 0x01)  # utm_eop_cnt=1
        device.write_reg(0x44, 0x29, 0x0A)  # dsel_mode=2
        device.write_reg(0x44, 0x2A, 0x0C)  # date_buf_sel=12
        device.write_reg(0x49, 0x6A, 0x01)  # utm_eop_cnt=1
        device.write_reg(0x45, 0x29, 0x0A)  # dsel_mode=2
        device.write_reg(0x45, 0x2A, 0x0C)  # date_buf_sel=12
        device.write_reg(0x4A, 0x6A, 0x01)  # utm_eop_cnt=1
        device.write_reg(0x46, 0x29, 0x0A)  # dsel_mode=2
        device.write_reg(0x46, 0x2A, 0x0C)  # date_buf_sel=12
        device.write_reg(0x4B, 0x6A, 0x01)  # utm_eop_cnt=1

    def func_01_05_10_USB2_Phy_ALL(self):
        """01-05-10 USB2 Phy ALL"""
        print("Cfg func_01_05_10_USB2_Phy_ALL...")
        device = self._get_device()
        self.func_01_05_04_USB2v2_UP_ANA()
        self.func_01_05_05_USB2v2_DP1_ANA()
        self.func_01_05_06_USB2v2_DP2_ANA()
        self.func_01_05_07_USB2v2_DP3_ANA()
        self.func_01_05_08_USB2v2_DP4_ANA()
        self.func_01_05_09_USB2v2_MODE2()

    def func_01_06_01_PIPE_ANA_UP(self):
        """01-06-01 PIPE ANA UP"""
        print("Cfg func_01_06_01_PIPE_ANA_UP...")
        device = self._get_device()
        device.write_reg(0x31, 0x21, 0x82)  # RXDET wait time
        device.write_reg(0x31, 0x22, 0x00)  # RXDET wait time
        device.write_reg(0x31, 0x23, 0x00)
        device.write_reg(0x31, 0x24, 0xFF)
        device.write_reg(0x31, 0x25, 0x3E)
        device.write_reg(0x31, 0x26, 0x41)  # rxdet clk is 10us/clk
        device.write_reg(0x31, 0x27, 0x90)  # lower rctime, ugreen ssd
        device.write_reg(0x31, 0xF9, 0x00)  # LFPS BW max
        device.write_reg(0x31, 0xEE, 0x07)  # LFPS fasel=3
        device.write_reg(0x31, 0xEF, 0x0C)  # LFPS ref_ctrl=3
        device.write_reg(0x31, 0xEB, 0x00)  # LFPS div4, 2.5G/4, short LFPS change to DIV8
        device.write_reg(0x31, 0xEA, 0x86)  # curadj=1, cm_ctrl=0b10, swing_man=1
        device.write_reg(0x31, 0xE9, 0x01)  # sterm_override=1
        device.write_reg(0x31, 0xF0, 0x14)  # sterm=101
        device.write_reg(0x31, 0x3A, 0xF0)
        device.write_reg(0x31, 0x3A, 0xF7)
        device.write_reg(0x31, 0x3B, 0x80)
        device.write_reg(0x31, 0x3B, 0xBC)
        device.write_reg(0x31, 0x3B, 0xBD)
        device.write_reg(0x31, 0x3C, 0xE0)
        device.write_reg(0x31, 0x3C, 0xEF)
        device.write_reg(0x31, 0x3D, 0x00)
        device.write_reg(0x31, 0x3D, 0x78)
        device.write_reg(0x31, 0x3D, 0x7B)
        device.write_reg(0x31, 0x3E, 0xC0)
        device.write_reg(0x31, 0x3E, 0xDE)
        device.write_reg(0x31, 0x3F, 0xF0)
        device.write_reg(0x31, 0x3F, 0xF7)
        device.write_reg(0x31, 0x40, 0x80)
        device.write_reg(0x31, 0x40, 0xBC)
        device.write_reg(0x31, 0x40, 0xBD)

    def func_01_06_02_PIPE_ANA_DP1(self):
        """01-06-02 PIPE ANA DP1"""
        print("Cfg func_01_06_02_PIPE_ANA_DP1...")
        device = self._get_device()
        device.write_reg(0x32, 0x21, 0x82)  # RXDET wait time
        device.write_reg(0x32, 0x22, 0x00)  # RXDET wait time
        device.write_reg(0x32, 0x23, 0x00)
        device.write_reg(0x32, 0x24, 0xFF)
        device.write_reg(0x32, 0x25, 0x3E)
        device.write_reg(0x32, 0x26, 0x41)  # rxdet clk is 10us/clk
        device.write_reg(0x32, 0x27, 0x90)  # lower rctime, ugreen ssd
        device.write_reg(0x32, 0xF9, 0x00)  # LFPS BW max
        device.write_reg(0x32, 0xEE, 0x07)  # LFPS fasel=3
        device.write_reg(0x32, 0xEF, 0x0C)  # LFPS ref_ctrl=3
        device.write_reg(0x32, 0xEB, 0x00)  # LFPS div4, 2.5G/4, short LFPS change to DIV8
        device.write_reg(0x32, 0xEA, 0x86)  # curadj=1, cm_ctrl=0b10, swing_man=1
        device.write_reg(0x32, 0xE9, 0x01)  # sterm_override=1
        device.write_reg(0x32, 0xF0, 0x14)  # sterm=101
        device.write_reg(0x32, 0x3A, 0xF0)
        device.write_reg(0x32, 0x3A, 0xF7)
        device.write_reg(0x32, 0x3B, 0x80)
        device.write_reg(0x32, 0x3B, 0xBC)
        device.write_reg(0x32, 0x3B, 0xBD)
        device.write_reg(0x32, 0x3C, 0xE0)
        device.write_reg(0x32, 0x3C, 0xEF)
        device.write_reg(0x32, 0x3D, 0x00)
        device.write_reg(0x32, 0x3D, 0x78)
        device.write_reg(0x32, 0x3D, 0x7B)
        device.write_reg(0x32, 0x3E, 0xC0)
        device.write_reg(0x32, 0x3E, 0xDE)
        device.write_reg(0x32, 0x3F, 0xF0)
        device.write_reg(0x32, 0x3F, 0xF7)
        device.write_reg(0x32, 0x40, 0x80)
        device.write_reg(0x32, 0x40, 0xBC)
        device.write_reg(0x32, 0x40, 0xBD)

    def func_01_06_03_PIPE_ANA_DP2(self):
        """01-06-03 PIPE ANA DP2"""
        print("Cfg func_01_06_03_PIPE_ANA_DP2...")
        device = self._get_device()
        device.write_reg(0x33, 0x21, 0x82)  # RXDET wait time
        device.write_reg(0x33, 0x22, 0x00)  # RXDET wait time
        device.write_reg(0x33, 0x23, 0x00)
        device.write_reg(0x33, 0x24, 0xFF)
        device.write_reg(0x33, 0x25, 0x3E)
        device.write_reg(0x33, 0x26, 0x41)  # rxdet clk is 10us/clk
        device.write_reg(0x33, 0x27, 0x90)  # lower rctime, ugreen ssd
        device.write_reg(0x33, 0xF9, 0x00)  # LFPS BWmax
        device.write_reg(0x33, 0xEE, 0x07)  # LFPS fasel=3
        device.write_reg(0x33, 0xEF, 0x0C)  # LFPS ref_ctrl=3
        device.write_reg(0x33, 0xEB, 0x00)  # LFPS div4, 2.5G/4, short LFPS change to DIV8
        device.write_reg(0x33, 0xEA, 0x86)  # curadj=1, cm_ctrl=0b10, swing_man=1
        device.write_reg(0x33, 0xE9, 0x01)  # sterm_override=1
        device.write_reg(0x33, 0xF0, 0x14)  # sterm=101
        device.write_reg(0x33, 0x3A, 0xF0)
        device.write_reg(0x33, 0x3A, 0xF7)
        device.write_reg(0x33, 0x3B, 0x80)
        device.write_reg(0x33, 0x3B, 0xBC)
        device.write_reg(0x33, 0x3B, 0xBD)
        device.write_reg(0x33, 0x3C, 0xE0)
        device.write_reg(0x33, 0x3C, 0xEF)
        device.write_reg(0x33, 0x3D, 0x00)
        device.write_reg(0x33, 0x3D, 0x78)
        device.write_reg(0x33, 0x3D, 0x7B)
        device.write_reg(0x33, 0x3E, 0xC0)
        device.write_reg(0x33, 0x3E, 0xDE)
        device.write_reg(0x33, 0x3F, 0xF0)
        device.write_reg(0x33, 0x3F, 0xF7)
        device.write_reg(0x33, 0x40, 0x80)
        device.write_reg(0x33, 0x40, 0xBC)
        device.write_reg(0x33, 0x40, 0xBD)

    def func_01_06_04_PIPE_ANA_DP3(self):
        """01-06-04 PIPE ANA DP3"""
        print("Cfg func_01_06_04_PIPE_ANA_DP3...")
        device = self._get_device()
        device.write_reg(0x34, 0x21, 0x82)  # RXDET wait time
        device.write_reg(0x34, 0x22, 0x00)  # RXDET wait time
        device.write_reg(0x34, 0x23, 0x00)
        device.write_reg(0x34, 0x24, 0xFF)
        device.write_reg(0x34, 0x25, 0x3E)
        device.write_reg(0x34, 0x26, 0x41)  # rxdet clk is 10us/clk
        device.write_reg(0x34, 0x27, 0x90)  # lower rctime, ugreen ssd
        device.write_reg(0x34, 0xF9, 0x00)  # LFPS BWmax
        device.write_reg(0x34, 0xEE, 0x07)  # LFPS fasel=3
        device.write_reg(0x34, 0xEF, 0x0C)  # LFPS ref_ctrl=3
        device.write_reg(0x34, 0xEB, 0x00)  # LFPS div4, 2.5G/4, short LFPS change to DIV8
        device.write_reg(0x34, 0xEA, 0x86)  # curadj=1, cm_ctrl=0b10, swing_man=1
        device.write_reg(0x34, 0xE9, 0x01)  # sterm_override=1
        device.write_reg(0x34, 0xF0, 0x14)  # sterm=101
        device.write_reg(0x34, 0x3A, 0xF0)
        device.write_reg(0x34, 0x3A, 0xF7)
        device.write_reg(0x34, 0x3B, 0x80)
        device.write_reg(0x34, 0x3B, 0xBC)
        device.write_reg(0x34, 0x3B, 0xBD)
        device.write_reg(0x34, 0x3C, 0xE0)
        device.write_reg(0x34, 0x3C, 0xEF)
        device.write_reg(0x34, 0x3D, 0x00)
        device.write_reg(0x34, 0x3D, 0x78)
        device.write_reg(0x34, 0x3D, 0x7B)
        device.write_reg(0x34, 0x3E, 0xC0)
        device.write_reg(0x34, 0x3E, 0xDE)
        device.write_reg(0x34, 0x3F, 0xF0)
        device.write_reg(0x34, 0x3F, 0xF7)
        device.write_reg(0x34, 0x40, 0x80)
        device.write_reg(0x34, 0x40, 0xBC)
        device.write_reg(0x34, 0x40, 0xBD)

    def func_01_06_05_PIPE_ANA_DP4(self):
        """01-06-05 PIPE ANA DP4"""
        print("Cfg func_01_06_05_PIPE_ANA_DP4...")
        device = self._get_device()
        device.write_reg(0x35, 0x21, 0x82)  # RXDET wait time
        device.write_reg(0x35, 0x22, 0x00)  # RXDET wait time
        device.write_reg(0x35, 0x23, 0x00)
        device.write_reg(0x35, 0x24, 0xFF)
        device.write_reg(0x35, 0x25, 0x3E)
        device.write_reg(0x35, 0x26, 0x41)  # rxdet clk is 10us/clk
        device.write_reg(0x35, 0x27, 0x90)  # lower rctime, ugreen ssd
        device.write_reg(0x35, 0xF9, 0x00)  # LFPS Bw max
        device.write_reg(0x35, 0xEE, 0x07)  # LFPS fasel=3
        device.write_reg(0x35, 0xEF, 0x0C)  # LFPS ref_ctrl=3
        device.write_reg(0x35, 0xEB, 0x00)  # LFPS div4, 2.5G/4, short LFPS change to DIV8
        device.write_reg(0x35, 0xEA, 0x86)  # curadj=1, cm_ctrl=0b10, swing_man=1
        device.write_reg(0x35, 0xE9, 0x01)  # sterm_override=1
        device.write_reg(0x35, 0xF0, 0x14)  # sterm=101
        device.write_reg(0x35, 0x3A, 0xF0)
        device.write_reg(0x35, 0x3A, 0xF7)
        device.write_reg(0x35, 0x3B, 0x80)
        device.write_reg(0x35, 0x3B, 0xBC)
        device.write_reg(0x35, 0x3B, 0xBD)
        device.write_reg(0x35, 0x3C, 0xE0)
        device.write_reg(0x35, 0x3C, 0xEF)
        device.write_reg(0x35, 0x3D, 0x00)
        device.write_reg(0x35, 0x3D, 0x78)
        device.write_reg(0x35, 0x3D, 0x7B)
        device.write_reg(0x35, 0x3E, 0xC0)
        device.write_reg(0x35, 0x3E, 0xDE)
        device.write_reg(0x35, 0x3F, 0xF0)
        device.write_reg(0x35, 0x3F, 0xF7)
        device.write_reg(0x35, 0x40, 0x80)
        device.write_reg(0x35, 0x40, 0xBC)
        device.write_reg(0x35, 0x40, 0xBD)

    def func_01_06_06_ana_debug_dp3_symbol_lock_use_rext(self):
        """01-06-06 ana_debug_dp3_symbol_lock_use_rext"""
        print("Cfg func_01_06_06_ana_debug_dp3_symbol_lock_use_rext...")
        device = self._get_device()
        device.write_reg(0x09, 0x83, 0x06)
        device.write_reg(0x09, 0x83, 0x06)
        device.write_reg(0x09, 0xC9, 0x00)
        device.write_reg(0x09, 0xC9, 0x00)
        device.write_reg(0x09, 0xCA, 0x00)
        device.write_reg(0x09, 0xCA, 0x00)
        device.write_reg(0x09, 0xC4, 0x3F)
        device.write_reg(0x09, 0xC4, 0x3F)
        device.write_reg(0x09, 0xC4, 0x3F)
        device.write_reg(0x09, 0xC4, 0x3F)
        device.write_reg(0x09, 0xC4, 0x3F)
        device.write_reg(0x09, 0xC4, 0x3F)
        device.write_reg(0x09, 0xC7, 0x00)
        device.write_reg(0x09, 0xC5, 0x00)
        device.write_reg(0x09, 0xC5, 0x00)
        device.write_reg(0x09, 0xC6, 0x00)
        device.write_reg(0x09, 0xC6, 0x00)
        device.write_reg(0x31, 0xE4, 0xDB)
        device.write_reg(0x31, 0x18, 0xDB)
        device.write_reg(0x32, 0xE4, 0x5B)
        device.write_reg(0x32, 0x18, 0x5B)
        device.write_reg(0x33, 0xE4, 0x5B)
        device.write_reg(0x33, 0x18, 0x5B)
        device.write_reg(0x34, 0xE4, 0x5B)
        device.write_reg(0x34, 0x18, 0x5B)
        device.write_reg(0x35, 0xE4, 0x5B)
        device.write_reg(0x35, 0x18, 0x5B)
        device.write_reg(0x31, 0xE4, 0x37)
        device.write_reg(0x31, 0x18, 0x37)
        device.write_reg(0x34, 0xE4, 0x37)
        device.write_reg(0x34, 0x18, 0x37)

    def func_01_06_07_ana_debug_up_symbol_lock_use_rext(self):
        """01-06-07 ana_debug_up_symbol_lock_use_rext"""
        print("Cfg func_01_06_07_ana_debug_up_symbol_lock_use_rext...")
        device = self._get_device()
        device.write_reg(0x09, 0x83, 0x06)
        device.write_reg(0x09, 0x83, 0x06)
        device.write_reg(0x09, 0xC9, 0x00)
        device.write_reg(0x09, 0xC9, 0x20)
        device.write_reg(0x09, 0xCA, 0x00)
        device.write_reg(0x09, 0xCA, 0x00)
        device.write_reg(0x09, 0xC4, 0x3F)
        device.write_reg(0x09, 0xC4, 0x3F)
        device.write_reg(0x09, 0xC4, 0x3F)
        device.write_reg(0x09, 0xC4, 0x3F)
        device.write_reg(0x09, 0xC4, 0x3F)
        device.write_reg(0x09, 0xC4, 0x3F)
        device.write_reg(0x09, 0xC7, 0x00)
        device.write_reg(0x09, 0xC5, 0x00)
        device.write_reg(0x09, 0xC5, 0x00)
        device.write_reg(0x09, 0xC6, 0x00)
        device.write_reg(0x09, 0xC6, 0x00)
        device.write_reg(0x31, 0xE4, 0xDB)
        device.write_reg(0x31, 0x18, 0xDB)
        device.write_reg(0x32, 0xE4, 0x5B)
        device.write_reg(0x32, 0x18, 0x5B)
        device.write_reg(0x33, 0xE4, 0x5B)
        device.write_reg(0x33, 0x18, 0x5B)
        device.write_reg(0x34, 0xE4, 0x5B)
        device.write_reg(0x34, 0x18, 0x5B)
        device.write_reg(0x35, 0xE4, 0x5B)
        device.write_reg(0x35, 0x18, 0x5B)
        device.write_reg(0x31, 0xE4, 0x37)
        device.write_reg(0x31, 0x18, 0x37)
        device.write_reg(0x34, 0xE4, 0x37)
        device.write_reg(0x34, 0x18, 0x37)

    def func_01_06_10_PIPE_ANA_ALL(self):
        """01-06-10 PIPE ANA ALL"""
        print("Cfg func_01_06_10_PIPE_ANA_ALL...")
        device = self._get_device()
        self.func_01_06_01_PIPE_ANA_UP()
        self.func_01_06_02_PIPE_ANA_DP1()
        self.func_01_06_03_PIPE_ANA_DP2()
        self.func_01_06_04_PIPE_ANA_DP3()
        self.func_01_06_05_PIPE_ANA_DP4()

    def func_01_07_01_USB3_UP_Rx_ANA(self):
        """01-07-01 USB3 UP Rx ANA"""
        print("Cfg func_01_07_01_USB3_UP_Rx_ANA...")
        device = self._get_device()
        device.write_reg(0x10, 0x01, 0x04)  # cdr ctrl,when after rstn,not skip
        device.write_reg(0x10, 0x06, 0x00)  # d_e_check balance set0
        device.write_reg(0x10, 0x09, 0x0E)  # cdr set seg mode
        device.write_reg(0x10, 0x0A, 0x20)  # 1D meas DAC settle time=100ns
        device.write_reg(0x10, 0x13, 0x01)  # h0 floor=1
        device.write_reg(0x10, 0x3F, 0x01)  # cdr_resetb man=0
        device.write_reg(0x10, 0x48, 0x80)  # man_en a0_t
        device.write_reg(0x10, 0x4A, 0x83)  # ES4 stg2 zero=3
        device.write_reg(0x10, 0x4B, 0x80)
        device.write_reg(0x10, 0x4C, 0x01)  # ES4 khp_t=1
        device.write_reg(0x10, 0x4D, 0x80)  # ES4 set00 1.2mA 3dB gain
        device.write_reg(0x10, 0x4E, 0x81)  # stg1_gain=1
        device.write_reg(0x10, 0x4F, 0x83)  # stg1_zero=3, es4
        device.write_reg(0x10, 0x54, 0x04)  # vga_cm=4
        device.write_reg(0x10, 0x55, 0x03)  # ES4 ipoly=3
        device.write_reg(0x10, 0x56, 0x02)  # ES4 iptat=2
        device.write_reg(0x10, 0x59, 0x04)  # pi_adj=100, 100uA
        device.write_reg(0x10, 0x5B, 0x11)  # meh settle use i2c
        device.write_reg(0x10, 0x60, 0x00)  # meh set 5000
        device.write_reg(0x10, 0x61, 0x13)  # meh set 5000
        device.write_reg(0x10, 0x62, 0x88)  # meh set 5000
        device.write_reg(0x10, 0x63, 0x03)
        device.write_reg(0x10, 0x64, 0xD0)
        device.write_reg(0x10, 0x65, 0x90)
        device.write_reg(0x10, 0x99, 0x30)  # dfe tap init reset=0, use pi 64step
        device.write_reg(0x10, 0x9B, 0x18)  # DFE enable
        device.write_reg(0x10, 0x9D, 0x00)
        device.write_reg(0x10, 0x9E, 0x00)
        device.write_reg(0x10, 0xA0, 0x00)  # loopen all 0
        device.write_reg(0x10, 0xA1, 0x00)  # loopen all 0
        device.write_reg(0x10, 0xA2, 0x00)  # loopen all 0
        device.write_reg(0x10, 0xA3, 0x00)  # loopen all 0
        device.write_reg(0x10, 0xA4, 0x00)  # loopen all 0
        device.write_reg(0x10, 0xA5, 0x00)  # loopen all 0
        device.write_reg(0x10, 0xA6, 0x00)  # loopen all 0
        device.write_reg(0x10, 0xBA, 0x3C)  # tap2-5 rst
        device.write_reg(0x10, 0xC6, 0xFD)  # min=253
        device.write_reg(0x10, 0xC7, 0x0A)  # max=10
        device.write_reg(0x10, 0xE0, 0x87)  # man_en=1
        device.write_reg(0x10, 0xE1, 0xCF)  # SSC
        device.write_reg(0x10, 0xE2, 0x00)  # CDR clk=1.25G
        device.write_reg(0x10, 0xE3, 0x02)  # cdr reset midway=00, midway sel=0
        device.write_reg(0x10, 0xEA, 0x54)  # ctle temp off, corner
        device.write_reg(0x10, 0xEB, 0x4C)
        device.write_reg(0x10, 0xEC, 0x2D)  # ES4 prevga=2
        device.write_reg(0x10, 0xED, 0x02)  # postvga=2
        device.write_reg(0x10, 0xEE, 0x20)  # ES4 pole_cap=2
        device.write_reg(0x10, 0xEF, 0x00)  # pole_cur_old=0, temp8
        device.write_reg(0x10, 0xF2, 0x00)  # spare1_0=0, SEL A, DFEclk use anareset
        device.write_reg(0x10, 0x9E, 0x0F)  # pd_use=00001111
        device.write_reg(0x10, 0x5F, 0x00)  # cdr fmin set
        device.write_reg(0x10, 0x5E, 0x10)  # cdr fmin set -4096
        device.write_reg(0x10, 0x5D, 0x00)  # cdr fmax set
        device.write_reg(0x10, 0x5C, 0x04)  # cdr fmax set +1024
        device.write_reg(0x10, 0x5B, 0xD1)  # cdr cicbw set2
        device.write_reg(0x10, 0x9D, 0x10)  # cdr use v4, debug sel=0

    def func_01_07_02_USB3_DP1_Rx_ANA(self):
        """01-07-02 USB3 DP1 Rx ANA"""
        print("Cfg func_01_07_02_USB3_DP1_Rx_ANA...")
        device = self._get_device()
        device.write_reg(0x11, 0x01, 0x04)  # cdr ctrl,when after rstn,not skip
        device.write_reg(0x11, 0x06, 0x00)  # d_e_check balance set0
        device.write_reg(0x11, 0x09, 0x0E)  # cdr set seg mode
        device.write_reg(0x11, 0x0A, 0x20)  # 1D meas DAC settle time=100ns
        device.write_reg(0x11, 0x13, 0x01)  # h0 floor=1
        device.write_reg(0x11, 0x3F, 0x01)  # cdr_resetb man=0
        device.write_reg(0x11, 0x48, 0x80)  # man_en a0_t
        device.write_reg(0x11, 0x4A, 0x83)  # ES4 stg2 zero=3
        device.write_reg(0x11, 0x4B, 0x80)
        device.write_reg(0x11, 0x4C, 0x01)  # ES4 khp_t=1
        device.write_reg(0x11, 0x4D, 0x80)  # ES4 set00 1.2mA 3dB gain
        device.write_reg(0x11, 0x4E, 0x81)  # stg1_gain=1
        device.write_reg(0x11, 0x4F, 0x83)  # stg1_zero=3, es4
        device.write_reg(0x11, 0x54, 0x04)  # vga_cm=4
        device.write_reg(0x11, 0x55, 0x03)  # ES4 ipoly=3
        device.write_reg(0x11, 0x56, 0x02)  # ES4 iptat=2
        device.write_reg(0x11, 0x59, 0x04)  # pi_adj=100, 100uA
        device.write_reg(0x11, 0x5B, 0x11)  # meh settle use i2c
        device.write_reg(0x11, 0x60, 0x00)  # meh set 5000
        device.write_reg(0x11, 0x61, 0x13)  # meh set 5000
        device.write_reg(0x11, 0x62, 0x88)  # meh set 5000
        device.write_reg(0x11, 0x63, 0x03)
        device.write_reg(0x11, 0x64, 0xD0)
        device.write_reg(0x11, 0x65, 0x90)
        device.write_reg(0x11, 0x99, 0x30)  # dfe tap init reset=0, use pi 64step
        device.write_reg(0x11, 0x9B, 0x18)  # DFE enable
        device.write_reg(0x11, 0x9D, 0x00)
        device.write_reg(0x11, 0x9E, 0x00)
        device.write_reg(0x11, 0xA0, 0x00)  # loopen all 0
        device.write_reg(0x11, 0xA1, 0x00)  # loopen all 0
        device.write_reg(0x11, 0xA2, 0x00)  # loopen all 0
        device.write_reg(0x11, 0xA3, 0x00)  # loopen all 0
        device.write_reg(0x11, 0xA4, 0x00)  # loopen all 0
        device.write_reg(0x11, 0xA5, 0x00)  # loopen all 0
        device.write_reg(0x11, 0xA6, 0x00)  # loopen all 0
        device.write_reg(0x11, 0xBA, 0x3C)  # tap2-5 rst
        device.write_reg(0x11, 0xC6, 0xFD)  # min=253
        device.write_reg(0x11, 0xC7, 0x0A)  # max=10
        device.write_reg(0x11, 0xE0, 0x87)  # man_en=1
        device.write_reg(0x11, 0xE1, 0xCF)  # SSC
        device.write_reg(0x11, 0xE2, 0x00)  # CDR clk=1.25G
        device.write_reg(0x11, 0xE3, 0x02)  # cdr reset midway=00, midway sel=0
        device.write_reg(0x11, 0xEA, 0x54)  # ctle temp off, corner
        device.write_reg(0x11, 0xEB, 0x4C)
        device.write_reg(0x11, 0xEC, 0x2D)  # ES4 prevga=2
        device.write_reg(0x11, 0xED, 0x02)  # postvga=2
        device.write_reg(0x11, 0xEE, 0x20)  # ES4 pole_cap=2
        device.write_reg(0x11, 0xEF, 0x00)  # pole_cur_old=0, temp8
        device.write_reg(0x11, 0xF2, 0x00)  # spare1_0=0, SEL A, DFEclk use anareset
        device.write_reg(0x11, 0x9E, 0x0F)  # pd_use=00001111
        device.write_reg(0x11, 0x5F, 0x00)  # cdr fmin set
        device.write_reg(0x11, 0x5E, 0x10)  # cdr fmin set -4096
        device.write_reg(0x11, 0x5D, 0x00)  # cdr fmax set
        device.write_reg(0x11, 0x5C, 0x04)  # cdr fmax set +1024
        device.write_reg(0x11, 0x5B, 0xD1)  # cdr cicbw set2
        device.write_reg(0x11, 0x9D, 0x10)  # cdr use v4, debug sel=0

    def func_01_07_03_USB3_DP2_Rx_ANA(self):
        """01-07-03 USB3 DP2 Rx ANA"""
        print("Cfg func_01_07_03_USB3_DP2_Rx_ANA...")
        device = self._get_device()
        device.write_reg(0x12, 0x01, 0x04)  # cdr ctrl,when after rstn,not skip
        device.write_reg(0x12, 0x06, 0x00)  # d_e_check balance set0
        device.write_reg(0x12, 0x09, 0x0E)  # cdr set seg mode
        device.write_reg(0x12, 0x0A, 0x20)  # 1D meas DAC settle time=100ns
        device.write_reg(0x12, 0x13, 0x01)  # h0 floor=1
        device.write_reg(0x12, 0x3F, 0x01)  # cdr_resetb man=0
        device.write_reg(0x12, 0x48, 0x80)  # man_en a0_t
        device.write_reg(0x12, 0x4A, 0x83)  # ES4 stg2 zero=3
        device.write_reg(0x12, 0x4B, 0x80)
        device.write_reg(0x12, 0x4C, 0x01)  # ES4 khp_t=1
        device.write_reg(0x12, 0x4D, 0x80)  # ES4 set00 1.2mA 3dB gain
        device.write_reg(0x12, 0x4E, 0x81)  # stg1_gain=1
        device.write_reg(0x12, 0x4F, 0x83)  # stg1_zero=3, es4
        device.write_reg(0x12, 0x54, 0x04)  # vga_cm=4
        device.write_reg(0x12, 0x55, 0x03)  # ES4 ipoly=3
        device.write_reg(0x12, 0x56, 0x02)  # ES4 iptat=2
        device.write_reg(0x12, 0x59, 0x04)  # pi_adj=100, 100uA
        device.write_reg(0x12, 0x5B, 0x11)  # meh settle use i2c
        device.write_reg(0x12, 0x60, 0x00)  # meh set 5000
        device.write_reg(0x12, 0x61, 0x13)  # meh set 5000
        device.write_reg(0x12, 0x62, 0x88)  # meh set 5000
        device.write_reg(0x12, 0x63, 0x03)
        device.write_reg(0x12, 0x64, 0xD0)
        device.write_reg(0x12, 0x65, 0x90)
        device.write_reg(0x12, 0x99, 0x30)  # dfe tap init reset=0, use pi 64step
        device.write_reg(0x12, 0x9B, 0x18)  # DFE enable
        device.write_reg(0x12, 0x9D, 0x00)
        device.write_reg(0x12, 0x9E, 0x00)
        device.write_reg(0x12, 0xA0, 0x00)  # loopen all 0
        device.write_reg(0x12, 0xA1, 0x00)  # loopen all 0
        device.write_reg(0x12, 0xA2, 0x00)  # loopen all 0
        device.write_reg(0x12, 0xA3, 0x00)  # loopen all 0
        device.write_reg(0x12, 0xA4, 0x00)  # loopen all 0
        device.write_reg(0x12, 0xA5, 0x00)  # loopen all 0
        device.write_reg(0x12, 0xA6, 0x00)  # loopen all 0
        device.write_reg(0x12, 0xBA, 0x3C)  # tap2-5 rst
        device.write_reg(0x12, 0xC6, 0xFD)  # min=253
        device.write_reg(0x12, 0xC7, 0x0A)  # max=10
        device.write_reg(0x12, 0xE0, 0x87)  # man_en=1
        device.write_reg(0x12, 0xE1, 0xCF)  # SSC
        device.write_reg(0x12, 0xE2, 0x00)  # CDR clk=1.25G
        device.write_reg(0x12, 0xE3, 0x02)  # cdr reset midway=00, midway sel=0
        device.write_reg(0x12, 0xEA, 0x54)  # ctle temp off, corner
        device.write_reg(0x12, 0xEB, 0x4C)
        device.write_reg(0x12, 0xEC, 0x2D)  # ES4 prevga=2
        device.write_reg(0x12, 0xED, 0x02)  # postvga=2
        device.write_reg(0x12, 0xEE, 0x20)  # ES4 pole_cap=2
        device.write_reg(0x12, 0xEF, 0x00)  # pole_cur_old=0, temp8
        device.write_reg(0x12, 0xF2, 0x00)  # spare1_0=0, SEL A, DFEclk use anareset
        device.write_reg(0x12, 0x9E, 0x0F)  # pd_use=00001111
        device.write_reg(0x12, 0x5F, 0x00)  # cdr fmin set
        device.write_reg(0x12, 0x5E, 0x10)  # cdr fmin set -4096
        device.write_reg(0x12, 0x5D, 0x00)  # cdr fmax set
        device.write_reg(0x12, 0x5C, 0x04)  # cdr fmax set +1024
        device.write_reg(0x12, 0x5B, 0xD1)  # cdr cicbw set2
        device.write_reg(0x12, 0x9D, 0x10)  # cdr use v4, debug sel=0

    def func_01_07_04_USB3_DP3_Rx_ANA(self):
        """01-07-04 USB3 DP3 Rx ANA"""
        print("Cfg func_01_07_04_USB3_DP3_Rx_ANA...")
        device = self._get_device()
        device.write_reg(0x13, 0x01, 0x04)  # cdr ctrl,when after rstn,not skip
        device.write_reg(0x13, 0x06, 0x00)  # d_e_check balance set0
        device.write_reg(0x13, 0x09, 0x0E)  # cdr set seg mode
        device.write_reg(0x13, 0x0A, 0x20)  # 1D meas DAC settle time=100ns
        device.write_reg(0x13, 0x13, 0x01)  # h0 floor=1
        device.write_reg(0x13, 0x3F, 0x01)  # cdr_resetb man=0
        device.write_reg(0x13, 0x48, 0x80)  # man_en a0_t
        device.write_reg(0x13, 0x4A, 0x83)  # ES4 stg2 zero=3
        device.write_reg(0x13, 0x4B, 0x80)
        device.write_reg(0x13, 0x4C, 0x01)  # ES4 khp_t=1
        device.write_reg(0x13, 0x4D, 0x80)  # ES4 set00 1.2mA 3dB gain
        device.write_reg(0x13, 0x4E, 0x81)  # stg1_gain=1
        device.write_reg(0x13, 0x4F, 0x83)  # stg1_zero=3, es4
        device.write_reg(0x13, 0x54, 0x04)  # vga_cm=4
        device.write_reg(0x13, 0x55, 0x03)  # ES4 ipoly=3
        device.write_reg(0x13, 0x56, 0x02)  # ES4 iptat=2
        device.write_reg(0x13, 0x59, 0x04)  # pi_adj=100, 100uA
        device.write_reg(0x13, 0x5B, 0x11)  # meh settle use i2c
        device.write_reg(0x13, 0x60, 0x00)  # meh set 5000
        device.write_reg(0x13, 0x61, 0x13)  # meh set 5000
        device.write_reg(0x13, 0x62, 0x88)  # meh set 5000
        device.write_reg(0x13, 0x63, 0x03)
        device.write_reg(0x13, 0x64, 0xD0)
        device.write_reg(0x13, 0x65, 0x90)
        device.write_reg(0x13, 0x99, 0x30)  # dfe tap init reset=0, use pi 64step
        device.write_reg(0x13, 0x9B, 0x18)  # DFE enable
        device.write_reg(0x13, 0x9D, 0x00)
        device.write_reg(0x13, 0x9E, 0x00)
        device.write_reg(0x13, 0xA0, 0x00)  # loopen all 0
        device.write_reg(0x13, 0xA1, 0x00)  # loopen all 0
        device.write_reg(0x13, 0xA2, 0x00)  # loopen all 0
        device.write_reg(0x13, 0xA3, 0x00)  # loopen all 0
        device.write_reg(0x13, 0xA4, 0x00)  # loopen all 0
        device.write_reg(0x13, 0xA5, 0x00)  # loopen all 0
        device.write_reg(0x13, 0xA6, 0x00)  # loopen all 0
        device.write_reg(0x13, 0xBA, 0x3C)  # tap2-5 rst
        device.write_reg(0x13, 0xC6, 0xFD)  # min=253
        device.write_reg(0x13, 0xC7, 0x0A)  # max=10
        device.write_reg(0x13, 0xE0, 0x87)  # man_en=1
        device.write_reg(0x13, 0xE1, 0xCF)  # SSC
        device.write_reg(0x13, 0xE2, 0x00)  # CDR clk=1.25G
        device.write_reg(0x13, 0xE3, 0x02)  # cdr reset midway=00, midway sel=0
        device.write_reg(0x13, 0xEA, 0x54)  # ctle temp off, corner
        device.write_reg(0x13, 0xEB, 0x4C)
        device.write_reg(0x13, 0xEC, 0x2D)  # ES4 prevga=2
        device.write_reg(0x13, 0xED, 0x02)  # postvga=2
        device.write_reg(0x13, 0xEE, 0x20)  # ES4 pole_cap=2
        device.write_reg(0x13, 0xEF, 0x00)  # pole_cur_old=0, temp8
        device.write_reg(0x13, 0xF2, 0x00)  # spare1_0=0, SEL A, DFEclk use anareset
        device.write_reg(0x13, 0x9E, 0x0F)  # pd_use=00001111
        device.write_reg(0x13, 0x5F, 0x00)  # cdr fmin set
        device.write_reg(0x13, 0x5E, 0x10)  # cdr fmin set -4096
        device.write_reg(0x13, 0x5D, 0x00)  # cdr fmax set
        device.write_reg(0x13, 0x5C, 0x04)  # cdr fmax set +1024
        device.write_reg(0x13, 0x5B, 0xD1)  # cdr cicbw set2
        device.write_reg(0x13, 0x9D, 0x10)  # cdr use v4, debug sel=0

    def func_01_07_05_USB3_DP4_Rx_ANA(self):
        """01-07-05 USB3 DP4 Rx ANA"""
        print("Cfg func_01_07_05_USB3_DP4_Rx_ANA...")
        device = self._get_device()
        device.write_reg(0x14, 0x01, 0x04)  # cdr ctrl,when after rstn,not skip
        device.write_reg(0x14, 0x06, 0x00)  # d_e_check balance set0
        device.write_reg(0x14, 0x09, 0x0E)  # cdr set seg mode
        device.write_reg(0x14, 0x0A, 0x20)  # 1D meas DAC settle time=100ns
        device.write_reg(0x14, 0x13, 0x01)  # h0 floor=1
        device.write_reg(0x14, 0x3F, 0x01)  # cdr_resetb man=0
        device.write_reg(0x14, 0x48, 0x80)  # man_en a0_t
        device.write_reg(0x14, 0x4A, 0x83)  # ES4 stg2 zero=3
        device.write_reg(0x14, 0x4B, 0x80)
        device.write_reg(0x14, 0x4C, 0x01)  # ES4 khp_t=1
        device.write_reg(0x14, 0x4D, 0x80)  # ES4 set00 1.2mA 3dB gain
        device.write_reg(0x14, 0x4E, 0x81)  # stg1_gain=1
        device.write_reg(0x14, 0x4F, 0x83)  # stg1_zero=3, es4
        device.write_reg(0x14, 0x54, 0x04)  # vga_cm=4
        device.write_reg(0x14, 0x55, 0x03)  # ES4 ipoly=3
        device.write_reg(0x14, 0x56, 0x02)  # ES4 iptat=2
        device.write_reg(0x14, 0x59, 0x04)  # pi_adj=100, 100uA
        device.write_reg(0x14, 0x5B, 0x11)  # meh settle use i2c
        device.write_reg(0x14, 0x60, 0x00)  # meh set 5000
        device.write_reg(0x14, 0x61, 0x13)  # meh set 5000
        device.write_reg(0x14, 0x62, 0x88)  # meh set 5000
        device.write_reg(0x14, 0x63, 0x03)
        device.write_reg(0x14, 0x64, 0xD0)
        device.write_reg(0x14, 0x65, 0x90)
        device.write_reg(0x14, 0x99, 0x30)  # dfe tap init reset=0, use pi 64step
        device.write_reg(0x14, 0x9B, 0x18)  # DFE enable
        device.write_reg(0x14, 0x9D, 0x00)
        device.write_reg(0x14, 0x9E, 0x00)
        device.write_reg(0x14, 0xA0, 0x00)  # loopen all 0
        device.write_reg(0x14, 0xA1, 0x00)  # loopen all 0
        device.write_reg(0x14, 0xA2, 0x00)  # loopen all 0
        device.write_reg(0x14, 0xA3, 0x00)  # loopen all 0
        device.write_reg(0x14, 0xA4, 0x00)  # loopen all 0
        device.write_reg(0x14, 0xA5, 0x00)  # loopen all 0
        device.write_reg(0x14, 0xA6, 0x00)  # loopen all 0
        device.write_reg(0x14, 0xBA, 0x3C)  # tap2-5 rst
        device.write_reg(0x14, 0xC6, 0xFD)  # min=253
        device.write_reg(0x14, 0xC7, 0x0A)  # max=10
        device.write_reg(0x14, 0xE0, 0x87)  # man_en=1
        device.write_reg(0x14, 0xE1, 0xCF)  # SSC
        device.write_reg(0x14, 0xE2, 0x00)  # CDR clk=1.25G
        device.write_reg(0x14, 0xE3, 0x02)  # cdr reset midway=00, midway sel=0
        device.write_reg(0x14, 0xEA, 0x54)  # ctle temp off, corner
        device.write_reg(0x14, 0xEB, 0x4C)
        device.write_reg(0x14, 0xEC, 0x2D)  # ES4 prevga=2
        device.write_reg(0x14, 0xED, 0x02)  # postvga=2
        device.write_reg(0x14, 0xEE, 0x20)  # ES4 pole_cap=2
        device.write_reg(0x14, 0xEF, 0x00)  # pole_cur_old=0, temp8
        device.write_reg(0x14, 0xF2, 0x00)  # spare1_0=0, SEL A, DFEclk use anareset
        device.write_reg(0x14, 0x9E, 0x0F)  # pd_use=00001111
        device.write_reg(0x14, 0x5F, 0x00)  # cdr fmin set
        device.write_reg(0x14, 0x5E, 0x10)  # cdr fmin set -4096
        device.write_reg(0x14, 0x5D, 0x00)  # cdr fmax set
        device.write_reg(0x14, 0x5C, 0x04)  # cdr fmax set +1024
        device.write_reg(0x14, 0x5B, 0xD1)  # cdr cicbw set2
        device.write_reg(0x14, 0x9D, 0x10)  # cdr use v4, debug sel=0

    def func_01_07_10_USB3_Rx_ANA_ALL(self):
        """01-07-10 USB3 Rx ANA ALL"""
        print("Cfg func_01_07_10_USB3_Rx_ANA_ALL...")
        device = self._get_device()
        self.func_01_07_01_USB3_UP_Rx_ANA()
        self.func_01_07_02_USB3_DP1_Rx_ANA()
        self.func_01_07_03_USB3_DP2_Rx_ANA()
        self.func_01_07_04_USB3_DP3_Rx_ANA()
        self.func_01_07_05_USB3_DP4_Rx_ANA()

    def func_01_10_USB_PHY_ALL(self):
        """01-10 USB PHY ALL"""
        print("Cfg func_01_10_USB_PHY_ALL...")
        device = self._get_device()
        self.func_01_01_03_ADC_test()
        self.func_01_05_10_USB2_Phy_ALL()
        self.func_01_06_10_PIPE_ANA_ALL()
        self.func_01_07_10_USB3_Rx_ANA_ALL()

    def func_02_01_HS_tx_UP_V2_PRBS(self):
        """02-01 HS_tx UP V2 PRBS"""
        print("Cfg func_02_01_HS_tx_UP_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x09, 0xC8, 0x08)  # i2c_utmi_port0_sel
        device.write_reg(0x47, 0x20, 0x82)  # i2c_utm_man_en
        device.write_reg(0x47, 0x31, 0x00)  # i2c_prbs_tx_wr_num 512
        device.write_reg(0x47, 0x32, 0x02)  # i2c_prbs_tx_wr_num
        device.write_reg(0x47, 0x33, 0xD0)  # i2c_prbs_tx_period_num  2000
        device.write_reg(0x47, 0x34, 0x07)  # i2c_prbs_tx_period_num
        device.write_reg(0x47, 0x30, 0x03)  # prbs_gen_enable & prbs_gen_preset_en

    def func_02_02_HS_tx_DP1_V2_PRBS(self):
        """02-02 HS_tx DP1 V2 PRBS"""
        print("Cfg func_02_02_HS_tx_DP1_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x48, 0x20, 0x82)  # i2c_utm_man_en
        device.write_reg(0x48, 0x31, 0x00)  # i2c_prbs_tx_wr_num 512
        device.write_reg(0x48, 0x32, 0x02)  # i2c_prbs_tx_wr_num
        device.write_reg(0x48, 0x33, 0xD0)  # i2c_prbs_tx_period_num  2000
        device.write_reg(0x48, 0x34, 0x07)  # i2c_prbs_tx_period_num
        device.write_reg(0x48, 0x30, 0x03)  # prbs_gen_enable & prbs_gen_preset_en

    def func_02_03_HS_tx_DP2_V2_PRBS(self):
        """02-03 HS_tx DP2 V2 PRBS"""
        print("Cfg func_02_03_HS_tx_DP2_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x49, 0x20, 0x82)  # i2c_utm_man_en
        device.write_reg(0x49, 0x31, 0x00)  # i2c_prbs_tx_wr_num 512
        device.write_reg(0x49, 0x32, 0x02)  # i2c_prbs_tx_wr_num
        device.write_reg(0x49, 0x33, 0xD0)  # i2c_prbs_tx_period_num  2000
        device.write_reg(0x49, 0x34, 0x07)  # i2c_prbs_tx_period_num
        device.write_reg(0x49, 0x30, 0x03)  # prbs_gen_enable & prbs_gen_preset_en

    def func_02_04_HS_tx_DP3_V2_PRBS(self):
        """02-04 HS_tx DP3 V2 PRBS"""
        print("Cfg func_02_04_HS_tx_DP3_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x4A, 0x20, 0x82)  # i2c_utm_man_en
        device.write_reg(0x4A, 0x31, 0x00)  # i2c_prbs_tx_wr_num 512
        device.write_reg(0x4A, 0x32, 0x02)  # i2c_prbs_tx_wr_num
        device.write_reg(0x4A, 0x33, 0xD0)  # i2c_prbs_tx_period_num  2000
        device.write_reg(0x4A, 0x34, 0x07)  # i2c_prbs_tx_period_num
        device.write_reg(0x4A, 0x30, 0x03)  # prbs_gen_enable & prbs_gen_preset_en

    def func_02_05_HS_tx_DP4_V2_PRBS(self):
        """02-05 HS_tx DP4 V2 PRBS"""
        print("Cfg func_02_05_HS_tx_DP4_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x4B, 0x20, 0x82)  # i2c_utm_man_en
        device.write_reg(0x4B, 0x31, 0x00)  # i2c_prbs_tx_wr_num 512
        device.write_reg(0x4B, 0x32, 0x02)  # i2c_prbs_tx_wr_num
        device.write_reg(0x4B, 0x33, 0xD0)  # i2c_prbs_tx_period_num  2000
        device.write_reg(0x4B, 0x34, 0x07)  # i2c_prbs_tx_period_num
        device.write_reg(0x4B, 0x30, 0x03)  # prbs_gen_enable & prbs_gen_preset_en

    def func_02_06_HS_rx_UP_V2_PRBS(self):
        """02-06 HS_rx UP V2 PRBS"""
        print("Cfg func_02_06_HS_rx_UP_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x09, 0xC8, 0x08)  # i2c_utmi_port0_sel
        device.write_reg(0x47, 0x20, 0x83)  # i2c_utm_man_en
        device.write_reg(0x47, 0x30, 0x0E)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en
        device.write_reg(0x47, 0x30, 0x06)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en

    def func_02_07_HS_rx_DP1_V2_PRBS(self):
        """02-07 HS_rx DP1 V2 PRBS"""
        print("Cfg func_02_07_HS_rx_DP1_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x48, 0x20, 0x83)  # i2c_utm_man_en
        device.write_reg(0x48, 0x30, 0x0E)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en
        device.write_reg(0x48, 0x30, 0x06)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en

    def func_02_08_HS_rx_DP2_V2_PRBS(self):
        """02-08 HS_rx DP2 V2 PRBS"""
        print("Cfg func_02_08_HS_rx_DP2_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x49, 0x20, 0x83)  # i2c_utm_man_en
        device.write_reg(0x49, 0x30, 0x0E)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en
        device.write_reg(0x49, 0x30, 0x06)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en

    def func_02_09_HS_rx_DP3_V2_PRBS(self):
        """02-09 HS_rx DP3 V2 PRBS"""
        print("Cfg func_02_09_HS_rx_DP3_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x4A, 0x20, 0x83)  # i2c_utm_man_en
        device.write_reg(0x4A, 0x30, 0x0E)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en
        device.write_reg(0x4A, 0x30, 0x06)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en

    def func_02_10_HS_rx_DP4_V2_PRBS(self):
        """02-10 HS_rx DP4 V2 PRBS"""
        print("Cfg func_02_10_HS_rx_DP4_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x4B, 0x20, 0x83)  # i2c_utm_man_en
        device.write_reg(0x4B, 0x30, 0x0E)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en
        device.write_reg(0x4B, 0x30, 0x06)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en

    def func_02_11_FS_tx_DP1_PRBS(self):
        """02-11 FS_tx DP1 PRBS"""
        print("Cfg func_02_11_FS_tx_DP1_PRBS...")
        device = self._get_device()
        device.write_reg(0x48, 0x20, 0xC6)  # i2c_xcvrselect & i2c_termselect & i2c_utm_man_en
        device.write_reg(0x48, 0x21, 0x13)  # i2c_dm_pd & i2c_dp_pd & i2c_fslsserialmode
        device.write_reg(0x48, 0x40, 0x03)  # i2c_fs_prbs_en
        device.write_reg(0x48, 0x31, 0x00)  # i2c_prbs_tx_wr_num 512
        device.write_reg(0x48, 0x32, 0x02)  # i2c_prbs_tx_wr_num
        device.write_reg(0x48, 0x33, 0x30)  # i2c_prbs_tx_period_num  30000
        device.write_reg(0x48, 0x34, 0x75)  # i2c_prbs_tx_period_num
        device.write_reg(0x48, 0x30, 0x03)  # prbs_gen_enable & prbs_gen_preset_en

    def func_02_12_FS_rx_UP_V2_PRBS(self):
        """02-12 FS_rx UP V2 PRBS"""
        print("Cfg func_02_12_FS_rx_UP_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x09, 0xC8, 0x08)  # i2c_utmi_port0_sel
        device.write_reg(0x47, 0x20, 0xC7)  # i2c_xcvrselect & i2c_termselect & i2c_utm_man_en
        device.write_reg(0x47, 0x21, 0x61)  # i2c_dm_pd & i2c_dp_pd & i2c_fslsserialmode
        device.write_reg(0x47, 0x40, 0x03)  # i2c_fs_prbs_en
        device.write_reg(0x47, 0x30, 0x0E)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en
        device.write_reg(0x47, 0x30, 0x06)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en

    def func_02_13_FS_rx_DP1_PRBS(self):
        """02-13 FS_rx DP1 PRBS"""
        print("Cfg func_02_13_FS_rx_DP1_PRBS...")
        device = self._get_device()
        device.write_reg(0x48, 0x20, 0xC7)  # i2c_xcvrselect & i2c_termselect & i2c_utm_man_en
        device.write_reg(0x48, 0x21, 0x61)  # i2c_dm_pd & i2c_dp_pd & i2c_fslsserialmode
        device.write_reg(0x48, 0x40, 0x03)  # i2c_fs_prbs_en
        device.write_reg(0x48, 0x30, 0x0E)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en
        device.write_reg(0x48, 0x30, 0x06)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en

    def func_02_14_FS_rx_DP2_PRBS(self):
        """02-14 FS_rx DP2 PRBS"""
        print("Cfg func_02_14_FS_rx_DP2_PRBS...")
        device = self._get_device()
        device.write_reg(0x49, 0x20, 0xC7)  # i2c_xcvrselect & i2c_termselect & i2c_utm_man_en
        device.write_reg(0x49, 0x21, 0x61)  # i2c_dm_pd & i2c_dp_pd & i2c_fslsserialmode
        device.write_reg(0x49, 0x40, 0x03)  # i2c_fs_prbs_en
        device.write_reg(0x49, 0x30, 0x0E)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en
        device.write_reg(0x49, 0x30, 0x06)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en

    def func_02_15_FS_rx_DP3_V2_PRBS(self):
        """02-15 FS_rx DP3 V2 PRBS"""
        print("Cfg func_02_15_FS_rx_DP3_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x4A, 0x20, 0xC7)  # i2c_xcvrselect & i2c_termselect & i2c_utm_man_en
        device.write_reg(0x4A, 0x21, 0x61)  # i2c_dm_pd & i2c_dp_pd & i2c_fslsserialmode
        device.write_reg(0x4A, 0x40, 0x03)  # i2c_fs_prbs_en
        device.write_reg(0x4A, 0x30, 0x0E)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en
        device.write_reg(0x4A, 0x30, 0x06)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en

    def func_02_16_FS_rx_DP4_V2_PRBS(self):
        """02-16 FS_rx DP4 V2 PRBS"""
        print("Cfg func_02_16_FS_rx_DP4_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x4B, 0x20, 0xC7)  # i2c_xcvrselect & i2c_termselect & i2c_utm_man_en
        device.write_reg(0x4B, 0x21, 0x61)  # i2c_dm_pd & i2c_dp_pd & i2c_fslsserialmode
        device.write_reg(0x4B, 0x40, 0x03)  # i2c_fs_prbs_en
        device.write_reg(0x4B, 0x30, 0x0E)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en
        device.write_reg(0x4B, 0x30, 0x06)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en

    def func_02_17_LS_tx_DP1_PRBS(self):
        """02-17 LS_tx DP1 PRBS"""
        print("Cfg func_02_17_LS_tx_DP1_PRBS...")
        device = self._get_device()
        device.write_reg(0x48, 0x20, 0xCA)  # i2c_xcvrselect & i2c_termselect & i2c_utm_man_en
        device.write_reg(0x48, 0x21, 0x13)  # i2c_dm_pd & i2c_dp_pd & i2c_fslsserialmode
        device.write_reg(0x48, 0x40, 0x01)  # i2c_fsls_speed & i2c_fs_prbs_en
        device.write_reg(0x48, 0x31, 0x08)  # i2c_prbs_tx_wr_num 8
        device.write_reg(0x48, 0x32, 0x00)  # i2c_prbs_tx_wr_num
        device.write_reg(0x48, 0x33, 0xB8)  # i2c_prbs_tx_period_num  3000
        device.write_reg(0x48, 0x34, 0x0B)  # i2c_prbs_tx_period_num
        device.write_reg(0x48, 0x30, 0x03)  # prbs_gen_enable & prbs_gen_preset_en

    def func_02_18_LS_rx_UP_V2_PRBS(self):
        """02-18 LS_rx UP V2 PRBS"""
        print("Cfg func_02_18_LS_rx_UP_V2_PRBS...")
        device = self._get_device()
        device.write_reg(0x09, 0xC8, 0x08)  # i2c_utmi_port0_sel
        device.write_reg(0x47, 0x20, 0xCB)  # i2c_xcvrselect & i2c_termselect & i2c_utm_man_en
        device.write_reg(0x47, 0x21, 0x0D)  # i2c_dm_pu2 & i2c_dm_pu1 & i2c_fslsserialmode
        device.write_reg(0x47, 0x40, 0x01)  # i2c_fsls_speed & i2c_fs_prbs_en
        device.write_reg(0x47, 0x30, 0x0E)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en
        device.write_reg(0x47, 0x30, 0x06)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en

    def func_02_19_LS_rx_DP1_PRBS(self):
        """02-19 LS_rx DP1 PRBS"""
        print("Cfg func_02_19_LS_rx_DP1_PRBS...")
        device = self._get_device()
        device.write_reg(0x48, 0x20, 0xCB)  # i2c_xcvrselect & i2c_termselect & i2c_utm_man_en
        device.write_reg(0x48, 0x21, 0x0D)  # i2c_dm_pu2 & i2c_dm_pu1 & i2c_fslsserialmode
        device.write_reg(0x48, 0x40, 0x01)  # i2c_fsls_speed & i2c_fs_prbs_en
        device.write_reg(0x48, 0x30, 0x0E)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en
        device.write_reg(0x48, 0x30, 0x06)  # prbs_check_clear & prbs_check_enable  &  prbs_gen_preset_en

    def func_03_01_PIPE_up_Tx_Rx_PRBS(self):
        """03-01 PIPE-up Tx/Rx PRBS"""
        print("Cfg func_03_01_PIPE_up_Tx_Rx_PRBS...")
        device = self._get_device()
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x05, 0x4F)
        device.write_reg(0x31, 0x05, 0x4F)
        device.write_reg(0x31, 0x05, 0x4F)
        device.write_reg(0x31, 0x05, 0x4F)
        device.write_reg(0x31, 0x05, 0x4F)
        device.write_reg(0x31, 0x05, 0x4F)
        device.write_reg(0x31, 0x05, 0x4F)
        device.write_reg(0x31, 0x05, 0x4F)
        device.write_reg(0x31, 0x05, 0x4F)
        device.write_reg(0x31, 0x05, 0x4F)
        device.write_reg(0x31, 0x0A, 0x10)
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0x0A, 0x10)
        device.write_reg(0x31, 0x08, 0x80)
        device.write_reg(0x31, 0x08, 0x80)
        device.write_reg(0x31, 0x08, 0x80)
        device.write_reg(0x31, 0x08, 0x80)
        device.write_reg(0x31, 0x08, 0x80)
        device.write_reg(0x31, 0x08, 0x80)
        device.write_reg(0x31, 0x0A, 0x10)
        device.write_reg(0x31, 0x09, 0x00)
        device.write_reg(0x31, 0xE5, 0xFF)
        device.write_reg(0x31, 0xE5, 0xFF)
        device.write_reg(0x31, 0xE5, 0xFF)
        device.write_reg(0x31, 0xE5, 0xFF)
        device.write_reg(0x31, 0xE5, 0xFF)
        device.write_reg(0x31, 0xE5, 0xFF)
        device.write_reg(0x31, 0xE5, 0xFF)
        device.write_reg(0x31, 0xE5, 0xFF)
        device.write_reg(0x31, 0xFF, 0x0E)
        device.write_reg(0x31, 0xFF, 0x0E)
        device.write_reg(0x31, 0xE6, 0x80)
        device.write_reg(0x31, 0xE6, 0x80)
        device.write_reg(0x31, 0xFF, 0x0E)
        device.write_reg(0x31, 0xFF, 0x0E)
        device.write_reg(0x31, 0x19, 0xC0)
        device.write_reg(0x31, 0x19, 0x80)
        device.write_reg(0x31, 0x19, 0x80)
        device.write_reg(0x31, 0x19, 0x80)
        device.write_reg(0x31, 0x1C, 0x26)
        device.write_reg(0x31, 0x1C, 0x26)
        device.write_reg(0x31, 0x19, 0x80)
        device.write_reg(0x31, 0x1E, 0x00)
        device.write_reg(0x31, 0x0E, 0x4F)
        device.write_reg(0x31, 0x0E, 0x4F)
        device.write_reg(0x31, 0x0E, 0x4F)
        device.write_reg(0x31, 0x0E, 0x4F)
        device.write_reg(0x31, 0x0E, 0x4F)
        device.write_reg(0x31, 0x0E, 0x4F)
        device.write_reg(0x31, 0x0E, 0x4F)
        device.write_reg(0x31, 0x0E, 0x4F)
        device.write_reg(0x31, 0x0E, 0x4F)
        device.write_reg(0x31, 0x0E, 0x4F)
        device.write_reg(0x31, 0x0F, 0x64)
        device.write_reg(0x31, 0x0F, 0x64)
        device.write_reg(0x31, 0x0F, 0x64)
        device.write_reg(0x31, 0x0F, 0x64)
        device.write_reg(0x31, 0x0F, 0x64)
        device.write_reg(0x31, 0x0E, 0x4F)
        device.write_reg(0x31, 0x0E, 0x4F)
        device.write_reg(0x31, 0x1E, 0x00)
        device.write_reg(0x31, 0x1E, 0x00)
        device.write_reg(0x31, 0x1E, 0x08)
        device.write_reg(0x31, 0x1E, 0x0C)
        device.write_reg(0x31, 0x1E, 0x08)
        device.write_reg(0x31, 0x1E, 0x00)
        device.write_reg(0x31, 0x19, 0xC0)
        device.write_reg(0x31, 0x0D, 0x60)
        device.write_reg(0x31, 0x0D, 0x60)
        device.write_reg(0x31, 0x0D, 0x60)
        device.write_reg(0x31, 0x0D, 0x60)
        device.write_reg(0x31, 0x10, 0x0C)
        device.write_reg(0x31, 0x10, 0x0C)
        device.write_reg(0x31, 0x64, 0xB0)
        device.write_reg(0x31, 0x63, 0x30)
        device.write_reg(0x31, 0x63, 0x30)
        device.write_reg(0x31, 0x63, 0x30)
        device.write_reg(0x31, 0x64, 0xB0)
        device.write_reg(0x31, 0x64, 0xB0)
        device.write_reg(0x31, 0x63, 0x20)
        device.write_reg(0x31, 0x64, 0x30)
        device.write_reg(0x31, 0x64, 0xB0)
        device.write_reg(0x31, 0x64, 0x30)
        device.write_reg(0x31, 0x63, 0x30)
        device.write_reg(0x31, 0x64, 0xB0)
        device.write_reg(0x31, 0x63, 0x20)
        device.write_reg(0x31, 0x64, 0x30)
        device.write_reg(0x31, 0x64, 0xB0)
        device.write_reg(0x31, 0x64, 0x30)
        device.write_reg(0x31, 0x63, 0x30)
        device.write_reg(0x31, 0x64, 0xB0)

    def func_03_02_PIPE_dp1_Tx_Rx_PRBS(self):
        """03-02 PIPE-dp1 Tx/Rx PRBS"""
        print("Cfg func_03_02_PIPE_dp1_Tx_Rx_PRBS...")
        device = self._get_device()
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x05, 0x4F)
        device.write_reg(0x32, 0x05, 0x4F)
        device.write_reg(0x32, 0x05, 0x4F)
        device.write_reg(0x32, 0x05, 0x4F)
        device.write_reg(0x32, 0x05, 0x4F)
        device.write_reg(0x32, 0x05, 0x4F)
        device.write_reg(0x32, 0x05, 0x4F)
        device.write_reg(0x32, 0x05, 0x4F)
        device.write_reg(0x32, 0x05, 0x4F)
        device.write_reg(0x32, 0x05, 0x4F)
        device.write_reg(0x32, 0x0A, 0x10)
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0x0A, 0x10)
        device.write_reg(0x32, 0x08, 0x80)
        device.write_reg(0x32, 0x08, 0x80)
        device.write_reg(0x32, 0x08, 0x80)
        device.write_reg(0x32, 0x08, 0x80)
        device.write_reg(0x32, 0x08, 0x80)
        device.write_reg(0x32, 0x08, 0x80)
        device.write_reg(0x32, 0x0A, 0x10)
        device.write_reg(0x32, 0x09, 0x00)
        device.write_reg(0x32, 0xE5, 0xFF)
        device.write_reg(0x32, 0xE5, 0xFF)
        device.write_reg(0x32, 0xE5, 0xFF)
        device.write_reg(0x32, 0xE5, 0xFF)
        device.write_reg(0x32, 0xE5, 0xFF)
        device.write_reg(0x32, 0xE5, 0xFF)
        device.write_reg(0x32, 0xE5, 0xFF)
        device.write_reg(0x32, 0xE5, 0xFF)
        device.write_reg(0x32, 0xFF, 0x0E)
        device.write_reg(0x32, 0xFF, 0x0E)
        device.write_reg(0x32, 0xE6, 0x80)
        device.write_reg(0x32, 0xE6, 0x80)
        device.write_reg(0x32, 0xFF, 0x0E)
        device.write_reg(0x32, 0xFF, 0x0E)
        device.write_reg(0x32, 0x19, 0xC0)
        device.write_reg(0x32, 0x19, 0x80)
        device.write_reg(0x32, 0x19, 0x80)
        device.write_reg(0x32, 0x19, 0x80)
        device.write_reg(0x32, 0x1C, 0x26)
        device.write_reg(0x32, 0x1C, 0x26)
        device.write_reg(0x32, 0x19, 0x80)
        device.write_reg(0x32, 0x1E, 0x00)
        device.write_reg(0x32, 0x0E, 0x4F)
        device.write_reg(0x32, 0x0E, 0x4F)
        device.write_reg(0x32, 0x0E, 0x4F)
        device.write_reg(0x32, 0x0E, 0x4F)
        device.write_reg(0x32, 0x0E, 0x4F)
        device.write_reg(0x32, 0x0E, 0x4F)
        device.write_reg(0x32, 0x0E, 0x4F)
        device.write_reg(0x32, 0x0E, 0x4F)
        device.write_reg(0x32, 0x0E, 0x4F)
        device.write_reg(0x32, 0x0E, 0x4F)
        device.write_reg(0x32, 0x0F, 0x64)
        device.write_reg(0x32, 0x0F, 0x64)
        device.write_reg(0x32, 0x0F, 0x64)
        device.write_reg(0x32, 0x0F, 0x64)
        device.write_reg(0x32, 0x0F, 0x64)
        device.write_reg(0x32, 0x0E, 0x4F)
        device.write_reg(0x32, 0x0E, 0x4F)
        device.write_reg(0x32, 0x1E, 0x00)
        device.write_reg(0x32, 0x1E, 0x00)
        device.write_reg(0x32, 0x1E, 0x08)
        device.write_reg(0x32, 0x1E, 0x0C)
        device.write_reg(0x32, 0x1E, 0x08)
        device.write_reg(0x32, 0x1E, 0x00)
        device.write_reg(0x32, 0x19, 0xC0)
        device.write_reg(0x32, 0x0D, 0x60)
        device.write_reg(0x32, 0x0D, 0x60)
        device.write_reg(0x32, 0x0D, 0x60)
        device.write_reg(0x32, 0x0D, 0x60)
        device.write_reg(0x32, 0x10, 0x0C)
        device.write_reg(0x32, 0x10, 0x0C)
        device.write_reg(0x32, 0x64, 0xB0)
        device.write_reg(0x32, 0x63, 0x30)
        device.write_reg(0x32, 0x63, 0x30)
        device.write_reg(0x32, 0x63, 0x30)
        device.write_reg(0x32, 0x64, 0xB0)
        device.write_reg(0x32, 0x64, 0xB0)
        device.write_reg(0x32, 0x63, 0x20)
        device.write_reg(0x32, 0x64, 0x30)
        device.write_reg(0x32, 0x64, 0xB0)
        device.write_reg(0x32, 0x64, 0x30)
        device.write_reg(0x32, 0x63, 0x30)
        device.write_reg(0x32, 0x64, 0xB0)
        device.write_reg(0x32, 0x63, 0x20)
        device.write_reg(0x32, 0x64, 0x30)
        device.write_reg(0x32, 0x64, 0xB0)
        device.write_reg(0x32, 0x64, 0x30)
        device.write_reg(0x32, 0x63, 0x30)
        device.write_reg(0x32, 0x64, 0xB0)

    def func_03_03_PIPE_dp2_Tx_Rx_PRBS(self):
        """03-03 PIPE-dp2 Tx/Rx PRBS"""
        print("Cfg func_03_03_PIPE_dp2_Tx_Rx_PRBS...")
        device = self._get_device()
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x05, 0x4F)
        device.write_reg(0x33, 0x05, 0x4F)
        device.write_reg(0x33, 0x05, 0x4F)
        device.write_reg(0x33, 0x05, 0x4F)
        device.write_reg(0x33, 0x05, 0x4F)
        device.write_reg(0x33, 0x05, 0x4F)
        device.write_reg(0x33, 0x05, 0x4F)
        device.write_reg(0x33, 0x05, 0x4F)
        device.write_reg(0x33, 0x05, 0x4F)
        device.write_reg(0x33, 0x05, 0x4F)
        device.write_reg(0x33, 0x0A, 0x10)
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0x0A, 0x10)
        device.write_reg(0x33, 0x08, 0x80)
        device.write_reg(0x33, 0x08, 0x80)
        device.write_reg(0x33, 0x08, 0x80)
        device.write_reg(0x33, 0x08, 0x80)
        device.write_reg(0x33, 0x08, 0x80)
        device.write_reg(0x33, 0x08, 0x80)
        device.write_reg(0x33, 0x0A, 0x10)
        device.write_reg(0x33, 0x09, 0x00)
        device.write_reg(0x33, 0xE5, 0xFF)
        device.write_reg(0x33, 0xE5, 0xFF)
        device.write_reg(0x33, 0xE5, 0xFF)
        device.write_reg(0x33, 0xE5, 0xFF)
        device.write_reg(0x33, 0xE5, 0xFF)
        device.write_reg(0x33, 0xE5, 0xFF)
        device.write_reg(0x33, 0xE5, 0xFF)
        device.write_reg(0x33, 0xE5, 0xFF)
        device.write_reg(0x33, 0xFF, 0x0E)
        device.write_reg(0x33, 0xFF, 0x0E)
        device.write_reg(0x33, 0xE6, 0x80)
        device.write_reg(0x33, 0xE6, 0x80)
        device.write_reg(0x33, 0xFF, 0x0E)
        device.write_reg(0x33, 0xFF, 0x0E)
        device.write_reg(0x33, 0x19, 0xC0)
        device.write_reg(0x33, 0x19, 0x80)
        device.write_reg(0x33, 0x19, 0x80)
        device.write_reg(0x33, 0x19, 0x80)
        device.write_reg(0x33, 0x1C, 0x26)
        device.write_reg(0x33, 0x1C, 0x26)
        device.write_reg(0x33, 0x19, 0x80)
        device.write_reg(0x33, 0x1E, 0x00)
        device.write_reg(0x33, 0x0E, 0x4F)
        device.write_reg(0x33, 0x0E, 0x4F)
        device.write_reg(0x33, 0x0E, 0x4F)
        device.write_reg(0x33, 0x0E, 0x4F)
        device.write_reg(0x33, 0x0E, 0x4F)
        device.write_reg(0x33, 0x0E, 0x4F)
        device.write_reg(0x33, 0x0E, 0x4F)
        device.write_reg(0x33, 0x0E, 0x4F)
        device.write_reg(0x33, 0x0E, 0x4F)
        device.write_reg(0x33, 0x0E, 0x4F)
        device.write_reg(0x33, 0x0F, 0x64)
        device.write_reg(0x33, 0x0F, 0x64)
        device.write_reg(0x33, 0x0F, 0x64)
        device.write_reg(0x33, 0x0F, 0x64)
        device.write_reg(0x33, 0x0F, 0x64)
        device.write_reg(0x33, 0x0E, 0x4F)
        device.write_reg(0x33, 0x0E, 0x4F)
        device.write_reg(0x33, 0x1E, 0x00)
        device.write_reg(0x33, 0x1E, 0x00)
        device.write_reg(0x33, 0x1E, 0x08)
        device.write_reg(0x33, 0x1E, 0x0C)
        device.write_reg(0x33, 0x1E, 0x08)
        device.write_reg(0x33, 0x1E, 0x00)
        device.write_reg(0x33, 0x19, 0xC0)
        device.write_reg(0x33, 0x0D, 0x60)
        device.write_reg(0x33, 0x0D, 0x60)
        device.write_reg(0x33, 0x0D, 0x60)
        device.write_reg(0x33, 0x0D, 0x60)
        device.write_reg(0x33, 0x10, 0x0C)
        device.write_reg(0x33, 0x10, 0x0C)
        device.write_reg(0x33, 0x64, 0xB0)
        device.write_reg(0x33, 0x63, 0x30)
        device.write_reg(0x33, 0x63, 0x30)
        device.write_reg(0x33, 0x63, 0x30)
        device.write_reg(0x33, 0x64, 0xB0)
        device.write_reg(0x33, 0x64, 0xB0)
        device.write_reg(0x33, 0x63, 0x20)
        device.write_reg(0x33, 0x64, 0x30)
        device.write_reg(0x33, 0x64, 0xB0)
        device.write_reg(0x33, 0x64, 0x30)
        device.write_reg(0x33, 0x63, 0x30)
        device.write_reg(0x33, 0x64, 0xB0)
        device.write_reg(0x33, 0x63, 0x20)
        device.write_reg(0x33, 0x64, 0x30)
        device.write_reg(0x33, 0x64, 0xB0)
        device.write_reg(0x33, 0x64, 0x30)
        device.write_reg(0x33, 0x63, 0x30)
        device.write_reg(0x33, 0x64, 0xB0)

    def func_03_04_PIPE_dp3_Tx_Rx_PRBS(self):
        """03-04 PIPE-dp3 Tx/Rx PRBS"""
        print("Cfg func_03_04_PIPE_dp3_Tx_Rx_PRBS...")
        device = self._get_device()
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x05, 0x4F)
        device.write_reg(0x34, 0x05, 0x4F)
        device.write_reg(0x34, 0x05, 0x4F)
        device.write_reg(0x34, 0x05, 0x4F)
        device.write_reg(0x34, 0x05, 0x4F)
        device.write_reg(0x34, 0x05, 0x4F)
        device.write_reg(0x34, 0x05, 0x4F)
        device.write_reg(0x34, 0x05, 0x4F)
        device.write_reg(0x34, 0x05, 0x4F)
        device.write_reg(0x34, 0x05, 0x4F)
        device.write_reg(0x34, 0x0A, 0x10)
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0x0A, 0x10)
        device.write_reg(0x34, 0x08, 0x80)
        device.write_reg(0x34, 0x08, 0x80)
        device.write_reg(0x34, 0x08, 0x80)
        device.write_reg(0x34, 0x08, 0x80)
        device.write_reg(0x34, 0x08, 0x80)
        device.write_reg(0x34, 0x08, 0x80)
        device.write_reg(0x34, 0x0A, 0x10)
        device.write_reg(0x34, 0x09, 0x00)
        device.write_reg(0x34, 0xE5, 0xFF)
        device.write_reg(0x34, 0xE5, 0xFF)
        device.write_reg(0x34, 0xE5, 0xFF)
        device.write_reg(0x34, 0xE5, 0xFF)
        device.write_reg(0x34, 0xE5, 0xFF)
        device.write_reg(0x34, 0xE5, 0xFF)
        device.write_reg(0x34, 0xE5, 0xFF)
        device.write_reg(0x34, 0xE5, 0xFF)
        device.write_reg(0x34, 0xFF, 0x0E)
        device.write_reg(0x34, 0xFF, 0x0E)
        device.write_reg(0x34, 0xE6, 0x80)
        device.write_reg(0x34, 0xE6, 0x80)
        device.write_reg(0x34, 0xFF, 0x0E)
        device.write_reg(0x34, 0xFF, 0x0E)
        device.write_reg(0x34, 0x19, 0xC0)
        device.write_reg(0x34, 0x19, 0x80)
        device.write_reg(0x34, 0x19, 0x80)
        device.write_reg(0x34, 0x19, 0x80)
        device.write_reg(0x34, 0x1C, 0x26)
        device.write_reg(0x34, 0x1C, 0x26)
        device.write_reg(0x34, 0x19, 0x80)
        device.write_reg(0x34, 0x1E, 0x00)
        device.write_reg(0x34, 0x0E, 0x4F)
        device.write_reg(0x34, 0x0E, 0x4F)
        device.write_reg(0x34, 0x0E, 0x4F)
        device.write_reg(0x34, 0x0E, 0x4F)
        device.write_reg(0x34, 0x0E, 0x4F)
        device.write_reg(0x34, 0x0E, 0x4F)
        device.write_reg(0x34, 0x0E, 0x4F)
        device.write_reg(0x34, 0x0E, 0x4F)
        device.write_reg(0x34, 0x0E, 0x4F)
        device.write_reg(0x34, 0x0E, 0x4F)
        device.write_reg(0x34, 0x0F, 0x64)
        device.write_reg(0x34, 0x0F, 0x64)
        device.write_reg(0x34, 0x0F, 0x64)
        device.write_reg(0x34, 0x0F, 0x64)
        device.write_reg(0x34, 0x0F, 0x64)
        device.write_reg(0x34, 0x0E, 0x4F)
        device.write_reg(0x34, 0x0E, 0x4F)
        device.write_reg(0x34, 0x1E, 0x00)
        device.write_reg(0x34, 0x1E, 0x00)
        device.write_reg(0x34, 0x1E, 0x08)
        device.write_reg(0x34, 0x1E, 0x0C)
        device.write_reg(0x34, 0x1E, 0x08)
        device.write_reg(0x34, 0x1E, 0x00)
        device.write_reg(0x34, 0x19, 0xC0)
        device.write_reg(0x34, 0x0D, 0x60)
        device.write_reg(0x34, 0x0D, 0x60)
        device.write_reg(0x34, 0x0D, 0x60)
        device.write_reg(0x34, 0x0D, 0x60)
        device.write_reg(0x34, 0x10, 0x0C)
        device.write_reg(0x34, 0x10, 0x0C)
        device.write_reg(0x34, 0x64, 0xB0)
        device.write_reg(0x34, 0x63, 0x30)
        device.write_reg(0x34, 0x63, 0x30)
        device.write_reg(0x34, 0x63, 0x30)
        device.write_reg(0x34, 0x64, 0xB0)
        device.write_reg(0x34, 0x64, 0xB0)
        device.write_reg(0x34, 0x63, 0x20)
        device.write_reg(0x34, 0x64, 0x30)
        device.write_reg(0x34, 0x64, 0xB0)
        device.write_reg(0x34, 0x64, 0x30)
        device.write_reg(0x34, 0x63, 0x30)
        device.write_reg(0x34, 0x64, 0xB0)
        device.write_reg(0x34, 0x63, 0x20)
        device.write_reg(0x34, 0x64, 0x30)
        device.write_reg(0x34, 0x64, 0xB0)
        device.write_reg(0x34, 0x64, 0x30)
        device.write_reg(0x34, 0x63, 0x30)
        device.write_reg(0x34, 0x64, 0xB0)

    def func_03_05_PIPE_dp4_Tx_Rx_PRBS(self):
        """03-05 PIPE-dp4 Tx/Rx PRBS"""
        print("Cfg func_03_05_PIPE_dp4_Tx_Rx_PRBS...")
        device = self._get_device()
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x05, 0x4F)
        device.write_reg(0x35, 0x05, 0x4F)
        device.write_reg(0x35, 0x05, 0x4F)
        device.write_reg(0x35, 0x05, 0x4F)
        device.write_reg(0x35, 0x05, 0x4F)
        device.write_reg(0x35, 0x05, 0x4F)
        device.write_reg(0x35, 0x05, 0x4F)
        device.write_reg(0x35, 0x05, 0x4F)
        device.write_reg(0x35, 0x05, 0x4F)
        device.write_reg(0x35, 0x05, 0x4F)
        device.write_reg(0x35, 0x0A, 0x10)
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0x0A, 0x10)
        device.write_reg(0x35, 0x08, 0x80)
        device.write_reg(0x35, 0x08, 0x80)
        device.write_reg(0x35, 0x08, 0x80)
        device.write_reg(0x35, 0x08, 0x80)
        device.write_reg(0x35, 0x08, 0x80)
        device.write_reg(0x35, 0x08, 0x80)
        device.write_reg(0x35, 0x0A, 0x10)
        device.write_reg(0x35, 0x09, 0x00)
        device.write_reg(0x35, 0xE5, 0xFF)
        device.write_reg(0x35, 0xE5, 0xFF)
        device.write_reg(0x35, 0xE5, 0xFF)
        device.write_reg(0x35, 0xE5, 0xFF)
        device.write_reg(0x35, 0xE5, 0xFF)
        device.write_reg(0x35, 0xE5, 0xFF)
        device.write_reg(0x35, 0xE5, 0xFF)
        device.write_reg(0x35, 0xE5, 0xFF)
        device.write_reg(0x35, 0xFF, 0x0E)
        device.write_reg(0x35, 0xFF, 0x0E)
        device.write_reg(0x35, 0xE6, 0x80)
        device.write_reg(0x35, 0xE6, 0x80)
        device.write_reg(0x35, 0xFF, 0x0E)
        device.write_reg(0x35, 0xFF, 0x0E)
        device.write_reg(0x35, 0x19, 0xC0)
        device.write_reg(0x35, 0x19, 0x80)
        device.write_reg(0x35, 0x19, 0x80)
        device.write_reg(0x35, 0x19, 0x80)
        device.write_reg(0x35, 0x1C, 0x26)
        device.write_reg(0x35, 0x1C, 0x26)
        device.write_reg(0x35, 0x19, 0x80)
        device.write_reg(0x35, 0x1E, 0x00)
        device.write_reg(0x35, 0x0E, 0x4F)
        device.write_reg(0x35, 0x0E, 0x4F)
        device.write_reg(0x35, 0x0E, 0x4F)
        device.write_reg(0x35, 0x0E, 0x4F)
        device.write_reg(0x35, 0x0E, 0x4F)
        device.write_reg(0x35, 0x0E, 0x4F)
        device.write_reg(0x35, 0x0E, 0x4F)
        device.write_reg(0x35, 0x0E, 0x4F)
        device.write_reg(0x35, 0x0E, 0x4F)
        device.write_reg(0x35, 0x0E, 0x4F)
        device.write_reg(0x35, 0x0F, 0x64)
        device.write_reg(0x35, 0x0F, 0x64)
        device.write_reg(0x35, 0x0F, 0x64)
        device.write_reg(0x35, 0x0F, 0x64)
        device.write_reg(0x35, 0x0F, 0x64)
        device.write_reg(0x35, 0x0E, 0x4F)
        device.write_reg(0x35, 0x0E, 0x4F)
        device.write_reg(0x35, 0x1E, 0x00)
        device.write_reg(0x35, 0x1E, 0x00)
        device.write_reg(0x35, 0x1E, 0x08)
        device.write_reg(0x35, 0x1E, 0x0C)
        device.write_reg(0x35, 0x1E, 0x08)
        device.write_reg(0x35, 0x1E, 0x00)
        device.write_reg(0x35, 0x19, 0xC0)
        device.write_reg(0x35, 0x0D, 0x60)
        device.write_reg(0x35, 0x0D, 0x60)
        device.write_reg(0x35, 0x0D, 0x60)
        device.write_reg(0x35, 0x0D, 0x60)
        device.write_reg(0x35, 0x10, 0x0C)
        device.write_reg(0x35, 0x10, 0x0C)
        device.write_reg(0x35, 0x64, 0xB0)
        device.write_reg(0x35, 0x63, 0x30)
        device.write_reg(0x35, 0x63, 0x30)
        device.write_reg(0x35, 0x63, 0x30)
        device.write_reg(0x35, 0x64, 0xB0)
        device.write_reg(0x35, 0x64, 0xB0)
        device.write_reg(0x35, 0x63, 0x20)
        device.write_reg(0x35, 0x64, 0x30)
        device.write_reg(0x35, 0x64, 0xB0)
        device.write_reg(0x35, 0x64, 0x30)
        device.write_reg(0x35, 0x63, 0x30)
        device.write_reg(0x35, 0x64, 0xB0)
        device.write_reg(0x35, 0x63, 0x20)
        device.write_reg(0x35, 0x64, 0x30)
        device.write_reg(0x35, 0x64, 0xB0)
        device.write_reg(0x35, 0x64, 0x30)
        device.write_reg(0x35, 0x63, 0x30)
        device.write_reg(0x35, 0x64, 0xB0)

    def func_03_06_PIPE_up_Tx_Rx_LFPS(self):
        """03-06 PIPE-up Tx/Rx LFPS"""
        print("Cfg func_03_06_PIPE_up_Tx_Rx_LFPS...")
        device = self._get_device()
        device.write_reg(0x31, 0x07, 0x40)
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0x06, 0x01)
        device.write_reg(0x31, 0x06, 0x03)
        device.write_reg(0x31, 0x06, 0x07)
        device.write_reg(0x31, 0x06, 0x0F)
        device.write_reg(0x31, 0x06, 0x1F)
        device.write_reg(0x31, 0x06, 0x3F)
        device.write_reg(0x31, 0x06, 0x7F)
        device.write_reg(0x31, 0x06, 0xFF)
        device.write_reg(0x31, 0x05, 0x01)
        device.write_reg(0x31, 0x05, 0x03)
        device.write_reg(0x31, 0x05, 0x07)
        device.write_reg(0x31, 0x05, 0x0F)
        device.write_reg(0x31, 0x05, 0x4F)
        device.write_reg(0x31, 0x0A, 0x10)
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0x0A, 0x10)
        device.write_reg(0x31, 0x08, 0x80)
        device.write_reg(0x31, 0x08, 0x80)
        device.write_reg(0x31, 0x08, 0x80)
        device.write_reg(0x31, 0x08, 0x80)
        device.write_reg(0x31, 0x08, 0x80)
        device.write_reg(0x31, 0x08, 0x80)
        device.write_reg(0x31, 0x0A, 0x10)
        device.write_reg(0x31, 0x09, 0x00)
        device.write_reg(0x31, 0x07, 0xC0)
        device.write_reg(0x31, 0xE5, 0x20)
        device.write_reg(0x31, 0xE5, 0x30)
        device.write_reg(0x31, 0xE5, 0x38)
        device.write_reg(0x31, 0xE5, 0x3C)
        device.write_reg(0x31, 0xE5, 0x3E)
        device.write_reg(0x31, 0xE5, 0x3F)
        device.write_reg(0x31, 0xE5, 0xBF)
        device.write_reg(0x31, 0xE5, 0xFF)
        device.write_reg(0x31, 0xFF, 0x08)
        device.write_reg(0x31, 0xFF, 0x0C)
        device.write_reg(0x31, 0xE6, 0x80)
        device.write_reg(0x31, 0xE6, 0x80)
        device.write_reg(0x31, 0xFF, 0x0E)
        device.write_reg(0x31, 0xFF, 0x0E)
        device.write_reg(0x31, 0xE6, 0x80)
        device.write_reg(0x31, 0xE6, 0x80)
        device.write_reg(0x31, 0x14, 0x90)
        device.write_reg(0x31, 0x14, 0x90)
        device.write_reg(0x31, 0x21, 0x9F)
        device.write_reg(0x31, 0x22, 0xFF)
        device.write_reg(0x31, 0x26, 0x7F)
        device.write_reg(0x31, 0x27, 0xFC)
        device.write_reg(0x31, 0x25, 0x00)
        device.write_reg(0x31, 0x26, 0x3F)
        device.write_reg(0x31, 0x23, 0x00)
        device.write_reg(0x31, 0x24, 0xFA)
        device.write_reg(0x31, 0x15, 0x80)
        device.write_reg(0x31, 0x15, 0xC0)
        device.write_reg(0x31, 0x13, 0x04)
        device.write_reg(0x31, 0x13, 0x04)
        device.write_reg(0x31, 0x14, 0x90)
        device.write_reg(0x31, 0x14, 0x90)
        device.write_reg(0x31, 0x2C, 0x00)
        device.write_reg(0x31, 0x2C, 0x00)
        device.write_reg(0x31, 0x0E, 0x01)
        device.write_reg(0x31, 0x0E, 0x03)
        device.write_reg(0x31, 0x0E, 0x07)
        device.write_reg(0x31, 0x0E, 0x0F)
        device.write_reg(0x31, 0x0E, 0x4F)
        device.write_reg(0x31, 0x0F, 0x00)
        device.write_reg(0x31, 0x0F, 0x40)
        device.write_reg(0x31, 0x0F, 0x60)
        device.write_reg(0x31, 0x0F, 0x70)
        device.write_reg(0x31, 0x0F, 0x70)
        device.write_reg(0x31, 0x14, 0xD0)
        device.write_reg(0x31, 0xFF, 0x0E)
        device.write_reg(0x31, 0xFF, 0x0E)
        device.write_reg(0x31, 0x51, 0x0D)
        device.write_reg(0x31, 0x51, 0x00)
        device.write_reg(0x31, 0x52, 0x4F)
        device.write_reg(0x31, 0x52, 0x4F)
        device.write_reg(0x31, 0x53, 0xAB)
        device.write_reg(0x31, 0x52, 0x47)
        device.write_reg(0x31, 0x56, 0x00)
        device.write_reg(0x31, 0x56, 0x00)
        device.write_reg(0x31, 0x56, 0x00)
        device.write_reg(0x31, 0x4F, 0x80)
        device.write_reg(0x31, 0x4F, 0xC0)
        device.write_reg(0x31, 0x63, 0x20)
        device.write_reg(0x31, 0x63, 0x20)
        device.write_reg(0x31, 0x0D, 0x20)
        device.write_reg(0x31, 0x0D, 0x30)
        device.write_reg(0x31, 0x0D, 0x70)
        device.write_reg(0x31, 0x10, 0x08)
        device.write_reg(0x31, 0x10, 0x18)
        device.write_reg(0x31, 0x10, 0x1C)
        device.write_reg(0x31, 0x63, 0x30)

    def func_03_07_PIPE_dp1_Tx_Rx_LFPS(self):
        """03-07 PIPE-dp1 Tx/Rx LFPS"""
        print("Cfg func_03_07_PIPE_dp1_Tx_Rx_LFPS...")
        device = self._get_device()
        device.write_reg(0x32, 0x07, 0x40)
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0x06, 0x01)
        device.write_reg(0x32, 0x06, 0x03)
        device.write_reg(0x32, 0x06, 0x07)
        device.write_reg(0x32, 0x06, 0x0F)
        device.write_reg(0x32, 0x06, 0x1F)
        device.write_reg(0x32, 0x06, 0x3F)
        device.write_reg(0x32, 0x06, 0x7F)
        device.write_reg(0x32, 0x06, 0xFF)
        device.write_reg(0x32, 0x05, 0x01)
        device.write_reg(0x32, 0x05, 0x03)
        device.write_reg(0x32, 0x05, 0x07)
        device.write_reg(0x32, 0x05, 0x0F)
        device.write_reg(0x32, 0x05, 0x4F)
        device.write_reg(0x32, 0x0A, 0x10)
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0x0A, 0x10)
        device.write_reg(0x32, 0x08, 0x80)
        device.write_reg(0x32, 0x08, 0x80)
        device.write_reg(0x32, 0x08, 0x80)
        device.write_reg(0x32, 0x08, 0x80)
        device.write_reg(0x32, 0x08, 0x80)
        device.write_reg(0x32, 0x08, 0x80)
        device.write_reg(0x32, 0x0A, 0x10)
        device.write_reg(0x32, 0x09, 0x00)
        device.write_reg(0x32, 0x07, 0xC0)
        device.write_reg(0x32, 0xE5, 0x20)
        device.write_reg(0x32, 0xE5, 0x30)
        device.write_reg(0x32, 0xE5, 0x38)
        device.write_reg(0x32, 0xE5, 0x3C)
        device.write_reg(0x32, 0xE5, 0x3E)
        device.write_reg(0x32, 0xE5, 0x3F)
        device.write_reg(0x32, 0xE5, 0xBF)
        device.write_reg(0x32, 0xE5, 0xFF)
        device.write_reg(0x32, 0xFF, 0x08)
        device.write_reg(0x32, 0xFF, 0x0C)
        device.write_reg(0x32, 0xE6, 0x80)
        device.write_reg(0x32, 0xE6, 0x80)
        device.write_reg(0x32, 0xFF, 0x0E)
        device.write_reg(0x32, 0xFF, 0x0E)
        device.write_reg(0x32, 0xE6, 0x80)
        device.write_reg(0x32, 0xE6, 0x80)
        device.write_reg(0x32, 0x14, 0x90)
        device.write_reg(0x32, 0x14, 0x90)
        device.write_reg(0x32, 0x21, 0x9F)
        device.write_reg(0x32, 0x22, 0xFF)
        device.write_reg(0x32, 0x26, 0x7F)
        device.write_reg(0x32, 0x27, 0xFC)
        device.write_reg(0x32, 0x25, 0x00)
        device.write_reg(0x32, 0x26, 0x3F)
        device.write_reg(0x32, 0x23, 0x00)
        device.write_reg(0x32, 0x24, 0xFA)
        device.write_reg(0x32, 0x15, 0x80)
        device.write_reg(0x32, 0x15, 0xC0)
        device.write_reg(0x32, 0x13, 0x04)
        device.write_reg(0x32, 0x13, 0x04)
        device.write_reg(0x32, 0x14, 0x90)
        device.write_reg(0x32, 0x14, 0x90)
        device.write_reg(0x32, 0x2C, 0x00)
        device.write_reg(0x32, 0x2C, 0x00)
        device.write_reg(0x32, 0x0E, 0x01)
        device.write_reg(0x32, 0x0E, 0x03)
        device.write_reg(0x32, 0x0E, 0x07)
        device.write_reg(0x32, 0x0E, 0x0F)
        device.write_reg(0x32, 0x0E, 0x4F)
        device.write_reg(0x32, 0x0F, 0x00)
        device.write_reg(0x32, 0x0F, 0x40)
        device.write_reg(0x32, 0x0F, 0x60)
        device.write_reg(0x32, 0x0F, 0x70)
        device.write_reg(0x32, 0x0F, 0x70)
        device.write_reg(0x32, 0x14, 0xD0)
        device.write_reg(0x32, 0xFF, 0x0E)
        device.write_reg(0x32, 0xFF, 0x0E)
        device.write_reg(0x32, 0x51, 0x0D)
        device.write_reg(0x32, 0x51, 0x00)
        device.write_reg(0x32, 0x52, 0x4F)
        device.write_reg(0x32, 0x52, 0x4F)
        device.write_reg(0x32, 0x53, 0xAB)
        device.write_reg(0x32, 0x52, 0x47)
        device.write_reg(0x32, 0x56, 0x00)
        device.write_reg(0x32, 0x56, 0x00)
        device.write_reg(0x32, 0x56, 0x00)
        device.write_reg(0x32, 0x4F, 0x80)
        device.write_reg(0x32, 0x4F, 0xC0)
        device.write_reg(0x32, 0x63, 0x20)
        device.write_reg(0x32, 0x63, 0x20)
        device.write_reg(0x32, 0x0D, 0x20)
        device.write_reg(0x32, 0x0D, 0x30)
        device.write_reg(0x32, 0x0D, 0x70)
        device.write_reg(0x32, 0x10, 0x08)
        device.write_reg(0x32, 0x10, 0x18)
        device.write_reg(0x32, 0x10, 0x1C)
        device.write_reg(0x32, 0x63, 0x30)

    def func_03_08_PIPE_dp2_Tx_Rx_LFPS(self):
        """03-08 PIPE-dp2 Tx/Rx LFPS"""
        print("Cfg func_03_08_PIPE_dp2_Tx_Rx_LFPS...")
        device = self._get_device()
        device.write_reg(0x33, 0x07, 0x40)
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0x06, 0x01)
        device.write_reg(0x33, 0x06, 0x03)
        device.write_reg(0x33, 0x06, 0x07)
        device.write_reg(0x33, 0x06, 0x0F)
        device.write_reg(0x33, 0x06, 0x1F)
        device.write_reg(0x33, 0x06, 0x3F)
        device.write_reg(0x33, 0x06, 0x7F)
        device.write_reg(0x33, 0x06, 0xFF)
        device.write_reg(0x33, 0x05, 0x01)
        device.write_reg(0x33, 0x05, 0x03)
        device.write_reg(0x33, 0x05, 0x07)
        device.write_reg(0x33, 0x05, 0x0F)
        device.write_reg(0x33, 0x05, 0x4F)
        device.write_reg(0x33, 0x0A, 0x10)
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0x0A, 0x10)
        device.write_reg(0x33, 0x08, 0x80)
        device.write_reg(0x33, 0x08, 0x80)
        device.write_reg(0x33, 0x08, 0x80)
        device.write_reg(0x33, 0x08, 0x80)
        device.write_reg(0x33, 0x08, 0x80)
        device.write_reg(0x33, 0x08, 0x80)
        device.write_reg(0x33, 0x0A, 0x10)
        device.write_reg(0x33, 0x09, 0x00)
        device.write_reg(0x33, 0x07, 0xC0)
        device.write_reg(0x33, 0xE5, 0x20)
        device.write_reg(0x33, 0xE5, 0x30)
        device.write_reg(0x33, 0xE5, 0x38)
        device.write_reg(0x33, 0xE5, 0x3C)
        device.write_reg(0x33, 0xE5, 0x3E)
        device.write_reg(0x33, 0xE5, 0x3F)
        device.write_reg(0x33, 0xE5, 0xBF)
        device.write_reg(0x33, 0xE5, 0xFF)
        device.write_reg(0x33, 0xFF, 0x08)
        device.write_reg(0x33, 0xFF, 0x0C)
        device.write_reg(0x33, 0xE6, 0x80)
        device.write_reg(0x33, 0xE6, 0x80)
        device.write_reg(0x33, 0xFF, 0x0E)
        device.write_reg(0x33, 0xFF, 0x0E)
        device.write_reg(0x33, 0xE6, 0x80)
        device.write_reg(0x33, 0xE6, 0x80)
        device.write_reg(0x33, 0x14, 0x90)
        device.write_reg(0x33, 0x14, 0x90)
        device.write_reg(0x33, 0x21, 0x9F)
        device.write_reg(0x33, 0x22, 0xFF)
        device.write_reg(0x33, 0x26, 0x7F)
        device.write_reg(0x33, 0x27, 0xFC)
        device.write_reg(0x33, 0x25, 0x00)
        device.write_reg(0x33, 0x26, 0x3F)
        device.write_reg(0x33, 0x23, 0x00)
        device.write_reg(0x33, 0x24, 0xFA)
        device.write_reg(0x33, 0x15, 0x80)
        device.write_reg(0x33, 0x15, 0xC0)
        device.write_reg(0x33, 0x13, 0x04)
        device.write_reg(0x33, 0x13, 0x04)
        device.write_reg(0x33, 0x14, 0x90)
        device.write_reg(0x33, 0x14, 0x90)
        device.write_reg(0x33, 0x2C, 0x00)
        device.write_reg(0x33, 0x2C, 0x00)
        device.write_reg(0x33, 0x0E, 0x01)
        device.write_reg(0x33, 0x0E, 0x03)
        device.write_reg(0x33, 0x0E, 0x07)
        device.write_reg(0x33, 0x0E, 0x0F)
        device.write_reg(0x33, 0x0E, 0x4F)
        device.write_reg(0x33, 0x0F, 0x00)
        device.write_reg(0x33, 0x0F, 0x40)
        device.write_reg(0x33, 0x0F, 0x60)
        device.write_reg(0x33, 0x0F, 0x70)
        device.write_reg(0x33, 0x0F, 0x70)
        device.write_reg(0x33, 0x14, 0xD0)
        device.write_reg(0x33, 0xFF, 0x0E)
        device.write_reg(0x33, 0xFF, 0x0E)
        device.write_reg(0x33, 0x51, 0x0D)
        device.write_reg(0x33, 0x51, 0x00)
        device.write_reg(0x33, 0x52, 0x4F)
        device.write_reg(0x33, 0x52, 0x4F)
        device.write_reg(0x33, 0x53, 0xAB)
        device.write_reg(0x33, 0x52, 0x47)
        device.write_reg(0x33, 0x56, 0x00)
        device.write_reg(0x33, 0x56, 0x00)
        device.write_reg(0x33, 0x56, 0x00)
        device.write_reg(0x33, 0x4F, 0x80)
        device.write_reg(0x33, 0x4F, 0xC0)
        device.write_reg(0x33, 0x63, 0x20)
        device.write_reg(0x33, 0x63, 0x20)
        device.write_reg(0x33, 0x0D, 0x20)
        device.write_reg(0x33, 0x0D, 0x30)
        device.write_reg(0x33, 0x0D, 0x70)
        device.write_reg(0x33, 0x10, 0x08)
        device.write_reg(0x33, 0x10, 0x18)
        device.write_reg(0x33, 0x10, 0x1C)
        device.write_reg(0x33, 0x63, 0x30)

    def func_03_09_PIPE_dp3_Tx_Rx_LFPS(self):
        """03-09 PIPE-dp3 Tx/Rx LFPS"""
        print("Cfg func_03_09_PIPE_dp3_Tx_Rx_LFPS...")
        device = self._get_device()
        device.write_reg(0x34, 0x07, 0x40)
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0x06, 0x01)
        device.write_reg(0x34, 0x06, 0x03)
        device.write_reg(0x34, 0x06, 0x07)
        device.write_reg(0x34, 0x06, 0x0F)
        device.write_reg(0x34, 0x06, 0x1F)
        device.write_reg(0x34, 0x06, 0x3F)
        device.write_reg(0x34, 0x06, 0x7F)
        device.write_reg(0x34, 0x06, 0xFF)
        device.write_reg(0x34, 0x05, 0x01)
        device.write_reg(0x34, 0x05, 0x03)
        device.write_reg(0x34, 0x05, 0x07)
        device.write_reg(0x34, 0x05, 0x0F)
        device.write_reg(0x34, 0x05, 0x4F)
        device.write_reg(0x34, 0x0A, 0x10)
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0x0A, 0x10)
        device.write_reg(0x34, 0x08, 0x80)
        device.write_reg(0x34, 0x08, 0x80)
        device.write_reg(0x34, 0x08, 0x80)
        device.write_reg(0x34, 0x08, 0x80)
        device.write_reg(0x34, 0x08, 0x80)
        device.write_reg(0x34, 0x08, 0x80)
        device.write_reg(0x34, 0x0A, 0x10)
        device.write_reg(0x34, 0x09, 0x00)
        device.write_reg(0x34, 0x07, 0xC0)
        device.write_reg(0x34, 0xE5, 0x20)
        device.write_reg(0x34, 0xE5, 0x30)
        device.write_reg(0x34, 0xE5, 0x38)
        device.write_reg(0x34, 0xE5, 0x3C)
        device.write_reg(0x34, 0xE5, 0x3E)
        device.write_reg(0x34, 0xE5, 0x3F)
        device.write_reg(0x34, 0xE5, 0xBF)
        device.write_reg(0x34, 0xE5, 0xFF)
        device.write_reg(0x34, 0xFF, 0x08)
        device.write_reg(0x34, 0xFF, 0x0C)
        device.write_reg(0x34, 0xE6, 0x80)
        device.write_reg(0x34, 0xE6, 0x80)
        device.write_reg(0x34, 0xFF, 0x0E)
        device.write_reg(0x34, 0xFF, 0x0E)
        device.write_reg(0x34, 0xE6, 0x80)
        device.write_reg(0x34, 0xE6, 0x80)
        device.write_reg(0x34, 0x14, 0x90)
        device.write_reg(0x34, 0x14, 0x90)
        device.write_reg(0x34, 0x21, 0x9F)
        device.write_reg(0x34, 0x22, 0xFF)
        device.write_reg(0x34, 0x26, 0x7F)
        device.write_reg(0x34, 0x27, 0xFC)
        device.write_reg(0x34, 0x25, 0x00)
        device.write_reg(0x34, 0x26, 0x3F)
        device.write_reg(0x34, 0x23, 0x00)
        device.write_reg(0x34, 0x24, 0xFA)
        device.write_reg(0x34, 0x15, 0x80)
        device.write_reg(0x34, 0x15, 0xC0)
        device.write_reg(0x34, 0x13, 0x04)
        device.write_reg(0x34, 0x13, 0x04)
        device.write_reg(0x34, 0x14, 0x90)
        device.write_reg(0x34, 0x14, 0x90)
        device.write_reg(0x34, 0x2C, 0x00)
        device.write_reg(0x34, 0x2C, 0x00)
        device.write_reg(0x34, 0x0E, 0x01)
        device.write_reg(0x34, 0x0E, 0x03)
        device.write_reg(0x34, 0x0E, 0x07)
        device.write_reg(0x34, 0x0E, 0x0F)
        device.write_reg(0x34, 0x0E, 0x4F)
        device.write_reg(0x34, 0x0F, 0x00)
        device.write_reg(0x34, 0x0F, 0x40)
        device.write_reg(0x34, 0x0F, 0x60)
        device.write_reg(0x34, 0x0F, 0x70)
        device.write_reg(0x34, 0x0F, 0x70)
        device.write_reg(0x34, 0x14, 0xD0)
        device.write_reg(0x34, 0xFF, 0x0E)
        device.write_reg(0x34, 0xFF, 0x0E)
        device.write_reg(0x34, 0x51, 0x0D)
        device.write_reg(0x34, 0x51, 0x00)
        device.write_reg(0x34, 0x52, 0x4F)
        device.write_reg(0x34, 0x52, 0x4F)
        device.write_reg(0x34, 0x53, 0xAB)
        device.write_reg(0x34, 0x52, 0x47)
        device.write_reg(0x34, 0x56, 0x00)
        device.write_reg(0x34, 0x56, 0x00)
        device.write_reg(0x34, 0x56, 0x00)
        device.write_reg(0x34, 0x4F, 0x80)
        device.write_reg(0x34, 0x4F, 0xC0)
        device.write_reg(0x34, 0x63, 0x20)
        device.write_reg(0x34, 0x63, 0x20)
        device.write_reg(0x34, 0x0D, 0x20)
        device.write_reg(0x34, 0x0D, 0x30)
        device.write_reg(0x34, 0x0D, 0x70)
        device.write_reg(0x34, 0x10, 0x08)
        device.write_reg(0x34, 0x10, 0x18)
        device.write_reg(0x34, 0x10, 0x1C)
        device.write_reg(0x34, 0x63, 0x30)

    def func_03_10_PIPE_dp4_Tx_Rx_LFPS(self):
        """03-10 PIPE-dp4 Tx/Rx LFPS"""
        print("Cfg func_03_10_PIPE_dp4_Tx_Rx_LFPS...")
        device = self._get_device()
        device.write_reg(0x35, 0x07, 0x40)
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0x06, 0x01)
        device.write_reg(0x35, 0x06, 0x03)
        device.write_reg(0x35, 0x06, 0x07)
        device.write_reg(0x35, 0x06, 0x0F)
        device.write_reg(0x35, 0x06, 0x1F)
        device.write_reg(0x35, 0x06, 0x3F)
        device.write_reg(0x35, 0x06, 0x7F)
        device.write_reg(0x35, 0x06, 0xFF)
        device.write_reg(0x35, 0x05, 0x01)
        device.write_reg(0x35, 0x05, 0x03)
        device.write_reg(0x35, 0x05, 0x07)
        device.write_reg(0x35, 0x05, 0x0F)
        device.write_reg(0x35, 0x05, 0x4F)
        device.write_reg(0x35, 0x0A, 0x10)
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0x0A, 0x10)
        device.write_reg(0x35, 0x08, 0x80)
        device.write_reg(0x35, 0x08, 0x80)
        device.write_reg(0x35, 0x08, 0x80)
        device.write_reg(0x35, 0x08, 0x80)
        device.write_reg(0x35, 0x08, 0x80)
        device.write_reg(0x35, 0x08, 0x80)
        device.write_reg(0x35, 0x0A, 0x10)
        device.write_reg(0x35, 0x09, 0x00)
        device.write_reg(0x35, 0x07, 0xC0)
        device.write_reg(0x35, 0xE5, 0x20)
        device.write_reg(0x35, 0xE5, 0x30)
        device.write_reg(0x35, 0xE5, 0x38)
        device.write_reg(0x35, 0xE5, 0x3C)
        device.write_reg(0x35, 0xE5, 0x3E)
        device.write_reg(0x35, 0xE5, 0x3F)
        device.write_reg(0x35, 0xE5, 0xBF)
        device.write_reg(0x35, 0xE5, 0xFF)
        device.write_reg(0x35, 0xFF, 0x08)
        device.write_reg(0x35, 0xFF, 0x0C)
        device.write_reg(0x35, 0xE6, 0x80)
        device.write_reg(0x35, 0xE6, 0x80)
        device.write_reg(0x35, 0xFF, 0x0E)
        device.write_reg(0x35, 0xFF, 0x0E)
        device.write_reg(0x35, 0xE6, 0x80)
        device.write_reg(0x35, 0xE6, 0x80)
        device.write_reg(0x35, 0x14, 0x90)
        device.write_reg(0x35, 0x14, 0x90)
        device.write_reg(0x35, 0x21, 0x9F)
        device.write_reg(0x35, 0x22, 0xFF)
        device.write_reg(0x35, 0x26, 0x7F)
        device.write_reg(0x35, 0x27, 0xFC)
        device.write_reg(0x35, 0x25, 0x00)
        device.write_reg(0x35, 0x26, 0x3F)
        device.write_reg(0x35, 0x23, 0x00)
        device.write_reg(0x35, 0x24, 0xFA)
        device.write_reg(0x35, 0x15, 0x80)
        device.write_reg(0x35, 0x15, 0xC0)
        device.write_reg(0x35, 0x13, 0x04)
        device.write_reg(0x35, 0x13, 0x04)
        device.write_reg(0x35, 0x14, 0x90)
        device.write_reg(0x35, 0x14, 0x90)
        device.write_reg(0x35, 0x2C, 0x00)
        device.write_reg(0x35, 0x2C, 0x00)
        device.write_reg(0x35, 0x0E, 0x01)
        device.write_reg(0x35, 0x0E, 0x03)
        device.write_reg(0x35, 0x0E, 0x07)
        device.write_reg(0x35, 0x0E, 0x0F)
        device.write_reg(0x35, 0x0E, 0x4F)
        device.write_reg(0x35, 0x0F, 0x00)
        device.write_reg(0x35, 0x0F, 0x40)
        device.write_reg(0x35, 0x0F, 0x60)
        device.write_reg(0x35, 0x0F, 0x70)
        device.write_reg(0x35, 0x0F, 0x70)
        device.write_reg(0x35, 0x14, 0xD0)
        device.write_reg(0x35, 0xFF, 0x0E)
        device.write_reg(0x35, 0xFF, 0x0E)
        device.write_reg(0x35, 0x51, 0x0D)
        device.write_reg(0x35, 0x51, 0x00)
        device.write_reg(0x35, 0x52, 0x4F)
        device.write_reg(0x35, 0x52, 0x4F)
        device.write_reg(0x35, 0x53, 0xAB)
        device.write_reg(0x35, 0x52, 0x47)
        device.write_reg(0x35, 0x56, 0x00)
        device.write_reg(0x35, 0x56, 0x00)
        device.write_reg(0x35, 0x56, 0x00)
        device.write_reg(0x35, 0x4F, 0x80)
        device.write_reg(0x35, 0x4F, 0xC0)
        device.write_reg(0x35, 0x63, 0x20)
        device.write_reg(0x35, 0x63, 0x20)
        device.write_reg(0x35, 0x0D, 0x20)
        device.write_reg(0x35, 0x0D, 0x30)
        device.write_reg(0x35, 0x0D, 0x70)
        device.write_reg(0x35, 0x10, 0x08)
        device.write_reg(0x35, 0x10, 0x18)
        device.write_reg(0x35, 0x10, 0x1C)
        device.write_reg(0x35, 0x63, 0x30)

    def func_03_11_PIPE_up_Tx_rxdetect(self):
        """03-11 PIPE-up Tx rxdetect"""
        print("Cfg func_03_11_PIPE_up_Tx_rxdetect...")
        device = self._get_device()
        device.write_reg(0x31, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x31, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x31, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x31, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x31, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x31, 0x07, 0x07)  # i2c_pipe_man[7:0],U0 tx lfps
        device.write_reg(0x31, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x31, 0x0C, 0x3F)  # i2c_ana_man_en[7:0],rtl ctrl rxdetect
        device.write_reg(0x31, 0x0D, 0x08)  # i2c_ana_man[12:8]
        device.write_reg(0x31, 0x0E, 0x00)  # i2c_ana_man[7:0] only rx term en
        device.write_reg(0x31, 0x34, 0xC3)  # man start {i2c_clk_rxdet_man_en,i2c_clk_rxdet_man,i2c_rxdet_man_en,i2c_rxdet_man_vrxdet_en,i2c_rxdet_man_vrxdet_sel,i2c_rxdet_rst_man_en,i2c_rxdet_start_man_en,i2c_rxdet_start_man} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_12_PIPE_dp1_Tx_rxdetect(self):
        """03-12 PIPE-dp1 Tx rxdetect"""
        print("Cfg func_03_12_PIPE_dp1_Tx_rxdetect...")
        device = self._get_device()
        device.write_reg(0x32, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x32, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x32, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x32, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x32, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x32, 0x07, 0x07)  # i2c_pipe_man[7:0],U0 tx lfps
        device.write_reg(0x32, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x32, 0x0C, 0x3F)  # i2c_ana_man_en[7:0],rtl ctrl rxdetect
        device.write_reg(0x32, 0x0D, 0x08)  # i2c_ana_man[12:8]
        device.write_reg(0x32, 0x0E, 0x00)  # i2c_ana_man[7:0] only rx term en
        device.write_reg(0x32, 0x34, 0xC3)  # man start {i2c_clk_rxdet_man_en,i2c_clk_rxdet_man,i2c_rxdet_man_en,i2c_rxdet_man_vrxdet_en,i2c_rxdet_man_vrxdet_sel,i2c_rxdet_rst_man_en,i2c_rxdet_start_man_en,i2c_rxdet_start_man} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_13_PIPE_dp2_Tx_rxdetect(self):
        """03-13 PIPE-dp2 Tx rxdetect"""
        print("Cfg func_03_13_PIPE_dp2_Tx_rxdetect...")
        device = self._get_device()
        device.write_reg(0x33, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x33, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x33, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x33, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x33, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x33, 0x07, 0x07)  # i2c_pipe_man[7:0],U0 tx lfps
        device.write_reg(0x33, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x33, 0x0C, 0x3F)  # i2c_ana_man_en[7:0],rtl ctrl rxdetect
        device.write_reg(0x33, 0x0D, 0x08)  # i2c_ana_man[12:8]
        device.write_reg(0x33, 0x0E, 0x00)  # i2c_ana_man[7:0] only rx term en
        device.write_reg(0x33, 0x34, 0xC3)  # man start {i2c_clk_rxdet_man_en,i2c_clk_rxdet_man,i2c_rxdet_man_en,i2c_rxdet_man_vrxdet_en,i2c_rxdet_man_vrxdet_sel,i2c_rxdet_rst_man_en,i2c_rxdet_start_man_en,i2c_rxdet_start_man} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_14_PIPE_dp3_Tx_rxdetect(self):
        """03-14 PIPE-dp3 Tx rxdetect"""
        print("Cfg func_03_14_PIPE_dp3_Tx_rxdetect...")
        device = self._get_device()
        device.write_reg(0x34, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x34, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x34, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x34, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x34, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x34, 0x07, 0x07)  # i2c_pipe_man[7:0],U0 tx lfps
        device.write_reg(0x34, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x34, 0x0C, 0x3F)  # i2c_ana_man_en[7:0],rtl ctrl rxdetect
        device.write_reg(0x34, 0x0D, 0x08)  # i2c_ana_man[12:8]
        device.write_reg(0x34, 0x0E, 0x00)  # i2c_ana_man[7:0] only rx term en
        device.write_reg(0x34, 0x34, 0xC3)  # man start {i2c_clk_rxdet_man_en,i2c_clk_rxdet_man,i2c_rxdet_man_en,i2c_rxdet_man_vrxdet_en,i2c_rxdet_man_vrxdet_sel,i2c_rxdet_rst_man_en,i2c_rxdet_start_man_en,i2c_rxdet_start_man} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_15_PIPE_dp4_Tx_rxdetect(self):
        """03-15 PIPE-dp4 Tx rxdetect"""
        print("Cfg func_03_15_PIPE_dp4_Tx_rxdetect...")
        device = self._get_device()
        device.write_reg(0x35, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x35, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x35, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x35, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x35, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x35, 0x07, 0x07)  # i2c_pipe_man[7:0],U0 tx lfps
        device.write_reg(0x35, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x35, 0x0C, 0x3F)  # i2c_ana_man_en[7:0],rtl ctrl rxdetect
        device.write_reg(0x35, 0x0D, 0x08)  # i2c_ana_man[12:8]
        device.write_reg(0x35, 0x0E, 0x00)  # i2c_ana_man[7:0] only rx term en
        device.write_reg(0x35, 0x34, 0xC3)  # man start {i2c_clk_rxdet_man_en,i2c_clk_rxdet_man,i2c_rxdet_man_en,i2c_rxdet_man_vrxdet_en,i2c_rxdet_man_vrxdet_sel,i2c_rxdet_rst_man_en,i2c_rxdet_start_man_en,i2c_rxdet_start_man} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_16_PIPE_up_Tx_Rx_20b_constant(self):
        """03-16 PIPE-up Tx/Rx 20b constant"""
        print("Cfg func_03_16_PIPE_up_Tx_Rx_20b_constant...")
        device = self._get_device()
        device.write_reg(0x31, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x31, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x31, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x31, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x31, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x31, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x31, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x31, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x31, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x31, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x31, 0x2F, 0x80)  # test en,sel constant,{i2c_tx_10b_test_en,i2c_tx_10b_test_sel[2],i2c_tx_10b_test_sel[1],i2c_tx_10b_test_sel[0],i2c_tx_10b_default_sel} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3]}
        device.write_reg(0x31, 0x19, 0x02)  # {i2c_clk_packet_8b_gen_man,i2c_tx_8b_test_packet_en,i2c_tx_8b_test_packet_max[10],i2c_tx_8b_test_packet_max[9],i2c_tx_8b_test_packet_max[8]} <= {dataIn[7],dataIn[6],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x31, 0x1A, 0xAA)  # CLK,01010,{i2c_tx_8b_test_packet_max[7],i2c_tx_8b_test_packet_max[6],i2c_tx_8b_test_packet_max[5],i2c_tx_8b_test_packet_max[4],i2c_tx_8b_test_packet_max[3],i2c_tx_8b_test_packet_max[2],i2c_tx_8b_test_packet_max[1],i2c_tx_8b_test_packet_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_17_PIPE_dp1_Tx_Rx_20b_constant(self):
        """03-17 PIPE-dp1 Tx/Rx 20b constant"""
        print("Cfg func_03_17_PIPE_dp1_Tx_Rx_20b_constant...")
        device = self._get_device()
        device.write_reg(0x32, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x32, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x32, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x32, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x32, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x32, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x32, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x32, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x32, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x32, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x32, 0x2F, 0x80)  # test en,sel constant,{i2c_tx_10b_test_en,i2c_tx_10b_test_sel[2],i2c_tx_10b_test_sel[1],i2c_tx_10b_test_sel[0],i2c_tx_10b_default_sel} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3]}
        device.write_reg(0x32, 0x19, 0x02)  # {i2c_clk_packet_8b_gen_man,i2c_tx_8b_test_packet_en,i2c_tx_8b_test_packet_max[10],i2c_tx_8b_test_packet_max[9],i2c_tx_8b_test_packet_max[8]} <= {dataIn[7],dataIn[6],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x32, 0x1A, 0xAA)  # CLK,01010,{i2c_tx_8b_test_packet_max[7],i2c_tx_8b_test_packet_max[6],i2c_tx_8b_test_packet_max[5],i2c_tx_8b_test_packet_max[4],i2c_tx_8b_test_packet_max[3],i2c_tx_8b_test_packet_max[2],i2c_tx_8b_test_packet_max[1],i2c_tx_8b_test_packet_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_18_PIPE_dp2_Tx_Rx_20b_constant(self):
        """03-18 PIPE-dp2 Tx/Rx 20b constant"""
        print("Cfg func_03_18_PIPE_dp2_Tx_Rx_20b_constant...")
        device = self._get_device()
        device.write_reg(0x33, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x33, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x33, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x33, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x33, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x33, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x33, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x33, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x33, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x33, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x33, 0x2F, 0x80)  # test en,sel constant,{i2c_tx_10b_test_en,i2c_tx_10b_test_sel[2],i2c_tx_10b_test_sel[1],i2c_tx_10b_test_sel[0],i2c_tx_10b_default_sel} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3]}
        device.write_reg(0x33, 0x19, 0x02)  # {i2c_clk_packet_8b_gen_man,i2c_tx_8b_test_packet_en,i2c_tx_8b_test_packet_max[10],i2c_tx_8b_test_packet_max[9],i2c_tx_8b_test_packet_max[8]} <= {dataIn[7],dataIn[6],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x33, 0x1A, 0xAA)  # CLK,01010,{i2c_tx_8b_test_packet_max[7],i2c_tx_8b_test_packet_max[6],i2c_tx_8b_test_packet_max[5],i2c_tx_8b_test_packet_max[4],i2c_tx_8b_test_packet_max[3],i2c_tx_8b_test_packet_max[2],i2c_tx_8b_test_packet_max[1],i2c_tx_8b_test_packet_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_19_PIPE_dp3_Tx_Rx_20b_constant(self):
        """03-19 PIPE-dp3 Tx/Rx 20b constant"""
        print("Cfg func_03_19_PIPE_dp3_Tx_Rx_20b_constant...")
        device = self._get_device()
        device.write_reg(0x34, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x34, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x34, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x34, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x34, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x34, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x34, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x34, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x34, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x34, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x34, 0x2F, 0x80)  # test en,sel constant,{i2c_tx_10b_test_en,i2c_tx_10b_test_sel[2],i2c_tx_10b_test_sel[1],i2c_tx_10b_test_sel[0],i2c_tx_10b_default_sel} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3]}
        device.write_reg(0x34, 0x19, 0x02)  # {i2c_clk_packet_8b_gen_man,i2c_tx_8b_test_packet_en,i2c_tx_8b_test_packet_max[10],i2c_tx_8b_test_packet_max[9],i2c_tx_8b_test_packet_max[8]} <= {dataIn[7],dataIn[6],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x34, 0x1A, 0xAA)  # CLK,01010,{i2c_tx_8b_test_packet_max[7],i2c_tx_8b_test_packet_max[6],i2c_tx_8b_test_packet_max[5],i2c_tx_8b_test_packet_max[4],i2c_tx_8b_test_packet_max[3],i2c_tx_8b_test_packet_max[2],i2c_tx_8b_test_packet_max[1],i2c_tx_8b_test_packet_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_20_PIPE_dp4_Tx_Rx_20b_constant(self):
        """03-20 PIPE-dp4 Tx/Rx 20b constant"""
        print("Cfg func_03_20_PIPE_dp4_Tx_Rx_20b_constant...")
        device = self._get_device()
        device.write_reg(0x35, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x35, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x35, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x35, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x35, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x35, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x35, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x35, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x35, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x35, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x35, 0x2F, 0x80)  # test en,sel constant,{i2c_tx_10b_test_en,i2c_tx_10b_test_sel[2],i2c_tx_10b_test_sel[1],i2c_tx_10b_test_sel[0],i2c_tx_10b_default_sel} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3]}
        device.write_reg(0x35, 0x19, 0x02)  # {i2c_clk_packet_8b_gen_man,i2c_tx_8b_test_packet_en,i2c_tx_8b_test_packet_max[10],i2c_tx_8b_test_packet_max[9],i2c_tx_8b_test_packet_max[8]} <= {dataIn[7],dataIn[6],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x35, 0x1A, 0xAA)  # CLK,01010,{i2c_tx_8b_test_packet_max[7],i2c_tx_8b_test_packet_max[6],i2c_tx_8b_test_packet_max[5],i2c_tx_8b_test_packet_max[4],i2c_tx_8b_test_packet_max[3],i2c_tx_8b_test_packet_max[2],i2c_tx_8b_test_packet_max[1],i2c_tx_8b_test_packet_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_21_PIPE_Up_tx8b_packet(self):
        """03-21 PIPE-Up tx8b packet"""
        print("Cfg func_03_21_PIPE_Up_tx8b_packet...")
        device = self._get_device()
        device.write_reg(0x31, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x31, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x31, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x31, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x31, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x31, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x31, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x31, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x31, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x31, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x31, 0x19, 0xC0)  # {i2c_clk_packet_8b_gen_man,i2c_tx_8b_test_packet_en,i2c_tx_8b_test_packet_max[10],i2c_tx_8b_test_packet_max[9],i2c_tx_8b_test_packet_max[8]} <= {dataIn[7],dataIn[6],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x31, 0x1A, 0xB5)  # {i2c_tx_8b_test_packet_max[7],i2c_tx_8b_test_packet_max[6],i2c_tx_8b_test_packet_max[5],i2c_tx_8b_test_packet_max[4],i2c_tx_8b_test_packet_max[3],i2c_tx_8b_test_packet_max[2],i2c_tx_8b_test_packet_max[1],i2c_tx_8b_test_packet_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x31, 0x1B, 0x20)  # {i2c_tx_8b_test_packet_com_num[3],i2c_tx_8b_test_packet_com_num[2],i2c_tx_8b_test_packet_com_num[1],i2c_tx_8b_test_packet_com_num[0],i2c_tx_8b_test_packet_com_time[10],i2c_tx_8b_test_packet_com_time[9],i2c_tx_8b_test_packet_com_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x31, 0x1C, 0x02)  # {i2c_tx_8b_test_packet_com_time[7],i2c_tx_8b_test_packet_com_time[6],i2c_tx_8b_test_packet_com_time[5],i2c_tx_8b_test_packet_com_time[4],i2c_tx_8b_test_packet_com_time[3],i2c_tx_8b_test_packet_com_time[2],i2c_tx_8b_test_packet_com_time[1],i2c_tx_8b_test_packet_com_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x31, 0x1D, 0x20)  # {i2c_tx_8b_test_packet_skp_num[3],i2c_tx_8b_test_packet_skp_num[2],i2c_tx_8b_test_packet_skp_num[1],i2c_tx_8b_test_packet_skp_num[0],i2c_tx_8b_test_packet_skp_time[10],i2c_tx_8b_test_packet_skp_time[9],i2c_tx_8b_test_packet_skp_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x31, 0x1E, 0xAA)  # {i2c_tx_8b_test_packet_skp_time[7],i2c_tx_8b_test_packet_skp_time[6],i2c_tx_8b_test_packet_skp_time[5],i2c_tx_8b_test_packet_skp_time[4],i2c_tx_8b_test_packet_skp_time[3],i2c_tx_8b_test_packet_skp_time[2],i2c_tx_8b_test_packet_skp_time[1],i2c_tx_8b_test_packet_skp_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x31, 0x1F, 0xB0)  # {i2c_tx_8b_test_en,i2c_tx_8b_test_sel[2],i2c_tx_8b_test_sel[1],i2c_tx_8b_test_sel[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4]}
        device.write_reg(0x31, 0xD1, 0xC0)  # {i2c_clk_packet_8b_pclk_check_man,i2c_rx_packet_8b_en,i2c_rx_packet_8b_err_cnt_clr} <= {dataIn[7],dataIn[6],dataIn[5]}
        device.write_reg(0x31, 0xD2, 0x00)  # {i2c_rx_packet_8b_max[10],i2c_rx_packet_8b_max[9],i2c_rx_packet_8b_max[8]} <= {dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x31, 0xD3, 0xB5)  # {i2c_rx_packet_8b_max[7],i2c_rx_packet_8b_max[6],i2c_rx_packet_8b_max[5],i2c_rx_packet_8b_max[4],i2c_rx_packet_8b_max[3],i2c_rx_packet_8b_max[2],i2c_rx_packet_8b_max[1],i2c_rx_packet_8b_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x31, 0xD4, 0x20)  # {i2c_rx_packet_8b_com_num[3],i2c_rx_packet_8b_com_num[2],i2c_rx_packet_8b_com_num[1],i2c_rx_packet_8b_com_num[0],i2c_rx_packet_8b_com_time[10],i2c_rx_packet_8b_com_time[9],i2c_rx_packet_8b_com_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x31, 0xD5, 0x02)  # {i2c_rx_packet_8b_com_time[7],i2c_rx_packet_8b_com_time[6],i2c_rx_packet_8b_com_time[5],i2c_rx_packet_8b_com_time[4],i2c_rx_packet_8b_com_time[3],i2c_rx_packet_8b_com_time[2],i2c_rx_packet_8b_com_time[1],i2c_rx_packet_8b_com_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_22_PIPE_dp1_tx8b_packet(self):
        """03-22 PIPE-dp1 tx8b packet"""
        print("Cfg func_03_22_PIPE_dp1_tx8b_packet...")
        device = self._get_device()
        device.write_reg(0x32, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x32, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x32, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x32, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x32, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x32, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x32, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x32, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x32, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x32, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x32, 0x19, 0xC0)  # {i2c_clk_packet_8b_gen_man,i2c_tx_8b_test_packet_en,i2c_tx_8b_test_packet_max[10],i2c_tx_8b_test_packet_max[9],i2c_tx_8b_test_packet_max[8]} <= {dataIn[7],dataIn[6],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x32, 0x1A, 0xB5)  # {i2c_tx_8b_test_packet_max[7],i2c_tx_8b_test_packet_max[6],i2c_tx_8b_test_packet_max[5],i2c_tx_8b_test_packet_max[4],i2c_tx_8b_test_packet_max[3],i2c_tx_8b_test_packet_max[2],i2c_tx_8b_test_packet_max[1],i2c_tx_8b_test_packet_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x32, 0x1B, 0x20)  # {i2c_tx_8b_test_packet_com_num[3],i2c_tx_8b_test_packet_com_num[2],i2c_tx_8b_test_packet_com_num[1],i2c_tx_8b_test_packet_com_num[0],i2c_tx_8b_test_packet_com_time[10],i2c_tx_8b_test_packet_com_time[9],i2c_tx_8b_test_packet_com_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x32, 0x1C, 0x02)  # {i2c_tx_8b_test_packet_com_time[7],i2c_tx_8b_test_packet_com_time[6],i2c_tx_8b_test_packet_com_time[5],i2c_tx_8b_test_packet_com_time[4],i2c_tx_8b_test_packet_com_time[3],i2c_tx_8b_test_packet_com_time[2],i2c_tx_8b_test_packet_com_time[1],i2c_tx_8b_test_packet_com_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x32, 0x1D, 0x20)  # {i2c_tx_8b_test_packet_skp_num[3],i2c_tx_8b_test_packet_skp_num[2],i2c_tx_8b_test_packet_skp_num[1],i2c_tx_8b_test_packet_skp_num[0],i2c_tx_8b_test_packet_skp_time[10],i2c_tx_8b_test_packet_skp_time[9],i2c_tx_8b_test_packet_skp_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x32, 0x1E, 0xAA)  # {i2c_tx_8b_test_packet_skp_time[7],i2c_tx_8b_test_packet_skp_time[6],i2c_tx_8b_test_packet_skp_time[5],i2c_tx_8b_test_packet_skp_time[4],i2c_tx_8b_test_packet_skp_time[3],i2c_tx_8b_test_packet_skp_time[2],i2c_tx_8b_test_packet_skp_time[1],i2c_tx_8b_test_packet_skp_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x32, 0x1F, 0xB0)  # {i2c_tx_8b_test_en,i2c_tx_8b_test_sel[2],i2c_tx_8b_test_sel[1],i2c_tx_8b_test_sel[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4]}
        device.write_reg(0x32, 0xD1, 0xC0)  # {i2c_clk_packet_8b_pclk_check_man,i2c_rx_packet_8b_en,i2c_rx_packet_8b_err_cnt_clr} <= {dataIn[7],dataIn[6],dataIn[5]}
        device.write_reg(0x32, 0xD2, 0x00)  # {i2c_rx_packet_8b_max[10],i2c_rx_packet_8b_max[9],i2c_rx_packet_8b_max[8]} <= {dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x32, 0xD3, 0xB5)  # {i2c_rx_packet_8b_max[7],i2c_rx_packet_8b_max[6],i2c_rx_packet_8b_max[5],i2c_rx_packet_8b_max[4],i2c_rx_packet_8b_max[3],i2c_rx_packet_8b_max[2],i2c_rx_packet_8b_max[1],i2c_rx_packet_8b_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x32, 0xD4, 0x20)  # {i2c_rx_packet_8b_com_num[3],i2c_rx_packet_8b_com_num[2],i2c_rx_packet_8b_com_num[1],i2c_rx_packet_8b_com_num[0],i2c_rx_packet_8b_com_time[10],i2c_rx_packet_8b_com_time[9],i2c_rx_packet_8b_com_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x32, 0xD5, 0x02)  # {i2c_rx_packet_8b_com_time[7],i2c_rx_packet_8b_com_time[6],i2c_rx_packet_8b_com_time[5],i2c_rx_packet_8b_com_time[4],i2c_rx_packet_8b_com_time[3],i2c_rx_packet_8b_com_time[2],i2c_rx_packet_8b_com_time[1],i2c_rx_packet_8b_com_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_23_PIPE_dp2_tx8b_packet(self):
        """03-23 PIPE-dp2 tx8b packet"""
        print("Cfg func_03_23_PIPE_dp2_tx8b_packet...")
        device = self._get_device()
        device.write_reg(0x33, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x33, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x33, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x33, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x33, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x33, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x33, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x33, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x33, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x33, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x33, 0x19, 0xC0)  # {i2c_clk_packet_8b_gen_man,i2c_tx_8b_test_packet_en,i2c_tx_8b_test_packet_max[10],i2c_tx_8b_test_packet_max[9],i2c_tx_8b_test_packet_max[8]} <= {dataIn[7],dataIn[6],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x33, 0x1A, 0xB5)  # {i2c_tx_8b_test_packet_max[7],i2c_tx_8b_test_packet_max[6],i2c_tx_8b_test_packet_max[5],i2c_tx_8b_test_packet_max[4],i2c_tx_8b_test_packet_max[3],i2c_tx_8b_test_packet_max[2],i2c_tx_8b_test_packet_max[1],i2c_tx_8b_test_packet_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x33, 0x1B, 0x20)  # {i2c_tx_8b_test_packet_com_num[3],i2c_tx_8b_test_packet_com_num[2],i2c_tx_8b_test_packet_com_num[1],i2c_tx_8b_test_packet_com_num[0],i2c_tx_8b_test_packet_com_time[10],i2c_tx_8b_test_packet_com_time[9],i2c_tx_8b_test_packet_com_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x33, 0x1C, 0x02)  # {i2c_tx_8b_test_packet_com_time[7],i2c_tx_8b_test_packet_com_time[6],i2c_tx_8b_test_packet_com_time[5],i2c_tx_8b_test_packet_com_time[4],i2c_tx_8b_test_packet_com_time[3],i2c_tx_8b_test_packet_com_time[2],i2c_tx_8b_test_packet_com_time[1],i2c_tx_8b_test_packet_com_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x33, 0x1D, 0x20)  # {i2c_tx_8b_test_packet_skp_num[3],i2c_tx_8b_test_packet_skp_num[2],i2c_tx_8b_test_packet_skp_num[1],i2c_tx_8b_test_packet_skp_num[0],i2c_tx_8b_test_packet_skp_time[10],i2c_tx_8b_test_packet_skp_time[9],i2c_tx_8b_test_packet_skp_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x33, 0x1E, 0xAA)  # {i2c_tx_8b_test_packet_skp_time[7],i2c_tx_8b_test_packet_skp_time[6],i2c_tx_8b_test_packet_skp_time[5],i2c_tx_8b_test_packet_skp_time[4],i2c_tx_8b_test_packet_skp_time[3],i2c_tx_8b_test_packet_skp_time[2],i2c_tx_8b_test_packet_skp_time[1],i2c_tx_8b_test_packet_skp_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x33, 0x1F, 0xB0)  # {i2c_tx_8b_test_en,i2c_tx_8b_test_sel[2],i2c_tx_8b_test_sel[1],i2c_tx_8b_test_sel[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4]}
        device.write_reg(0x33, 0xD1, 0xC0)  # {i2c_clk_packet_8b_pclk_check_man,i2c_rx_packet_8b_en,i2c_rx_packet_8b_err_cnt_clr} <= {dataIn[7],dataIn[6],dataIn[5]}
        device.write_reg(0x33, 0xD2, 0x00)  # {i2c_rx_packet_8b_max[10],i2c_rx_packet_8b_max[9],i2c_rx_packet_8b_max[8]} <= {dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x33, 0xD3, 0xB5)  # {i2c_rx_packet_8b_max[7],i2c_rx_packet_8b_max[6],i2c_rx_packet_8b_max[5],i2c_rx_packet_8b_max[4],i2c_rx_packet_8b_max[3],i2c_rx_packet_8b_max[2],i2c_rx_packet_8b_max[1],i2c_rx_packet_8b_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x33, 0xD4, 0x20)  # {i2c_rx_packet_8b_com_num[3],i2c_rx_packet_8b_com_num[2],i2c_rx_packet_8b_com_num[1],i2c_rx_packet_8b_com_num[0],i2c_rx_packet_8b_com_time[10],i2c_rx_packet_8b_com_time[9],i2c_rx_packet_8b_com_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x33, 0xD5, 0x02)  # {i2c_rx_packet_8b_com_time[7],i2c_rx_packet_8b_com_time[6],i2c_rx_packet_8b_com_time[5],i2c_rx_packet_8b_com_time[4],i2c_rx_packet_8b_com_time[3],i2c_rx_packet_8b_com_time[2],i2c_rx_packet_8b_com_time[1],i2c_rx_packet_8b_com_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_24_PIPE_dp3_tx8b_packet(self):
        """03-24 PIPE-dp3 tx8b packet"""
        print("Cfg func_03_24_PIPE_dp3_tx8b_packet...")
        device = self._get_device()
        device.write_reg(0x34, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x34, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x34, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x34, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x34, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x34, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x34, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x34, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x34, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x34, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x34, 0x19, 0xC0)  # {i2c_clk_packet_8b_gen_man,i2c_tx_8b_test_packet_en,i2c_tx_8b_test_packet_max[10],i2c_tx_8b_test_packet_max[9],i2c_tx_8b_test_packet_max[8]} <= {dataIn[7],dataIn[6],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x34, 0x1A, 0xB5)  # {i2c_tx_8b_test_packet_max[7],i2c_tx_8b_test_packet_max[6],i2c_tx_8b_test_packet_max[5],i2c_tx_8b_test_packet_max[4],i2c_tx_8b_test_packet_max[3],i2c_tx_8b_test_packet_max[2],i2c_tx_8b_test_packet_max[1],i2c_tx_8b_test_packet_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x34, 0x1B, 0x20)  # {i2c_tx_8b_test_packet_com_num[3],i2c_tx_8b_test_packet_com_num[2],i2c_tx_8b_test_packet_com_num[1],i2c_tx_8b_test_packet_com_num[0],i2c_tx_8b_test_packet_com_time[10],i2c_tx_8b_test_packet_com_time[9],i2c_tx_8b_test_packet_com_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x34, 0x1C, 0x02)  # {i2c_tx_8b_test_packet_com_time[7],i2c_tx_8b_test_packet_com_time[6],i2c_tx_8b_test_packet_com_time[5],i2c_tx_8b_test_packet_com_time[4],i2c_tx_8b_test_packet_com_time[3],i2c_tx_8b_test_packet_com_time[2],i2c_tx_8b_test_packet_com_time[1],i2c_tx_8b_test_packet_com_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x34, 0x1D, 0x20)  # {i2c_tx_8b_test_packet_skp_num[3],i2c_tx_8b_test_packet_skp_num[2],i2c_tx_8b_test_packet_skp_num[1],i2c_tx_8b_test_packet_skp_num[0],i2c_tx_8b_test_packet_skp_time[10],i2c_tx_8b_test_packet_skp_time[9],i2c_tx_8b_test_packet_skp_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x34, 0x1E, 0xAA)  # {i2c_tx_8b_test_packet_skp_time[7],i2c_tx_8b_test_packet_skp_time[6],i2c_tx_8b_test_packet_skp_time[5],i2c_tx_8b_test_packet_skp_time[4],i2c_tx_8b_test_packet_skp_time[3],i2c_tx_8b_test_packet_skp_time[2],i2c_tx_8b_test_packet_skp_time[1],i2c_tx_8b_test_packet_skp_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x34, 0x1F, 0xB0)  # {i2c_tx_8b_test_en,i2c_tx_8b_test_sel[2],i2c_tx_8b_test_sel[1],i2c_tx_8b_test_sel[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4]}
        device.write_reg(0x34, 0xD1, 0xC0)  # {i2c_clk_packet_8b_pclk_check_man,i2c_rx_packet_8b_en,i2c_rx_packet_8b_err_cnt_clr} <= {dataIn[7],dataIn[6],dataIn[5]}
        device.write_reg(0x34, 0xD2, 0x00)  # {i2c_rx_packet_8b_max[10],i2c_rx_packet_8b_max[9],i2c_rx_packet_8b_max[8]} <= {dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x34, 0xD3, 0xB5)  # {i2c_rx_packet_8b_max[7],i2c_rx_packet_8b_max[6],i2c_rx_packet_8b_max[5],i2c_rx_packet_8b_max[4],i2c_rx_packet_8b_max[3],i2c_rx_packet_8b_max[2],i2c_rx_packet_8b_max[1],i2c_rx_packet_8b_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x34, 0xD4, 0x20)  # {i2c_rx_packet_8b_com_num[3],i2c_rx_packet_8b_com_num[2],i2c_rx_packet_8b_com_num[1],i2c_rx_packet_8b_com_num[0],i2c_rx_packet_8b_com_time[10],i2c_rx_packet_8b_com_time[9],i2c_rx_packet_8b_com_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x34, 0xD5, 0x02)  # {i2c_rx_packet_8b_com_time[7],i2c_rx_packet_8b_com_time[6],i2c_rx_packet_8b_com_time[5],i2c_rx_packet_8b_com_time[4],i2c_rx_packet_8b_com_time[3],i2c_rx_packet_8b_com_time[2],i2c_rx_packet_8b_com_time[1],i2c_rx_packet_8b_com_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_25_PIPE_dp4_tx8b_packet(self):
        """03-25 PIPE-dp4 tx8b packet"""
        print("Cfg func_03_25_PIPE_dp4_tx8b_packet...")
        device = self._get_device()
        device.write_reg(0x35, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x35, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x35, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x35, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x35, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x35, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x35, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x35, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x35, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x35, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x35, 0x19, 0xC0)  # {i2c_clk_packet_8b_gen_man,i2c_tx_8b_test_packet_en,i2c_tx_8b_test_packet_max[10],i2c_tx_8b_test_packet_max[9],i2c_tx_8b_test_packet_max[8]} <= {dataIn[7],dataIn[6],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x35, 0x1A, 0xB5)  # {i2c_tx_8b_test_packet_max[7],i2c_tx_8b_test_packet_max[6],i2c_tx_8b_test_packet_max[5],i2c_tx_8b_test_packet_max[4],i2c_tx_8b_test_packet_max[3],i2c_tx_8b_test_packet_max[2],i2c_tx_8b_test_packet_max[1],i2c_tx_8b_test_packet_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x35, 0x1B, 0x20)  # {i2c_tx_8b_test_packet_com_num[3],i2c_tx_8b_test_packet_com_num[2],i2c_tx_8b_test_packet_com_num[1],i2c_tx_8b_test_packet_com_num[0],i2c_tx_8b_test_packet_com_time[10],i2c_tx_8b_test_packet_com_time[9],i2c_tx_8b_test_packet_com_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x35, 0x1C, 0x02)  # {i2c_tx_8b_test_packet_com_time[7],i2c_tx_8b_test_packet_com_time[6],i2c_tx_8b_test_packet_com_time[5],i2c_tx_8b_test_packet_com_time[4],i2c_tx_8b_test_packet_com_time[3],i2c_tx_8b_test_packet_com_time[2],i2c_tx_8b_test_packet_com_time[1],i2c_tx_8b_test_packet_com_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x35, 0x1D, 0x20)  # {i2c_tx_8b_test_packet_skp_num[3],i2c_tx_8b_test_packet_skp_num[2],i2c_tx_8b_test_packet_skp_num[1],i2c_tx_8b_test_packet_skp_num[0],i2c_tx_8b_test_packet_skp_time[10],i2c_tx_8b_test_packet_skp_time[9],i2c_tx_8b_test_packet_skp_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x35, 0x1E, 0xAA)  # {i2c_tx_8b_test_packet_skp_time[7],i2c_tx_8b_test_packet_skp_time[6],i2c_tx_8b_test_packet_skp_time[5],i2c_tx_8b_test_packet_skp_time[4],i2c_tx_8b_test_packet_skp_time[3],i2c_tx_8b_test_packet_skp_time[2],i2c_tx_8b_test_packet_skp_time[1],i2c_tx_8b_test_packet_skp_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x35, 0x1F, 0xB0)  # {i2c_tx_8b_test_en,i2c_tx_8b_test_sel[2],i2c_tx_8b_test_sel[1],i2c_tx_8b_test_sel[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4]}
        device.write_reg(0x35, 0xD1, 0xC0)  # {i2c_clk_packet_8b_pclk_check_man,i2c_rx_packet_8b_en,i2c_rx_packet_8b_err_cnt_clr} <= {dataIn[7],dataIn[6],dataIn[5]}
        device.write_reg(0x35, 0xD2, 0x00)  # {i2c_rx_packet_8b_max[10],i2c_rx_packet_8b_max[9],i2c_rx_packet_8b_max[8]} <= {dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x35, 0xD3, 0xB5)  # {i2c_rx_packet_8b_max[7],i2c_rx_packet_8b_max[6],i2c_rx_packet_8b_max[5],i2c_rx_packet_8b_max[4],i2c_rx_packet_8b_max[3],i2c_rx_packet_8b_max[2],i2c_rx_packet_8b_max[1],i2c_rx_packet_8b_max[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x35, 0xD4, 0x20)  # {i2c_rx_packet_8b_com_num[3],i2c_rx_packet_8b_com_num[2],i2c_rx_packet_8b_com_num[1],i2c_rx_packet_8b_com_num[0],i2c_rx_packet_8b_com_time[10],i2c_rx_packet_8b_com_time[9],i2c_rx_packet_8b_com_time[8]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[2],dataIn[1],dataIn[0]}
        device.write_reg(0x35, 0xD5, 0x02)  # {i2c_rx_packet_8b_com_time[7],i2c_rx_packet_8b_com_time[6],i2c_rx_packet_8b_com_time[5],i2c_rx_packet_8b_com_time[4],i2c_rx_packet_8b_com_time[3],i2c_rx_packet_8b_com_time[2],i2c_rx_packet_8b_com_time[1],i2c_rx_packet_8b_com_time[0]} <= {dataIn[7],dataIn[6],dataIn[5],dataIn[4],dataIn[3],dataIn[2],dataIn[1],dataIn[0]}

    def func_03_26_PIPE_up_tx_tseq(self):
        """03-26 PIPE-up tx tseq"""
        print("Cfg func_03_26_PIPE_up_tx_tseq...")
        device = self._get_device()
        device.write_reg(0x31, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x31, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x31, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x31, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x31, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x31, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x31, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x31, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x31, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x31, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x31, 0x17, 0xC0)  # man en
        device.write_reg(0x31, 0x1F, 0x90)  # tx tseq

    def func_03_27_PIPE_dp1_tx_tseq(self):
        """03-27 PIPE-dp1 tx tseq"""
        print("Cfg func_03_27_PIPE_dp1_tx_tseq...")
        device = self._get_device()
        device.write_reg(0x32, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x32, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x32, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x32, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x32, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x32, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x32, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x32, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x32, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x32, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x32, 0x17, 0xC0)  # man en
        device.write_reg(0x32, 0x1F, 0x90)  # tx tseq

    def func_03_28_PIPE_dp2_tx_tseq(self):
        """03-28 PIPE-dp2 tx tseq"""
        print("Cfg func_03_28_PIPE_dp2_tx_tseq...")
        device = self._get_device()
        device.write_reg(0x33, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x33, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x33, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x33, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x33, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x33, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x33, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x33, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x33, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x33, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x33, 0x17, 0xC0)  # man en
        device.write_reg(0x33, 0x1F, 0x90)  # tx tseq

    def func_03_29_PIPE_dp3_tx_tseq(self):
        """03-29 PIPE-dp3 tx tseq"""
        print("Cfg func_03_29_PIPE_dp3_tx_tseq...")
        device = self._get_device()
        device.write_reg(0x34, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x34, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x34, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x34, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x34, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x34, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x34, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x34, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x34, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x34, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x34, 0x17, 0xC0)  # man en
        device.write_reg(0x34, 0x1F, 0x90)  # tx tseq

    def func_03_30_PIPE_dp4_tx_tseq(self):
        """03-30 PIPE-dp4 tx tseq"""
        print("Cfg func_03_30_PIPE_dp4_tx_tseq...")
        device = self._get_device()
        device.write_reg(0x35, 0x02, 0xFF)  # i2c_pipe_man_en[15:8]
        device.write_reg(0x35, 0x03, 0xFF)  # i2c_pipe_man_en[7:0]
        device.write_reg(0x35, 0x04, 0x00)  # i2c_pipe_man[25:24]
        device.write_reg(0x35, 0x05, 0x00)  # i2c_pipe_man[23:16]
        device.write_reg(0x35, 0x06, 0x00)  # i2c_pipe_man[15:8]
        device.write_reg(0x35, 0x07, 0x01)  # i2c_pipe_man[7:0],U0 tx 20b
        device.write_reg(0x35, 0x0B, 0xFF)  # i2c_ana_man_en[12:8]
        device.write_reg(0x35, 0x0C, 0xFF)  # i2c_ana_man_en[7:0]
        device.write_reg(0x35, 0x0D, 0x0C)  # i2c_ana_man[12:8]
        device.write_reg(0x35, 0x0E, 0x17)  # i2c_ana_man[7:0] tx en,rx en
        device.write_reg(0x35, 0x17, 0xC0)  # man en
        device.write_reg(0x35, 0x1F, 0x90)  # tx tseq

    def func_03_31_up_debug_testdata(self):
        """03-31 up debug testdata"""
        print("Cfg func_03_31_up_debug_testdata...")
        device = self._get_device()
        self.func_03_06_PIPE_up_Tx_Rx_LFPS()
        device.write_reg(0x31, 0x0F, 0x60)  # disable lfps tx en
        device.write_reg(0x31, 0xEA, 0x20)  # test en = 1
        device.write_reg(0x31, 0xE4, 0x13)  # debug io select test data from extern

    def func_03_31_dp1_debug_testdata(self):
        """03-31 dp1 debug testdata"""
        print("Cfg func_03_31_dp1_debug_testdata...")
        device = self._get_device()
        self.func_03_07_PIPE_dp1_Tx_Rx_LFPS()
        device.write_reg(0x32, 0x0F, 0x60)  # disable lfps tx en
        device.write_reg(0x32, 0xEA, 0x20)  # test en = 1
        device.write_reg(0x32, 0xE4, 0x13)  # debug io select test data from extern

    def func_03_31_dp2_debug_testdata(self):
        """03-31 dp2 debug testdata"""
        print("Cfg func_03_31_dp2_debug_testdata...")
        device = self._get_device()
        self.func_03_08_PIPE_dp2_Tx_Rx_LFPS()
        device.write_reg(0x33, 0x0F, 0x60)  # disable lfps tx en
        device.write_reg(0x33, 0xEA, 0x20)  # test en = 1
        device.write_reg(0x33, 0xE4, 0x13)  # debug io select test data from extern

    def func_03_31_dp3_debug_testdata(self):
        """03-31 dp3 debug testdata"""
        print("Cfg func_03_31_dp3_debug_testdata...")
        device = self._get_device()
        self.func_03_09_PIPE_dp3_Tx_Rx_LFPS()
        device.write_reg(0x34, 0x0F, 0x60)  # disable lfps tx en
        device.write_reg(0x34, 0xEA, 0x20)  # test en = 1
        device.write_reg(0x34, 0xE4, 0x13)  # debug io select test data from extern
        device.write_reg(0x34, 0xF8, 0x06)  # pll debug mux sel
        device.write_reg(0x34, 0xF9, 0x04)  # pll debug mux sel

    def func_03_31_dp4_debug_testdata(self):
        """03-31 dp4 debug testdata"""
        print("Cfg func_03_31_dp4_debug_testdata...")
        device = self._get_device()
        self.func_03_10_PIPE_dp4_Tx_Rx_LFPS()
        device.write_reg(0x35, 0x0F, 0x60)  # disable lfps tx en
        device.write_reg(0x35, 0xEA, 0x20)  # test en = 1
        device.write_reg(0x35, 0xE4, 0x13)  # debug io select test data from extern

    def func_03_35_pipe_no_lowpower(self):
        """03-35 pipe no lowpower"""
        print("Cfg func_03_35_pipe_no_lowpower...")
        device = self._get_device()
        device.write_reg(0x31, 0x0D, 0x34)  # ana man en
        device.write_reg(0x31, 0x0E, 0xC0)  # ana man en
        device.write_reg(0x31, 0x0F, 0x04)  # ana man
        device.write_reg(0x31, 0x10, 0x18)  # ana man
        device.write_reg(0x31, 0xFF, 0xEE)  # pclk on man
        device.write_reg(0x31, 0xE5, 0xFF)  # pipe all gate on
        device.write_reg(0x31, 0xE6, 0x80)  # free run mux is plck
        device.write_reg(0x31, 0x17, 0x30)  # tx encoder clk man
        device.write_reg(0x31, 0x21, 0xE2)  # rxdet clk man
        device.write_reg(0x31, 0x80, 0x80)  # symbol lock clk man en
        device.write_reg(0x31, 0x82, 0x80)  # symbol lock clk man
        device.write_reg(0x31, 0x88, 0xCF)  # symbol unlock clk man
        device.write_reg(0x31, 0x1E, 0x08)  # tx unreset
        device.write_reg(0x31, 0x1E, 0x0C)  # tx reset
        device.write_reg(0x31, 0x1E, 0x08)  # tx unreset,but man
        device.write_reg(0x31, 0x36, 0x00)
        device.write_reg(0x31, 0x37, 0x00)
        device.write_reg(0x31, 0x38, 0x10)  # tx depmh only tx20bit en
        device.write_reg(0x32, 0x0D, 0x34)  # ana man en
        device.write_reg(0x32, 0x0E, 0xC0)  # ana man en
        device.write_reg(0x32, 0x0F, 0x04)  # ana man
        device.write_reg(0x32, 0x10, 0x18)  # ana man
        device.write_reg(0x32, 0xFF, 0xEE)  # pclk on man
        device.write_reg(0x32, 0xE5, 0xFF)  # pipe all gate on
        device.write_reg(0x32, 0xE6, 0x80)  # free run mux is plck
        device.write_reg(0x32, 0x17, 0x30)  # tx encoder clk man
        device.write_reg(0x32, 0x21, 0xE2)  # rxdet clk man
        device.write_reg(0x32, 0x80, 0x80)  # symbol lock clk man en
        device.write_reg(0x32, 0x82, 0x80)  # symbol lock clk man
        device.write_reg(0x32, 0x88, 0xCF)  # symbol unlock clk man
        device.write_reg(0x32, 0x1E, 0x08)  # tx unreset
        device.write_reg(0x32, 0x1E, 0x0C)  # tx reset
        device.write_reg(0x32, 0x1E, 0x08)  # tx unreset,but man
        device.write_reg(0x32, 0x36, 0x00)
        device.write_reg(0x32, 0x37, 0x00)
        device.write_reg(0x32, 0x38, 0x10)  # tx depmh only tx20bit en
        device.write_reg(0x33, 0x0D, 0x34)  # ana man en
        device.write_reg(0x33, 0x0E, 0xC0)  # ana man en
        device.write_reg(0x33, 0x0F, 0x04)  # ana man
        device.write_reg(0x33, 0x10, 0x18)  # ana man
        device.write_reg(0x33, 0xFF, 0xEE)  # pclk on man
        device.write_reg(0x33, 0xE5, 0xFF)  # pipe all gate on
        device.write_reg(0x33, 0xE6, 0x80)  # free run mux is plck
        device.write_reg(0x33, 0x17, 0x30)  # tx encoder clk man
        device.write_reg(0x33, 0x21, 0xE2)  # rxdet clk man
        device.write_reg(0x33, 0x80, 0x80)  # symbol lock clk man en
        device.write_reg(0x33, 0x82, 0x80)  # symbol lock clk man
        device.write_reg(0x33, 0x88, 0xCF)  # symbol unlock clk man
        device.write_reg(0x33, 0x1E, 0x08)  # tx unreset
        device.write_reg(0x33, 0x1E, 0x0C)  # tx reset
        device.write_reg(0x33, 0x1E, 0x08)  # tx unreset,but man
        device.write_reg(0x33, 0x36, 0x00)
        device.write_reg(0x33, 0x37, 0x00)
        device.write_reg(0x33, 0x38, 0x10)  # tx depmh only tx20bit en
        device.write_reg(0x34, 0x0D, 0x34)  # ana man en
        device.write_reg(0x34, 0x0E, 0xC0)  # ana man en
        device.write_reg(0x34, 0x0F, 0x04)  # ana man
        device.write_reg(0x34, 0x10, 0x18)  # ana man
        device.write_reg(0x34, 0xFF, 0xEE)  # pclk on man
        device.write_reg(0x34, 0xE5, 0xFF)  # pipe all gate on
        device.write_reg(0x34, 0xE6, 0x80)  # free run mux is plck
        device.write_reg(0x34, 0x17, 0x30)  # tx encoder clk man
        device.write_reg(0x34, 0x21, 0xE2)  # rxdet clk man
        device.write_reg(0x34, 0x80, 0x80)  # symbol lock clk man en
        device.write_reg(0x34, 0x82, 0x80)  # symbol lock clk man
        device.write_reg(0x34, 0x88, 0xCF)  # symbol unlock clk man
        device.write_reg(0x34, 0x1E, 0x08)  # tx unreset
        device.write_reg(0x34, 0x1E, 0x0C)  # tx reset
        device.write_reg(0x34, 0x1E, 0x08)  # tx unreset,but man
        device.write_reg(0x34, 0x36, 0x00)
        device.write_reg(0x34, 0x37, 0x00)
        device.write_reg(0x34, 0x38, 0x10)  # tx depmh only tx20bit en
        device.write_reg(0x35, 0x0D, 0x34)  # ana man en
        device.write_reg(0x35, 0x0E, 0xC0)  # ana man en
        device.write_reg(0x35, 0x0F, 0x04)  # ana man
        device.write_reg(0x35, 0x10, 0x18)  # ana man
        device.write_reg(0x35, 0xFF, 0xEE)  # pclk on man
        device.write_reg(0x35, 0xE5, 0xFF)  # pipe all gate on
        device.write_reg(0x35, 0xE6, 0x80)  # free run mux is plck
        device.write_reg(0x35, 0x17, 0x30)  # tx encoder clk man
        device.write_reg(0x35, 0x21, 0xE2)  # rxdet clk man
        device.write_reg(0x35, 0x80, 0x80)  # symbol lock clk man en
        device.write_reg(0x35, 0x82, 0x80)  # symbol lock clk man
        device.write_reg(0x35, 0x88, 0xCF)  # symbol unlock clk man
        device.write_reg(0x35, 0x1E, 0x08)  # tx unreset
        device.write_reg(0x35, 0x1E, 0x0C)  # tx reset
        device.write_reg(0x35, 0x1E, 0x08)  # tx unreset,but man
        device.write_reg(0x35, 0x36, 0x00)
        device.write_reg(0x35, 0x37, 0x00)
        device.write_reg(0x35, 0x38, 0x10)  # tx depmh only tx20bit en

    def func_03_36_dp2_dp3_debug_retimer_up_dn(self):
        """03-36 dp2/dp3 debug retimer up/dn"""
        print("Cfg func_03_36_dp2_dp3_debug_retimer_up_dn...")
        device = self._get_device()
        device.write_reg(0x09, 0xC0, 0x28)  # dp2 test sel
        device.write_reg(0x09, 0xC1, 0x05)  # dp3 test sel
        self.func_03_08_PIPE_dp2_Tx_Rx_LFPS()
        device.write_reg(0x33, 0x0F, 0x60)  # disable dpx lfps tx en
        device.write_reg(0x33, 0xEA, 0x20)  # DPx test en = 1
        device.write_reg(0x33, 0xE4, 0x13)  # dp x debug io select test data from extern
        self.func_03_09_PIPE_dp3_Tx_Rx_LFPS()
        device.write_reg(0x34, 0x0F, 0x60)  # disable dpx lfps tx en
        device.write_reg(0x34, 0xEA, 0x20)  # DPx test en = 1
        device.write_reg(0x34, 0xE4, 0x13)  # dp x debug io select test data from extern

    def func_03_37_five_pipe_digital(self):
        """03-37 five pipe digital"""
        print("Cfg func_03_37_five_pipe_digital...")
        device = self._get_device()
        self.func_03_38_pipe_up_dig_init()
        self.func_03_39_pipe_dp1_dig_init()
        self.func_03_40_pipe_dp2_dig_init()
        self.func_03_41_pipe_dp3_dig_init()
        self.func_03_42_pipe_dp4_dig_init()

    def func_03_38_pipe_up_dig_init(self):
        """03-38 pipe up dig init"""
        print("Cfg func_03_38_pipe_up_dig_init...")
        device = self._get_device()
        device.write_reg(0x31, 0xFF, 0xEC)
        device.write_reg(0x31, 0xDE, 0x00)
        device.write_reg(0x31, 0xDF, 0x00)
        device.write_reg(0x31, 0xD8, 0x60)
        device.write_reg(0x31, 0xE6, 0x00)
        device.write_reg(0x31, 0xE5, 0xFF)
        device.write_reg(0x31, 0x05, 0x00)
        device.write_reg(0x31, 0x06, 0x00)
        device.write_reg(0x31, 0x07, 0x00)
        device.write_reg(0x31, 0x0D, 0x34)
        device.write_reg(0x31, 0x0E, 0x40)
        device.write_reg(0x31, 0x0F, 0x77)
        device.write_reg(0x31, 0x10, 0xBC)
        device.write_reg(0x31, 0x52, 0x4F)
        device.write_reg(0x31, 0x53, 0xAA)
        device.write_reg(0x31, 0x54, 0x88)
        device.write_reg(0x31, 0x55, 0x88)
        device.write_reg(0x31, 0x56, 0x00)
        device.write_reg(0x31, 0x4F, 0xC0)
        device.write_reg(0x31, 0x70, 0x01)
        device.write_reg(0x31, 0x71, 0x5E)
        device.write_reg(0x31, 0x72, 0x64)
        device.write_reg(0x31, 0x73, 0x64)
        device.write_reg(0x31, 0x74, 0x40)
        device.write_reg(0x31, 0x75, 0x04)
        device.write_reg(0x31, 0x76, 0x00)
        device.write_reg(0x31, 0x77, 0x03)
        device.write_reg(0x31, 0x78, 0xE8)
        device.write_reg(0x31, 0x50, 0x00)
        device.write_reg(0x31, 0x64, 0x30)
        device.write_reg(0x31, 0x63, 0x00)
        device.write_reg(0x31, 0x80, 0x00)
        device.write_reg(0x31, 0x82, 0x00)
        device.write_reg(0x31, 0x83, 0xC8)
        device.write_reg(0x31, 0x88, 0xC0)
        device.write_reg(0x31, 0x95, 0x10)
        device.write_reg(0x31, 0x97, 0x9A)
        device.write_reg(0x31, 0xB6, 0x40)
        device.write_reg(0x31, 0xB5, 0x30)
        device.write_reg(0x31, 0xAE, 0x80)
        device.write_reg(0x31, 0xAA, 0x2A)
        device.write_reg(0x31, 0xAB, 0xF8)
        device.write_reg(0x31, 0xAF, 0x00)
        device.write_reg(0x31, 0xAC, 0x00)
        device.write_reg(0x31, 0xAD, 0x64)
        device.write_reg(0x31, 0xB0, 0x00)
        device.write_reg(0x31, 0xB1, 0x00)
        device.write_reg(0x31, 0xB2, 0x00)
        device.write_reg(0x31, 0xB3, 0x00)
        device.write_reg(0x31, 0x9A, 0x1E)
        device.write_reg(0x31, 0xA4, 0xFF)
        device.write_reg(0x31, 0xA5, 0xFF)
        device.write_reg(0x31, 0xA7, 0x00)
        device.write_reg(0x31, 0xA8, 0x00)
        device.write_reg(0x31, 0xA9, 0x07)
        device.write_reg(0x31, 0xA6, 0x00)
        device.write_reg(0x31, 0x9D, 0x00)
        device.write_reg(0x31, 0x9E, 0x00)
        device.write_reg(0x31, 0x9F, 0xC8)
        device.write_reg(0x31, 0xA2, 0x00)
        device.write_reg(0x31, 0xA3, 0x00)
        device.write_reg(0x31, 0x9B, 0x00)
        device.write_reg(0x31, 0xA0, 0x00)
        device.write_reg(0x31, 0xA1, 0x08)
        device.write_reg(0x31, 0x9C, 0x00)
        device.write_reg(0x31, 0xC6, 0x58)
        device.write_reg(0x31, 0xC8, 0x20)
        device.write_reg(0x31, 0x8D, 0xD0)
        device.write_reg(0x31, 0x90, 0x00)
        device.write_reg(0x31, 0x8E, 0x00)
        device.write_reg(0x31, 0x8F, 0x00)
        device.write_reg(0x31, 0xC9, 0x00)
        device.write_reg(0x31, 0xCA, 0x3C)
        device.write_reg(0x31, 0xD2, 0x58)
        device.write_reg(0x31, 0xD1, 0x20)
        device.write_reg(0x31, 0x14, 0x10)
        device.write_reg(0x31, 0x13, 0x07)
        device.write_reg(0x31, 0x17, 0x30)
        device.write_reg(0x31, 0x1B, 0x50)
        device.write_reg(0x31, 0x19, 0x00)
        device.write_reg(0x31, 0x1C, 0x01)
        device.write_reg(0x31, 0x1E, 0x08)
        device.write_reg(0x31, 0x1F, 0x10)
        device.write_reg(0x31, 0x28, 0x00)
        device.write_reg(0x31, 0x21, 0xE2)
        device.write_reg(0x31, 0x2C, 0x00)
        device.write_reg(0x31, 0x2D, 0x00)
        device.write_reg(0x31, 0x2E, 0x6F)
        device.write_reg(0x31, 0x2F, 0xF6)
        device.write_reg(0x31, 0x30, 0xFA)
        device.write_reg(0x31, 0x31, 0xFF)
        device.write_reg(0x31, 0x32, 0xF0)
        device.write_reg(0x31, 0x34, 0x6F)
        device.write_reg(0x31, 0x35, 0xF0)
        device.write_reg(0x31, 0x36, 0x00)
        device.write_reg(0x31, 0x37, 0x00)
        device.write_reg(0x31, 0x38, 0x10)
        device.write_reg(0x31, 0xFA, 0x00)
        device.write_reg(0x31, 0xFC, 0x01)
        device.write_reg(0x31, 0xFB, 0x10)
        device.write_reg(0x31, 0xFA, 0x80)
        device.write_reg(0x31, 0xFA, 0x00)
        device.write_reg(0x31, 0x1E, 0x08)
        device.write_reg(0x31, 0x1E, 0x0C)
        device.write_reg(0x31, 0x1E, 0x08)
        device.write_reg(0x31, 0x1E, 0x00)

    def func_03_39_pipe_dp1_dig_init(self):
        """03-39 pipe dp1 dig init"""
        print("Cfg func_03_39_pipe_dp1_dig_init...")
        device = self._get_device()
        device.write_reg(0x32, 0xFF, 0xEC)
        device.write_reg(0x32, 0xDE, 0x00)
        device.write_reg(0x32, 0xDF, 0x00)
        device.write_reg(0x32, 0xD8, 0x60)
        device.write_reg(0x32, 0xE6, 0x00)
        device.write_reg(0x32, 0xE5, 0xFF)
        device.write_reg(0x32, 0x05, 0x00)
        device.write_reg(0x32, 0x06, 0x00)
        device.write_reg(0x32, 0x07, 0x00)
        device.write_reg(0x32, 0x0D, 0x34)
        device.write_reg(0x32, 0x0E, 0x40)
        device.write_reg(0x32, 0x0F, 0x77)
        device.write_reg(0x32, 0x10, 0xBC)
        device.write_reg(0x32, 0x52, 0x4F)
        device.write_reg(0x32, 0x53, 0xAA)
        device.write_reg(0x32, 0x54, 0x88)
        device.write_reg(0x32, 0x55, 0x88)
        device.write_reg(0x32, 0x56, 0x00)
        device.write_reg(0x32, 0x4F, 0xC0)
        device.write_reg(0x32, 0x70, 0x01)
        device.write_reg(0x32, 0x71, 0x5E)
        device.write_reg(0x32, 0x72, 0x64)
        device.write_reg(0x32, 0x73, 0x64)
        device.write_reg(0x32, 0x74, 0x40)
        device.write_reg(0x32, 0x75, 0x04)
        device.write_reg(0x32, 0x76, 0x00)
        device.write_reg(0x32, 0x77, 0x03)
        device.write_reg(0x32, 0x78, 0xE8)
        device.write_reg(0x32, 0x50, 0x00)
        device.write_reg(0x32, 0x64, 0x30)
        device.write_reg(0x32, 0x63, 0x00)
        device.write_reg(0x32, 0x80, 0x00)
        device.write_reg(0x32, 0x82, 0x00)
        device.write_reg(0x32, 0x83, 0xC8)
        device.write_reg(0x32, 0x88, 0xC0)
        device.write_reg(0x32, 0x95, 0x10)
        device.write_reg(0x32, 0x97, 0x9A)
        device.write_reg(0x32, 0xB6, 0x40)
        device.write_reg(0x32, 0xB5, 0x30)
        device.write_reg(0x32, 0xAE, 0x80)
        device.write_reg(0x32, 0xAA, 0x2A)
        device.write_reg(0x32, 0xAB, 0xF8)
        device.write_reg(0x32, 0xAF, 0x00)
        device.write_reg(0x32, 0xAC, 0x00)
        device.write_reg(0x32, 0xAD, 0x64)
        device.write_reg(0x32, 0xB0, 0x00)
        device.write_reg(0x32, 0xB1, 0x00)
        device.write_reg(0x32, 0xB2, 0x00)
        device.write_reg(0x32, 0xB3, 0x00)
        device.write_reg(0x32, 0x9A, 0x1E)
        device.write_reg(0x32, 0xA4, 0xFF)
        device.write_reg(0x32, 0xA5, 0xFF)
        device.write_reg(0x32, 0xA7, 0x00)
        device.write_reg(0x32, 0xA8, 0x00)
        device.write_reg(0x32, 0xA9, 0x07)
        device.write_reg(0x32, 0xA6, 0x00)
        device.write_reg(0x32, 0x9D, 0x00)
        device.write_reg(0x32, 0x9E, 0x00)
        device.write_reg(0x32, 0x9F, 0xC8)
        device.write_reg(0x32, 0xA2, 0x00)
        device.write_reg(0x32, 0xA3, 0x00)
        device.write_reg(0x32, 0x9B, 0x00)
        device.write_reg(0x32, 0xA0, 0x00)
        device.write_reg(0x32, 0xA1, 0x08)
        device.write_reg(0x32, 0x9C, 0x00)
        device.write_reg(0x32, 0xC6, 0x58)
        device.write_reg(0x32, 0xC8, 0x20)
        device.write_reg(0x32, 0x8D, 0xD0)
        device.write_reg(0x32, 0x90, 0x00)
        device.write_reg(0x32, 0x8E, 0x00)
        device.write_reg(0x32, 0x8F, 0x00)
        device.write_reg(0x32, 0xC9, 0x00)
        device.write_reg(0x32, 0xCA, 0x3C)
        device.write_reg(0x32, 0xD2, 0x58)
        device.write_reg(0x32, 0xD1, 0x20)
        device.write_reg(0x32, 0x14, 0x10)
        device.write_reg(0x32, 0x13, 0x07)
        device.write_reg(0x32, 0x17, 0x30)
        device.write_reg(0x32, 0x1B, 0x50)
        device.write_reg(0x32, 0x19, 0x00)
        device.write_reg(0x32, 0x1C, 0x01)
        device.write_reg(0x32, 0x1E, 0x08)
        device.write_reg(0x32, 0x1F, 0x10)
        device.write_reg(0x32, 0x28, 0x00)
        device.write_reg(0x32, 0x21, 0xE2)
        device.write_reg(0x32, 0x2C, 0x00)
        device.write_reg(0x32, 0x2D, 0x00)
        device.write_reg(0x32, 0x2E, 0x6F)
        device.write_reg(0x32, 0x2F, 0xF6)
        device.write_reg(0x32, 0x30, 0xFA)
        device.write_reg(0x32, 0x31, 0xFF)
        device.write_reg(0x32, 0x32, 0xF0)
        device.write_reg(0x32, 0x34, 0x6F)
        device.write_reg(0x32, 0x35, 0xF0)
        device.write_reg(0x32, 0x36, 0x00)
        device.write_reg(0x32, 0x37, 0x00)
        device.write_reg(0x32, 0x38, 0x10)
        device.write_reg(0x32, 0xFA, 0x00)
        device.write_reg(0x32, 0xFC, 0x01)
        device.write_reg(0x32, 0xFB, 0x10)
        device.write_reg(0x32, 0xFA, 0x80)
        device.write_reg(0x32, 0xFA, 0x00)
        device.write_reg(0x32, 0x1E, 0x08)
        device.write_reg(0x32, 0x1E, 0x0C)
        device.write_reg(0x32, 0x1E, 0x08)
        device.write_reg(0x32, 0x1E, 0x00)

    def func_03_40_pipe_dp2_dig_init(self):
        """03-40 pipe dp2 dig init"""
        print("Cfg func_03_40_pipe_dp2_dig_init...")
        device = self._get_device()
        device.write_reg(0x33, 0xFF, 0xEC)
        device.write_reg(0x33, 0xDE, 0x00)
        device.write_reg(0x33, 0xDF, 0x00)
        device.write_reg(0x33, 0xD8, 0x60)
        device.write_reg(0x33, 0xE6, 0x00)
        device.write_reg(0x33, 0xE5, 0xFF)
        device.write_reg(0x33, 0x05, 0x00)
        device.write_reg(0x33, 0x06, 0x00)
        device.write_reg(0x33, 0x07, 0x00)
        device.write_reg(0x33, 0x0D, 0x34)
        device.write_reg(0x33, 0x0E, 0x40)
        device.write_reg(0x33, 0x0F, 0x77)
        device.write_reg(0x33, 0x10, 0xBC)
        device.write_reg(0x33, 0x52, 0x4F)
        device.write_reg(0x33, 0x53, 0xAA)
        device.write_reg(0x33, 0x54, 0x88)
        device.write_reg(0x33, 0x55, 0x88)
        device.write_reg(0x33, 0x56, 0x00)
        device.write_reg(0x33, 0x4F, 0xC0)
        device.write_reg(0x33, 0x70, 0x01)
        device.write_reg(0x33, 0x71, 0x5E)
        device.write_reg(0x33, 0x72, 0x64)
        device.write_reg(0x33, 0x73, 0x64)
        device.write_reg(0x33, 0x74, 0x40)
        device.write_reg(0x33, 0x75, 0x04)
        device.write_reg(0x33, 0x76, 0x00)
        device.write_reg(0x33, 0x77, 0x03)
        device.write_reg(0x33, 0x78, 0xE8)
        device.write_reg(0x33, 0x50, 0x00)
        device.write_reg(0x33, 0x64, 0x30)
        device.write_reg(0x33, 0x63, 0x00)
        device.write_reg(0x33, 0x80, 0x00)
        device.write_reg(0x33, 0x82, 0x00)
        device.write_reg(0x33, 0x83, 0xC8)
        device.write_reg(0x33, 0x88, 0xC0)
        device.write_reg(0x33, 0x95, 0x10)
        device.write_reg(0x33, 0x97, 0x9A)
        device.write_reg(0x33, 0xB6, 0x40)
        device.write_reg(0x33, 0xB5, 0x30)
        device.write_reg(0x33, 0xAE, 0x80)
        device.write_reg(0x33, 0xAA, 0x2A)
        device.write_reg(0x33, 0xAB, 0xF8)
        device.write_reg(0x33, 0xAF, 0x00)
        device.write_reg(0x33, 0xAC, 0x00)
        device.write_reg(0x33, 0xAD, 0x64)
        device.write_reg(0x33, 0xB0, 0x00)
        device.write_reg(0x33, 0xB1, 0x00)
        device.write_reg(0x33, 0xB2, 0x00)
        device.write_reg(0x33, 0xB3, 0x00)
        device.write_reg(0x33, 0x9A, 0x1E)
        device.write_reg(0x33, 0xA4, 0xFF)
        device.write_reg(0x33, 0xA5, 0xFF)
        device.write_reg(0x33, 0xA7, 0x00)
        device.write_reg(0x33, 0xA8, 0x00)
        device.write_reg(0x33, 0xA9, 0x07)
        device.write_reg(0x33, 0xA6, 0x00)
        device.write_reg(0x33, 0x9D, 0x00)
        device.write_reg(0x33, 0x9E, 0x00)
        device.write_reg(0x33, 0x9F, 0xC8)
        device.write_reg(0x33, 0xA2, 0x00)
        device.write_reg(0x33, 0xA3, 0x00)
        device.write_reg(0x33, 0x9B, 0x00)
        device.write_reg(0x33, 0xA0, 0x00)
        device.write_reg(0x33, 0xA1, 0x08)
        device.write_reg(0x33, 0x9C, 0x00)
        device.write_reg(0x33, 0xC6, 0x58)
        device.write_reg(0x33, 0xC8, 0x20)
        device.write_reg(0x33, 0x8D, 0xD0)
        device.write_reg(0x33, 0x90, 0x00)
        device.write_reg(0x33, 0x8E, 0x00)
        device.write_reg(0x33, 0x8F, 0x00)
        device.write_reg(0x33, 0xC9, 0x00)
        device.write_reg(0x33, 0xCA, 0x3C)
        device.write_reg(0x33, 0xD2, 0x58)
        device.write_reg(0x33, 0xD1, 0x20)
        device.write_reg(0x33, 0x14, 0x10)
        device.write_reg(0x33, 0x13, 0x07)
        device.write_reg(0x33, 0x17, 0x30)
        device.write_reg(0x33, 0x1B, 0x50)
        device.write_reg(0x33, 0x19, 0x00)
        device.write_reg(0x33, 0x1C, 0x01)
        device.write_reg(0x33, 0x1E, 0x08)
        device.write_reg(0x33, 0x1F, 0x10)
        device.write_reg(0x33, 0x28, 0x00)
        device.write_reg(0x33, 0x21, 0xE2)
        device.write_reg(0x33, 0x2C, 0x00)
        device.write_reg(0x33, 0x2D, 0x00)
        device.write_reg(0x33, 0x2E, 0x6F)
        device.write_reg(0x33, 0x2F, 0xF6)
        device.write_reg(0x33, 0x30, 0xFA)
        device.write_reg(0x33, 0x31, 0xFF)
        device.write_reg(0x33, 0x32, 0xF0)
        device.write_reg(0x33, 0x34, 0x6F)
        device.write_reg(0x33, 0x35, 0xF0)
        device.write_reg(0x33, 0x36, 0x00)
        device.write_reg(0x33, 0x37, 0x00)
        device.write_reg(0x33, 0x38, 0x10)
        device.write_reg(0x33, 0xFA, 0x00)
        device.write_reg(0x33, 0xFC, 0x01)
        device.write_reg(0x33, 0xFB, 0x10)
        device.write_reg(0x33, 0xFA, 0x80)
        device.write_reg(0x33, 0xFA, 0x00)
        device.write_reg(0x33, 0x1E, 0x08)
        device.write_reg(0x33, 0x1E, 0x0C)
        device.write_reg(0x33, 0x1E, 0x08)
        device.write_reg(0x33, 0x1E, 0x00)

    def func_03_41_pipe_dp3_dig_init(self):
        """03-41 pipe dp3 dig init"""
        print("Cfg func_03_41_pipe_dp3_dig_init...")
        device = self._get_device()
        device.write_reg(0x34, 0xFF, 0xEC)
        device.write_reg(0x34, 0xDE, 0x00)
        device.write_reg(0x34, 0xDF, 0x00)
        device.write_reg(0x34, 0xD8, 0x60)
        device.write_reg(0x34, 0xE6, 0x00)
        device.write_reg(0x34, 0xE5, 0xFF)
        device.write_reg(0x34, 0x05, 0x00)
        device.write_reg(0x34, 0x06, 0x00)
        device.write_reg(0x34, 0x07, 0x00)
        device.write_reg(0x34, 0x0D, 0x34)
        device.write_reg(0x34, 0x0E, 0x40)
        device.write_reg(0x34, 0x0F, 0x77)
        device.write_reg(0x34, 0x10, 0xBC)
        device.write_reg(0x34, 0x52, 0x4F)
        device.write_reg(0x34, 0x53, 0xAA)
        device.write_reg(0x34, 0x54, 0x88)
        device.write_reg(0x34, 0x55, 0x88)
        device.write_reg(0x34, 0x56, 0x00)
        device.write_reg(0x34, 0x4F, 0xC0)
        device.write_reg(0x34, 0x70, 0x01)
        device.write_reg(0x34, 0x71, 0x5E)
        device.write_reg(0x34, 0x72, 0x64)
        device.write_reg(0x34, 0x73, 0x64)
        device.write_reg(0x34, 0x74, 0x40)
        device.write_reg(0x34, 0x75, 0x04)
        device.write_reg(0x34, 0x76, 0x00)
        device.write_reg(0x34, 0x77, 0x03)
        device.write_reg(0x34, 0x78, 0xE8)
        device.write_reg(0x34, 0x50, 0x00)
        device.write_reg(0x34, 0x64, 0x30)
        device.write_reg(0x34, 0x63, 0x00)
        device.write_reg(0x34, 0x80, 0x00)
        device.write_reg(0x34, 0x82, 0x00)
        device.write_reg(0x34, 0x83, 0xC8)
        device.write_reg(0x34, 0x88, 0xC0)
        device.write_reg(0x34, 0x95, 0x10)
        device.write_reg(0x34, 0x97, 0x9A)
        device.write_reg(0x34, 0xB6, 0x40)
        device.write_reg(0x34, 0xB5, 0x30)
        device.write_reg(0x34, 0xAE, 0x80)
        device.write_reg(0x34, 0xAA, 0x2A)
        device.write_reg(0x34, 0xAB, 0xF8)
        device.write_reg(0x34, 0xAF, 0x00)
        device.write_reg(0x34, 0xAC, 0x00)
        device.write_reg(0x34, 0xAD, 0x64)
        device.write_reg(0x34, 0xB0, 0x00)
        device.write_reg(0x34, 0xB1, 0x00)
        device.write_reg(0x34, 0xB2, 0x00)
        device.write_reg(0x34, 0xB3, 0x00)
        device.write_reg(0x34, 0x9A, 0x1E)
        device.write_reg(0x34, 0xA4, 0xFF)
        device.write_reg(0x34, 0xA5, 0xFF)
        device.write_reg(0x34, 0xA7, 0x00)
        device.write_reg(0x34, 0xA8, 0x00)
        device.write_reg(0x34, 0xA9, 0x07)
        device.write_reg(0x34, 0xA6, 0x00)
        device.write_reg(0x34, 0x9D, 0x00)
        device.write_reg(0x34, 0x9E, 0x00)
        device.write_reg(0x34, 0x9F, 0xC8)
        device.write_reg(0x34, 0xA2, 0x00)
        device.write_reg(0x34, 0xA3, 0x00)
        device.write_reg(0x34, 0x9B, 0x00)
        device.write_reg(0x34, 0xA0, 0x00)
        device.write_reg(0x34, 0xA1, 0x08)
        device.write_reg(0x34, 0x9C, 0x00)
        device.write_reg(0x34, 0xC6, 0x58)
        device.write_reg(0x34, 0xC8, 0x20)
        device.write_reg(0x34, 0x8D, 0xD0)
        device.write_reg(0x34, 0x90, 0x00)
        device.write_reg(0x34, 0x8E, 0x00)
        device.write_reg(0x34, 0x8F, 0x00)
        device.write_reg(0x34, 0xC9, 0x00)
        device.write_reg(0x34, 0xCA, 0x3C)
        device.write_reg(0x34, 0xD2, 0x58)
        device.write_reg(0x34, 0xD1, 0x20)
        device.write_reg(0x34, 0x14, 0x10)
        device.write_reg(0x34, 0x13, 0x07)
        device.write_reg(0x34, 0x17, 0x30)
        device.write_reg(0x34, 0x1B, 0x50)
        device.write_reg(0x34, 0x19, 0x00)
        device.write_reg(0x34, 0x1C, 0x01)
        device.write_reg(0x34, 0x1E, 0x08)
        device.write_reg(0x34, 0x1F, 0x10)
        device.write_reg(0x34, 0x28, 0x00)
        device.write_reg(0x34, 0x21, 0xE2)
        device.write_reg(0x34, 0x2C, 0x00)
        device.write_reg(0x34, 0x2D, 0x00)
        device.write_reg(0x34, 0x2E, 0x6F)
        device.write_reg(0x34, 0x2F, 0xF6)
        device.write_reg(0x34, 0x30, 0xFA)
        device.write_reg(0x34, 0x31, 0xFF)
        device.write_reg(0x34, 0x32, 0xF0)
        device.write_reg(0x34, 0x34, 0x6F)
        device.write_reg(0x34, 0x35, 0xF0)
        device.write_reg(0x34, 0x36, 0x00)
        device.write_reg(0x34, 0x37, 0x00)
        device.write_reg(0x34, 0x38, 0x10)
        device.write_reg(0x34, 0xFA, 0x00)
        device.write_reg(0x34, 0xFC, 0x01)
        device.write_reg(0x34, 0xFB, 0x10)
        device.write_reg(0x34, 0xFA, 0x80)
        device.write_reg(0x34, 0xFA, 0x00)
        device.write_reg(0x34, 0x1E, 0x08)
        device.write_reg(0x34, 0x1E, 0x0C)
        device.write_reg(0x34, 0x1E, 0x08)
        device.write_reg(0x34, 0x1E, 0x00)

    def func_03_42_pipe_dp4_dig_init(self):
        """03-42 pipe dp4 dig init"""
        print("Cfg func_03_42_pipe_dp4_dig_init...")
        device = self._get_device()
        device.write_reg(0x35, 0xFF, 0xEC)
        device.write_reg(0x35, 0xDE, 0x00)
        device.write_reg(0x35, 0xDF, 0x00)
        device.write_reg(0x35, 0xD8, 0x60)
        device.write_reg(0x35, 0xE6, 0x00)
        device.write_reg(0x35, 0xE5, 0xFF)
        device.write_reg(0x35, 0x05, 0x00)
        device.write_reg(0x35, 0x06, 0x00)
        device.write_reg(0x35, 0x07, 0x00)
        device.write_reg(0x35, 0x0D, 0x34)
        device.write_reg(0x35, 0x0E, 0x40)
        device.write_reg(0x35, 0x0F, 0x77)
        device.write_reg(0x35, 0x10, 0xBC)
        device.write_reg(0x35, 0x52, 0x4F)
        device.write_reg(0x35, 0x53, 0xAA)
        device.write_reg(0x35, 0x54, 0x88)
        device.write_reg(0x35, 0x55, 0x88)
        device.write_reg(0x35, 0x56, 0x00)
        device.write_reg(0x35, 0x4F, 0xC0)
        device.write_reg(0x35, 0x70, 0x01)
        device.write_reg(0x35, 0x71, 0x5E)
        device.write_reg(0x35, 0x72, 0x64)
        device.write_reg(0x35, 0x73, 0x64)
        device.write_reg(0x35, 0x74, 0x40)
        device.write_reg(0x35, 0x75, 0x04)
        device.write_reg(0x35, 0x76, 0x00)
        device.write_reg(0x35, 0x77, 0x03)
        device.write_reg(0x35, 0x78, 0xE8)
        device.write_reg(0x35, 0x50, 0x00)
        device.write_reg(0x35, 0x64, 0x30)
        device.write_reg(0x35, 0x63, 0x00)
        device.write_reg(0x35, 0x80, 0x00)
        device.write_reg(0x35, 0x82, 0x00)
        device.write_reg(0x35, 0x83, 0xC8)
        device.write_reg(0x35, 0x88, 0xC0)
        device.write_reg(0x35, 0x95, 0x10)
        device.write_reg(0x35, 0x97, 0x9A)
        device.write_reg(0x35, 0xB6, 0x40)
        device.write_reg(0x35, 0xB5, 0x30)
        device.write_reg(0x35, 0xAE, 0x80)
        device.write_reg(0x35, 0xAA, 0x2A)
        device.write_reg(0x35, 0xAB, 0xF8)
        device.write_reg(0x35, 0xAF, 0x00)
        device.write_reg(0x35, 0xAC, 0x00)
        device.write_reg(0x35, 0xAD, 0x64)
        device.write_reg(0x35, 0xB0, 0x00)
        device.write_reg(0x35, 0xB1, 0x00)
        device.write_reg(0x35, 0xB2, 0x00)
        device.write_reg(0x35, 0xB3, 0x00)
        device.write_reg(0x35, 0x9A, 0x1E)
        device.write_reg(0x35, 0xA4, 0xFF)
        device.write_reg(0x35, 0xA5, 0xFF)
        device.write_reg(0x35, 0xA7, 0x00)
        device.write_reg(0x35, 0xA8, 0x00)
        device.write_reg(0x35, 0xA9, 0x07)
        device.write_reg(0x35, 0xA6, 0x00)
        device.write_reg(0x35, 0x9D, 0x00)
        device.write_reg(0x35, 0x9E, 0x00)
        device.write_reg(0x35, 0x9F, 0xC8)
        device.write_reg(0x35, 0xA2, 0x00)
        device.write_reg(0x35, 0xA3, 0x00)
        device.write_reg(0x35, 0x9B, 0x00)
        device.write_reg(0x35, 0xA0, 0x00)
        device.write_reg(0x35, 0xA1, 0x08)
        device.write_reg(0x35, 0x9C, 0x00)
        device.write_reg(0x35, 0xC6, 0x58)
        device.write_reg(0x35, 0xC8, 0x20)
        device.write_reg(0x35, 0x8D, 0xD0)
        device.write_reg(0x35, 0x90, 0x00)
        device.write_reg(0x35, 0x8E, 0x00)
        device.write_reg(0x35, 0x8F, 0x00)
        device.write_reg(0x35, 0xC9, 0x00)
        device.write_reg(0x35, 0xCA, 0x3C)
        device.write_reg(0x35, 0xD2, 0x58)
        device.write_reg(0x35, 0xD1, 0x20)
        device.write_reg(0x35, 0x14, 0x10)
        device.write_reg(0x35, 0x13, 0x07)
        device.write_reg(0x35, 0x17, 0x30)
        device.write_reg(0x35, 0x1B, 0x50)
        device.write_reg(0x35, 0x19, 0x00)
        device.write_reg(0x35, 0x1C, 0x01)
        device.write_reg(0x35, 0x1E, 0x08)
        device.write_reg(0x35, 0x1F, 0x10)
        device.write_reg(0x35, 0x28, 0x00)
        device.write_reg(0x35, 0x21, 0xE2)
        device.write_reg(0x35, 0x2C, 0x00)
        device.write_reg(0x35, 0x2D, 0x00)
        device.write_reg(0x35, 0x2E, 0x6F)
        device.write_reg(0x35, 0x2F, 0xF6)
        device.write_reg(0x35, 0x30, 0xFA)
        device.write_reg(0x35, 0x31, 0xFF)
        device.write_reg(0x35, 0x32, 0xF0)
        device.write_reg(0x35, 0x34, 0x6F)
        device.write_reg(0x35, 0x35, 0xF0)
        device.write_reg(0x35, 0x36, 0x00)
        device.write_reg(0x35, 0x37, 0x00)
        device.write_reg(0x35, 0x38, 0x10)
        device.write_reg(0x35, 0xFA, 0x00)
        device.write_reg(0x35, 0xFC, 0x01)
        device.write_reg(0x35, 0xFB, 0x10)
        device.write_reg(0x35, 0xFA, 0x80)
        device.write_reg(0x35, 0xFA, 0x00)
        device.write_reg(0x35, 0x1E, 0x08)
        device.write_reg(0x35, 0x1E, 0x0C)
        device.write_reg(0x35, 0x1E, 0x08)
        device.write_reg(0x35, 0x1E, 0x00)

    def func_03_43_pipe_up_dig_init_for_gse(self):
        """03-43 pipe up dig init for gse"""
        print("Cfg func_03_43_pipe_up_dig_init_for_gse...")
        device = self._get_device()
        device.write_reg(0x31, 0xFF, 0xEC)
        device.write_reg(0x31, 0xDE, 0x00)
        device.write_reg(0x31, 0xDF, 0x00)
        device.write_reg(0x31, 0xD8, 0x60)
        device.write_reg(0x31, 0xE6, 0x00)
        device.write_reg(0x31, 0xE5, 0xFF)
        device.write_reg(0x31, 0x05, 0x00)
        device.write_reg(0x31, 0x06, 0x00)
        device.write_reg(0x31, 0x07, 0x00)
        device.write_reg(0x31, 0x0D, 0x34)
        device.write_reg(0x31, 0x0E, 0x40)
        device.write_reg(0x31, 0x0F, 0x77)
        device.write_reg(0x31, 0x10, 0xBC)
        device.write_reg(0x31, 0x52, 0x4F)
        device.write_reg(0x31, 0x53, 0xAA)
        device.write_reg(0x31, 0x54, 0x88)
        device.write_reg(0x31, 0x55, 0x88)
        device.write_reg(0x31, 0x56, 0x00)
        device.write_reg(0x31, 0x4F, 0xC0)
        device.write_reg(0x31, 0x70, 0x01)
        device.write_reg(0x31, 0x71, 0x5E)
        device.write_reg(0x31, 0x72, 0x64)
        device.write_reg(0x31, 0x73, 0x64)
        device.write_reg(0x31, 0x74, 0x40)
        device.write_reg(0x31, 0x75, 0x04)
        device.write_reg(0x31, 0x76, 0x00)
        device.write_reg(0x31, 0x77, 0x03)
        device.write_reg(0x31, 0x78, 0xE8)
        device.write_reg(0x31, 0x50, 0x00)
        device.write_reg(0x31, 0x64, 0x30)
        device.write_reg(0x31, 0x63, 0x00)
        device.write_reg(0x31, 0x80, 0x00)
        device.write_reg(0x31, 0x82, 0x00)
        device.write_reg(0x31, 0x83, 0xC8)
        device.write_reg(0x31, 0x88, 0xC0)
        device.write_reg(0x31, 0x95, 0x10)
        device.write_reg(0x31, 0x97, 0x9A)
        device.write_reg(0x31, 0xB6, 0x40)
        device.write_reg(0x31, 0xB5, 0x30)
        device.write_reg(0x31, 0xAE, 0x80)
        device.write_reg(0x31, 0xAA, 0x2A)
        device.write_reg(0x31, 0xAB, 0xF8)
        device.write_reg(0x31, 0xAF, 0x00)
        device.write_reg(0x31, 0xAC, 0x00)
        device.write_reg(0x31, 0xAD, 0x64)
        device.write_reg(0x31, 0xB0, 0x00)
        device.write_reg(0x31, 0xB1, 0x00)
        device.write_reg(0x31, 0xB2, 0x00)
        device.write_reg(0x31, 0xB3, 0x00)
        device.write_reg(0x31, 0x9A, 0x1E)
        device.write_reg(0x31, 0xA4, 0xFF)
        device.write_reg(0x31, 0xA5, 0xFF)
        device.write_reg(0x31, 0xA7, 0x00)
        device.write_reg(0x31, 0xA8, 0x00)
        device.write_reg(0x31, 0xA9, 0x07)
        device.write_reg(0x31, 0xA6, 0x00)
        device.write_reg(0x31, 0x9D, 0x00)
        device.write_reg(0x31, 0x9E, 0x00)
        device.write_reg(0x31, 0x9F, 0xC8)
        device.write_reg(0x31, 0xA2, 0x00)
        device.write_reg(0x31, 0xA3, 0x00)
        device.write_reg(0x31, 0x9B, 0x00)
        device.write_reg(0x31, 0xA0, 0x00)
        device.write_reg(0x31, 0xA1, 0x08)
        device.write_reg(0x31, 0x9C, 0x00)
        device.write_reg(0x31, 0xC6, 0x58)
        device.write_reg(0x31, 0xC8, 0x20)
        device.write_reg(0x31, 0x8D, 0xD0)
        device.write_reg(0x31, 0x90, 0x00)
        device.write_reg(0x31, 0x8E, 0x00)
        device.write_reg(0x31, 0x8F, 0x00)
        device.write_reg(0x31, 0xC9, 0x00)
        device.write_reg(0x31, 0xCA, 0x3C)
        device.write_reg(0x31, 0xD2, 0x58)
        device.write_reg(0x31, 0xD1, 0x20)
        device.write_reg(0x31, 0x14, 0x10)
        device.write_reg(0x31, 0x13, 0x07)
        device.write_reg(0x31, 0x17, 0x30)
        device.write_reg(0x31, 0x1B, 0x50)
        device.write_reg(0x31, 0x19, 0x00)
        device.write_reg(0x31, 0x1C, 0x01)
        device.write_reg(0x31, 0x1E, 0x08)
        device.write_reg(0x31, 0x1F, 0x10)
        device.write_reg(0x31, 0x28, 0x00)
        device.write_reg(0x31, 0x21, 0xE1)
        device.write_reg(0x31, 0x2C, 0x00)
        device.write_reg(0x31, 0x2D, 0x00)
        device.write_reg(0x31, 0x2E, 0x6F)
        device.write_reg(0x31, 0x2F, 0xF6)
        device.write_reg(0x31, 0x30, 0xFA)
        device.write_reg(0x31, 0x31, 0xFF)
        device.write_reg(0x31, 0x32, 0xF0)
        device.write_reg(0x31, 0x34, 0x6F)
        device.write_reg(0x31, 0x35, 0xF0)
        device.write_reg(0x31, 0x36, 0x00)
        device.write_reg(0x31, 0x37, 0x00)
        device.write_reg(0x31, 0x38, 0x10)
        device.write_reg(0x31, 0xFA, 0x00)
        device.write_reg(0x31, 0xFC, 0x01)
        device.write_reg(0x31, 0xFB, 0x10)
        device.write_reg(0x31, 0xFA, 0x80)
        device.write_reg(0x31, 0xFA, 0x00)
        device.write_reg(0x31, 0x1E, 0x08)
        device.write_reg(0x31, 0x1E, 0x0C)
        device.write_reg(0x31, 0x1E, 0x08)
        device.write_reg(0x31, 0x1E, 0x00)

    def func_03_50_only_pipe_up_eq_set(self):
        """03-50 only pipe up eq set"""
        print("Cfg func_03_50_only_pipe_up_eq_set...")
        device = self._get_device()
        device.write_reg(0x09, 0x09, 0x00)
        device.write_reg(0x31, 0x95, 0x00)
        device.write_reg(0x31, 0x95, 0x00)
        device.write_reg(0x31, 0x95, 0x00)
        device.write_reg(0x31, 0x95, 0x00)
        device.write_reg(0x31, 0x97, 0x9A)
        device.write_reg(0x31, 0x97, 0x9A)
        device.write_reg(0x31, 0x97, 0x9A)
        device.write_reg(0x31, 0x97, 0x9A)
        device.write_reg(0x31, 0x97, 0x9A)
        device.write_reg(0x31, 0x97, 0x9A)
        device.write_reg(0x31, 0x97, 0x9A)
        device.write_reg(0x31, 0xB5, 0x80)
        device.write_reg(0x31, 0xB6, 0x40)
        device.write_reg(0x31, 0xAE, 0x80)
        device.write_reg(0x31, 0xAA, 0x2A)
        device.write_reg(0x31, 0xAB, 0xF8)
        device.write_reg(0x31, 0xAF, 0x00)
        device.write_reg(0x31, 0xAC, 0x00)
        device.write_reg(0x31, 0xAD, 0x64)
        device.write_reg(0x31, 0xB6, 0x60)
        device.write_reg(0x31, 0xB0, 0x0F)
        device.write_reg(0x31, 0xB1, 0xA0)
        device.write_reg(0x31, 0xB6, 0x70)
        device.write_reg(0x31, 0xB2, 0x00)
        device.write_reg(0x31, 0xB3, 0x80)
        device.write_reg(0x31, 0x9A, 0x1E)
        device.write_reg(0x31, 0x9B, 0x10)
        device.write_reg(0x31, 0x9C, 0x00)
        device.write_reg(0x31, 0x9D, 0x00)
        device.write_reg(0x31, 0x9E, 0xFF)
        device.write_reg(0x31, 0x9F, 0x64)
        device.write_reg(0x31, 0xA4, 0xFF)
        device.write_reg(0x31, 0xA5, 0xFA)
        device.write_reg(0x31, 0x97, 0x9A)
        device.write_reg(0x31, 0xA6, 0x00)
        device.write_reg(0x31, 0xA7, 0x00)
        device.write_reg(0x31, 0xA8, 0x00)
        device.write_reg(0x31, 0xA9, 0x02)
        device.write_reg(0x31, 0xA2, 0x00)
        device.write_reg(0x31, 0xA3, 0x02)
        device.write_reg(0x31, 0xA0, 0x00)
        device.write_reg(0x31, 0xA1, 0x80)

    def func_04_00_HUB1_1_UP_PC_CONNCET(self):
        """04-00 HUB1.1 UP PC_CONNCET"""
        print("Cfg func_04_00_HUB1_1_UP_PC_CONNCET...")
        device = self._get_device()
        device.write_reg(0x28, 0x10, 0xDC)  # i2c_dpport_count_50us
        device.write_reg(0x28, 0x11, 0x05)  # i2c_dpport_count_50us
        device.write_reg(0x28, 0x12, 0x70)  # i2c_dpport_count_200us
        device.write_reg(0x28, 0x13, 0x17)  # i2c_dpport_count_200us
        device.write_reg(0x28, 0x14, 0xE0)  # i2c_dpport_cnt_reset_complete
        device.write_reg(0x28, 0x15, 0x93)  # i2c_dpport_cnt_reset_complete
        device.write_reg(0x28, 0x16, 0x04)  # i2c_dpport_cnt_reset_complete
        device.write_reg(0x28, 0x0A, 0x80)  # i2c_hub_ctrl_count_1ms
        device.write_reg(0x28, 0x0B, 0x8C)  # i2c_hub_ctrl_count_1ms
        device.write_reg(0x28, 0x01, 0xC0)  # i2c_hub11_reset_timer
        device.write_reg(0x28, 0x02, 0xD4)  # i2c_hub11_reset_timer
        device.write_reg(0x28, 0x03, 0x01)  # i2c_hub11_reset_timer
        device.write_reg(0x28, 0x04, 0x80)  # i2c_hub11_resume_timer
        device.write_reg(0x28, 0x05, 0xA9)  # i2c_hub11_resume_timer
        device.write_reg(0x28, 0x06, 0x03)  # i2c_hub11_resume_timer
        device.write_reg(0x28, 0xE9, 0x08)  # i2c_hub1p1_port_reset_en
        device.write_reg(0x28, 0x45, 0x03)  # i2c_up_force_fsmode
        device.write_reg(0x09, 0x64, 0x00)  # hub_2_rstn
        device.write_reg(0x09, 0x64, 0x01)  # remove hub_2_rstn

    def func_04_01_HUB2_0_UP_PC_CONNCET(self):
        """04-01 HUB2.0 UP PC_CONNCET"""
        print("Cfg func_04_01_HUB2_0_UP_PC_CONNCET...")
        device = self._get_device()
        device.write_reg(0x47, 0x6C, 0x2D)  # UP_v2 rx_wrreq_cnt
        device.write_reg(0x4A, 0x6C, 0x2D)  # DP3_v2 rx_wrreq_cnt
        device.write_reg(0x4B, 0x6C, 0x2D)  # DP4_v2 rx_wrreq_cnt
        device.write_reg(0x28, 0x10, 0xDC)  # i2c_dpport_count_50us
        device.write_reg(0x28, 0x11, 0x05)  # i2c_dpport_count_50us
        device.write_reg(0x28, 0x12, 0x70)  # i2c_dpport_count_200us
        device.write_reg(0x28, 0x13, 0x17)  # i2c_dpport_count_200us
        device.write_reg(0x28, 0x14, 0x10)  # i2c_dpport_cnt_reset_complete
        device.write_reg(0x28, 0x15, 0x09)  # i2c_dpport_cnt_reset_complete
        device.write_reg(0x28, 0x16, 0x05)  # i2c_dpport_cnt_reset_complete
        device.write_reg(0x28, 0x17, 0xC0)  # i2c_dpport_resume_cntr
        device.write_reg(0x28, 0x18, 0x27)  # i2c_dpport_resume_cntr
        device.write_reg(0x28, 0x19, 0x09)  # i2c_dpport_resume_cntr
        device.write_reg(0x28, 0x0A, 0x80)  # i2c_hub_ctrl_count_1ms
        device.write_reg(0x28, 0x0B, 0x8C)  # i2c_hub_ctrl_count_1ms
        device.write_reg(0x28, 0x01, 0xC0)  # i2c_hub11_reset_timer
        device.write_reg(0x28, 0x02, 0xD4)  # i2c_hub11_reset_timer
        device.write_reg(0x28, 0x03, 0x01)  # i2c_hub11_reset_timer
        device.write_reg(0x28, 0x04, 0x80)  # i2c_hub11_resume_timer
        device.write_reg(0x28, 0x05, 0xA9)  # i2c_hub11_resume_timer
        device.write_reg(0x28, 0x06, 0x03)  # i2c_hub11_resume_timer
        device.write_reg(0x28, 0xE9, 0x08)  # i2c_hub1p1_port_reset_en
        device.write_reg(0x28, 0x45, 0x01)  # i2c_up_force_fsmode  hs_mode
        device.write_reg(0x09, 0x00, 0x08)  # 480m_domain_rst
        device.write_reg(0x09, 0x00, 0x00)  # 480m_domain_rst
        device.write_reg(0x09, 0x64, 0x00)  # hub_2_rstn
        device.write_reg(0x09, 0x64, 0x01)  # remove hub_2_rstn

    def func_04_02_HUB_SS_PC_CONNECT(self):
        """04-02 HUB_SS PC CONNECT"""
        print("Cfg func_04_02_HUB_SS_PC_CONNECT...")
        device = self._get_device()
        device.write_reg(0x38, 0x40, 0xBC)  # DP1 i2c_count_100ms_ux
        device.write_reg(0x39, 0x40, 0xBC)  # DP2 i2c_count_100ms_ux
        device.write_reg(0x3A, 0x40, 0xBC)  # DP3 i2c_count_100ms_ux
        device.write_reg(0x3B, 0x40, 0xBC)  # DP4 i2c_count_100ms_ux
        device.write_reg(0x38, 0x41, 0xBE)  # DP1 i2c_count_100ms_ux
        device.write_reg(0x39, 0x41, 0xBE)  # DP2 i2c_count_100ms_ux
        device.write_reg(0x3A, 0x41, 0xBE)  # DP3 i2c_count_100ms_ux
        device.write_reg(0x3B, 0x41, 0xBE)  # DP4 i2c_count_100ms_ux
        device.write_reg(0x38, 0xBE, 0x3F)  # DP1 i2c_lgo_u1_time
        device.write_reg(0x39, 0xBE, 0x3F)  # DP2 i2c_lgo_u1_time
        device.write_reg(0x3A, 0xBE, 0x3F)  # DP3 i2c_lgo_u1_time
        device.write_reg(0x3B, 0xBE, 0x3F)  # DP4 i2c_lgo_u1_time
        device.write_reg(0x38, 0xBF, 0x3F)  # DP1 i2c_lgo_u2_time
        device.write_reg(0x39, 0xBF, 0x3F)  # DP2 i2c_lgo_u2_time
        device.write_reg(0x3A, 0xBF, 0x3F)  # DP3 i2c_lgo_u2_time
        device.write_reg(0x3B, 0xBF, 0x3F)  # DP4 i2c_lgo_u2_time
        device.write_reg(0x37, 0xA6, 0x04)  # UP  u1_u2 initiate_en,accept_en
        device.write_reg(0x38, 0xA6, 0x04)  # DP1 u1_u2 initiate_en,accept_en
        device.write_reg(0x39, 0xA6, 0x04)  # DP2 u1_u2 initiate_en,accept_en
        device.write_reg(0x3A, 0xA6, 0x04)  # DP3 u1_u2 initiate_en,accept_en
        device.write_reg(0x3B, 0xA6, 0x04)  # DP4 u1_u2 initiate_en,accept_en
        device.write_reg(0x37, 0x00, 0xC4)  # UP  i2c_CREDIT_HP_timer
        device.write_reg(0x38, 0x00, 0xC4)  # DP1 i2c_CREDIT_HP_timer
        device.write_reg(0x39, 0x00, 0xC4)  # DP2 i2c_CREDIT_HP_timer
        device.write_reg(0x3A, 0x00, 0xC4)  # DP3 i2c_CREDIT_HP_timer
        device.write_reg(0x3B, 0x00, 0xC4)  # DP4 i2c_CREDIT_HP_timer
        device.write_reg(0x37, 0x62, 0x80)  # UP  i2c_adv_hp_pending_timer
        device.write_reg(0x37, 0x63, 0x9D)  # UP  i2c_adv_hp_pending_timer
        device.write_reg(0x38, 0x62, 0x80)  # DP1 i2c_adv_hp_pending_timer
        device.write_reg(0x38, 0x63, 0x9D)  # DP1 i2c_adv_hp_pending_timer
        device.write_reg(0x39, 0x62, 0x80)  # DP2 i2c_adv_hp_pending_timer
        device.write_reg(0x39, 0x63, 0x9D)  # DP2 i2c_adv_hp_pending_timer
        device.write_reg(0x3A, 0x62, 0x80)  # DP3 i2c_adv_hp_pending_timer
        device.write_reg(0x3A, 0x63, 0x9D)  # DP3 i2c_adv_hp_pending_timer
        device.write_reg(0x3B, 0x62, 0x80)  # DP4 i2c_adv_hp_pending_timer
        device.write_reg(0x3B, 0x63, 0x9D)  # DP4 i2c_adv_hp_pending_timer
        device.write_reg(0x37, 0x11, 0x18)  # UP  i2c_count_16_times
        device.write_reg(0x38, 0x11, 0x18)  # DP1 i2c_count_16_times
        device.write_reg(0x39, 0x11, 0x18)  # DP2 i2c_count_16_times
        device.write_reg(0x3A, 0x11, 0x18)  # DP3 i2c_count_16_times
        device.write_reg(0x3B, 0x11, 0x18)  # DP4 i2c_count_16_times
        device.write_reg(0x37, 0x18, 0x14)  # UP  i2c_timeout_12ms
        device.write_reg(0x37, 0x19, 0x72)  # UP  i2c_timeout_12ms
        device.write_reg(0x38, 0x18, 0x14)  # DP1 i2c_timeout_12ms
        device.write_reg(0x38, 0x19, 0x72)  # DP1 i2c_timeout_12ms
        device.write_reg(0x39, 0x18, 0x14)  # DP2 i2c_timeout_12ms
        device.write_reg(0x39, 0x19, 0x72)  # DP2 i2c_timeout_12ms
        device.write_reg(0x3A, 0x18, 0x14)  # DP3 i2c_timeout_12ms
        device.write_reg(0x3A, 0x19, 0x72)  # DP3 i2c_timeout_12ms
        device.write_reg(0x3B, 0x18, 0x14)  # DP4 i2c_timeout_12ms
        device.write_reg(0x3B, 0x19, 0x72)  # DP4 i2c_timeout_12ms
        device.write_reg(0x37, 0x43, 0xA0)  # UP  u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x37, 0x44, 0x86)  # UP  u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x37, 0x45, 0x01)  # UP  u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x38, 0x43, 0xA0)  # DP1 u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x38, 0x44, 0x86)  # DP1 u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x38, 0x45, 0x01)  # DP1 u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x39, 0x43, 0xA0)  # DP2 u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x39, 0x44, 0x86)  # DP2 u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x39, 0x45, 0x01)  # DP2 u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x3A, 0x43, 0xA0)  # DP3 u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x3A, 0x44, 0x86)  # DP3 u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x3A, 0x45, 0x01)  # DP3 u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x3B, 0x43, 0xA0)  # DP4 u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x3B, 0x44, 0x86)  # DP4 u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x3B, 0x45, 0x01)  # DP4 u3_exit_lp1_tx  i2c_count_80us_tx_pci
        device.write_reg(0x37, 0x53, 0x10)  # UP  i2c_lfps_polling_tx_total_cnt
        device.write_reg(0x38, 0x53, 0x10)  # DP1 i2c_lfps_polling_tx_total_cnt
        device.write_reg(0x39, 0x53, 0x10)  # DP2 i2c_lfps_polling_tx_total_cnt
        device.write_reg(0x3A, 0x53, 0x10)  # DP3 i2c_lfps_polling_tx_total_cnt
        device.write_reg(0x3B, 0x53, 0x10)  # DP4 i2c_lfps_polling_tx_total_cnt
        device.write_reg(0x37, 0x57, 0x05)  # UP  i2c_lfps_polling_tx_cnt_after_rx
        device.write_reg(0x38, 0x57, 0x05)  # DP1 i2c_lfps_polling_tx_cnt_after_rx
        device.write_reg(0x39, 0x57, 0x05)  # DP2 i2c_lfps_polling_tx_cnt_after_rx
        device.write_reg(0x3A, 0x57, 0x05)  # DP3 i2c_lfps_polling_tx_cnt_after_rx
        device.write_reg(0x3B, 0x57, 0x05)  # DP4 i2c_lfps_polling_tx_cnt_after_rx
        device.write_reg(0x37, 0x88, 0x01)  # UP  i2c_compliance_mode_en
        device.write_reg(0x38, 0x88, 0x01)  # DP1 i2c_compliance_mode_en
        device.write_reg(0x39, 0x88, 0x01)  # DP2 i2c_compliance_mode_en
        device.write_reg(0x3A, 0x88, 0x01)  # DP3 i2c_compliance_mode_en
        device.write_reg(0x3B, 0x88, 0x01)  # DP4 i2c_compliance_mode_en
        device.write_reg(0x37, 0x12, 0xFF)  # UP  i2c_tseq_cnt_times
        device.write_reg(0x37, 0x13, 0xFF)  # UP  i2c_tseq_cnt_times
        device.write_reg(0x38, 0x12, 0xFF)  # DP1 i2c_tseq_cnt_times
        device.write_reg(0x38, 0x13, 0xFF)  # DP1 i2c_tseq_cnt_times
        device.write_reg(0x39, 0x12, 0xFF)  # DP2 i2c_tseq_cnt_times
        device.write_reg(0x39, 0x13, 0xFF)  # DP2 i2c_tseq_cnt_times
        device.write_reg(0x3A, 0x12, 0xFF)  # DP3 i2c_tseq_cnt_times
        device.write_reg(0x3A, 0x13, 0xFF)  # DP3 i2c_tseq_cnt_times
        device.write_reg(0x3B, 0x12, 0xFF)  # DP4 i2c_tseq_cnt_times
        device.write_reg(0x3B, 0x13, 0xFF)  # DP4 i2c_tseq_cnt_times
        device.write_reg(0x37, 0x11, 0x18)  # UP  TS2_tx_count
        device.write_reg(0x38, 0x11, 0x18)  # DP1 TS2_tx_count
        device.write_reg(0x39, 0x11, 0x18)  # DP1 TS2_tx_count
        device.write_reg(0x3A, 0x11, 0x18)  # DP1 TS2_tx_count
        device.write_reg(0x3B, 0x11, 0x18)  # DP1 TS2_tx_count
        device.write_reg(0x38, 0x1F, 0x10)  # DP1 i2c_count0_100ms  warm_rst
        device.write_reg(0x38, 0x20, 0x5E)  # DP1 i2c_count0_100ms  warm_rst
        device.write_reg(0x38, 0x21, 0x5F)  # DP1 i2c_count0_100ms  warm_rst
        device.write_reg(0x39, 0x1F, 0x10)  # DP2 i2c_count0_100ms  warm_rst
        device.write_reg(0x39, 0x20, 0x5E)  # DP2 i2c_count0_100ms  warm_rst
        device.write_reg(0x39, 0x21, 0x5F)  # DP2 i2c_count0_100ms  warm_rst
        device.write_reg(0x3A, 0x1F, 0x10)  # DP3 i2c_count0_100ms  warm_rst
        device.write_reg(0x3A, 0x20, 0x5E)  # DP3 i2c_count0_100ms  warm_rst
        device.write_reg(0x3A, 0x21, 0x5F)  # DP3 i2c_count0_100ms  warm_rst
        device.write_reg(0x3B, 0x1F, 0x10)  # DP4 i2c_count0_100ms  warm_rst
        device.write_reg(0x3B, 0x20, 0x5E)  # DP4 i2c_count0_100ms  warm_rst
        device.write_reg(0x3B, 0x21, 0x5F)  # DP4 i2c_count0_100ms  warm_rst
        device.write_reg(0x37, 0x07, 0x23)  # UP  SKP  35*8
        device.write_reg(0x37, 0x03, 0x71)  # UP  i2c_pending_hp_timer  10us
        device.write_reg(0x37, 0x04, 0x02)  # UP  i2c_pending_hp_timer
        device.write_reg(0x38, 0x03, 0x71)  # DP1 i2c_pending_hp_timer  10us
        device.write_reg(0x38, 0x04, 0x02)  # DP1 i2c_pending_hp_timer
        device.write_reg(0x39, 0x03, 0x71)  # DP2 i2c_pending_hp_timer  10us
        device.write_reg(0x39, 0x04, 0x02)  # DP2 i2c_pending_hp_timer
        device.write_reg(0x3A, 0x03, 0x71)  # DP3 i2c_pending_hp_timer  10us
        device.write_reg(0x3A, 0x04, 0x02)  # DP3 i2c_pending_hp_timer
        device.write_reg(0x3B, 0x03, 0x71)  # DP4 i2c_pending_hp_timer  10us
        device.write_reg(0x3B, 0x04, 0x02)  # DP4 i2c_pending_hp_timer
        device.write_reg(0x37, 0x83, 0x19)  # UP  U1_Exit_lp1_rx  400ns
        device.write_reg(0x38, 0x83, 0x19)  # DP1 U1_Exit_lp1_rx  400ns
        device.write_reg(0x39, 0x83, 0x19)  # DP2 U1_Exit_lp1_rx  400ns
        device.write_reg(0x3A, 0x83, 0x19)  # DP3 U1_Exit_lp1_rx  400ns
        device.write_reg(0x3B, 0x83, 0x19)  # DP4 U1_Exit_lp1_rx  400ns
        device.write_reg(0x37, 0x9B, 0x41)  # UP  U1_Exit_lp1_tx  1040ns
        device.write_reg(0x38, 0x9B, 0x41)  # DP1 U1_Exit_lp1_tx  1040ns
        device.write_reg(0x39, 0x9B, 0x41)  # DP2 U1_Exit_lp1_tx  1040ns
        device.write_reg(0x3A, 0x9B, 0x41)  # DP3 U1_Exit_lp1_tx  1040ns
        device.write_reg(0x3B, 0x9B, 0x41)  # DP4 U1_Exit_lp1_tx  1040ns
        device.write_reg(0x37, 0x4C, 0x26)  # UP  U1_Exit_lp2_rx  600ns
        device.write_reg(0x38, 0x4C, 0x26)  # DP1 U1_Exit_lp2_rx  600ns
        device.write_reg(0x39, 0x4C, 0x26)  # DP2 U1_Exit_lp2_rx  600ns
        device.write_reg(0x3A, 0x4C, 0x26)  # DP3 U1_Exit_lp2_rx  600ns
        device.write_reg(0x3B, 0x4C, 0x26)  # DP4 U1_Exit_lp2_rx  600ns
        device.write_reg(0x37, 0xA0, 0x41)  # UP  U1_Exit_lp2_tx  1040ns
        device.write_reg(0x38, 0xA0, 0x41)  # DP1 U1_Exit_lp2_tx  1040ns
        device.write_reg(0x39, 0xA0, 0x41)  # DP2 U1_Exit_lp2_tx  1040ns
        device.write_reg(0x3A, 0xA0, 0x41)  # DP3 U1_Exit_lp2_tx  1040ns
        device.write_reg(0x3B, 0xA0, 0x41)  # DP4 U1_Exit_lp2_tx  1040ns
        device.write_reg(0x37, 0x4D, 0xA0)  # UP  U2_Exit_lp1_rx  64us
        device.write_reg(0x37, 0x4E, 0x0F)  # UP  U2_Exit_lp1_rx
        device.write_reg(0x38, 0x4D, 0xA0)  # DP1 U2_Exit_lp1_rx  64us
        device.write_reg(0x38, 0x4E, 0x0F)  # DP1 U2_Exit_lp1_rx
        device.write_reg(0x39, 0x4D, 0xA0)  # DP2 U2_Exit_lp1_rx  64us
        device.write_reg(0x39, 0x4E, 0x0F)  # DP2 U2_Exit_lp1_rx
        device.write_reg(0x3A, 0x4D, 0xA0)  # DP3 U2_Exit_lp1_rx  64us
        device.write_reg(0x3A, 0x4E, 0x0F)  # DP3 U2_Exit_lp1_rx
        device.write_reg(0x3B, 0x4D, 0xA0)  # DP4 U2_Exit_lp1_rx  64us
        device.write_reg(0x3B, 0x4E, 0x0F)  # DP4 U2_Exit_lp1_rx
        device.write_reg(0x37, 0x9D, 0x10)  # UP  U2_Exit_lp1_tx  160 us
        device.write_reg(0x37, 0x9E, 0x27)  # UP  U2_Exit_lp1_tx
        device.write_reg(0x38, 0x9D, 0x10)  # DP1 U2_Exit_lp1_tx  160 us
        device.write_reg(0x38, 0x9E, 0x27)  # DP1 U2_Exit_lp1_tx
        device.write_reg(0x39, 0x9D, 0x10)  # DP2 U2_Exit_lp1_tx  160 us
        device.write_reg(0x39, 0x9E, 0x27)  # DP2 U2_Exit_lp1_tx
        device.write_reg(0x3A, 0x9D, 0x10)  # DP3 U2_Exit_lp1_tx  160 us
        device.write_reg(0x3A, 0x9E, 0x27)  # DP3 U2_Exit_lp1_tx
        device.write_reg(0x3B, 0x9D, 0x10)  # DP4 U2_Exit_lp1_tx  160 us
        device.write_reg(0x3B, 0x9E, 0x27)  # DP4 U2_Exit_lp1_tx
        device.write_reg(0x37, 0x9F, 0x26)  # UP  U2_Exit_lp2_rx  600ns
        device.write_reg(0x38, 0x9F, 0x26)  # DP1 U2_Exit_lp2_rx  600ns
        device.write_reg(0x39, 0x9F, 0x26)  # DP2 U2_Exit_lp2_rx  600ns
        device.write_reg(0x3A, 0x9F, 0x26)  # DP3 U2_Exit_lp2_rx  600ns
        device.write_reg(0x3B, 0x9F, 0x26)  # DP4 U2_Exit_lp2_rx  600ns
        device.write_reg(0x37, 0xA2, 0x34)  # UP  U3_Exit_lp2_tx  2.9 ms
        device.write_reg(0x37, 0xA3, 0x1B)  # UP  U3_Exit_lp2_tx
        device.write_reg(0x37, 0xA4, 0x01)  # UP  U3_Exit_lp2_tx
        device.write_reg(0x38, 0x43, 0xA0)  # DP1 U3_Exit_lp1_tx  4 ms
        device.write_reg(0x38, 0x44, 0x86)  # DP1 U3_Exit_lp1_tx
        device.write_reg(0x38, 0x45, 0x01)  # DP1 U3_Exit_lp1_tx
        device.write_reg(0x39, 0x43, 0xA0)  # DP2 U3_Exit_lp1_tx  4 ms
        device.write_reg(0x39, 0x44, 0x86)  # DP2 U3_Exit_lp1_tx
        device.write_reg(0x39, 0x45, 0x01)  # DP2 U3_Exit_lp1_tx
        device.write_reg(0x3A, 0x43, 0xA0)  # DP3 U3_Exit_lp1_tx  4 ms
        device.write_reg(0x3A, 0x44, 0x86)  # DP3 U3_Exit_lp1_tx
        device.write_reg(0x3A, 0x45, 0x01)  # DP3 U3_Exit_lp1_tx
        device.write_reg(0x3B, 0x43, 0xA0)  # DP4 U3_Exit_lp1_tx  4 ms
        device.write_reg(0x3B, 0x44, 0x86)  # DP4 U3_Exit_lp1_tx
        device.write_reg(0x3B, 0x45, 0x01)  # DP4 U3_Exit_lp1_tx
        device.write_reg(0x38, 0x35, 0x10)  # DP1 i2c_ping_chk_300ns  240ns
        device.write_reg(0x39, 0x35, 0x10)  # DP2 i2c_ping_chk_300ns  240ns
        device.write_reg(0x3A, 0x35, 0x10)  # DP3 i2c_ping_chk_300ns  240ns
        device.write_reg(0x3B, 0x35, 0x10)  # DP4 i2c_ping_chk_300ns  240ns
        device.write_reg(0x30, 0x3C, 0x55)  # DP*_c_connenct_en
        device.write_reg(0x36, 0x88, 0x10)  # hub_name
        device.write_reg(0x36, 0x89, 0x03)
        device.write_reg(0x36, 0x8A, 0x47)
        device.write_reg(0x36, 0x8B, 0x00)
        device.write_reg(0x36, 0x8C, 0x53)
        device.write_reg(0x36, 0x8D, 0x00)
        device.write_reg(0x36, 0x8E, 0x55)
        device.write_reg(0x36, 0x8F, 0x00)
        device.write_reg(0x36, 0x90, 0x31)
        device.write_reg(0x36, 0x91, 0x00)
        device.write_reg(0x36, 0x92, 0x30)
        device.write_reg(0x36, 0x93, 0x00)
        device.write_reg(0x36, 0x94, 0x30)
        device.write_reg(0x36, 0x95, 0x00)
        device.write_reg(0x36, 0x96, 0x31)
        device.write_reg(0x36, 0x97, 0x00)
        device.write_reg(0x36, 0x1F, 0xE0)  # Self-powered
        device.write_reg(0x36, 0x20, 0x00)  # bMaxPower
        device.write_reg(0x36, 0x7D, 0x32)  # bPwrOn2PwrGood
        device.write_reg(0x36, 0x7F, 0x04)  # bHubHdrDecLat
        device.write_reg(0x36, 0x80, 0x90)  # wHubDelay
        device.write_reg(0x36, 0x52, 0xF0)  # container ID
        device.write_reg(0x36, 0x53, 0x56)  # container ID
        device.write_reg(0x36, 0x54, 0x4B)  # container ID
        device.write_reg(0x36, 0x55, 0x9F)  # container ID
        device.write_reg(0x36, 0x56, 0xF6)  # container ID
        device.write_reg(0x36, 0x57, 0x1D)  # container ID
        device.write_reg(0x36, 0x58, 0xE0)  # container ID
        device.write_reg(0x36, 0x59, 0x11)  # container ID
        device.write_reg(0x36, 0x5A, 0xAC)  # container ID
        device.write_reg(0x36, 0x5B, 0x64)  # container ID
        device.write_reg(0x36, 0x5C, 0x08)  # container ID
        device.write_reg(0x36, 0x5D, 0x00)  # container ID
        device.write_reg(0x36, 0x5E, 0x20)  # container ID
        device.write_reg(0x36, 0x5F, 0x0C)  # container ID
        device.write_reg(0x36, 0x60, 0x9A)  # container ID
        device.write_reg(0x36, 0x61, 0x66)  # container ID
        device.write_reg(0x09, 0x64, 0x01)  # hub_ss_rstn
        device.write_reg(0x09, 0x64, 0x03)  # remove hub_ss_rstn

    def func_04_05_HUB_SS_clk_gate_all(self):
        """04-05 HUB_SS clk gate all"""
        print("Cfg func_04_05_HUB_SS_clk_gate_all...")
        device = self._get_device()
        device.write_reg(0x32, 0xF5, 0x50)
        device.write_reg(0x33, 0xF5, 0x50)
        device.write_reg(0x34, 0xF5, 0x50)
        device.write_reg(0x35, 0xF5, 0x50)

    def func_04_06_HUB_SS_ana_gate_all(self):
        """04-06 HUB_SS ana gate all"""
        print("Cfg func_04_06_HUB_SS_ana_gate_all...")
        device = self._get_device()
        device.write_reg(0x32, 0x0B, 0xFF)
        device.write_reg(0x32, 0x0C, 0xFF)
        device.write_reg(0x33, 0x0B, 0xFF)
        device.write_reg(0x33, 0x0C, 0xFF)
        device.write_reg(0x34, 0x0B, 0xFF)
        device.write_reg(0x34, 0x0C, 0xFF)
        device.write_reg(0x35, 0x0B, 0xFF)
        device.write_reg(0x35, 0x0C, 0xFF)

    def func_04_07_HUB_u2_HS_ana_gate_all(self):
        """04-07 HUB u2 HS ana gate all"""
        print("Cfg func_04_07_HUB_u2_HS_ana_gate_all...")
        device = self._get_device()
        device.write_reg(0x0A, 0x02, 0x73)
        device.write_reg(0x0A, 0x08, 0x30)
        device.write_reg(0x0B, 0x02, 0x73)
        device.write_reg(0x0B, 0x08, 0x30)
        device.write_reg(0x0C, 0x02, 0x73)
        device.write_reg(0x0C, 0x08, 0x30)
        device.write_reg(0x0D, 0x02, 0x73)
        device.write_reg(0x0D, 0x08, 0x30)
        device.write_reg(0x0E, 0x02, 0x73)
        device.write_reg(0x0E, 0x08, 0x30)
        device.write_reg(0x09, 0x50, 0x09)
        device.write_reg(0x09, 0x51, 0x09)
        device.write_reg(0x09, 0x52, 0x01)

    def func_04_08_all_pipe_disable_eq_start_ebuf_rst_auto(self):
        """04-08 all pipe disable eq start/ebuf rst auto"""
        print("Cfg func_04_08_all_pipe_disable_eq_start_ebuf_rst_auto...")
        device = self._get_device()
        device.write_reg(0x31, 0x97, 0x23)  # no eq adj auto,eq/cdr is default value
        device.write_reg(0x31, 0xC9, 0x8E)  # ebuf rst man
        device.write_reg(0x32, 0x97, 0x23)  # no eq adj auto,eq/cdr is default value
        device.write_reg(0x32, 0xC9, 0x8E)  # ebuf rst man
        device.write_reg(0x33, 0x97, 0x23)  # no eq adj auto,eq/cdr is default value
        device.write_reg(0x33, 0xC9, 0x8E)  # ebuf rst man
        device.write_reg(0x34, 0x97, 0x23)  # no eq adj auto,eq/cdr is default value
        device.write_reg(0x34, 0xC9, 0x8E)  # ebuf rst man
        device.write_reg(0x35, 0x97, 0x23)  # no eq adj auto,eq/cdr is default value
        device.write_reg(0x35, 0xC9, 0x8E)  # ebuf rst man

    def func_04_09_all_pipe_enable_cdr_tracking_auto(self):
        """04-09 all pipe enable cdr tracking auto"""
        print("Cfg func_04_09_all_pipe_enable_cdr_tracking_auto...")
        device = self._get_device()
        device.write_reg(0x31, 0x74, 0x20)  # ss valid only lfps
        device.write_reg(0x31, 0x76, 0x80)
        device.write_reg(0x31, 0x77, 0x00)
        device.write_reg(0x31, 0x78, 0x00)  # mini cnt = 0
        device.write_reg(0x32, 0x74, 0x20)  # ss valid only lfps
        device.write_reg(0x32, 0x76, 0x80)
        device.write_reg(0x32, 0x77, 0x00)
        device.write_reg(0x32, 0x78, 0x00)  # mini cnt = 0
        device.write_reg(0x33, 0x74, 0x20)  # ss valid only lfps
        device.write_reg(0x33, 0x76, 0x80)
        device.write_reg(0x33, 0x77, 0x00)
        device.write_reg(0x33, 0x78, 0x00)  # mini cnt = 0
        device.write_reg(0x34, 0x74, 0x20)  # ss valid only lfps
        device.write_reg(0x34, 0x76, 0x80)
        device.write_reg(0x34, 0x77, 0x00)
        device.write_reg(0x34, 0x78, 0x00)  # mini cnt = 0
        device.write_reg(0x35, 0x74, 0x20)  # ss valid only lfps
        device.write_reg(0x35, 0x76, 0x80)
        device.write_reg(0x35, 0x77, 0x00)
        device.write_reg(0x35, 0x78, 0x00)  # mini cnt = 0

    def func_04_10_write_EQ_ram(self):
        """04-10 write EQ ram"""
        print("Cfg func_04_10_write_EQ_ram...")
        device = self._get_device()
        device.write_reg(0x09, 0x05, 0x05)
        device.write_reg(0x15, 0x00, 0x01)  # group 0
        device.write_reg(0x15, 0x01, 0xC0)
        device.write_reg(0x15, 0x02, 0x43)
        device.write_reg(0x15, 0x03, 0x3C)
        device.write_reg(0x15, 0x04, 0x0A)
        device.write_reg(0x15, 0x05, 0x00)
        device.write_reg(0x15, 0x06, 0x80)
        device.write_reg(0x15, 0x07, 0x00)
        device.write_reg(0x15, 0x08, 0x68)
        device.write_reg(0x15, 0x09, 0x00)
        device.write_reg(0x15, 0x0A, 0x00)
        device.write_reg(0x15, 0x0B, 0x01)  # group 1
        device.write_reg(0x15, 0x0C, 0xC0)
        device.write_reg(0x15, 0x0D, 0x41)
        device.write_reg(0x15, 0x0E, 0xBC)
        device.write_reg(0x15, 0x0F, 0x09)
        device.write_reg(0x15, 0x10, 0x00)
        device.write_reg(0x15, 0x11, 0x80)
        device.write_reg(0x15, 0x12, 0x00)
        device.write_reg(0x15, 0x13, 0x68)
        device.write_reg(0x15, 0x14, 0x00)
        device.write_reg(0x15, 0x15, 0x00)
        device.write_reg(0x15, 0x16, 0x01)  # group 2
        device.write_reg(0x15, 0x17, 0xC0)
        device.write_reg(0x15, 0x18, 0x60)
        device.write_reg(0x15, 0x19, 0x3C)
        device.write_reg(0x15, 0x1A, 0x0D)
        device.write_reg(0x15, 0x1B, 0x00)
        device.write_reg(0x15, 0x1C, 0x80)
        device.write_reg(0x15, 0x1D, 0x00)
        device.write_reg(0x15, 0x1E, 0x68)
        device.write_reg(0x15, 0x1F, 0x00)
        device.write_reg(0x15, 0x20, 0x00)
        device.write_reg(0x15, 0x21, 0x01)  # group 3
        device.write_reg(0x15, 0x22, 0x40)
        device.write_reg(0x15, 0x23, 0x60)
        device.write_reg(0x15, 0x24, 0xBC)
        device.write_reg(0x15, 0x25, 0x0C)
        device.write_reg(0x15, 0x26, 0x00)
        device.write_reg(0x15, 0x27, 0x80)
        device.write_reg(0x15, 0x28, 0x00)
        device.write_reg(0x15, 0x29, 0x68)
        device.write_reg(0x15, 0x2A, 0x00)
        device.write_reg(0x15, 0x2B, 0x00)
        device.write_reg(0x15, 0x2C, 0x01)  # group 4
        device.write_reg(0x15, 0x2D, 0x00)
        device.write_reg(0x15, 0x2E, 0x60)
        device.write_reg(0x15, 0x2F, 0x3C)
        device.write_reg(0x15, 0x30, 0x0C)
        device.write_reg(0x15, 0x31, 0x00)
        device.write_reg(0x15, 0x32, 0x80)
        device.write_reg(0x15, 0x33, 0x00)
        device.write_reg(0x15, 0x34, 0x68)
        device.write_reg(0x15, 0x35, 0x00)
        device.write_reg(0x15, 0x36, 0x00)
        device.write_reg(0x15, 0x37, 0x01)  # group 5
        device.write_reg(0x15, 0x38, 0x00)
        device.write_reg(0x15, 0x39, 0x60)
        device.write_reg(0x15, 0x3A, 0x3C)
        device.write_reg(0x15, 0x3B, 0x0C)
        device.write_reg(0x15, 0x3C, 0x00)
        device.write_reg(0x15, 0x3D, 0x80)
        device.write_reg(0x15, 0x3E, 0x00)
        device.write_reg(0x15, 0x3F, 0x68)
        device.write_reg(0x15, 0x40, 0x00)
        device.write_reg(0x15, 0x41, 0x00)
        device.write_reg(0x15, 0x42, 0x01)  # group 6
        device.write_reg(0x15, 0x43, 0x00)
        device.write_reg(0x15, 0x44, 0x60)
        device.write_reg(0x15, 0x45, 0x3C)
        device.write_reg(0x15, 0x46, 0x0C)
        device.write_reg(0x15, 0x47, 0x00)
        device.write_reg(0x15, 0x48, 0x80)
        device.write_reg(0x15, 0x49, 0x00)
        device.write_reg(0x15, 0x4A, 0x68)
        device.write_reg(0x15, 0x4B, 0x00)
        device.write_reg(0x15, 0x4C, 0x00)
        device.write_reg(0x15, 0x4D, 0x01)  # group 7
        device.write_reg(0x15, 0x4E, 0x00)
        device.write_reg(0x15, 0x4F, 0x60)
        device.write_reg(0x15, 0x50, 0x3C)
        device.write_reg(0x15, 0x51, 0x0C)
        device.write_reg(0x15, 0x52, 0x00)
        device.write_reg(0x15, 0x53, 0x80)
        device.write_reg(0x15, 0x54, 0x00)
        device.write_reg(0x15, 0x55, 0x68)
        device.write_reg(0x15, 0x56, 0x00)
        device.write_reg(0x15, 0x57, 0x00)
        device.write_reg(0x09, 0x05, 0x00)

    def func_04_11_UP_EQ_AUTO_ADJ(self):
        """04-11 UP EQ AUTO ADJ"""
        print("Cfg func_04_11_UP_EQ_AUTO_ADJ...")
        device = self._get_device()
        device.write_reg(0x10, 0x3F, 0x00)  # rst man=0
        device.write_reg(0x10, 0x01, 0x00)  # i2c_skip_init_sweep=0
        device.write_reg(0x10, 0x09, 0x02)  # i2c_eq_dfe_mode=0,i2c_eq_d_e_check_en=0,i2c_adp_only_meas_init_eq_cfg=0,i2c_eq_seg_cfg_en=1,i2c_eq_init_sel=0
        device.write_reg(0x10, 0x63, 0x00)
        device.write_reg(0x10, 0x64, 0x09)
        device.write_reg(0x10, 0x65, 0xC4)  # i2c_cdr_settle_cycles=10us
        device.write_reg(0x10, 0x69, 0xF0)  # seg en
        device.write_reg(0x10, 0x6A, 0x03)  # eg en
        device.write_reg(0x10, 0x4B, 0x00)  # iic man !en
        device.write_reg(0x10, 0x4A, 0x00)  # iic man !en
        device.write_reg(0x10, 0x4D, 0x00)  # iic man !en
        device.write_reg(0x10, 0x48, 0x00)  # iic man !en
        device.write_reg(0x10, 0x4E, 0x00)  # iic man !en
        device.write_reg(0x10, 0x4F, 0x00)  # iic man !en
        device.write_reg(0x10, 0x6B, 0x00)  # iic man !en
        device.write_reg(0x10, 0x6C, 0x00)  # iic man !en
        device.write_reg(0x10, 0xE0, 0x07)  # freq man en =0
        device.write_reg(0x31, 0x97, 0x1B)  # pl+eq en,group share
        device.write_reg(0x31, 0xA4, 0x13)
        device.write_reg(0x31, 0xA5, 0x88)  # eq no resp 200us
        device.write_reg(0x31, 0xB6, 0x40)  # adj then check mode

    def func_04_12_all_cdr_freqtrack_man_en_0(self):
        """04-12 all cdr freqtrack man en = 0"""
        print("Cfg func_04_12_all_cdr_freqtrack_man_en_0...")
        device = self._get_device()
        device.write_reg(0x10, 0xE0, 0x07)
        device.write_reg(0x11, 0xE0, 0x07)
        device.write_reg(0x12, 0xE0, 0x07)
        device.write_reg(0x13, 0xE0, 0x07)
        device.write_reg(0x14, 0xE0, 0x07)
        device.write_reg(0x10, 0x9A, 0x09)
        device.write_reg(0x11, 0x9A, 0x09)
        device.write_reg(0x12, 0x9A, 0x09)
        device.write_reg(0x13, 0x9A, 0x09)
        device.write_reg(0x14, 0x9A, 0x09)

    def func_04_13_all(self):
        """04-13 all"""
        print("Cfg func_04_13_all...")
        device = self._get_device()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_02_PLL_no_ssc_init()
        self.func_01_01_04_PLL_with_ssc_init_lpmode()
        self.func_01_10_USB_PHY_ALL()
        self.func_03_37_five_pipe_digital()
        self.func_04_01_HUB2_0_UP_PC_CONNCET()
        self.func_04_02_HUB_SS_PC_CONNECT()

    def func_04_14_hub_2_0_all(self):
        """04-14 hub_2.0 all"""
        print("Cfg func_04_14_hub_2_0_all...")
        device = self._get_device()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_02_PLL_no_ssc_init()
        self.func_01_10_USB_PHY_ALL()
        self.func_04_01_HUB2_0_UP_PC_CONNCET()

    def func_04_15_hub_fs_all(self):
        """04-15 hub_fs all"""
        print("Cfg func_04_15_hub_fs_all...")
        device = self._get_device()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_02_PLL_no_ssc_init()
        self.func_01_10_USB_PHY_ALL()
        self.func_04_00_HUB1_1_UP_PC_CONNCET()

    def func_04_16_all_up_support_long_channel(self):
        """04-16 all_up_support_long_channel"""
        print("Cfg func_04_16_all_up_support_long_channel...")
        device = self._get_device()
        self.func_01_01_Chip_Power_Up()
        device.write_reg(0x09, 0x64, 0x00)  # hub rst
        self.func_01_01_02_PLL_no_ssc_init()
        self.func_01_01_05_ANA_Rx_RAM_EQ()
        self.func_01_10_USB_PHY_ALL()
        self.func_01_01_12_USB3_Upcdr_adaptive_param()
        self.func_03_37_five_pipe_digital()
        self.func_03_50_only_pipe_up_eq_set()
        self.func_04_01_HUB2_0_UP_PC_CONNCET()
        self.func_04_02_HUB_SS_PC_CONNECT()

    def func_05_00_retimer_only(self):
        """05-00 retimer only"""
        print("Cfg func_05_00_retimer_only...")
        device = self._get_device()
        device.write_reg(0x0A, 0x00, 0xFF)
        device.write_reg(0x0B, 0x00, 0xFF)
        device.write_reg(0x10, 0x9A, 0x08)
        device.write_reg(0x11, 0x9A, 0x08)
        device.write_reg(0x10, 0x57, 0x07)
        device.write_reg(0x11, 0x57, 0x07)
        device.write_reg(0x09, 0x5F, 0x05)  # switch route sel = 5,pipe0+pipe1
        device.write_reg(0x09, 0x64, 0x06)  # retimer rstn =1
        device.write_reg(0x31, 0x52, 0x4F)  # rx powerdown man
        device.write_reg(0x31, 0x4F, 0x20)  # tx p_state man
        device.write_reg(0x31, 0x50, 0x01)
        device.write_reg(0x40, 0x00, 0xF9)  # 1us div
        device.write_reg(0x40, 0x0E, 0x00)  # cp mode = 0
        device.write_reg(0x40, 0xE2, 0x08)  # u2 inactive done had bug so go u2 auto
        device.write_reg(0x40, 0xE3, 0x01)  # fix rxdet jump out step7
        device.write_reg(0x40, 0x81, 0x00)  # u2 min fix for cover u1
        device.write_reg(0x40, 0x82, 0x40)
        device.write_reg(0x40, 0x83, 0x2C)
        device.write_reg(0x40, 0xF0, 0x03)  # rg_statble_cnt,if so big,may tsx error handshake
        device.write_reg(0x32, 0x52, 0x4F)  # rx powerdown man
        device.write_reg(0x32, 0x4F, 0x20)  # tx p_state man
        device.write_reg(0x32, 0x50, 0x01)
        device.write_reg(0x41, 0x00, 0xF9)  # 1us div
        device.write_reg(0x41, 0x0E, 0x00)  # cp mode = 0
        device.write_reg(0x41, 0xE2, 0x08)  # u2 inactive done had bug so go u2 auto
        device.write_reg(0x41, 0xE3, 0x01)  # fix rxdet jump out step7
        device.write_reg(0x41, 0x81, 0x00)  # u2 min fix for cover u1
        device.write_reg(0x41, 0x82, 0x40)
        device.write_reg(0x41, 0x83, 0x2C)
        device.write_reg(0x41, 0xF0, 0x03)  # rg_statble_cnt,if so big,may tsx error handshake

    def func_05_01_retimer_skp_mode_0(self):
        """05-01 retimer skp mode 0"""
        print("Cfg func_05_01_retimer_skp_mode_0...")
        device = self._get_device()
        device.write_reg(0x31, 0xC8, 0x18)  # skp remove up limit,if we no ssc,should bigger,fifo is 32
        device.write_reg(0x31, 0xD3, 0x10)  # 16 dn limit
        device.write_reg(0x31, 0xD2, 0x00)  # skp add mode 0 for pipe
        device.write_reg(0x40, 0xE7, 0xC4)  # retimer skp fifo mode 1,input skp rm
        device.write_reg(0x40, 0xE8, 0x70)  # retimer skp fifo read start num = 7
        device.write_reg(0x40, 0xE9, 0xA7)  # retimer skp cnt 167
        device.write_reg(0x32, 0xC8, 0x18)  # skp remove up limit,if we no ssc,should bigger,fifo is 32
        device.write_reg(0x32, 0xD3, 0x10)  # 16 dn limit
        device.write_reg(0x32, 0xD2, 0x00)  # skp add mode 0 for pipe
        device.write_reg(0x41, 0xE7, 0xC4)  # retimer skp fifo mode 1,input skp rm
        device.write_reg(0x41, 0xE8, 0x70)  # retimer skp fifo read start num = 7
        device.write_reg(0x41, 0xE9, 0xA7)  # retimer skp cnt 167

    def func_05_02_retimer_skp_mode_1(self):
        """05-02 retimer skp mode 1"""
        print("Cfg func_05_02_retimer_skp_mode_1...")
        device = self._get_device()
        device.write_reg(0x31, 0xC8, 0x18)  # skp remove up limit,if we no ssc,should bigger,fifo is 32
        device.write_reg(0x31, 0xD3, 0x10)  # 16 dn limit
        device.write_reg(0x31, 0xD2, 0x20)  # skp add mode 1 for pipe
        device.write_reg(0x31, 0xD1, 0x10)  # mode1 dn limit
        device.write_reg(0x31, 0xD5, 0x0C)  # mode1 dn limit0
        device.write_reg(0x31, 0xD6, 0x0A)  # mode1 dn limit1
        device.write_reg(0x31, 0xFA, 0x08)  # mode1 dn limit2
        device.write_reg(0x31, 0xFB, 0x12)  # mode1 insert 0+1
        device.write_reg(0x31, 0xFC, 0x48)  # mode1 insert 2+3
        device.write_reg(0x40, 0xE7, 0xA0)  # retimer skp nofifo mode 1,input skp not rm,skp bypass
        device.write_reg(0x32, 0xC8, 0x18)  # skp remove up limit,if we no ssc,should bigger,fifo is 32
        device.write_reg(0x32, 0xD3, 0x10)  # 16 dn limit
        device.write_reg(0x32, 0xD2, 0x20)  # skp add mode 1 for pipe
        device.write_reg(0x32, 0xD1, 0x10)  # mode1 dn limit
        device.write_reg(0x32, 0xD5, 0x0C)  # mode1 dn limit0
        device.write_reg(0x32, 0xD6, 0x0A)  # mode1 dn limit1
        device.write_reg(0x32, 0xFA, 0x08)  # mode1 dn limit2
        device.write_reg(0x32, 0xFB, 0x12)  # mode1 insert 0+1
        device.write_reg(0x32, 0xFC, 0x48)  # mode1 insert 2+3
        device.write_reg(0x41, 0xE7, 0xA0)  # retimer skp nofifo mode 1,input skp not rm,skp bypass

    def func_05_98_retimer_dp1_cp_test(self):
        """05-98 retimer-dp1 cp test"""
        print("Cfg func_05_98_retimer_dp1_cp_test...")
        device = self._get_device()
        device.write_reg(0x40, 0xE3, 0x00)  # fix rxdet jump out step7
        device.write_reg(0x40, 0x0E, 0x02)  # cp mode en
        device.write_reg(0x40, 0x04, 0xFF)  # 24ms never time out
        device.write_reg(0x40, 0x05, 0xFF)
        device.write_reg(0x41, 0xE3, 0x00)  # fix rxdet jump out step7
        device.write_reg(0x41, 0x0E, 0x02)  # cp mode en
        device.write_reg(0x41, 0x04, 0xFF)  # 24ms never time out
        device.write_reg(0x41, 0x05, 0xFF)
        device.write_reg(0x32, 0x28, 0x06)  # pipe dp1 man rxdet = 1

    def func_05_99_retimer_all(self):
        """05-99 retimer-all"""
        print("Cfg func_05_99_retimer_all...")
        device = self._get_device()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_02_PLL_no_ssc_init()
        self.func_01_10_USB_PHY_ALL()
        self.func_04_08_all_pipe_disable_eq_start_ebuf_rst_auto()
        self.func_05_00_retimer_only()
        self.func_05_02_retimer_skp_mode_1()
        self.func_03_35_pipe_no_lowpower()
        self.func_03_36_dp2_dp3_debug_retimer_up_dn()

    def func_06_01_gse_pll_init(self):
        """06-01 gse pll init"""
        print("Cfg func_06_01_gse_pll_init...")
        device = self._get_device()
        self.func_01_01_02_PLL_no_ssc_init()

    def func_06_01_01_gse_pll_ssc_enable(self):
        """06-01-01 gse pll ssc enable"""
        print("Cfg func_06_01_01_gse_pll_ssc_enable...")
        device = self._get_device()
        device.write_reg(0x05, 0xB0, 0x88)
        device.write_reg(0x05, 0xF5, 0x05)
        device.write_reg(0x04, 0x1F, 0x81)  # rxc prediv man=1
        device.write_reg(0x04, 0x20, 0x00)  # rxc postdiv25
        device.write_reg(0x04, 0x21, 0x19)  # rxc postdiv25
        device.write_reg(0x06, 0xB6, 0x00)
        device.write_reg(0x06, 0xB7, 0x00)
        device.write_reg(0x06, 0xB8, 0x00)
        device.write_reg(0x06, 0xB9, 0x80)
        device.write_reg(0x06, 0xB1, 0xFA)
        device.write_reg(0x06, 0xB2, 0xDB)
        device.write_reg(0x06, 0xB3, 0x03)
        device.write_reg(0x06, 0xB4, 0x00)
        device.write_reg(0x06, 0xB5, 0x09)
        device.write_reg(0x06, 0xC0, 0x1F)
        device.write_reg(0x04, 0x23, 0x43)  # rxcpll on
        device.write_reg(0x09, 0x02, 0x33)  # dig clk sel to RXc
        device.write_reg(0x09, 0xCC, 0x01)  # phy tx clksel=rxc, mpll600mode=0

    def func_06_01_02_USB2v2_UP_POWERDOWN(self):
        """06-01-02 USB2v2 UP POWERDOWN"""
        print("Cfg func_06_01_02_USB2v2_UP_POWERDOWN...")
        device = self._get_device()
        device.write_reg(0x09, 0x50, 0x2A)  # up powerdown
        device.write_reg(0x42, 0x00, 0x06)  # rprd bypass
        device.write_reg(0x42, 0x02, 0x08)  # usb2 phy clk off
        device.write_reg(0x42, 0x04, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x05, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x06, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x07, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x08, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x09, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x0A, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x0B, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x0C, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x0D, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x0E, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x0F, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x10, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x11, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x12, 0x00)  # i2c set 0
        device.write_reg(0x42, 0x1B, 0x00)  # rprd set to 0

    def func_06_01_03_USB3_UP_RX_LPmode_debug(self):
        """06-01-03 USB3 UP RX LPmode debug"""
        print("Cfg func_06_01_03_USB3_UP_RX_LPmode_debug...")
        device = self._get_device()
        device.write_reg(0x10, 0xEC, 0x4D)  # prevga=4
        device.write_reg(0x10, 0x4C, 0x01)  # khp_t=1
        device.write_reg(0x10, 0x99, 0x30)  # enable pi 64step

    def func_06_01_04_USB2v2_UP_mode2(self):
        """06-01-04 USB2v2 UP mode2"""
        print("Cfg func_06_01_04_USB2v2_UP_mode2...")
        device = self._get_device()
        device.write_reg(0x42, 0x29, 0x0A)  # dsel_mode=2
        device.write_reg(0x42, 0x2A, 0x0C)  # date_buf_sel=12
        device.write_reg(0x47, 0x6A, 0x01)  # utm_eop_cnt=1

    def func_06_01_05_saradcv2_enable(self):
        """06-01-05 saradcv2 enable"""
        print("Cfg func_06_01_05_saradcv2_enable...")
        device = self._get_device()
        device.write_reg(0x64, 0xA1, 0x04)  # clkdiv=4
        device.write_reg(0x64, 0xA2, 0x10)  # refsel=1
        device.write_reg(0x64, 0xA3, 0x10)  # sample_ctrl=1
        device.write_reg(0x64, 0xA7, 0x30)  # auto=1, cali=1
        device.write_reg(0x64, 0xA0, 0xA0)  # poweron, waitcalib

    def func_06_01_07_Set_pipe_up_send_clkdiv10(self):
        """06-01-07 Set pipe_up send clkdiv10"""
        print("Cfg func_06_01_07_Set_pipe_up_send_clkdiv10...")
        device = self._get_device()
        self.func_03_01_PIPE_up_Tx_Rx_PRBS()
        device.write_reg(0x31, 0x1C, 0x20)
        device.write_reg(0x31, 0x21, 0x9F)
        device.write_reg(0x31, 0x22, 0xFF)
        device.write_reg(0x31, 0x26, 0x80)
        device.write_reg(0x31, 0x27, 0x00)

    def func_06_02_gse_phy_init(self):
        """06-02 gse phy init"""
        print("Cfg func_06_02_gse_phy_init...")
        device = self._get_device()
        self.func_01_05_04_USB2v2_UP_ANA()
        self.func_06_01_04_USB2v2_UP_mode2()
        self.func_01_06_01_PIPE_ANA_UP()
        self.func_01_07_01_USB3_UP_Rx_ANA()
        self.func_06_01_05_saradcv2_enable()

    def func_06_20_gse_usb_set_all(self):
        """06-20 gse usb set all"""
        print("Cfg func_06_20_gse_usb_set_all...")
        device = self._get_device()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_Chip_Power_Up()
        self.func_01_01_Chip_Power_Up()
        self.func_06_01_gse_pll_init()
        self.func_06_02_gse_phy_init()
        self.func_03_43_pipe_up_dig_init_for_gse()

    def func_11_01_dp4_debug_up_usb2v2_adbug3(self):
        """11-01 dp4 debug up usb2v2 adbug3"""
        print("Cfg func_11_01_dp4_debug_up_usb2v2_adbug3...")
        device = self._get_device()
        device.write_reg(0x09, 0xC4, 0x21)  # misc debug sel
        device.write_reg(0x09, 0xC7, 0x00)  # misc debug io sel
        self.func_03_31_up_debug_testdata()
