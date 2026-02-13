# USB3 PRBS Test Spec


## DUT
GSU1K1 (i2c_port: 0, chip_addr: 0x58, type: ftdi)


## Test Purpose
USB3.0 5Gbps PRBS7 loopback test on single board

## Port Config
| Signal | Port | I2C Page |
|--------|------|----------|
| TX | USB3 Upstream | PipeUp (0x31) |
| RX | USB3 Upstream | CdrUp (0x10) |

## Test Parameters
- Pattern: PRBS7 (Mode 2)
- SSC: Disabled
- Check duration: 5 sec
- Eye samples: 10

## Test Flow

```
1. Chip Init
   - Reset all
   - Power up
   - PLL init (no SSC)
   - USB PHY init
   - Hub reset remove

2. PRBS Setup
   - PIPE PRBS mode enable
   - Set PRBS7 pattern
   - TX serializer reset

3. CDR Config
   - Write 0x0F to CdrUp:0x9E
   - CDR reset
   - Wait 500ms

4. PRBS Check
   - Clear error counter
   - Check errors for 5 sec
   - Pass: < 1 error

5. Measurements
   - Eye height (10 samples avg)
   - CDR phase/freq DAC (1000 samples)
```

## Pass Criteria
| Item | Criteria |
|------|----------|
| PRBS Errors | 0 errors in 5 sec |
| Eye Height | > TBD mV |
| CDR Lock | freq_dac stable |

## Notes
- Single board internal loopback
- CDR reset triggers EQ handshake
