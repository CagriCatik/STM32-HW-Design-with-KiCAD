# Connecting the Crystal Oscillator in STM32 Microcontroller Circuits

Integrating a `crystal oscillator`  into your STM32 microcontroller circuit is a pivotal step in ensuring accurate timing, especially for high-speed communication protocols such as USB, CAN, and UART.

A `crystal oscillator` is a tiny electronic part that keeps time for a circuit. Inside it is a piece of quartz. Quartz has a useful property called the piezoelectric effect, which means it vibrates when you apply electricity. These vibrations happen at a very precise frequency, so the crystal can act like a super-accurate clock.

> In microcontrollers such as STM32, the crystal and two load capacitors form part of the external high speed oscillator (HSE). The internal amplifier in the MCU drives the crystal. This configuration yields a precise reference clock used for peripherals that need tight timing tolerance, such as USB (48 MHz domain), CAN, high baud UART, and accurate system time.

A schematic typically includes the crystal between `OSC_IN` and `OSC_OUT` pins, two capacitors referenced to ground sized to match the crystal load capacitance specification, a short symmetric layout, and a protective series resistor if needed for drive-level control. The board layout must minimize stray capacitance and loop area to maintain frequency accuracy and startup robustness.

This following part provides a guide on designing and implementing a `crystal oscillator` circuit using KiCad, covering fundamental principles, component selection, schematic design, and best practices.

## 1. The Role of the Crystal Oscillator in STM32 Microcontrollers

### Importance of a Precise Clock Source

- Accurate Timing: Critical for the reliable operation of microcontrollers, especially in applications involving high-speed data transmission.
- Stable Communication Protocols: Ensures consistency and reduces errors in protocols like USB, CAN, and UART.

### Internal vs. External Oscillators

- Internal Oscillator:
  - Advantages: Simplifies the design by reducing external components.
  - Disadvantages: Generally less accurate and stable, unsuitable for timing-critical applications.
- High-Speed External (HSE) Clock:
  - Advantages: Provides higher accuracy and stability.
  - Implementation: Utilizes a `crystal oscillator`  connected to the HSE pins (OSC_IN and OSC_OUT) on the STM32 microcontroller.

### Typical Crystal Oscillator Circuit Components

- Crystal: Typically a 16 MHz component connected between OSC_IN and OSC_OUT.
- Load Capacitors: Stabilize the oscillation frequency, ensuring accurate timing.
- Optional Feedback Resistors: May be used for controlling signal distortion.

## 2. Crystal Package Types and Symbol Selection in KiCad

### Crystal Oscillator Package Configurations

- Two-Pin Configuration:
  - Common Usage: Widely used due to simplicity.
  - Applications: Suitable for most standard `crystal oscillator`  requirements.

- Four-Pin Configuration:
  - Enhanced Stability: Grounding additional pins can improve signal stability and reduce electromagnetic interference (EMI).
  - Use Case: Preferred in environments where noise reduction is critical.

### Selecting the Crystal Symbol in KiCad

1. Accessing Symbols:
   - Navigate to the Add Symbol tool within KiCad’s schematic editor.

2. Searching for Crystal Symbols:
   - Enter "Crystal" in the symbol library search bar.

3. Choosing the Appropriate Symbol:
   - Two-Pin Crystal: Select for simpler designs.
   - Four-Pin Crystal: Opt for enhanced stability and noise reduction.

4. Placing the Symbol:
   - Position the crystal symbol near the HSE_IN and HSE_OUT pins of the STM32 microcontroller on the schematic for logical layout and ease of routing.

### Pin Configuration for a Four-Pin Crystal

- Pins 1 and 3:
  - Function: Connect to HSE_IN (OSC_IN) and HSE_OUT (OSC_OUT) on the STM32.
  
- Pins 2 and 4:
  - Function: Grounded to enhance stability and minimize electromagnetic interference.

## 3. Understanding the Crystal Circuit Design

### Built-in Microcontroller Features

- Inverters and Feedback Resistors:
  - Integrated into the STM32, these components assist in forming a stable oscillation circuit.

### External Components Required

