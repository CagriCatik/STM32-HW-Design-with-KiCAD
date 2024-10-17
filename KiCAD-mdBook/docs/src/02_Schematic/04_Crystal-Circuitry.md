# Connecting the Crystal Oscillator

In this section, we will discuss the process of integrating a crystal oscillator into your STM32 microcontroller circuit using KiCad. This step is critical for providing accurate timing to the microcontroller, particularly for high-speed communication protocols such as USB, CAN, and UART. We will cover the basic principles of crystal oscillators, necessary external components (capacitors, resistors), and the practical application of these components in the schematic.

---

## **1. The Role of the Crystal Oscillator in STM32 Microcontrollers**

STM32 microcontrollers require a precise external clock source for various functions. While they do have an internal clock, the internal oscillator is typically less accurate and unstable for protocols requiring precise timing. The **High-Speed External (HSE) clock** is provided by a crystal oscillator connected to the HSE pins on the STM32 microcontroller.

A typical crystal oscillator circuit comprises:
- A **crystal** (e.g., 16 MHz) connected to the HSE input (OSC_IN) and output (OSC_OUT) pins.
- **Load capacitors** to stabilize the oscillation frequency.
- **Optional feedback resistors** (sometimes used for distortion control).

---

## **2. Crystal Package Types and Symbol Selection in KiCad**

Crystal oscillators come in different packages, including the common **two-pin** or **four-pin** configurations. For this example, we will focus on a **four-pin** crystal.

### **Selecting the Crystal Symbol in KiCad**
1. Click on **Add Symbol** in KiCad.
2. Search for **Crystal** in the symbol library.
3. Select the **two-pin or four-pin crystal** depending on the package of your chosen crystal. Most crystals use the **two-pin package**, but the four-pin configuration allows grounding for additional stability.
4. Place the crystal symbol on your schematic, typically near the HSE_IN and HSE_OUT pins of the STM32 microcontroller.

### **Pin Configuration for a Four-Pin Crystal**
- Pins **1 and 3** of the crystal are the actual crystal input and output, which will connect to the HSE_IN (OSC_IN) and HSE_OUT (OSC_OUT) pins of the STM32.
- Pins **2 and 4** are grounded to improve stability and reduce electromagnetic interference.

---

## **3. Understanding the Crystal Circuit Design**

STM32 microcontrollers have built-in inverters and feedback resistors that help form the oscillation circuit. However, external **load capacitors** and **optional feedback resistors** are required to stabilize the crystal and avoid overdriving.

### **Typical Crystal Oscillator Circuit**
The oscillator circuit typically involves:
- **Crystal** connected between the HSE_IN (PD0) and HSE_OUT (PD1) pins.
- **Two identical load capacitors** connected from each crystal pin to ground.
- **Optional series resistor** (feedback resistor) to limit distortion.

### **External Components: Load Capacitors**
- Load capacitors ensure that the crystal oscillates at the desired frequency.
- The value of these capacitors depends on the **crystal load capacitance** and the **stray capacitance** of the PCB.
  
---

## **4. Application Note AN2867: Oscillator Design for STM32**

STMicroelectronics provides a valuable resource, **Application Note AN2867**, which offers guidelines on designing crystal oscillator circuits for STM32 microcontrollers. Following these guidelines helps ensure reliable operation.

1. **Crystal Load Capacitors**: According to **AN2867**, load capacitors are critical for stabilizing the oscillation. The STM32's internal oscillator circuit works with external load capacitors and the crystal to generate the clock signal.
2. **Stray Capacitance**: Stray capacitance is the inherent capacitance from PCB traces and other components. Typically, it ranges between **3-5 pF**.
3. **Feedback Resistor**: While many designs omit the feedback resistor, some circuits may include it to prevent the crystal from being overdriven and distorted. Most designs work fine without this resistor.

---

## **5. Calculating the Load Capacitor Values**

To determine the correct values for the load capacitors, use the following formula:

\[
C_{load} = \frac{C_{crystal} - C_{stray}}{2}
\]

Where:
- **C_crystal** is the load capacitance specified in the crystal datasheet (typically 10-20 pF).
- **C_stray** is the estimated stray capacitance (typically 3-5 pF).

### **Example Calculation**:
If the **load capacitance (C_crystal)** of your 16 MHz crystal is **10 pF**, and you estimate **C_stray** as **5 pF**, the required load capacitor value for each capacitor is:

\[
C_{load} = \frac{10 \, \text{pF} - 5 \, \text{pF}}{2} = 5 \, \text{pF}
\]

Multiplying by two (for two capacitors) gives a **total load capacitance of 10 pF**. In this case, you would place two **10 pF capacitors** connected from each crystal pin to ground.

### **Steps in KiCad to Add Load Capacitors**:
1. Click **Add Symbol** and search for **capacitor**.
2. Select a **10 pF capacitor** and place two on the schematic, one connected to HSE_IN and one to HSE_OUT.
3. Connect the other ends of both capacitors to **GND**.

### **Crystal Circuit Without Feedback Resistor**:
In most cases, the feedback resistor is not necessary. If STMicroelectronics' application note suggests omitting it, you can confidently skip this component.

---

## **6. Connecting the Crystal in KiCad**

### **Connecting the Crystal to the STM32**
1. **Connect Pin 1 of the Crystal** to the **HSE_IN** pin (PD0) on the STM32.
2. **Connect Pin 3 of the Crystal** to the **HSE_OUT** pin (PD1) on the STM32.
3. **Ground Pin 2 and Pin 4** to reduce noise interference (for four-pin packages).

### **Routing and Naming the Net Labels**
- Assign appropriate **net labels** to these connections for clarity in the PCB layout. Label the crystal pins as **HSE_IN** and **HSE_OUT**, and the corresponding STM32 pins as **HSE_IN** and **HSE_OUT** in the schematic.

---

## **7. Reviewing the Schematic for the Crystal Circuit**

At this point, your crystal circuit in KiCad should look like this:
- A crystal oscillator connected between **PD0 (HSE_IN)** and **PD1 (HSE_OUT)**.
- Two **10 pF capacitors** connected from each crystal pin to **GND**.
- Pins **2 and 4** of the four-pin crystal grounded to reduce noise.

## **8. Validating the Crystal Circuit**

Once your crystal oscillator is connected, it is essential to review the schematic and ensure everything is set up correctly:
1. **Check Net Names**: Ensure that all the nets are named correctly and consistently (e.g., HSE_IN, HSE_OUT).
2. **Load Capacitor Values**: Verify that the calculated load capacitors are correct based on the crystal datasheet.
3. **Ground Connections**: Make sure the ground pins of the crystal and capacitors are correctly routed.

---

## **Conclusion**

The crystal oscillator circuit is an essential part of your STM32 design, providing stable clock signals for timing-critical applications. By following the guidelines outlined in **Application Note AN2867**, you ensure that your design is both reliable and optimized. You’ve now learned how to:
- Select and place a crystal oscillator in KiCad.
- Calculate and add the necessary load capacitors.
- Connect the crystal to the STM32’s HSE pins and ground.

With this configuration in place, your STM32 microcontroller will have a stable and accurate clock source for high-speed operations.