# USB Interface

The STM32F103 has a full-speed (12 Mbit/s) USB device peripheral on PA11 (D−) and PA12 (D+). This page
summarises what the schematic needs around it.

---

## Connector

* **USB-C receptacle, USB 2.0 only** (16-pin, e.g. HRO TYPE-C-31-M-12). Both rows of the connector carry the data
  pair: connect A6 and B6 to D+, A7 and B7 to D−, so the plug works in both orientations.
* **CC1 and CC2:** one **5.1 kΩ resistor to GND on each pin** (never shared). They mark the board as a sink; without
  them a USB-C to USB-C cable does not switch VBUS on.
* **SBU1/SBU2:** not used, no-connect flags.
* **Shield:** to GND through 1 MΩ ∥ 4.7 nF. This drains static charge without creating a hard ground loop through
  the cable shield.

---

## Protection

* **ESD:** a USBLC6-2SC6 directly behind the connector clamps D+, D− and VBUS.
* **Over-current:** a 500 mA PTC fuse in VBUS protects the host port.
* **Back-feeding:** a Schottky diode from the fused VBUS to the board's 5 V rail prevents a second supply (battery,
  header pin) from pushing current into the host.

---

## Signal path

* **D+ pull-up:** the STM32F103 has **no internal pull-up**. A **1.5 kΩ resistor from D+ (PA12) to 3.3 V** tells
  the host that a full-speed device is attached. Without it the board never enumerates.
* **Series resistors:** footprints for 0–22 Ω resistors in D+ and D− close to the MCU. Fit 0 Ω first; 22 Ω only if
  measurements show ringing.
* **Clock:** USB needs exactly 48 MHz. With an 8 MHz crystal: PLL × 9 = 72 MHz, USB prescaler 1.5 → 48 MHz.
  The internal HSI oscillator is not accurate enough for USB.

---

## Layout reminders

* Keep the pair short, routed together (0.3 mm tracks, 0.15 mm gap on a 4-layer board) over an unbroken ground plane.
* At 12 Mbit/s length matching is not critical; a few millimetres of mismatch is fine.
* ESD protection right at the connector, then the series resistors, then the MCU, in a straight line.

---

## Checklist

* [x] D+ on PA12, D− on PA11 (not swapped)
* [x] 1.5 kΩ pull-up on D+
* [x] 5.1 kΩ on CC1 and on CC2
* [x] ESD protection at the connector
* [x] 48 MHz USB clock from the crystal (HSE), not from the HSI
