# PHY USB3 PRBS Test Spec
yfzhao 20260214

## DUT
GSU1K1 (i2c_port: 0, chip_addr: 0x58, type: ftdi)

## Test Purpose
USB3.0 5Gbps PRBS loopback test on single board

## Port Config
| Signal | Port | I2C Page |
|--------|------|----------|
| TX | USB3 Upstream | PipeUp CdrUp |
| RX | USB3 Upstream | PipeDp1 CdrDp1 |

## Test Parameters
- Pattern: PRBS15
- SSC: Disabled
- Check duration: 5 sec
- Eye samples: 10

## Test Flow

```
1. Chip Init
   - Reset all
   - Power up
   - Hub reset remove
   - PLL init (no SSC)
   - USB PHY init


2. PRBS Setup
   - :03-01 PIPE-up Tx/Rx PRBS:
   - :03-02 PIPE-dp1 Tx/Rx PRBS:
   - Set PRBS mode, set to PRBS15
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

## Notes
- Single board internal loopback
- CDR reset triggers EQ handshake
