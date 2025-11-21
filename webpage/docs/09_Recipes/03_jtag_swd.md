## Table of Contents

1. [JTAG and SWD](#jtag-and-swd)
   1.1 [JTAG Overview](#jtag-overview)
   1.2 [SWD Overview](#swd-overview)
   1.3 [JTAG vs SWD in Practice](#jtag-vs-swd-in-practice)

2. [Oscillators in PCB Design](#oscillators-in-pcb-design)
   2.1 [Role of the Oscillator](#role-of-the-oscillator)
   2.2 [External vs Internal Oscillator](#external-vs-internal-oscillator)
   2.3 [PCB Layout Considerations](#pcb-layout-considerations)

3. [Voltage Reference Points: VSS and VSSA](#voltage-reference-points-vss-and-vssa)
   3.1 [VSS (Digital Ground)](#vss-digital-ground)
   3.2 [VSSA (Analog Ground)](#vssa-analog-ground)
   3.3 [Grounding Strategies](#grounding-strategies)

4. [Voltage Rails: VDD and VDDA](#voltage-rails-vdd-and-vdda)
   4.1 [VDD (Digital Supply)](#vdd-digital-supply)
   4.2 [VDDA (Analog Supply)](#vdda-analog-supply)
   4.3 [Filtering and Isolation](#filtering-and-isolation)

5. [Decoupling in PCB Design](#decoupling-in-pcb-design)
   5.1 [Purpose of Decoupling Capacitors](#purpose-of-decoupling-capacitors)
   5.2 [Placement and Routing](#placement-and-routing)
   5.3 [Capacitance Selection and Stacking](#capacitance-selection-and-stacking)

6. [Ferrite Cores and Ferrite Beads](#ferrite-cores-and-ferrite-beads)
   6.1 [Operating Principle](#operating-principle)
   6.2 [Typical Use Cases](#typical-use-cases)
   6.3 [Selection Guidelines](#selection-guidelines)

7. [Crystal Oscillators in PCB Design](#crystal-oscillators-in-pcb-design)
   7.1 [How Crystal Oscillators Work](#how-crystal-oscillators-work)
   7.2 [Why Use a Crystal Oscillator](#why-use-a-crystal-oscillator)
   7.3 [Design and Layout Guidelines](#design-and-layout-guidelines)

8. [BOOT0 and NRST Pins on STM32](#boot0-and-nrst-pins-on-stm32)
   8.1 [BOOT0: Boot Mode Selection](#boot0-boot-mode-selection)
   8.2 [NRST: Reset Function](#nrst-reset-function)
   8.3 [Typical Hardware Implementations](#typical-hardware-implementations)

# 1. JTAG and SWD

## 1.1 JTAG Overview

JTAG (Joint Test Action Group) is a standard interface defined by IEEE 1149.1 for testing, programming, and debugging integrated circuits.

Key properties:

* Primary purpose:

  * Boundary scan testing of PCBs.
  * In-system programming of devices.
  * Debug access to internal registers and memory.
* Typical signals:

  * TCK: Test Clock.
  * TMS: Test Mode Select (controls TAP state machine).
  * TDI: Test Data In.
  * TDO: Test Data Out.
  * TRST (optional): Test Reset.
* Boundary scan:

  * Every I/O pin has a boundary scan cell.
  * These cells form a shift register that allows external tools to:

    * Drive pins to specific logic levels.
    * Sample pin states.
  * Very useful for manufacturing test and debugging connectivity issues (open/short circuits).
* Debugging:

  * For MCUs such as STM32, JTAG provides access to:

    * CPU halt, step, breakpoint control.
    * Memory read/write.
    * Flash programming.
* Disadvantages in MCU designs:

  * Requires 4 or 5 dedicated pins.
  * Pin count overhead is significant in small packages.
  * Routing several tightly-coupled signals can be more complex.

## 1.2 SWD Overview

SWD (Serial Wire Debug) is an ARM-specific, 2-wire alternative to JTAG for debugging and programming.

Key properties:

* Signals:

  * SWDIO: Bidirectional data line.
  * SWCLK: Clock signal.
  * Optional: RESET (NRST) line for full hardware reset.
* Functionality:

  * Provides a debug access port (DAP) to the ARM core.
  * Supports memory access, breakpoints, single-step, flash programming, etc.
  * Provides functionality comparable to JTAG for most firmware development tasks.
* Advantages:

  * Only 2 pins plus optional NRST.
  * Reduced pin usage is attractive for small packages.
  * Often faster and simpler to route.
  * Widely supported by modern debug probes (ST-Link, J-Link, etc.).
* Limitations:

  * Does not provide classic boundary scan in the same way as JTAG.
  * Less suitable for board-level production test than full JTAG chains.

## 1.3 JTAG vs SWD in Practice

* For firmware development on STM32:

  * SWD is usually preferred due to fewer pins and good tool support.
* For complex boards with many ICs:

  * JTAG chains may be used for manufacturing test and device programming.
* Typical STM32 board:

  * Provides a small 4- or 6-pin SWD header:

    * SWDIO, SWCLK, NRST, GND, VREF, optionally SWO (trace output).
  * JTAG pins may be multiplexed with SWD pins but often left unused.

# 2. Oscillators in PCB Design

## 2.1 Role of the Oscillator

The oscillator provides the fundamental timing reference for the microcontroller and many digital/communication subsystems.

Main functions:

* Clock generation:

  * Defines the execution speed of the CPU core.
  * Drives peripheral clocks (timers, communication interfaces, etc.).
* Timing accuracy:

  * Accurate time measurement.
  * Stable baud rates for UART, precise bit timing for CAN, USB, Ethernet, etc.
* System coordination:

  * Synchronizes operations across different modules and interfaces.

## 2.2 External vs Internal Oscillator

Most MCUs, including STM32, offer:

* Internal RC oscillator:

  * Integrated, no external components.
  * Lower accuracy and higher drift with temperature and voltage.
  * Suitable for non-critical timing or low-cost designs.
* External crystal or oscillator:

  * Uses a quartz crystal or a full oscillator module.
  * Much higher accuracy and stability.
  * Required or strongly recommended for:

    * USB, Ethernet, high-speed serial interfaces.
    * Precise timing or frequency generation.

Trade-offs:

* Internal RC:

  * Pros: Cheap, fewer components, simpler layout.
  * Cons: Limited accuracy, potentially unstable across conditions.
* External crystal:

  * Pros: High accuracy, low drift, low jitter.
  * Cons: Extra BOM cost, layout effort, sensitivity to PCB parasitics.

## 2.3 PCB Layout Considerations

For an external crystal:

* Place the crystal as close as possible to the MCU oscillator pins.
* Place load capacitors next to the crystal and close to the MCU pins.
* Keep traces:

  * As short as possible.
  * Symmetric and with minimal loop area.
* Avoid:

  * Running high-speed or noisy signals (e.g., switching power traces, fast digital buses) under or near the crystal and its traces.
* Connect the crystal ground (if present) to the closest ground reference, preferably analog or quiet ground region.

# 3. Voltage Reference Points: VSS and VSSA

## 3.1 VSS (Digital Ground)

VSS is the main ground reference for the digital domain.

Characteristics:

* Reference point for digital logic levels (0 V).
* All digital currents return through VSS.
* Typically forms the main ground plane on the PCB.
* Used by:

  * Core logic.
  * Digital I/O.
  * Digital peripherals.

## 3.2 VSSA (Analog Ground)

VSSA is the ground reference for the analog domain.

Characteristics:

* Used by:

  * ADC reference circuits.
  * DACs.
  * Analog front-ends such as op-amps connected to the MCU.
* Goal:

  * Provide a clean, low-noise reference for analog measurements.
  * Reduce coupling of digital switching noise into analog circuitry.

## 3.3 Grounding Strategies

Common strategies for dealing with VSS and VSSA:

* Single ground plane with local separation:

  * Use one continuous ground plane.
  * Route digital return currents away from the analog region.
  * Connect analog components near VSSA pin region.
* Star connection:

  * VSSA and VSS are connected at a single point (star point) close to the MCU.
  * Sometimes a small impedance (ferrite bead or small resistor) is used between VSSA and VSS.
* Guidelines:

  * Place analog components near the MCU analog pins (VSSA, VDDA, analog inputs).
  * Avoid routing high-current or high-frequency digital currents through the analog area.
  * Keep ADC reference and sensing circuits compact and shielded by ground.

# 4. Voltage Rails: VDD and VDDA

## 4.1 VDD (Digital Supply)

VDD powers all digital circuitry.

Typical properties:

* Voltage level, for example:

  * 3.3 V, 1.8 V, etc., depending on MCU.
* Supplies:

  * CPU core (sometimes via internal regulator).
  * Digital I/O pins.
  * Digital peripherals and internal logic.

## 4.2 VDDA (Analog Supply)

VDDA is the supply voltage for analog circuitry.

Typical properties:

* Often same nominal voltage as VDD (for example, both 3.3 V), but:

  * VDDA should be cleaner and better filtered.
* Powers:

  * ADC and DAC analog stages.
  * Internal voltage references.
  * Analog comparators, op-amps, etc. (if present).

## 4.3 Filtering and Isolation

To protect analog performance:

* Provide a dedicated RC or LC filter between VDD and VDDA:

  * Example: VDD -- ferrite bead -- VDDA.
  * Add local decoupling capacitors from VDDA to VSSA.
* Place decoupling capacitors:

  * As close as possible to the VDDA and VSSA pins.
* In precision designs:

  * A low-noise LDO regulator may generate VDDA separately from the main VDD.

# 5. Decoupling in PCB Design

## 5.1 Purpose of Decoupling Capacitors

Decoupling capacitors provide local energy storage and noise suppression.

Roles:

* Supply transient current:

  * When digital logic switches, instantaneous current demand rises.
  * Decoupling caps supply this current locally, preventing voltage droop.
* Reduce noise:

  * They shunt high-frequency noise to ground.
  * Improve power integrity and reduce EMI.
* Stabilize regulators:

  * Some regulators require specific output capacitance for stability.

## 5.2 Placement and Routing

Key rules:

* Distance:

  * Place each decoupling capacitor as close as physically possible to its associated power pin.
* Routing:

  * Use short, wide traces to connect cap to VDD/VDDA and to ground.
  * Prefer direct via-to-plane connections for ground.
* Per-pin decoupling:

  * Many MCUs require one capacitor per VDD pin (e.g., 100 nF).
* Ground reference:

  * Decoupling capacitors must connect to a solid, low-impedance ground plane.

## 5.3 Capacitance Selection and Stacking

Typical approach:

* Use multiple values in parallel:

  * Small capacitors (e.g., 100 nF, 10 nF) handle high-frequency transients.
  * Larger capacitors (e.g., 1 uF, 4.7 uF, 10 uF) handle lower-frequency load changes.
* Placement strategy:

  * Small caps very close to power pins.
  * Bulk caps per rail or per section of the board.
* Considerations:

  * Use X7R or similar dielectric for decoupling (stable over temperature, reasonable ESR).
  * Account for derating at operating voltage (effective capacitance may be lower than nominal).

# 6. Ferrite Cores and Ferrite Beads

## 6.1 Operating Principle

Ferrite beads are frequency-dependent resistive elements:

* At DC and low frequency:

  * Behave like a small inductor or very low impedance.
* At higher frequency:

  * Present significant impedance (mainly resistive).
  * Convert high-frequency noise energy into heat, thereby attenuating it.

## 6.2 Typical Use Cases

Main applications:

* EMI filtering on power lines:

  * Between noisy digital power and sensitive analog power (e.g., VDD to VDDA).
  * At board entry for external power lines (USB VBUS, external DC).
* Signal integrity in high-speed lines:

  * As part of common-mode chokes (for differential pairs).
* Common-mode noise suppression:

  * Placed on cable interfaces (USB, Ethernet, etc.).
* Noise suppression for RF paths:

  * Filter out unwanted harmonics or spurious emissions.

## 6.3 Selection Guidelines

When selecting a ferrite bead:

* Check impedance vs frequency curve:

  * Ensure high impedance at the relevant noise frequencies (for example, tens to hundreds of MHz).
* Current rating:

  * Must handle the DC current of the rail without saturation or overheating.
* DC resistance:

  * Should be low enough not to cause unacceptable voltage drop.
* Placement:

  * Place close to the noise source or at the domain boundary (for example, near VDDA pin).

# 7. Crystal Oscillators in PCB Design

## 7.1 How Crystal Oscillators Work

A quartz crystal behaves as a very high-Q resonant element:

* Mechanical resonance:

  * Applying an AC voltage causes the crystal to mechanically vibrate at its resonance frequency.
* Electrical model:

  * Equivalent circuit includes motional inductance, capacitance, resistance, and shunt capacitance.
* In an MCU:

  * The internal oscillator circuit plus the external crystal form a feedback loop.
  * The loop oscillates at the crystal resonance with very stable frequency.

## 7.2 Why Use a Crystal Oscillator

Reasons to use a crystal oscillator:

1. Precision:

   * Frequency error typically in the tens of ppm or better.
2. Stability:

   * Low drift with temperature and supply voltage.
3. Low jitter:

   * Critical for high-speed serial links and precise timing.
4. Regulatory and protocol requirements:

   * USB, Ethernet, and many RF protocols require accurate clock tolerances.
5. Long-term reliability:

   * Slow aging of frequency, suitable for long-lived systems.

Example use case:

* Wireless communication device:

  * Needs precise RF reference frequency.
  * Needs accurate symbol timing for modulation/demodulation.
  * Crystal ensures stable, repeatable operation over temperature and lifetime.

## 7.3 Design and Layout Guidelines

For MCU plus crystal:

* Load capacitors:

  * Choose according to crystal datasheet and MCU recommendations.
  * Effective load capacitance is a function of both capacitors and stray capacitances.
* Placement:

  * Place crystal and its load capacitors very close to the MCU oscillator pins.
* Routing:

  * Keep traces short and symmetric.
  * Avoid crossing other signals or power splits under the crystal area.
* Grounding:

  * Provide a clean ground reference under the crystal region if possible.
  * Avoid stitching vias that create loops for currents from noisy sections under the crystal.

# 8. BOOT0 and NRST Pins on STM32

## 8.1 BOOT0: Boot Mode Selection

BOOT0 selects the boot source when the MCU exits reset.

Typical modes (exact details depend on STM32 family):

* BOOT0 = 0 (low, GND):

  * Boot from main flash memory (normal user code).
* BOOT0 = 1 (high, VCC):

  * Enter system bootloader.
  * Allows programming via built-in interfaces (UART, USB, CAN, etc.).

Design considerations:

* Ensure BOOT0 has a defined level at power-on:

  * Typically via pull-down resistor to GND for normal operation.
  * Optionally accessible via jumper or button to pull high when bootloader is needed.
* During normal device operation in the field:

  * BOOT0 is usually fixed to GND to prevent unintended bootloader entry.

## 8.2 NRST: Reset Function

NRST is the hardware reset input/output (depending on family).

Core behaviors:

* Driving NRST low:

  * Forces the MCU into reset.
  * All registers and peripherals return to their reset state.
* Releasing NRST:

  * Starts the boot sequence, sampling BOOT0 (and sometimes BOOT1) to decide boot mode.
* Debug use:

  * Debug probes often control NRST to reliably reset the device and synchronize debug sessions.

Electrical details:

* Internal pull-up:

  * NRST is often internally pulled up, but external components are recommended.
* Glitch sensitivity:

  * NRST must be protected against noise spikes that could cause unintended resets.

## 8.3 Typical Hardware Implementations

Common circuitry around BOOT0 and NRST:

* BOOT0:

  * Pull-down resistor (for example, 10 kOhm) to GND.
  * Optional:

    * Pin broken out to jumper or header for forcing bootloader mode.
* NRST:

  * External pull-up resistor (for example, 10 kOhm) to VCC.
  * Low-pass filter elements:

    * Small capacitor (for example, 100 nF) from NRST to ground to filter short glitches.
  * Reset button:

    * Normally-open pushbutton between NRST and GND.
  * Connection to debug header:

    * NRST routed to SWD/JTAG connector so debugger can perform hardware reset.

Example sequence for using bootloader on STM32:

1. Set BOOT0 high (jumper to VCC).
2. Assert reset:

   * Press reset button (NRST to GND).
3. Release reset:

   * MCU samples BOOT0 high and enters system bootloader.
4. Program via chosen interface (UART, USB, etc.).
5. Set BOOT0 back to low (normal mode).
6. Reset again:

   * Device boots from flash with new firmware.
