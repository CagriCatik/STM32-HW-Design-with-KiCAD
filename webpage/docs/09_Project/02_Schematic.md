# Schematic

The schematic is hierarchical: a root sheet with four sub-sheets.

| Sheet | Content |
|---|---|
| `mcu.kicad_sch` | STM32F103C8T6, decoupling, crystal, BOOT0/RESET, user LED, USB series resistors |
| `power.kicad_sch` | Battery input, reverse protection, 5 V buck, USB-C, logic 5 V, 3.3 V LDO |
| `drive.kicad_sch` | Motor driver, servo outputs, receiver inputs, light outputs |
| `io.kicad_sch` | Cortex-Debug, IMU, Qwiic, UART, expansion header, mounting holes |

The sheets are generated from a declarative part list (`scripts/revc_schematic/gen.py`). Every pin gets a short
wire stub with a label, power symbol or no-connect flag, so the connectivity is defined in one place. `check.sh`
runs the ERC and compares the exported netlist with the intended one (74 nets).
Custom symbols (DRV8870, AO4407A) live in the project library `rcboard.kicad_sym`.

=== "MCU"
    ![MCU sheet](../assets/schematic/revc_mcu.svg)
=== "Power"
    ![Power sheet](../assets/schematic/revc_power.svg)
=== "Drive"
    ![Drive sheet](../assets/schematic/revc_drive.svg)
=== "IO"
    ![IO sheet](../assets/schematic/revc_io.svg)

## MCU core

- **Decoupling:** one 100 nF per VDD pin plus 4.7 µF bulk. VDDA has its own net behind a 600 Ω ferrite bead with
  10 nF + 1 µF. VBAT is tied to 3V3 through a solder jumper (cut it to run the RTC from a coin cell).
- **Clock:** 8 MHz crystal (C_L = 12 pF). Load capacitors: C = 2 · (C_L − C_stray) = 2 · (12 − 4) pF = 16 pF → 15 pF C0G.
  Oscillator margin per AN2867: g_m,crit ≈ 0.34 mA/V against 25 mA/V available, a margin of about 70 (≥ 5 required).
  The optional 32.768 kHz LSE is placed but not populated.
- **Boot:** BOOT0 has a 10 kΩ pull-down and a button to 3V3; BOOT1 (PB2) has a 10 kΩ pull-down. NRST has 100 nF
  and a reset button.

## Power

```text
XT30 ─► AO4407A (reverse protection) ─► VBAT ─┬─► TPS563201 ─► V5_SERVO (5.07 V / 3 A) ─► servos, receiver, lights
                                              ├─► DRV8870 VM
                                              └─► 33k/10k ─► PA4
V5_SERVO ─► B5819W ─┐
USB VBUS ─► PTC ─► B5819W ─┴─► +5V ─► AP2112K-3.3 ─► +3V3
```

- **Reverse protection:** P-channel MOSFET in the high side, gate to GND. With correct polarity the body diode
  conducts first, V_GS becomes −V_BAT and the FET turns fully on (38 mΩ). With the battery reversed the FET stays off.
- **TVS:** SMAJ15A after the FET clamps spikes from the motor and long battery leads.
- **Buck:** V_out = 0.768 V · (1 + 56 kΩ / 10 kΩ) = 5.07 V; 3.3 µH, 2 × 10 µF in, 3 × 22 µF out.
- **Logic supply:** the servo rail and USB are ORed with Schottky diodes, so USB never powers the servos and the
  buck is never back-fed. The LDO still has ~4.6 V input, enough for its 250 mV dropout.
- **Battery sense:** 12.6 V · 10 k / 43 k = 2.93 V at the ADC; firmware multiplies by 4.3.

## Motor driver

The DRV8870 drives the motor with IN1/IN2 PWM from TIM3 (20 kHz). Its current regulation trips at
I_TRIP = V_REF / (10 · R_ISEN) = 3.3 V / (10 · 0.1 Ω) = 3.3 A. Bulk capacitance: 100 µF electrolytic + 22 µF ceramic
next to VM. The exposed pad is soldered to GND with thermal vias into the inner GND plane.

## Servos, receiver, lights

- **Servo / ESC outputs:** signal, +5 V, GND (standard servo order). When an ESC is plugged in, cut its BEC red wire;
  the board already provides 5 V.
- **Receiver inputs:** on the 5 V tolerant pins PB6–PB8, each with 1 kΩ series resistance. The receiver is powered
  from the servo rail through the same header.
- **Lights:** AO3400A low-side switches with 100 Ω gate resistors and 100 kΩ pull-downs, PWM-dimmable from TIM3.

## IO

- **IMU:** LSM6DS3TR-C on I2C2 at 0x6A (SA0 pulled low), INT1/INT2 to PB12/PB13, two 100 nF capacitors.
- **Qwiic:** shares I2C2; 4.7 kΩ pull-ups behind a solder jumper.
- **UART:** GND, 5 V, TX, RX for a Bluetooth module or telemetry.
- **Expansion:** 2×5 header with 3V3, GND and the free GPIOs PA5, PA8, PA15, PB4, PB5, PB9, PB14, PB15.

## Checks

```bash
kicad-cli sch erc --severity-all --exit-code-violations stm32_prototype/stm32_prototype.kicad_sch
```

Result: 0 errors, 0 warnings. The netlist comparison in `scripts/revc_schematic/check.sh` matches all 74 nets.
