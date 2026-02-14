"""
USB Common Class - USB PHY 通用配置类

提供 USB2.0 和 USB3.0 PHY 的常用配置功能。

Usage:
    >>> from hw_bridge import DeviceManager
    >>> from library.usb_common_class import USBCommonClass
    >>> dm = DeviceManager(auto_open=True)
    >>> dm.register("chip", "ftdi", i2c_port=0, chip_addr=0x58)
    >>> device = dm["chip"]
    >>> usb = USBCommonClass(device)
    >>> from library.reg_define import UtmUp, U2AnaUp
    >>> usb.init_usb2_tx_prbs(utmi_addr=UtmUp, u2_ana_addr=U2AnaUp)
"""

from typing import List, Tuple, Dict
import time


class USBCommonClass:
    """
    USB PHY 通用配置类

    支持 USB2.0 和 USB3.0 的常用配置功能。
    所有端口地址从外部传入，不在类内部进行选择。
    """

    def __init__(self, device):
        """
        Initialize the USB Common Class.

        Args:
            device: I2C device instance implementing IDevice interface.
                   Must provide methods: write_reg, read_reg, write_bits, read_bits
        """
        self.device = device

    @staticmethod
    def _dac_to_code(num_in: int) -> int:
        """
        Convert DAC input to temperature code.

        Args:
            num_in: Input number (0-8)

        Returns:
            int: Temperature code
        """
        code_map = {
            0: 0x00,
            1: 0x01,
            2: 0x03,
            3: 0x07,
            4: 0x0F,
            5: 0x1F,
            6: 0x3F,
            7: 0x7F,
            8: 0xFF,
        }
        return code_map.get(num_in, 0x00)

    # =========================================================================
    # USB2.0 Initialization Functions
    # =========================================================================

    def init_usb2_tx_prbs(self, utmi_addr: int, u2_ana_addr: int) -> None:
        """
        Initialize USB2.0 TX PRBS mode.

        Args:
            utmi_addr: UTMI register page address
            u2_ana_addr: USB2 Analog register page address
        """
        # TX reset
        self.usb2_tx_reset(utmi_addr)

        # Enable HS TX PRBS
        self.device.write_bits(utmi_addr, 0x30, 4, 1, 1)  # prbs_gen_en=1
        self.device.write_bits(utmi_addr, 0x30, 5, 1, 1)  # prbs_gen_mode=1
        self.device.write_bits(utmi_addr, 0x63, 3, 2, 0)  # test_mode=0

    def init_usb2_rx_prbs(self, utmi_addr: int, u2_ana_addr: int) -> None:
        """
        Initialize USB2.0 RX PRBS mode.

        Args:
            utmi_addr: UTMI register page address
            u2_ana_addr: USB2 Analog register page address
        """
        # Enable HS RX PRBS
        self.device.write_bits(utmi_addr, 0x30, 2, 1, 1)  # prbs_check_en=1
        self.device.write_bits(utmi_addr, 0x30, 3, 1, 1)  # prbs_check_clear=1
        self.device.write_bits(utmi_addr, 0x30, 3, 1, 0)  # prbs_check_clear=0



    # =========================================================================
    # USB2.0 Configuration Functions
    # =========================================================================

    def usb2_tx_reset(self, utmi_addr: int) -> None:
        """
        Reset USB2.0 TX.

        Args:
            utmi_addr: UTMI register page address
        """
        self.device.write_bits(utmi_addr, 0x62, 7, 1, 0)  # auto_en_tx_reset_hs=0
        self.device.write_bits(utmi_addr, 0x63, 5, 1, 1)  # set reset_hs=1
        self.device.write_bits(utmi_addr, 0x63, 5, 1, 0)  # set reset_hs=0

    def usb2_cdr_config(
        self,
        u2_ana_addr: int,
        drop2: int,
        drop4: int,
        lp_mode: int,
        mv_mode: int,
        sync_cond: int,
        lp_sel: int,
    ) -> None:
        """
        Configure USB2.0 CDR settings.

        Args:
            u2_ana_addr: USB2 Analog register page address
            drop2: Drop 2 setting
            drop4: Drop 4 setting
            lp_mode: Low power mode
            mv_mode: MV mode
            sync_cond: Sync condition
            lp_sel: Low power select (2-bit)
        """
        self.device.write_bits(u2_ana_addr, 0x01, 5, 1, drop2)
        self.device.write_bits(u2_ana_addr, 0x01, 6, 1, drop4)
        self.device.write_bits(u2_ana_addr, 0x02, 4, 1, lp_mode)
        self.device.write_bits(u2_ana_addr, 0x02, 5, 1, mv_mode)
        self.device.write_bits(u2_ana_addr, 0x02, 6, 1, sync_cond)
        self.device.write_bits(u2_ana_addr, 0x14, 4, 2, lp_sel)

    def usb2_rx_squelch_config(
        self, u2_ana_addr: int, sql_ctrl: int, sql_bias: int, sql_refbias: int
    ) -> None:
        """
        Configure USB2.0 RX squelch detection.

        Args:
            u2_ana_addr: USB2 Analog register page address
            sql_ctrl: Squelch control (2-bit)
            sql_bias: Squelch bias (3-bit)
            sql_refbias: Squelch reference bias (3-bit)
        """
        self.device.write_bits(u2_ana_addr, 0x04, 0, 3, sql_bias)
        self.device.write_bits(u2_ana_addr, 0x04, 3, 2, sql_ctrl)
        self.device.write_bits(u2_ana_addr, 0x04, 5, 3, sql_refbias)

    def usb2_pll_clk_set(self, ana_pll_addr: int, clk_val: int) -> bool:
        """
        Set USB2.0 PLL clock frequency.

        Args:
            ana_pll_addr: Analog PLL register page address
            clk_val: Clock value in MHz (must be divisible by 25)

        Returns:
            bool: True if successful, False otherwise
        """
        div_ratio = clk_val / 25
        if div_ratio != int(div_ratio):
            return False

        int_div = int(div_ratio)
        int_msb = int_div // 256
        int_lsb = int_div % 256

        self.device.write_reg(ana_pll_addr, 0xF2, int_msb)
        self.device.write_reg(ana_pll_addr, 0xF1, int_lsb)

        # MPLL restart
        self.device.write_bits(ana_pll_addr, 0xF0, 0, 1, 0)
        self.device.write_bits(ana_pll_addr, 0xF0, 0, 1, 1)

        return True

    def usb2_rx_config(self, u2_ana_addr: int, preamp_gain: int, sql_sel: int) -> None:
        """
        Configure USB2.0 RX settings.

        Args:
            u2_ana_addr: USB2 Analog register page address
            preamp_gain: Preamplifier gain (4-bit)
            sql_sel: Squelch select (2-bit)
        """
        self.device.write_bits(u2_ana_addr, 0x07, 0, 4, preamp_gain)
        self.device.write_bits(u2_ana_addr, 0x05, 3, 2, sql_sel)

    def usb2_clk_reverse(
        self, utmi_addr: int, u2_ana_addr: int, reverse: int, clk_delay: int
    ) -> None:
        """
        Configure USB2.0 RX clock reverse.

        Args:
            utmi_addr: UTMI register page address
            u2_ana_addr: USB2 Analog register page address
            reverse: 1 for reverse, 0 for normal
            clk_delay: 00=nodelay, 01=1x, 10=2x, 11=reverse
        """
        self.device.write_bits(utmi_addr, 0x62, 3, 1, 0)
        self.device.write_bits(utmi_addr, 0x62, 3, 1, 1)

        self.device.write_bits(u2_ana_addr, 0x06, 7, 1, reverse)
        self.device.write_bits(u2_ana_addr, 0x06, 0, 2, clk_delay)

    # =========================================================================
    # USB3.0 Configuration Functions
    # =========================================================================

    def usb3_cdr_config(
        self,
        cdr_addr: int,
        freq_tracking_en: int,
        phase_gain: int,
        freq_gain: int,
        mv_sel: int,
    ) -> None:
        """
        Configure USB3.0 CDR settings.

        Args:
            cdr_addr: CDR register page address
            freq_tracking_en: Frequency tracking enable (0 or 1)
            phase_gain: Phase gain (0-15, step=1, default=4)
            freq_gain: Frequency gain (0-3, default=0)
            mv_sel: MV select (0-3, default=3)
        """
        # Set to manual mode
        self.device.write_bits(cdr_addr, 0xE0, 7, 1, 1)

        self.device.write_bits(cdr_addr, 0xE0, 0, 1, freq_tracking_en)
        self.device.write_bits(cdr_addr, 0xE1, 0, 4, phase_gain)
        self.device.write_bits(cdr_addr, 0xE1, 4, 4, freq_gain)
        self.device.write_bits(cdr_addr, 0xE2, 2, 2, mv_sel)

    def usb3_pi_config(self, cdr_addr: int, slewrate: int, picuradj: int) -> None:
        """
        Configure USB3.0 PI (Phase Interpolator) settings.

        Args:
            cdr_addr: CDR register page address
            slewrate: Slew rate (2-bit)
            picuradj: PI current adjust (3-bit)
        """
        self.device.write_bits(cdr_addr, 0x50, 0, 2, slewrate)
        self.device.write_bits(cdr_addr, 0x59, 0, 3, picuradj)

    def usb3_tx_swing_config(self, pipe_addr: int, swing: int) -> None:
        """
        Configure USB3.0 TX swing settings.

        Args:
            pipe_addr: PIPE register page address
            swing: Swing value (5-bit)
        """
        # swing0
        self.device.write_bits(pipe_addr, 0x3A, 3, 5, swing)

        # swing1
        swing_msb = swing >> 2
        swing_lsb = swing & 0x03
        self.device.write_bits(pipe_addr, 0x3A, 0, 3, swing_msb)
        self.device.write_bits(pipe_addr, 0x3B, 6, 2, swing_lsb)

        # swing2
        self.device.write_bits(pipe_addr, 0x3B, 1, 5, swing)

        # swing3
        swing_msb = swing >> 4
        swing_lsb = swing & 0x0F
        self.device.write_bits(pipe_addr, 0x3B, 0, 1, swing_msb)
        self.device.write_bits(pipe_addr, 0x3C, 4, 4, swing_lsb)

        # swing4
        swing_msb = swing >> 1
        swing_lsb = swing & 0x01
        self.device.write_bits(pipe_addr, 0x3C, 0, 4, swing_msb)
        self.device.write_bits(pipe_addr, 0x3D, 7, 1, swing_lsb)

        # swing5
        self.device.write_bits(pipe_addr, 0x3D, 2, 5, swing)

        # swing6
        swing_msb = swing >> 3
        swing_lsb = swing & 0x07
        self.device.write_bits(pipe_addr, 0x3D, 0, 2, swing_msb)
        self.device.write_bits(pipe_addr, 0x3E, 5, 3, swing_lsb)

        # swing7
        self.device.write_bits(pipe_addr, 0x3E, 0, 5, swing)

        # swing8
        self.device.write_bits(pipe_addr, 0x3F, 3, 5, swing)

        # swing9
        swing_msb = swing >> 2
        swing_lsb = swing & 0x03
        self.device.write_bits(pipe_addr, 0x3F, 0, 3, swing_msb)
        self.device.write_bits(pipe_addr, 0x40, 6, 2, swing_lsb)

        # swing10
        self.device.write_bits(pipe_addr, 0x40, 1, 5, swing)

        # swing11
        swing_msb = swing >> 4
        swing_lsb = swing & 0x0F
        self.device.write_bits(pipe_addr, 0x40, 0, 1, swing_msb)
        self.device.write_bits(pipe_addr, 0x41, 4, 4, swing_lsb)

    def usb3_tx_term_config(self, pipe_addr: int, term: int) -> None:
        """
        Configure USB3.0 TX termination.

        Args:
            pipe_addr: PIPE register page address
            term: Termination value (3-bit)
        """
        self.device.write_bits(pipe_addr, 0xE9, 0, 1, 1)  # sterm override=1
        self.device.write_bits(pipe_addr, 0xF0, 2, 3, term)

    def usb3_tx_ffe_config(
        self,
        pipe_addr: int,
        tapw_post2: int,
        tapw_post3: int,
        preemp_sel: int,
        pre_en: int,
    ) -> None:
        """
        Configure USB3.0 TX FFE (Feed Forward Equalization).

        Args:
            pipe_addr: PIPE register page address
            tapw_post2: Post tap 2 weight (2-bit)
            tapw_post3: Post tap 3 weight (2-bit)
            preemp_sel: Pre-emphasis select (3-bit)
            pre_en: Pre-emphasis enable (1-bit)
        """
        self.device.write_bits(pipe_addr, 0xEA, 6, 1, 0)  # tap_weight_en
        self.device.write_bits(pipe_addr, 0x0E, 0, 1, 1)  # ana_man[0]=1
        self.device.write_bits(pipe_addr, 0x0F, 7, 1, 1)  # pre_emp_en=1
        self.device.write_bits(pipe_addr, 0xF7, 7, 1, pre_en)
        self.device.write_bits(pipe_addr, 0xEE, 2, 3, preemp_sel)
        self.device.write_bits(pipe_addr, 0xF6, 4, 2, tapw_post2)
        self.device.write_bits(pipe_addr, 0xF6, 2, 2, tapw_post3)

    def usb3_tx_curadj_config(self, pipe_addr: int, curadj: int) -> None:
        """
        Configure USB3.0 TX current adjustment.

        Args:
            pipe_addr: PIPE register page address
            curadj: Current adjustment (0-3)
        """
        self.device.write_bits(pipe_addr, 0xE9, 7, 1, 1)  # en curadj
        self.device.write_bits(pipe_addr, 0xEA, 2, 2, curadj)

    # =========================================================================
    # CTLE Configuration Functions
    # =========================================================================

    def ctle_manual_config(
        self,
        cdr_addr: int,
        att_en: int,
        zero_en: int,
        khp_t_en: int,
        att: int,
        zero: int,
        khp_t: int,
        ctle_vga_mode: int,
        pole_cap: int,
        post_vga_gain: int,
    ) -> None:
        """
        Manual CTLE configuration for SMIC55.

        Args:
            cdr_addr: CDR register page address
            att_en: Attenuation enable
            zero_en: Zero enable
            khp_t_en: KHP_T enable
            att: Attenuation value (0-8, converted to temp code)
            zero: Zero value (3-bit)
            khp_t: KHP_T value (0-8, converted to temp code)
            ctle_vga_mode: CTLE VGA mode (2-bit)
            pole_cap: Pole capacitor (3-bit)
            post_vga_gain: Post VGA gain (2-bit)
        """
        # Post VGA gain
        self.device.write_bits(cdr_addr, 0x4D, 7, 1, 1)
        self.device.write_bits(cdr_addr, 0x4D, 0, 2, post_vga_gain)

        # ATT
        self.device.write_bits(cdr_addr, 0x48, 7, 1, att_en)
        self.device.write_bits(cdr_addr, 0x49, 0, 6, self._dac_to_code(att))

        # CTLE as VGA
        self.device.write_bits(cdr_addr, 0xEF, 0, 2, ctle_vga_mode)

        # Pole cap
        self.device.write_bits(cdr_addr, 0xEE, 4, 3, pole_cap)

        # Zero
        self.device.write_bits(cdr_addr, 0x4A, 7, 1, zero_en)
        self.device.write_bits(cdr_addr, 0x4A, 0, 3, zero)
        self.device.write_bits(cdr_addr, 0x4F, 7, 1, zero_en)
        self.device.write_bits(cdr_addr, 0x4F, 0, 3, zero)

        # CTLE stage 2 gain
        self.device.write_bits(cdr_addr, 0x4B, 7, 1, khp_t_en)
        self.device.write_bits(cdr_addr, 0x4C, 0, 7, self._dac_to_code(khp_t))

        # CTLE stage 1 gain
        self.device.write_bits(cdr_addr, 0x4E, 7, 1, khp_t_en)
        self.device.write_bits(cdr_addr, 0x4E, 0, 3, khp_t)

    # =========================================================================
    # DFE Configuration Functions
    # =========================================================================

    def dfe_manual_tap_config(self, cdr_addr: int, tap_num: int) -> bool:
        """
        Set DFE manual tap value.

        Args:
            cdr_addr: CDR register page address
            tap_num: Tap number (-100 to 100)

        Returns:
            bool: True if successful, False if out of range
        """
        if tap_num > 100 or tap_num < -100:
            print("DFE manual tap num out of range, need check...")
            return False

        # Convert to Verilog format
        if tap_num >= 0:
            tap_verilog = tap_num
        else:
            tap_verilog = (~abs(tap_num) & 0xFF) + 1

        # Set manual DFE mode
        self.device.write_bits(cdr_addr, 0x09, 5, 1, 1)

        # Write tap value
        self.device.write_reg(cdr_addr, 0xAD, tap_verilog)

        # Reset FSM
        self.device.write_bits(cdr_addr, 0x01, 1, 1, 0)
        self.device.write_bits(cdr_addr, 0x01, 1, 1, 1)
        self.device.write_bits(cdr_addr, 0x01, 1, 1, 0)

        time.sleep(0.1)

        # Verify
        rb_tap_verilog = self.device.read_reg(cdr_addr, 0x66) - 128

        if rb_tap_verilog != tap_num:
            print("DFE manual tap ERROR, not equal")
            return False
        else:
            print(f"DFE manual to: {rb_tap_verilog}")
            return True

    def dfe_reset(self, cdr_addr: int) -> None:
        """
        Reset DFE taps.

        Args:
            cdr_addr: CDR register page address
        """
        self.device.write_reg(cdr_addr, 0xBA, 0x3F)  # Reset DFE Tap
        self.device.write_reg(cdr_addr, 0xBA, 0x00)  # Normal DFE Tap

    def dfe_read_taps(self, cdr_addr: int) -> List[int]:
        """
        Read DFE tap values.

        Args:
            cdr_addr: CDR register page address

        Returns:
            List[int]: [d_lev, tap1]
        """
        d_lev = self.device.read_reg(cdr_addr, 0xD8)
        tap1 = self.device.read_reg(cdr_addr, 0xD9)

        return [int(d_lev), int(tap1)]

    # =========================================================================
    # CDR Control Functions
    # =========================================================================

    def cdr_reset(self, cdr_addr: int) -> None:
        """
        Reset CDR.

        Args:
            cdr_addr: CDR register page address
        """
        self.device.write_bits(cdr_addr, 0x3F, 1, 1, 1)  # rx_cdr_rstb_man_en=1
        self.device.write_bits(cdr_addr, 0x3F, 0, 1, 0)  # rx_cdr_rstb_man=0
        self.device.write_bits(cdr_addr, 0x3F, 0, 1, 1)  # rx_cdr_rstb_man=1

    def cdr_set_eq_bias(self, cdr_addr: int, poly: int, ptat: int, ac_cm: int) -> None:
        """
        Set CDR equalizer bias.

        Args:
            cdr_addr: CDR register page address
            poly: Poly value
            ptat: PTAT value
            ac_cm: AC CM value
        """
        self.device.write_reg(cdr_addr, 0x54, ac_cm)
        self.device.write_reg(cdr_addr, 0x55, poly)
        self.device.write_reg(cdr_addr, 0x56, ptat)

    def cdr_read_status(
        self, cdr_addr: int, catch_times: int
    ) -> Tuple[List[int], List[int]]:
        """
        Read CDR status.

        Args:
            cdr_addr: CDR register page address
            catch_times: Number of times to read

        Returns:
            Tuple[List[int], List[int]]: (phase_dac_array, freq_dac_array)
        """
        # Enable debug mode
        self.device.write_bits(cdr_addr, 0x9D, 0, 1, 1)

        phase_dac_array = []
        freq_dac_array = []

        for _ in range(catch_times):
            freq_reg_0 = self.device.read_reg(cdr_addr, 0xE5)
            freq_reg_1 = self.device.read_reg(cdr_addr, 0xE6)

            freq_cnt = freq_reg_0 * 256 + freq_reg_1
            phase_cnt = 0

            freq_cnt_sign = freq_reg_0 & 0x40
            if freq_cnt_sign == 0:
                freq_cnt_val = freq_cnt
            else:
                freq_cnt_val = -((32768 - freq_cnt) + 1)

            phase_dac_array.append(phase_cnt >> 5)
            freq_dac_array.append(freq_cnt_val)

        return (phase_dac_array, freq_dac_array)

    # =========================================================================
    # TX Control Functions
    # =========================================================================

    def tx_ser_reset(self, pipe_addr: int) -> None:
        """
        Reset TX serializer.

        Args:
            pipe_addr: PIPE register page address
        """
        self.device.write_bits(pipe_addr, 0x1E, 3, 1, 1)  # tx_ser_rst_man_en=1
        self.device.write_bits(pipe_addr, 0x1E, 2, 1, 1)  # ser_rst=1
        self.device.write_bits(pipe_addr, 0x1E, 2, 1, 0)  # ser_rst=0

    # =========================================================================
    # PRBS Control Functions
    # =========================================================================

    def prbs_set_mode(self, pipe_addr_list: List[int], prbs_mode: int) -> None:
        """
        Set PRBS mode for multiple PIPE ports.

        Args:
            pipe_addr_list: List of PIPE register page addresses
            prbs_mode: 
                PRBS mode 0, PRBS7
                PRBS mode 1, PRBS10
                PRBS mode 2, PRBS15
                PRBS mode 3, PRBS23
                PRBS mode 4, PRBS31
        """
        for pipe_addr in pipe_addr_list:
            self.device.write_bits(pipe_addr, 0x63, 1, 3, prbs_mode)
            self.device.write_bits(pipe_addr, 0x19, 3, 3, prbs_mode)

    def usb2_prbs_clear(self, utmi_addr_list: List[int]) -> None:
        """
        Clear USB2.0 PRBS error counters.

        Args:
            utmi_addr_list: List of UTMI register page addresses
        """
        for utmi_addr in utmi_addr_list:
            self.device.write_bits(utmi_addr, 0x30, 2, 1, 0)  # prbs_check_en=0
            self.device.write_bits(utmi_addr, 0x30, 3, 1, 1)  # prbs_check_clear=1
            self.device.write_bits(utmi_addr, 0x30, 3, 1, 0)  # prbs_check_clear=0
            self.device.write_bits(utmi_addr, 0x30, 2, 1, 1)  # prbs_check_en=1

    def usb3_prbs_clear(self, pipe_addr_list: List[int]) -> None:
        """
        Clear USB3.0 PRBS error counters.

        Args:
            pipe_addr_list: List of PIPE register page addresses
        """
        for pipe_addr in pipe_addr_list:
            self.device.write_bits(pipe_addr, 0x63, 4, 1, 1)  # prbs en=1
            self.device.write_bits(pipe_addr, 0x64, 7, 1, 1)  # prbs_compare en=1
            self.device.write_bits(pipe_addr, 0x63, 4, 1, 0)  # prbs en=0
            self.device.write_bits(pipe_addr, 0x64, 7, 1, 0)  # prbs_compare en=0
            self.device.write_bits(pipe_addr, 0x64, 7, 1, 1)  # prbs_compare en=1
            self.device.write_bits(pipe_addr, 0x64, 7, 1, 0)  # prbs_compare en=0
            self.device.write_bits(pipe_addr, 0x63, 4, 1, 1)  # prbs en=1
            self.device.write_bits(pipe_addr, 0x64, 7, 1, 1)  # prbs_compare en=1

    def read_usb3_prbs_errors(self, pipe_addr: int) -> int:
        """
        Read USB3.0 PRBS error count.

        Args:
            pipe_addr: PIPE register page address

        Returns:
            int: PRBS error count
        """
        a = self.device.read_reg(pipe_addr, 0x6C)
        b = self.device.read_reg(pipe_addr, 0x6B)
        c = self.device.read_reg(pipe_addr, 0x6A)

        return int(a) + int(b) * 256 + int(c) * 65536

    def read_usb2_prbs_errors(self, utmi_addr: int) -> Tuple[int, int]:
        """
        Read USB2.0 PRBS error count and length.

        Args:
            utmi_addr: UTMI register page address

        Returns:
            Tuple[int, int]: (error_count, length)
        """
        # Read length
        length_msb = self.device.read_reg(utmi_addr, 0x3B)
        length_lsb = self.device.read_reg(utmi_addr, 0x3A)
        length = length_msb * 256 + length_lsb

        # Read error
        err_0 = self.device.read_reg(utmi_addr, 0x36)
        err_1 = self.device.read_reg(utmi_addr, 0x37)
        err_2 = self.device.read_reg(utmi_addr, 0x38)
        err_3 = self.device.read_reg(utmi_addr, 0x39)
        error = err_3 * 16777216 + err_2 * 65536 + err_1 * 256 + err_0

        return (error, length)

    def check_usb3_prbs_with_break(self, pipe_addr: int, mins: int, unit: int) -> List:
        """
        Check USB3.0 PRBS with break on error.

        Args:
            pipe_addr: PIPE register page address
            mins: Number of minutes/iterations to check
            unit: Sleep time per iteration in seconds

        Returns:
            List: [error_count, check_result]
        """
        check_result = "pass"
        prbs_error = 0

        # Check PRBS constant
        prbs_constant_list = []
        for _ in range(10):
            prbs_constant_list.append(self.device.read_reg(pipe_addr, 0x69))

        prbs_constant = not all(x == prbs_constant_list[0] for x in prbs_constant_list)

        for _ in range(mins):
            prbs_error = self.read_usb3_prbs_errors(pipe_addr)

            if not prbs_constant:
                print("PRBS ALL equal, Need check, quit")
                check_result = "fail"
                break
            elif prbs_error < 10:
                time.sleep(int(unit))
            else:
                check_result = "fail"
                break

        return [prbs_error, check_result]

    def check_usb2_prbs_with_break(
        self, utmi_addr: int, mins: int, unit: int, length_expect: int = 512
    ) -> List:
        """
        Check USB2.0 PRBS with break on error.

        Args:
            utmi_addr: UTMI register page address
            mins: Number of minutes/iterations to check
            unit: Sleep time per iteration in seconds
            length_expect: Expected packet length

        Returns:
            List: [error_count, check_result, time_iterations]
        """
        check_result = "pass"
        time_i = mins * unit
        error = 0

        # Get max length from initial reads
        length_array = []
        for _ in range(20):
            _, length = self.read_usb2_prbs_errors(utmi_addr)
            length_array.append(length)
            time.sleep(0.1)

        max_length = max(length_array)

        for min_i in range(mins):
            error, length = self.read_usb2_prbs_errors(utmi_addr)
            length_diff = abs(length_expect - max_length)

            if error < 10 and length_diff < 10:
                time.sleep(int(unit))
            else:
                check_result = "fail"
                time_i = min_i
                break

        return [error, check_result, time_i]

    # =========================================================================
    # Eye Measurement Functions
    # =========================================================================

    def measure_eye_1d(self, cdr_addr: int) -> int:
        """
        Perform 1D eye measurement.

        Args:
            cdr_addr: CDR register page address

        Returns:
            int: Eye measurement value
        """
        # Save registers
        reg_backup = {
            0x09: self.device.read_reg(cdr_addr, 0x09),
            0x13: self.device.read_reg(cdr_addr, 0x13),
            0xBB: self.device.read_reg(cdr_addr, 0xBB),
            0xA0: self.device.read_reg(cdr_addr, 0xA0),
            0xA1: self.device.read_reg(cdr_addr, 0xA1),
            0xA2: self.device.read_reg(cdr_addr, 0xA2),
            0xA3: self.device.read_reg(cdr_addr, 0xA3),
            0xA4: self.device.read_reg(cdr_addr, 0xA4),
            0xA5: self.device.read_reg(cdr_addr, 0xA5),
            0xA6: self.device.read_reg(cdr_addr, 0xA6),
            0xAE: self.device.read_reg(cdr_addr, 0xAE),
            0x01: self.device.read_reg(cdr_addr, 0x01),
            0x3F: self.device.read_reg(cdr_addr, 0x3F),
            0xE0: self.device.read_reg(cdr_addr, 0xE0),
            0xF1: self.device.read_reg(cdr_addr, 0xF1),
        }

        try:
            # Configure for eye measurement
            self.device.write_bits(cdr_addr, 0x99, 0, 1, 1)  # enable Slicer eye clk
            self.device.write_bits(cdr_addr, 0x09, 3, 1, 1)  # enable d_e_check_en
            self.device.write_bits(cdr_addr, 0xBB, 7, 1, 1)  # DFE dis in track=1
            self.device.write_bits(cdr_addr, 0xBB, 6, 1, 1)  # enable EYE CDR follow
            self.device.write_bits(cdr_addr, 0xF1, 0, 1, 1)  # enable floor

            # Fix SSC eye meas bug
            self.device.write_bits(cdr_addr, 0x3F, 0, 1, 1)  # cdr rstb=1
            self.device.write_bits(cdr_addr, 0x3F, 1, 1, 1)  # cdr man rstb en=1
            self.device.write_bits(cdr_addr, 0xE0, 0, 1, 1)  # freqtrack_en=1
            self.device.write_bits(cdr_addr, 0xE0, 7, 1, 1)  # freqtrack_en man=1

            # Clear all EQ param loop
            self.device.write_reg(cdr_addr, 0xA0, 0x40)
            self.device.write_reg(cdr_addr, 0xA1, 0x00)
            self.device.write_reg(cdr_addr, 0xA2, 0x00)
            self.device.write_reg(cdr_addr, 0xA3, 0x00)
            self.device.write_reg(cdr_addr, 0xA4, 0x00)
            self.device.write_reg(cdr_addr, 0xA5, 0x00)
            self.device.write_reg(cdr_addr, 0xA6, 0x00)

            # Set fixed parameters
            self.device.write_reg(cdr_addr, 0xAE, 0x21)
            self.device.write_reg(cdr_addr, 0x01, 0x04)

            # Do FSM reset
            self.device.write_bits(cdr_addr, 0x3F, 3, 1, 1)  # man_en=1
            self.device.write_bits(cdr_addr, 0x3F, 2, 1, 1)  # reset=1
            self.device.write_bits(cdr_addr, 0x3F, 2, 1, 0)  # reset=0
            self.device.write_bits(cdr_addr, 0x3F, 3, 1, 0)  # man_en=0

            # Wait for stable
            time.sleep(0.1)

            # Read eye measurement
            eye_lsb = self.device.read_reg(cdr_addr, 0x38)
            eye_msb = self.device.read_reg(cdr_addr, 0x37)
            eye_value = eye_msb * 256 + eye_lsb

        finally:
            # Restore registers
            for addr, value in reg_backup.items():
                self.device.write_reg(cdr_addr, addr, value)

        return eye_value

    def measure_eye_1d_avg(self, cdr_addr: int, avg_time: int) -> Tuple[float, float]:
        """
        Perform 1D eye measurement with averaging.

        Args:
            cdr_addr: CDR register page address
            avg_time: Number of measurements to average

        Returns:
            Tuple[float, float]: (average_eye, valid_percentage)
        """
        eye_list = []

        for _ in range(avg_time):
            eye_value = self.measure_eye_1d(cdr_addr)
            if eye_value != 0:
                eye_list.append(eye_value)

        if eye_list:
            avg_eye = sum(eye_list) / len(eye_list)
        else:
            avg_eye = 0.0

        valid_per = (float(len(eye_list)) / avg_time) * 100

        return (avg_eye, valid_per)

    # =========================================================================
    # ADC Functions
    # =========================================================================

    def adc_measure_voltage(
        self, misc_addr: int, channel: int, meas_time: int = 30
    ) -> float:
        """
        Measure voltage using ADC.

        Args:
            misc_addr: Misc register page address
            channel: ADC channel to measure
            meas_time: Number of measurement samples

        Returns:
            float: Average voltage measured
        """
        # Configure ADC
        self.device.write_reg(misc_addr, 0x20, 0x08)  # ADC clkdiv ctrl
        self.device.write_reg(misc_addr, 0x21, 0x1F)  # ADC power on
        self.device.write_reg(misc_addr, 0x24, 0x0F)  # ADC sample ctrl
        self.device.write_reg(misc_addr, 0x22, channel)  # SEL channel

        # Take measurements
        vout_list = []
        for _ in range(meas_time):
            vout = (self.device.read_reg(misc_addr, 0x45) / 255) * 2
            vout_list.append(vout)
            time.sleep(0.1)

        # Calculate mean
        vout_mean = sum(vout_list) / len(vout_list) if vout_list else 0.0

        return vout_mean

    # =========================================================================
    # Debug Functions
    # =========================================================================

    def read_pipe_rameq_status(self, pipe_addr: int) -> Dict:
        """
        Read PIPE RAM EQ status.

        Args:
            pipe_addr: PIPE register page address

        Returns:
            Dict: Dictionary containing all status fields
        """
        lock_rb_list = []
        for i in range(13):
            self.device.write_bits(pipe_addr, 0xB8, 0, 4, i)
            lock_rb_msb = self.device.read_reg(pipe_addr, 0xBC)
            lock_rb_lsb = self.device.read_reg(pipe_addr, 0xBD)
            lock_rb_list.append(lock_rb_msb << 8 | lock_rb_lsb)

        result = {
            "i2c_tseq_lock_eq_cnt_rb": lock_rb_list[0],
            "i2c_tseq_lock_done_cnt_rb": lock_rb_list[1],
            "i2c_tseq_lock_err_cnt_rb": lock_rb_list[2],
            "i2c_tseq_lock_all_time_rb": lock_rb_list[3],
            "i2c_tseq_lock_eye_2d_est_rb": lock_rb_list[4],
            "i2c_tseq_lock_group_repeat_rb": (lock_rb_list[5] >> 12) & 15,
            "i2c_tseq_lock_temp_group_num_rb": (lock_rb_list[5] >> 7) & 31,
            "i2c_tseq_lock_group_num_rb": (lock_rb_list[5] >> 2) & 31,
            "i2c_tseq_lock_pl_lock_rb": (lock_rb_list[5] >> 1) & 1,
            "i2c_tseq_lock_pass_rb": lock_rb_list[5] & 1,
            "i2c_tseq_check_time_out_rb": self.device.read_bits(pipe_addr, 0xBE, 7, 1),
            "i2c_tseq_resp_time_out_rb": self.device.read_bits(pipe_addr, 0xBE, 6, 1),
            "i2c_ssvalid_rb": self.device.read_bits(pipe_addr, 0x7C, 7, 1),
        }

        return result
