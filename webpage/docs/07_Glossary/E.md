# E

## ERC

## ESR

Equivalent Series Resistance (ESR) is the measure of the resistive losses in a capacitor when subjected to an alternating current (AC) voltage. It is the sum of all resistive components within the capacitor and is expressed in ohms (Ω).

- Voltage Stability: Low ESR minimizes voltage drops during current surges, ensuring stable voltage supply to components.
- Noise Filtering: A lower ESR allows capacitors to respond quickly to rapid changes in current, effectively filtering high-frequency noise.
- Power Dissipation: High ESR can lead to increased power loss in the form of heat, affecting capacitor and circuit reliability.
- Resonance Effects: ESR, in conjunction with Equivalent Series Inductance (ESL), can create resonant circuits that impact decoupling performance.



# STM32 uC Decoupling

## Introduction

The process of creating a PCB design step by step will be walked through in this guide. Whether you are a beginner or an experienced hardware designer, detailed instructions will be provided in this document to help you achieve your goals.

### 2. Create a New Project

- Launch the software after installation.
- Navigate to File > New Project.
- Provide a name for your project and create it.

## Drawing the Schematic

### 1. Open the Schematic Editor

- Once your project is created, access the schematic editor.

### 2. Place Components

- Begin by placing schematic symbols or components onto the blank schematic page.
- Start with the main component, in this case, the eSIM32 microcontroller.

### 3. Connect Components

- Connect the components using appropriate connections based on the schematic.
- Ensure proper alignment and organization of the components on the schematic page.

### 4. Power and Ground Connections

- Add ground symbols (GND) and connect them to all ground pins (VSS).
- Incorporate power ports for +3.3V and VBAT if necessary and connect them to relevant pins.

### 5. Decoupling Capacitors

- Place 100nF capacitors per VDD and VDDA pins for decoupling.
- Include a bulk decoupling capacitor (e.g., 10uF) close to the microcontroller.

### 6. Additional Filtering for Analog Sections

- Add 100nF and 1uF capacitors in parallel for VDDA pins.
- Utilize ferrite beads (e.g., 120 ohms at 100MHz) for additional filtering.

### 7. Configuration Pins and Reset

- Connect configuration pins and reset pins as required by the microcontroller datasheet.

### 8. Power Regulation

- Determine the source of 2.3V and incorporate necessary regulators and power sources.

## What did you learned?

### Capacitors and Bulk Capacitors

A **capacitor** is an electronic component that stores electrical energy in an electric field. It consists of two conductive plates separated by an insulating material called a dielectric. When a voltage is applied across the plates, opposite charges accumulate on each plate, creating an electric field between them. This electric field stores energy, which can be released when the capacitor is connected in a circuit.

Capacitors are commonly used in electronic circuits for various purposes, including:

1. **Energy Storage**: Capacitors store electrical energy temporarily and release it when needed. They are often used to provide short-term power backup, filter out noise in power supplies, or store energy in timing circuits.

2. **Filtering**: Capacitors can filter out unwanted signals or noise from electrical signals. They are often used in combination with resistors to create low-pass, high-pass, or band-pass filters, allowing specific frequencies to pass while blocking others.

3. **Coupling**: Capacitors can couple or connect different parts of a circuit while blocking DC (direct current). This is useful for transferring AC (alternating current) signals between stages of an amplifier or isolating one part of a circuit from another.

4. **Decoupling**: Capacitors are used for decoupling to stabilize the voltage levels in electronic circuits. They provide a stable voltage reference for integrated circuits, ensuring proper operation and reducing noise and voltage fluctuations.

**Bulk capacitors**, also known as reservoir capacitors or power supply capacitors, are large-value capacitors used in power supply circuits to provide energy storage and smoothing. They are typically electrolytic capacitors with high capacitance values, designed to handle large currents and provide a stable voltage output.

Here are some key characteristics and applications of bulk capacitors:

1. **Energy Storage**: Bulk capacitors store energy from the power supply and release it to the load when needed, helping to maintain a stable voltage output.

