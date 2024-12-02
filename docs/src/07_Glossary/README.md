# Glossary

## B

### Bulk Decoupling

### BOOT0 & BOOT1

## D

### DRC

### Decoupling

Decoupling refers to the practice of using capacitors (called decoupling capacitors) to filter out noise in power supply lines and provide instantaneous current when needed by a component. In electronic circuits, particularly for microcontrollers like STM32, the power supply can experience fluctuations and noise caused by various components switching on and off or due to interference from other parts of the circuit. Decoupling capacitors serve to "decouple" these unwanted fluctuations from sensitive devices.

When a component, such as a microcontroller, switches states or processes data, it demands a quick surge of current that the power supply may not be able to deliver instantly due to inductance or resistance in the supply lines. A decoupling capacitor, placed close to the device, acts as a local energy reservoir. It stores charge and releases it as needed, ensuring that the component gets the required current without causing dips or spikes in the power rail.

- Placement: Decoupling capacitors must be placed as close as possible to the power pins of the component. The typical value for these capacitors is 100nF (0.1µF).
- Types: For microcontrollers like STM32, it's common to use ceramic capacitors with low Equivalent Series Resistance **(ESR)** for decoupling.

## E

### ERC

### ESR

Equivalent Series Resistance (ESR) is the measure of the resistive losses in a capacitor when subjected to an alternating current (AC) voltage. It is the sum of all resistive components within the capacitor and is expressed in ohms (Ω).

- Voltage Stability: Low ESR minimizes voltage drops during current surges, ensuring stable voltage supply to components.
- Noise Filtering: A lower ESR allows capacitors to respond quickly to rapid changes in current, effectively filtering high-frequency noise.
- Power Dissipation: High ESR can lead to increased power loss in the form of heat, affecting capacitor and circuit reliability.
- Resonance Effects: ESR, in conjunction with Equivalent Series Inductance (ESL), can create resonant circuits that impact decoupling performance.

## F

## G

### GPIO

GPIO pins are versatile digital pins on a microcontroller that can be configured as either input or output. They allow the microcontroller to interact with external components, such as sensors, LEDs, buttons, and other peripherals.

- Input Mode: When a GPIO is configured as input, the microcontroller can read external signals (e.g., sensing a button press).
- Output Mode: When configured as output, the microcontroller can send signals to control other devices (e.g., turning an LED on or off).
- Pin Banks: STM32 microcontrollers group GPIO pins into banks (PA, PB, PC, etc.). Each bank may have several pins that can be individually controlled.

### GND

GND, or Ground, serves as the common reference point for all voltage levels in an electronic circuit. All current in the circuit must return to ground, making it essential for completing electrical circuits.

- Common Reference: Every voltage in the circuit is measured relative to ground. For example, if the VDD of a microcontroller is 3.3V, that voltage is relative to the GND.
- Return Path for Current: Ground also serves as the return path for current. In digital circuits, signals fluctuate between VDD and GND, and the integrity of this return path is crucial for stable circuit operation.


## N

### NRST

## V

### VSSA

### VDD

###