- Load Capacitors:
  - Purpose: Stabilize the oscillation frequency.
  - Selection Criteria: Based on crystal load capacitance and PCB stray capacitance.

- Optional Feedback Resistors:
  - Function: Limit signal distortion.
  - Consideration: Often omitted unless specific distortion control is required.

### Typical Crystal Oscillator Circuit Layout

- Crystal Connection:
  - Between HSE_IN (PD0) and HSE_OUT (PD1) pins of the STM32.

- Load Capacitors:
  - Two identical capacitors connected from each crystal pin to ground.

- Feedback Resistor:
  - Optional series resistor connected to manage signal integrity.

### External Components: Load Capacitors

- Role in Oscillation:
  - Ensure the crystal oscillates at its designated frequency by providing necessary capacitive loading.

- Determining Capacitor Values:
  - Based on the crystal’s specified load capacitance and the PCB’s stray capacitance.

## 4. Application Note AN2867: Oscillator Design for STM32

STMicroelectronics' Application Note AN2867 serves as an essential reference for designing reliable `crystal oscillator`  circuits for STM32 microcontrollers.

### Key Guidelines from AN2867

1. Crystal Load Capacitors:
   - Critical for stabilizing oscillation.
   - Work in conjunction with the STM32's internal oscillator circuitry to generate a stable clock signal.

2. Stray Capacitance Considerations:
   - Arises from PCB traces and nearby components.
   - Typically ranges between 3-5 pF.
   - Must be accounted for when calculating load capacitor values.

3. Feedback Resistor Usage:
   - Generally optional.
   - May be included to prevent overdriving the crystal and reduce distortion.
   - Many designs operate effectively without it, simplifying the circuit.

### Best Practices

- Adherence to Guidelines:
  - Following AN2867 ensures reliable oscillator performance and minimizes design errors.
  
- Component Selection:
  - Carefully choose capacitors and resistors based on the application requirements and guidelines provided.

## 5. Calculating the Load Capacitor Values

Accurate calculation of load capacitors is essential for ensuring the crystal oscillates at the desired frequency.

### Load Capacitor Calculation Formula

$$
C_{load} = \frac{C_{crystal} - C_{stray}}{2}
$$

- C_crystal: Load capacitance specified in the crystal's datasheet (typically 10-20 pF).
- C_stray: Estimated stray capacitance from the PCB (typically 3-5 pF).

### Example Calculation

Given:

- Crystal Load Capacitance (C_crystal): 10 pF
- Stray Capacitance (C_stray): 5 pF

Calculation:

$$
C_{load} = \frac{10 \, \text{pF} - 5 \, \text{pF}}{2} = 2.5 \, \text{pF}
$$

Implementation:

- Use two 2.5 pF capacitors connected from each crystal pin to ground.
- Alternatively, if 2.5 pF capacitors are not readily available, use the nearest standard value (e.g., 3 pF) and adjust as necessary.

### Steps in KiCad to Add Load Capacitors

1. Add Capacitors:
   - Select Add Symbol and search for "capacitor".

2. Choose Appropriate Capacitors:
   - Select capacitors with the calculated value (e.g., 2.5 pF or 3 pF).

3. Place Capacitors on the Schematic:
   - Position one capacitor connected to HSE_IN.
   - Position the second capacitor connected to HSE_OUT.

4. Connect to Ground:
   - Ensure the other ends of both capacitors are connected to GND.

### Crystal Circuit Without Feedback Resistor

- Simplified Design:
  - Omit the feedback resistor unless specific conditions necessitate its inclusion.
  
- Advantages:
  - Reduced component count.
  - Simplified routing and potentially lower cost.

- Verification:
  - Consult AN2867 to confirm that omitting the feedback resistor is suitable for your specific application.

## 6. Connecting the Crystal in KiCad

### Steps to Connect the Crystal to the STM32

1. Connect Pin 1 of the Crystal:
   - Link to the HSE_IN pin (PD0) on the STM32 microcontroller.

2. Connect Pin 3 of the Crystal:
   - Link to the HSE_OUT pin (PD1) on the STM32 microcontroller.

3. Ground Pins 2 and 4 (Four-Pin Package):
   - Connect to GND to minimize noise interference and enhance stability.

