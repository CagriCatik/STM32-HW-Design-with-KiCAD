# Power and Decoupling Network

The schematic defines the STM32F103C8T6 power subsystem with correct isolation between digital and analog domains, proper decoupling topology, and an LC-filtered analog supply. The circuit implements the recommended STM32F1 power architecture in a clean, stable configuration. This document also summarizes the step-by-step process used to build the schematic in KiCad.

import schematic from '@site/static/pcb/schematic_stm32_decoupling.png';

## Decoupling

<div style={{ textAlign: 'center' }}>
  <img  
    src={schematic}
    alt="decoupling"
    style={{ width: '500px' }}
  />
</div>

---

## 1. Tooling and project setup

1. Create a new project: `File -> New Project`, choose a name and location.
2. Open the schematic editor.
3. Basic navigation:

   * Middle mouse button: pan
   * Scroll wheel: zoom
   * Right click: context menu
   * `Esc`: cancel current command

The first task in any PCB design is schematic capture: placing symbols (components) and wiring them together.

---

## 2. Placing the STM32 microcontroller

1. Click `Add Symbol` in the right toolbar.
2. In the symbol chooser, search for `STM32F103C8Tx`.
   * `STM32` is the family.
   * `F1` denotes the performance and feature line.
   * The trailing letters (for example `C8T6`) encode package, flash, and RAM size.
3. Place the `STM32F103C8Tx` symbol roughly in the center of the schematic.
4. Optionally:
   * Align the reference designator (`U1`) at the top of the symbol.
   * Edit the value field to the exact part number (for example `STM32F103C8T6`).

The MCU symbol groups pins into:

* Power pins: `VBAT`, `VDD`, `VDDA`, `VSS`, `VSSA`
* Configuration and reset: `BOOT0`, `NRST`
* GPIO banks: `PAx`, `PBx`, `PCx`, `PDx`

The rest of the schematic builds the infrastructure this device requires to run reliably: power rails, grounds, clocks, connectors, and so on. This document focuses on power and decoupling.

---

## 3. Ground system

### Symbol placement

1. Use `Add Power Port` and choose the `GND` symbol.
2. Place a single `GND` symbol below the MCU.
3. Optionally hide the text label if there is only one ground domain in the design.

### Connections

Use the wire tool (`W`) to connect:

* All `VSS` pins to the ground node
* `VSSA` (analog ground) to the same ground node

Rationale:

* `VSS` is the digital ground reference.
* `VSSA` is the analog ground reference for the ADC and DAC.
* For STM32F1, both must be tied together. Layout can implement this as a local star point or short trace, but logically they share a single ground net.

---

## 4. Power distribution

The MCU is powered from a 3.3 V rail. Two related rails are used.

### Digital rail (+3.3 V)

1. Add a `+3.3V` power symbol and place it near `VBAT` and the `VDD` pins.
2. Connect `VBAT` to `+3.3V` when no backup battery is used and the internal RTC is not powered from a separate source.
3. Connect both `VDD` pins to the same `+3.3V` node.

Voltage range for this STM32F1 variant is roughly 2.7 V to 3.6 V; 3.3 V is the standard operating point.

### Analog rail (+3.3VA)

1. Introduce a separate net label, for example `+3.3VA`, for the analog supply.
2. Derive this rail from the digital 3.3 V rail through a ferrite bead and its own decoupling network, as described in section 6.

---

## 5. Digital supply decoupling

### Topology

Five capacitors (C1 through C5) are connected in parallel between the digital +3.3 V node and ground:

* Several 100 nF capacitors
* One 10 nF capacitor

Each VDD and VBAT pin should have a local 100 nF capacitor. In addition, a bulk capacitor provides extra energy storage.

### Implementation steps in KiCad

1. Add a capacitor symbol (`C`) and place it near a VDD pin.
2. Set its value to `100n`.
3. Wire one side to `+3.3V` at the corresponding pin, the other side to the ground node.
4. Copy (`C`, then `Ctrl+V`) this capacitor for each VDD and VBAT pin.
5. Add one bulk capacitor (for example `10uF`) between `+3.3V` and `GND` close to the MCU symbol.

### Purpose

* The 100 nF capacitors present a low impedance at high frequencies and handle fast current edges when the core and I O switch.
* The bulk capacitor stabilizes the local rail against slower transients and cable inductance.

Placement rule: these capacitors must be placed as close as possible to the associated pins in the PCB layout, with short, wide traces to the power and ground planes.

---

## 6. Analog supply decoupling and filtering

The analog supply is more sensitive to noise, especially for ADC and DAC performance. The schematic uses an LC type filter plus local decoupling.

### Network structure

1. A ferrite bead FB1 (120 ohms at 100 MHz) connects the digital +3.3 V rail to the analog rail.
2. On the analog side of FB1:

   * C8: 1 uF between `+3.3VA` and ground (right after the bead)
   * C6: 10 nF between `VDDA` and ground
   * C7: 1 uF between `VDDA` and ground

`VDDA` is tied to the `+3.3VA` rail, which is the output of the ferrite bead filter.

### Rationale

* The ferrite bead presents high impedance at high frequency, blocking digital switching noise from entering the analog domain.
* C8 provides bulk decoupling for the entire analog rail.
* The C6 and C7 pair at VDDA provides both high frequency and low frequency local charge storage directly at the pin.

This topology matches STMicroelectronics reference schematics for STM32F1 devices.

---

## 7. Pin configuration status

On this schematic page, GPIO pins are intentionally left unconnected, because the focus is solely on the power system.

Two important pins are present but not fully constrained yet:

* `BOOT0`: must be pulled down, typically with a 10 k resistor, to ensure normal boot from flash.
* `NRST`: should be pulled up, typically with a 10 k resistor, and may have an additional 100 nF capacitor to ground for reset pulse shaping and noise immunity.

These constraints are usually implemented on the same page or on a dedicated reset and configuration page.

---

## 8. Design rules checklist

The implemented network satisfies the key power integrity rules for a basic STM32F103C8T6 design:

* All digital supply pins (VDD, VBAT) share a low impedance 3.3 V node.
* Each VDD and VBAT pin has a dedicated 100 nF ceramic capacitor to ground.
* A bulk capacitor around 10 uF is placed on the digital 3.3 V rail near the MCU.
* VDDA is supplied from 3.3 V through a ferrite bead and has its own 10 nF and 1 uF capacitors.
* An additional 1 uF capacitor is placed immediately after the ferrite bead on the analog rail.
* VSS and VSSA are tied together to a single ground reference.
* The schematic clearly distinguishes digital (`+3.3V`) and analog (`+3.3VA`) rails with separate net names.

This structure is directly suitable as the power and decoupling foundation for a Blue Pill style STM32F103 board.
