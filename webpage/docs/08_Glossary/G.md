# G

## GPIO

GPIO pins are versatile digital pins on a microcontroller that can be configured as either input or output. They allow the microcontroller to interact with external components, such as sensors, LEDs, buttons, and other peripherals.

- Input Mode: When a GPIO is configured as input, the microcontroller can read external signals (e.g., sensing a button press).
- Output Mode: When configured as output, the microcontroller can send signals to control other devices (e.g., turning an LED on or off).
- Pin Banks: STM32 microcontrollers group GPIO pins into banks (PA, PB, PC, etc.). Each bank may have several pins that can be individually controlled.

## GND

GND, or Ground, serves as the common reference point for all voltage levels in an electronic circuit. All current in the circuit must return to ground, making it essential for completing electrical circuits.

- Common Reference: Every voltage in the circuit is measured relative to ground. For example, if the VDD of a microcontroller is 3.3V, that voltage is relative to the GND.
- Return Path for Current: Ground also serves as the return path for current. In digital circuits, signals fluctuate between VDD and GND, and the integrity of this return path is crucial for stable circuit operation.