2. **Smoothing**: Bulk capacitors smooth out fluctuations or ripple in the output voltage of power supplies, ensuring a steady and regulated voltage for the electronic circuitry.

3. **Transient Response**: Bulk capacitors improve the transient response of power supplies by supplying additional energy during sudden changes in load or input voltage, thereby reducing voltage droop or sag.

4. **Filtering**: Bulk capacitors filter out high-frequency noise or ripple present in the power supply, improving the overall quality of the output voltage.

In summary, while standard capacitors have various uses in electronic circuits for energy storage, coupling, filtering, and decoupling, bulk capacitors specifically serve to stabilize and smooth the output voltage of power supplies, ensuring reliable operation of electronic devices.

### GND and VSS

**GND** stands for "ground" in electronics. It represents the common reference point in an electrical circuit from which voltages are measured. Ground serves as a zero-voltage reference point against which all other voltages in the circuit are measured. Here are some key points about GND:

- GND provides a common reference point for voltage measurements within an electrical circuit, typically designated as the point of zero voltage potential.
- In many electrical systems, GND is connected to the earth ground for safety purposes, preventing electrical shock hazards by dissipating excess electrical current safely into the ground.
- GND often acts as the return path for electrical signals in a circuit, completing the circuit as current flows from the voltage source through the load and back to the ground.
- Additionally, GND helps stabilize voltages within a circuit by offering a low-impedance path for excess charge to flow, thereby minimizing voltage fluctuations.
- Many electronic components, including integrated circuits (ICs), microcontrollers, and sensors, require a GND connection to operate correctly. This connection ensures that the component's internal circuitry operates with respect to a consistent reference point.

**VSS** stands for "Voltage Supply Source" or "Voltage Source, Ground." It is a term commonly used in the context of integrated circuits (ICs), particularly in datasheets and specifications.

- VSS typically denotes the ground connection or reference point within an IC or electronic system.
- In digital circuits, VSS serves as the common reference for voltage levels within the circuit.
- It is connected to the ground terminal of the power supply and provides the necessary ground connection for the internal circuitry of the IC.
- VSS pins on IC packages are often labeled as such to indicate their function as the ground connection.
- They are connected to the ground plane or ground trace on the printed circuit board (PCB) to establish a common ground reference for the entire circuit.

### Decoupling

Decoupling in PCB (Printed Circuit Board) design refers to the practice of adding capacitors strategically across the power supply rails of integrated circuits (ICs) or other components on the board. The purpose of decoupling capacitors is to stabilize the voltage supplied to the components, reducing noise and preventing fluctuations that could lead to malfunctions or performance issues.

Here's why decoupling is important and how it works:

- Noise Reduction: Digital circuits, especially those with high-speed switching, generate noise that can propagate through the power supply lines. Decoupling capacitors provide a low-impedance path for high-frequency noise to bypass the components, preventing it from affecting the performance of sensitive components.

- Voltage Stability: Integrated circuits require stable and clean power supplies to function correctly. Decoupling capacitors act as reservoirs of charge, supplying additional current to the ICs during transient load changes. This helps maintain a stable voltage level, ensuring reliable operation.

- Preventing Ground Bounce: In digital circuits, rapid changes in signal levels can cause ground bounce, where the ground voltage momentarily rises due to the inductance of the ground trace. Decoupling capacitors placed strategically between power and ground planes can help mitigate this effect by providing a low-impedance path to stabilize ground voltage.

- Minimizing Signal Coupling: Decoupling capacitors can also help minimize signal coupling between different parts of the circuit by providing a local return path for current loops. This can reduce electromagnetic interference (EMI) and crosstalk between traces.

- Component Protection: Decoupling capacitors can provide some protection to ICs from voltage spikes or transient events on the power supply lines. They can absorb and dissipate energy from these events, helping to prevent damage to the ICs.

### Ferrite beads

Ferrite beads, also known as ferrite chokes or ferrite rings, are passive electronic components commonly used in PCB design to suppress high-frequency noise and electromagnetic interference (EMI). They are composed of a ferrite core, typically in the form of a bead or cylindrical ring, with wire wound around it. Ferrite beads are placed in series with a signal or power line to attenuate unwanted high-frequency noise while allowing the desired signals to pass through with minimal attenuation.

