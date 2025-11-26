# External High-Speed Crystal Oscillator, USB/SWD Routing, and Pin-Out Integration

This documentation provides a complete explanation of the external crystal oscillator subsystem, its load capacitors, grounding strategy, and supporting references. It also integrates the previously defined USB differential pair and SWD debug signals. Together, these additions finalize the electrical infrastructure required for accurate MCU timing, USB full-speed operation, and reliable firmware development with STM32CubeIDE.

import schematic from '@site/static/pcb/external_clock.png';

<div style={{ textAlign: 'center' }}>
  <img  
    src={schematic}
    alt="external_clock"
    style={{ width: '500px' }}
  />
</div>

---

## External High-Speed Crystal (HSE) Subsystem

### Crystal Symbol and Package

The added crystal (Y1) uses a **four-pin HC49/US or SMD 4-pad package**, commonly used for through-hole or low-profile surface-mount crystals.

The pin functions are:

* Pins **1** and **3**: Crystal terminals (oscillator input/output).
* Pins **2** and **4**: Grounded case pads, connected to GND for shielding and noise reduction.

Only pins 1 and 3 participate in the oscillation; pins 2 and 4 mechanically stabilize the package and provide EMI shielding.

### Microcontroller Oscillator Architecture

STM32 microcontrollers include the active components internally:

* An **inverter amplifier** between HSE_IN and HSE_OUT
* A **feedback resistor** inside the chip
* Bias and drive-strength control logic

External components only need to provide:

* The crystal resonator
* Two matched load capacitors

This matches ST’s recommended design documented in:
**Application Note AN2867 – “Oscillator design guide for STM32 microcontrollers.”**

### Schematic Implementation

The schematic correctly mirrors the recommended topology:

* **Y1** is connected between **PD0 (HSE_IN)** and **PD1 (HSE_OUT)**.
* **C10** and **C11** (10 pF each) connect from each crystal pin to ground.
* Pins **2** and **4** of the crystal footprint are tied to GND for shielding.
* No external series resistor is used (optional; rarely required).

This is the canonical STM32 HSE configuration.

---

## Selecting Load Capacitor Values

### Crystal Load Capacitance

The selected crystal specifies:

* Load capacitance (**CL**) = **10 pF**
* Frequency = 16 MHz
* Package = 4-pin SMD with grounded shell

### Stray Capacitance

PCB traces and MCU input pins introduce unavoidable stray capacitance, typically:

**3–5 pF total** from both sides combined.

### Load Capacitor Formula

For symmetrical load capacitors:

$$
[
C_{\text{load}} = \frac{C_L - C_{stray}}{2}
]
$$

Using values from the transcript:

* $(C_L = 10) pF$
* $(C_{stray} = 5) pF$ (worst-case assumption)

$$
[
C_{\text{load}} = \frac{10 - 5}{2} = 2.5 \text{ pF}
]
$$

However, manufacturers assume individual stray capacitance per side, so practical selection doubles that effective value. Designers generally choose **8–12 pF** per capacitor.

### Final Selection

The schematic uses:

* **C10 = 10 pF**
* **C11 = 10 pF**

These values match:

* The crystal’s load capacitance
* The expected PCB parasitics
* ST’s recommended values for 8–16 MHz crystals

This achieves accurate oscillation frequency and reliable startup.

---

## Notes on Optional Series Resistor

Some designs use a series resistor between the crystal and HSE_OUT to limit drive strength.
This is only required if:

* The crystal manufacturer specifies a maximum drive level, or
* The MCU overdrives the crystal at high temperatures.

STM32F103 rarely requires this resistor, so leaving it out is correct.

---

## USB Differential Pair Integration

The added labels:

* **USB_DM → PA11**
* **USB_DP → PA12**

define the USB full-speed (12 Mbps) differential signals.

KiCad recognizes differential pairs based on naming, enabling:

* Controlled impedance routing (≈ 90 Ω differential)
* Matched trace lengths
* Automated USB pair routing tools

