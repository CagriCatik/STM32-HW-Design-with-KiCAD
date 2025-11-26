# V

## VSSA

VSSA is the analog ground reference in a mixed-signal PCB. It defines the 0 V reference for analog circuitry such as ADCs, DACs, and precision amplifiers. VSSA is typically kept isolated from digital ground (VSSD) to reduce noise coupling, then connected at a single low-impedance point to avoid ground loops. This configuration reduces digital switching noise propagation into sensitive analog domains.

## VDD

VDD is the positive supply rail for digital circuitry. In CMOS devices it represents the drain supply voltage for logic transistors. Common values include 1.2 V, 1.8 V, 3.3 V, and 5 V depending on technology. PCB layouts route VDD through power planes or wide traces with proper decoupling capacitors placed at each device pin to ensure stable voltage and minimize transient effects.