Here's how ferrite beads work and their typical applications in PCB design:

- Noise Suppression: Ferrite beads exploit the magnetic properties of ferrite material to selectively impede the flow of high-frequency noise signals. When high-frequency noise currents pass through the ferrite bead, the ferrite core's impedance increases, effectively filtering out the noise while allowing lower-frequency signals to pass through relatively unaffected.

- EMI Reduction: Ferrite beads are effective in reducing electromagnetic interference (EMI) caused by high-frequency signals radiating from PCB traces or components. By introducing impedance to the high-frequency noise currents, ferrite beads prevent them from propagating further along the signal or power lines and radiating as EMI.

- Power Supply Filtering: Ferrite beads are commonly used in power supply circuits to filter out noise from the power lines. Placing ferrite beads in series with power supply lines can help suppress high-frequency noise generated by switching regulators, digital circuits, or other sources, ensuring clean and stable power delivery to sensitive components.

- Signal Integrity: Ferrite beads can also be used to improve signal integrity by reducing reflections and attenuating unwanted harmonics or ringing on signal lines. They are often placed in series with high-speed data lines or clock signals to suppress noise and maintain signal integrity, especially in high-speed digital communication interfaces.

- RF Circuits: Ferrite beads find extensive use in radio frequency (RF) circuits, such as RF amplifiers, filters, and antennas. They help isolate RF signals from noise and interference, improving the overall performance and sensitivity of RF systems.

- Common Mode Chokes: In addition to their use as signal line filters, ferrite beads can also function as common mode chokes when multiple signal lines are routed through them. Common mode chokes suppress common mode noise by creating equal and opposite currents in the signal lines, effectively canceling out the unwanted noise.

### Power regulation

Power regulation in PCB design refers to the process of ensuring that the electrical power supplied to the components on the circuit board meets their specified requirements with minimal variations. It involves the use of voltage regulators, filters, and other techniques to maintain stable and reliable power delivery to the circuit components, even in the presence of fluctuations in the input voltage or load conditions.

Here are key aspects of power regulation in PCB design:

- Voltage Regulation: Voltage regulation is the primary goal of power regulation. It involves maintaining a stable output voltage level despite changes in the input voltage or load conditions. Voltage regulators, such as linear regulators or switching regulators, are commonly used to achieve this by adjusting the output voltage based on feedback signals.

- Load Regulation: Load regulation refers to the ability of the power supply to maintain a constant output voltage when the load current changes. A well-regulated power supply will exhibit minimal variations in output voltage even with significant changes in load current.

- Ripple and Noise Reduction: Power regulation also involves minimizing ripple and noise on the output voltage. Ripple is the AC component superimposed on the DC output voltage, typically caused by rectification and filtering processes. Noise can come from various sources, including the power supply itself, switching transients, or external interference. Decoupling capacitors, filters, and voltage regulators are used to suppress ripple and noise, ensuring a clean and stable power supply to the circuit components.

- Efficiency Optimization: Power regulation aims to maximize the efficiency of the power supply by minimizing power losses. This is particularly important in battery-powered or energy-efficient devices where minimizing power consumption is crucial for extending battery life or reducing heat dissipation. Switching regulators are often preferred over linear regulators in such cases due to their higher efficiency.

- Overvoltage and Overcurrent Protection: Power regulation circuits may incorporate overvoltage and overcurrent protection mechanisms to safeguard the circuit components from damage due to excessive voltage or current. These protections typically involve the use of voltage clamping devices, current limiting circuits, or electronic fuses.

- Thermal Management: Power regulation circuits generate heat, especially in voltage regulators where excess voltage is dissipated as heat. Proper thermal management is essential to prevent overheating of the components and ensure reliable operation over the entire operating range. Heat sinks, thermal vias, and adequate airflow are commonly employed techniques for dissipating heat effectively.


### Comprehensive and Detailed Documentation on Key PCB Design Concepts