### Routing and Naming the Net Labels

- Net Labeling:
  - Assign clear and consistent net labels to facilitate PCB layout and troubleshooting.
  
- Recommended Labels:
  - HSE_IN: For connections to the HSE_IN (OSC_IN) pin.
  - HSE_OUT: For connections to the HSE_OUT (OSC_OUT) pin.

- Schematic Clarity:
  - Ensure that all connections are logically organized and labeled to prevent confusion during the PCB design phase.

### Best Practices for Routing

- Minimize Trace Lengths:
  - Keep traces between the crystal and STM32 pins as short as possible to reduce inductance and potential signal integrity issues.

- Avoid Routing Near High-Frequency Signals:
  - Prevent interference by keeping the crystal circuit away from other high-speed or high-frequency signals on the PCB.

- Use Ground Planes:
  - Implement ground planes to provide a low-impedance path for return currents, enhancing signal stability.

## 7. Reviewing the Schematic for the Crystal Circuit

After integrating all components, it is crucial to thoroughly review the schematic to ensure correctness and reliability.

### Schematic Components Overview

- `crystal oscillator` :
  - Connected between PD0 (HSE_IN) and PD1 (HSE_OUT) of the STM32.

- Load Capacitors:
  - Two 10 pF capacitors connected from each crystal pin to GND.

- Grounded Pins (Two and Four):
  - Grounded to reduce noise and enhance signal stability.

### Verification Checklist

1. Component Placement:
   - Ensure all components (crystal, capacitors, resistors) are correctly placed and oriented.

2. Net Connections:
   - Confirm that all connections align with the intended net labels (e.g., HSE_IN, HSE_OUT).

3. Value Accuracy:
   - Verify that all component values, especially load capacitors, match the calculated requirements.

4. Ground Connections:
   - Check that all ground connections are properly routed and connected to the common ground plane.

5. Symbol Accuracy:
   - Ensure that the correct symbols (two-pin or four-pin crystal) are used based on the selected crystal package.

## 8. Validating the Crystal Circuit

Prior to proceeding to PCB layout and manufacturing, validate the `crystal oscillator`  circuit to prevent potential issues during operation.

### Validation Steps

1. Check Net Names:
   - Ensure all nets are labeled correctly and consistently (e.g., HSE_IN, HSE_OUT).

2. Load Capacitor Verification:
   - Cross-reference the calculated load capacitors with the crystal's datasheet to ensure compliance.

3. Ground Connections:
   - Confirm that all ground connections for the crystal and capacitors are correctly routed and connected to the ground plane.

4. Component Footprints:
   - Verify that all components have the correct footprints assigned for PCB layout.

5. Electrical Rules Check (ERC):
   - Run ERC in KiCad to identify and rectify any schematic errors or connectivity issues.

6. Peer Review:
   - Have another engineer or team member review the schematic for additional verification.

### Troubleshooting Common Issues

- Oscillation Failure:
  - Re-examine load capacitor values and connections.
  - Ensure that the crystal is compatible with the microcontroller.

- Noise and Interference:
  - Improve grounding and shielding.
  - Adjust component placement to minimize electromagnetic interference.

- Incorrect Frequency:
  - Double-check crystal specifications and load capacitor calculations.

## Conclusion

Integrating a `crystal oscillator`  into your STM32 microcontroller design is fundamental for achieving precise and stable timing, which is essential for high-speed communication protocols and other time-critical applications. By meticulously selecting and placing the `crystal oscillator`  and its associated components in KiCad, and adhering to the guidelines outlined in Application Note AN2867, you ensure a reliable and optimized design.

### Key Takeaways

- Symbol Selection: Choose the appropriate crystal symbol in KiCad based on the package type.
- Load Capacitors: Accurately calculate and implement load capacitors to stabilize oscillation.
- Schematic Integrity: Maintain clear and consistent net labeling and grounding practices.
- Validation: Thoroughly review and validate the schematic to prevent design flaws.

With a well-designed `crystal oscillator`  circuit, your STM32 microcontroller will operate with a stable and accurate clock source, enabling robust performance in high-speed and timing-sensitive applications.
