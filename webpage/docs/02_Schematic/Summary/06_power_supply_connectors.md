# Power Supply and Connectors

---

## Choosing the 3.3 V regulator

| Property | AMS1117-3.3 (course example) | AP2112K-3.3 (used on the board) |
|---|---|---|
| Dropout | ~1.1 V | ~0.25 V at 600 mA |
| Quiescent current | ~5 mA | ~55 µA |
| Output capacitor | needs tantalum/ESR in a window | stable with ceramic capacitors |
| Package | SOT-223 | SOT-23-5 |

With a 5 V input reduced by a Schottky diode (~4.6 V), the AMS1117 leaves almost no headroom. The AP2112K works
comfortably and the small SOT-23-5 package saves space. Capacitors: 1 µF at the input, 1 µF + 10 µF at the output,
EN tied to VIN.

---

## Higher input voltages: buck converter

A linear regulator turns the voltage difference into heat: P = (V_in − V_out) · I. From a 3S LiPo (12.6 V) to 5 V at
1 A that is 7.6 W, far too much for a small package. The RC controller therefore uses a **synchronous buck
converter** (TPS563201, 3 A) for its 5 V servo rail and keeps the LDO only for the 3.3 V logic.

Buck layout rules: input capacitors directly at VIN/GND, short switch node, inductor next to the IC, feedback divider
away from the inductor.

---

## Status LEDs

* **Power LED** on 3.3 V with a resistor for 1–2 mA.
* **User LED** on PC13, low-active (LED from 3.3 V through the resistor into the pin). PC13 may only sink about
  3 mA, so use 1 kΩ (~1.3 mA with a red LED).
* Use LEDs whose forward voltage fits the rail: a red LED (~2 V) works at 3.3 V, a "3.3 V" green or blue LED does not.

---

## Connectors

| Connector | Pins | Notes |
|---|---|---|
| SWD (Cortex-Debug 10-pin, 1.27 mm) | VTref, SWDIO, SWCLK, SWO, nRESET, GND | fits ST-Link V3 and J-Link directly |
| SWD 1×4, 2.54 mm | 3.3 V, SWDIO, SWCLK, GND | for low-cost ST-Link clones |
| UART | GND, 5 V, TX, RX | USART1 (PA9/PA10), also the system bootloader |
| Qwiic / STEMMA QT (JST-SH 4-pin) | GND, 3.3 V, SDA, SCL | I²C, 4.7 kΩ pull-ups (cuttable) |

I²C pull-ups: 4.7 kΩ is right for 100/400 kHz on a short bus. 1.5 kΩ, as sometimes suggested, is stronger than
needed and wastes current.

---

## Checklist

* [x] Regulator dropout fits the lowest input voltage
* [x] Input and output capacitors per datasheet, close to the pins
* [x] Every connector has GND and a clearly defined supply pin
* [x] PWR_FLAG on supply nets without a driving output (for a clean ERC)