In PCB design, especially for microcontroller-based projects such as STM32, it’s essential to understand several key concepts. These principles ensure the stability, functionality, and efficiency of your electronic design. Below, I will break down and comprehensively explain important notions like decoupling, GPIO, GND, VSS, VSSA, VDD, bulk decoupling, and configuration pins such as NRST, BOOT0, BOOT1, as well as the significance of voltage regulators.

---

### **1. Decoupling**

#### **What is Decoupling?**
Decoupling refers to the practice of using capacitors (called decoupling capacitors) to filter out noise in power supply lines and provide instantaneous current when needed by a component. In electronic circuits, particularly for microcontrollers like STM32, the power supply can experience fluctuations and noise caused by various components switching on and off or due to interference from other parts of the circuit. Decoupling capacitors serve to "decouple" these unwanted fluctuations from sensitive devices.

#### **How Decoupling Capacitors Work**
When a component, such as a microcontroller, switches states or processes data, it demands a quick surge of current that the power supply may not be able to deliver instantly due to inductance or resistance in the supply lines. A decoupling capacitor, placed close to the device, acts as a local energy reservoir. It stores charge and releases it as needed, ensuring that the component gets the required current without causing dips or spikes in the power rail.

- **Placement**: Decoupling capacitors must be placed as close as possible to the power pins of the component. The typical value for these capacitors is 100nF (0.1µF).
- **Types**: For microcontrollers like STM32, it's common to use ceramic capacitors with low Equivalent Series Resistance (ESR) for decoupling.

---

### **2. GPIO (General Purpose Input/Output)**

#### **What is GPIO?**
GPIO pins are versatile digital pins on a microcontroller that can be configured as either input or output. They allow the microcontroller to interact with external components, such as sensors, LEDs, buttons, and other peripherals.

- **Input Mode**: When a GPIO is configured as input, the microcontroller can read external signals (e.g., sensing a button press).
- **Output Mode**: When configured as output, the microcontroller can send signals to control other devices (e.g., turning an LED on or off).
- **Pin Banks**: STM32 microcontrollers group GPIO pins into banks (PA, PB, PC, etc.). Each bank may have several pins that can be individually controlled.

---

### **3. GND (Ground)**

#### **What is Ground?**
GND, or Ground, serves as the common reference point for all voltage levels in an electronic circuit. All current in the circuit must return to ground, making it essential for completing electrical circuits.

- **Common Reference**: Every voltage in the circuit is measured relative to ground. For example, if the VDD of a microcontroller is 3.3V, that voltage is relative to the GND.
- **Return Path for Current**: Ground also serves as the return path for current. In digital circuits, signals fluctuate between VDD and GND, and the integrity of this return path is crucial for stable circuit operation.

---

### **4. VSS (Ground for Digital Circuits)**