This is essential for USB-C or USB-micro connectors used later in the design.

---

## SWD Debug Interface Integration

The added SWD pins:

* **SWDIO → PA13**
* **SWCLK → PA14**

provide the required interface for:

* ST-Link V2
* J-Link
* PyOCD
* OpenOCD

These pins must remain free of pull-ups, pull-downs, or alternate assignments.

Clear labeling ensures correct wiring to the SWD header during layout.

---

## Summary of the Added Crystal and Pin-Out Subsystem

The schematic additions include:

* A **16 MHz external crystal** connected to PD0/PD1
* Two **10 pF load capacitors** that match the crystal’s required load
* Grounded shielding pads for the crystal package
* USB differential pair labels for impedance-controlled routing
* SWD labels for programming and debugging
* A topology consistent with ST’s AN2867 oscillator design guide

Together, these components complete the clock generation, USB signaling, and debug infrastructure for the STM32F103C8Tx design.

## External 16 MHz Crystal Oscillator (HSE)

The new crystal subsystem is built around a **16 MHz parallel-resonant crystal** connected to the MCU's high-speed external oscillator pins:

* **PD0 → HSE_IN**
* **PD1 → HSE_OUT**

These pins are assigned automatically in STM32CubeIDE when the high-speed external clock is enabled.

### Y1 (16 MHz Crystal)

The crystal (Y1) forms the core of the MCU’s primary timing source. At 16 MHz, it provides sufficiently accurate timing for:

* USB full-speed operation
* UART/SPI baud-rate precision
* Deterministic MCU clocking
* Reliable PLL multiplication to system frequencies up to 72 MHz

The crystal is connected directly between HSE_IN and HSE_OUT.

### C10 and C11 (10 pF Load Capacitors)

Two load capacitors (C10 and C11) are connected from each crystal pin to ground.

Their values are tuned to match the crystal's specified load capacitance. Typical values range from **10–22 pF**, depending on PCB trace parasitics and crystal specifications. Here, **10 pF** provides appropriate loading for most 16 MHz crystals.

These capacitors ensure:

* Stable oscillation
* Correct frequency accuracy
* Consistent startup characteristics

### Crystal Ground Reference

The capacitors share a tight, local ground reference near the MCU. Proper placement minimizes loop area and reduces susceptibility to EMI. This matches STMicroelectronics’ recommended oscillator layout guidelines.

---

## USB Differential Pair Labeling

Two USB signals have now been properly named:

* **PA11 → USB_DM**
* **PA12 → USB_DP**

These labels ensure that KiCad recognizes the signals as a matched differential pair when routing to a USB-C connector.

Differential naming allows:

* Impedance-controlled routing (typically 90 Ω differential)
* Pair-length matching
* Scribble-free automatic D+/D- pairing during layout

This is mandatory for reliable USB 2.0 full-speed signaling.

---

## SWD Debug Interface Labeling

Two critical debug pins have been labeled:

* **PA13 → SWDIO**
* **PA14 → SWCLK**

These signals allow programming and debugging via an ST-Link V2 or similar SWD debugger. Net labels establish a one-to-one correspondence with STM32CubeIDE configuration and prevent accidental reuse of these pins for other functions.

Labeling ensures:

* Easy routing to a 4-pin SWD header
* Guaranteed compatibility with ST-Link tools
* Clean separation from general-purpose I/O

SWD is preferred over JTAG because it uses fewer pins and is directly supported by the STM32F1 series.

---

## Integration Summary

The newly added circuitry and labels achieve the following:

* Provide a stable 16 MHz clock source with proper load capacitors
* Enable USB full-speed operation through correctly named differential signals
* Reserve SWDIO/SWCLK for programming and debugging
* Maintain exact alignment with STM32CubeIDE pin assignments
* Prepare the design for correct routing in KiCad, including differential pairs and oscillator placement

These upgrades complete the microcontroller’s foundational hardware, ensuring precise timing, full USB capability, and robust debugging support.
