# D

## DRC

## Decoupling

Decoupling refers to the practice of using capacitors (called decoupling capacitors) to filter out noise in power supply lines and provide instantaneous current when needed by a component. In electronic circuits, particularly for microcontrollers like STM32, the power supply can experience fluctuations and noise caused by various components switching on and off or due to interference from other parts of the circuit. Decoupling capacitors serve to "decouple" these unwanted fluctuations from sensitive devices.

When a component, such as a microcontroller, switches states or processes data, it demands a quick surge of current that the power supply may not be able to deliver instantly due to inductance or resistance in the supply lines. A decoupling capacitor, placed close to the device, acts as a local energy reservoir. It stores charge and releases it as needed, ensuring that the component gets the required current without causing dips or spikes in the power rail.

- Placement: Decoupling capacitors must be placed as close as possible to the power pins of the component. The typical value for these capacitors is 100nF (0.1µF).
- Types: For microcontrollers like STM32, it's common to use ceramic capacitors with low Equivalent Series Resistance **(ESR)** for decoupling.


# STM32 uC Decoupling

## Introduction

The process of creating a PCB design step by step will be walked through in this guide. Whether you are a beginner or an experienced hardware designer, detailed instructions will be provided in this document to help you achieve your goals.

## Getting Started

### 1. Install the Software

- To install KiCad using Bash, you can typically use package managers available for your operating system. Here are the steps for different platforms:

    **Ubuntu/Debian:**

    ```bash
    sudo apt update
    sudo apt install kicad
    ```

    **Windows:**

    For Windows, KiCad provides an installer available on their website. You can download it from KiCad's official website.

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