VSS is a specific designation for the ground connection in digital circuits. It stands for "Voltage Source Supply" (which can be misleading, as it's used for ground in this context). In STM32 microcontrollers and most digital devices, VSS is tied to the ground reference for digital signals.

- **Function**: VSS provides a stable reference for all digital logic operations inside the microcontroller. It ensures that digital signals switch cleanly between high (VDD) and low (VSS or GND).

---

### **5. VSSA (Analog Ground)**

VSSA is the ground reference specifically for the analog portions of a mixed-signal microcontroller, such as the analog-to-digital converter (ADC) or digital-to-analog converter (DAC).

- **Why Separate?**: Analog circuits are more sensitive to noise than digital circuits. A separate ground (VSSA) helps to isolate the sensitive analog components from the noisy digital circuitry.
- **Tying VSSA and VSS**: In many designs, VSSA and VSS are tied together at a single point to avoid ground loops, but the routing of analog signals and their ground paths should be handled carefully to minimize noise.

---

### **6. VDD (Power Supply for Digital Circuits)**

#### **What is VDD?**
VDD is the positive supply voltage that powers the digital circuits inside the microcontroller. For STM32 microcontrollers, VDD typically ranges from 2.7V to 3.6V, with 3.3V being the most common.

- **Connection to VDD Pins**: Multiple VDD pins on the microcontroller must be connected to the same power rail (3.3V in most designs). Proper decoupling is required to ensure that these power pins get clean, noise-free power.

---

### **7. Bulk Decoupling**

#### **What is Bulk Decoupling?**
While decoupling capacitors (typically 100nF) are used to filter high-frequency noise, bulk decoupling capacitors (usually in the range of 10µF to 47µF) handle lower frequency noise and provide a local energy reservoir to smooth out large fluctuations in current demand.

- **Purpose**: Bulk decoupling capacitors are used to stabilize the power supply over longer periods or to handle larger current spikes that small decoupling capacitors cannot.
- **Placement**: Typically placed near the power source or close to high-power components.

---

### **8. NRST (Reset Pin)**

#### **What is NRST?**
NRST is the reset pin of the STM32 microcontroller. It is used to reset the microcontroller to its initial state, restarting the execution of code from the beginning.

- **Typical Circuit**: A **10kΩ pull-up resistor** is often connected between NRST and VDD to keep the pin high during normal operation. A momentary push-button switch is connected between NRST and GND, allowing manual reset when pressed.
- **Function**: When NRST is pulled low (to GND), the microcontroller resets, re-initializing its registers, peripherals, and code execution.

---

### **9. BOOT0 and BOOT1 Pins**

#### **What are BOOT Pins?**
The BOOT0 and BOOT1 pins on an STM32 microcontroller determine the boot mode of the microcontroller during power-up. The settings on these pins control whether the microcontroller boots from Flash memory (the normal operating mode), system memory (for programming or debugging), or SRAM.

- **BOOT0**: This pin selects between different boot modes. It is often configured using a pull-up or pull-down resistor to set the default mode.
- **BOOT1**: Used in combination with BOOT0 to select the exact boot mode.

#### **BOOT Mode Selection**
- **Flash Boot (Normal Operation)**: BOOT0 is typically tied to **GND**, which configures the microcontroller to boot from Flash memory. This is the mode used during normal operation when the microcontroller runs the code you’ve programmed into it.
- **System Boot (Programming Mode)**: Setting BOOT0 high (connected to VDD) during power-up enables the bootloader, allowing you to program the microcontroller via interfaces like UART or USB.

##### **Typical Circuit for BOOT Pins:**
- **BOOT0** is connected to a pull-down resistor (10kΩ to GND) to default it to boot from Flash.
- **BOOT1** may not need to be connected for most configurations but can be tied to a defined logic level if required.

---

### **10. Voltage Regulator**

#### **What is a Voltage Regulator?**
A voltage regulator is an electronic component that ensures a stable voltage supply to a circuit. For microcontroller designs like STM32, which typically require 3.3V, a voltage regulator is used to step down higher voltages (e.g., 5V from USB or a battery) to the required level.

#### **Types of Voltage Regulators**
- **Linear Regulators**: Simple and cost-effective, linear regulators, like the **AMS1117-3.3**, drop excess voltage as heat to maintain a constant output voltage. They are easy to use but less efficient.
- **Switching Regulators**: More efficient but complex, switching regulators convert higher voltages to lower ones using inductors and capacitors without generating excessive heat.

#### **Designing with Voltage Regulators**
- **Input/Output Capacitors**: Both the input and output of the voltage regulator require capacitors to stabilize the voltage and prevent oscillations. Typically, a **10µF capacitor** is placed at both the input and output.
- **Grounding**: Ensure that the regulator’s GND is properly connected to the common ground (GND) of your system.
- **Heat Dissipation**: In the case of linear regulators, pay attention to heat dissipation. Depending on the input voltage and current draw, a heatsink might be required.

---

### **Conclusion**

Understanding these key concepts is critical for designing stable and efficient PCBs, particularly when working with microcontrollers like STM32. Proper grounding, decoupling, and voltage regulation are the foundation of good PCB design, while the configuration pins (NRST, BOOT0/BOOT1) ensure your microcontroller operates correctly. Keep these principles in mind as you move through the design process in KiCad

, ensuring that your designs are both functional and reliable.