# Bring-up Checklist

Bring a new board up one block at a time, so a fault cannot damage the next block.

## 1. Visual check and shorts (no power)

- Check the orientation of U1 (dot), the DRV8870, the electrolytic capacitors (stripe = minus) and the diodes.
- Measure the resistance from GND to `+3V3`, `+5V`, `V5_SERVO` and `VBAT`. None should be a short (a few kΩ or more
  is normal; the capacitors charge from the meter).

## 2. USB only

- Connect USB-C, no battery. The power LED lights; measure 3.3 V ± 3 % at the LDO output.
- The servo rail stays off (the Schottky OR does not feed it from USB).
- Connect an ST-Link to the Cortex-Debug header and read the chip ID:

```bash
STM32_Programmer_CLI -c port=SWD
```

- Flash the bring-up firmware (see [Firmware](05_Firmware.md)). The PC13 LED blinks, the board enumerates as a
  virtual COM port, and the status line shows `IMU=0x6A`.
- Test both orientations of the USB-C plug.

## 3. Battery, current-limited

- Use a lab supply instead of a LiPo: 7.4 V, current limit 200 mA. Reverse the leads once on purpose; nothing may
  happen (reverse protection).
- With correct polarity: `V5_SERVO` = 5.07 V, `VBAT` in the status line within a few percent of the supply.

## 4. Servos and receiver

- Plug one servo into SERVO1; it moves to centre. `s1 1000` / `s1 2000` move it to the ends.
- Plug a receiver into RC1–RC3; the status line shows the stick positions in µs.

## 5. Motor

- Raise the supply current limit to 3 A, connect a small brushed motor.
- `m 20`, `m -20`, `m 0`: forward, reverse, coast. At stall the DRV8870 limits the current to about 3.3 A.

## 6. Lights and clock

- `l1 100` / `l2 50`: LEDs on the light outputs.
- Optional: output the HSE on MCO (PA8, expansion header) and check 8 MHz with a scope.
