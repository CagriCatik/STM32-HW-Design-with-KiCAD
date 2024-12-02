# Prioritizing and Placing Critical Circuitry

In this section, we will focus on the **priority placement** of critical components, particularly the **USB differential pair** and **Serial Wire Debug (SWD)** connections. These high-speed and critical signals require careful attention during layout to ensure proper functionality and minimize performance degradation. After completing the decoupling capacitors and crystal placement, we now proceed with these important connections.

---

## **1. Prioritizing Placement of Critical Components**

When laying out a PCB, it is essential to prioritize the placement of critical components that affect performance the most. For this design, the **USB differential pair** and **SWD** connector are next in line after decoupling capacitors and the crystal oscillator.

### **Step 1: Understanding High-Speed Signals**
- **USB differential pairs** (D+ and D-) need to be routed together with equal trace lengths and minimal separation to maintain signal integrity.
- **SWD** signals (SWDIO, SWCLK) are lower-speed signals but still need to be placed optimally for ease of routing and proper debug functionality.

### **Step 2: USB Differential Pair Considerations**
For **USB 2.0 full-speed** designs, such as ours, we do not need to worry about controlled impedance for short traces (less than 10mm), but we do need to keep the traces as short as possible and close together.

---

## **2. Placing the USB Connector and Differential Pair**

The **USB connector** is a crucial interface that connects your microcontroller to external devices. Proper placement and alignment of the USB connector and differential pair ensure smooth signal routing.

### **Step 1: Positioning the USB Connector**
1. **Select the USB connector** (e.g., **J2**) in the PCB Editor.
2. **Move (M)** the connector toward the edge of the board, as this is where most USB connectors are placed to allow external access.
3. Ensure the **USB differential pair** (D+ and D-) lines from the microcontroller (pins 33 and 32) can be routed directly to the connector without crossing other signals.
   - Use the **rat’s nest lines** to visualize where the connections are supposed to go.
   - Position the connector **close enough** to the microcontroller to keep the differential pair short, but leave enough space for ease of soldering if manually assembling.

### **Step 2: Optimizing Differential Pair Routing**
1. Keep the **USB differential pair traces** (D+ and D-) as short as possible, ideally less than **10mm**.
   - Use the **measurement tool** (**Ctrl + Shift + M**) to check the trace length.
2. Align the connector in such a way that **D+ and D-** traces from the microcontroller flow **directly** into the USB connector, minimizing bends and crossovers.

### **Step 3: Adding the 1.5kΩ Resistor to D+**
1. The **1.5kΩ pull-up resistor** is essential for USB detection. It needs to be placed in series with the **D+ line**.
   - Select the **1.5kΩ resistor** and place it **inline** with the D+ signal trace, ensuring that it is positioned between the microcontroller and the USB connector.
2. Place the resistor in such a way that the trace can pass through it easily, reducing the need for unnecessary detours.
   - Align the resistor such that the trace from **D+** flows directly from the microcontroller, through the resistor, and into the USB connector pin.

---

## **3. Placing the Serial Wire Debug (SWD) Connector**

The **SWD connector** is used for programming and debugging the STM32 microcontroller. Proper placement of the SWD connector allows easy access for debug tools while ensuring clean and direct signal routing.

### **Step 1: Positioning the SWD Connector**
1. **Select the SWD connector** (e.g., **J3**) in the PCB layout.
2. Move it to a location near the **SWDIO** and **SWCLK** pins on the microcontroller.
   - These signals should be placed where you can **minimize trace length** and ensure clear, unobstructed routing.

### **Step 2: Rotating and Aligning the SWD Connector**
1. Use **R** to rotate the SWD connector and align its pins with the **SWDIO** and **SWCLK** signals from the microcontroller.
   - Typically, **SWCLK** (pin 32 on the microcontroller) should align with **SWCLK** on the SWD connector.
   - Similarly, **SWDIO** (pin 31) should align with **SWDIO** on the connector.

2. Ensure the connector is positioned close enough to the microcontroller to **minimize trace lengths** but with enough space for easy access during assembly.

### **Step 3: Making Debug Connections Simple**
- By properly aligning the SWD connector with the microcontroller’s **SWDIO** and **SWCLK** pins, you simplify the routing process.
- Leave some space between the connector and the edge of the board for easy access with debugging tools, like an ST-Link or J-Link programmer.

---

## **4. Fine-Tuning Placement for Connectors**

Now that the critical components have been placed, we can move on to the **power and auxiliary connectors**. These are typically positioned at the edges of the PCB for accessibility.

### **Step 1: Arranging Connectors at the Board Edges**
- Place **power connectors**, such as the **3.3V power input**, at the edge of the board to ensure easy access when the board is in an enclosure.
- Group similar connectors (e.g., **UART** and **I²C** connectors) in one section to simplify routing and to give a clean structure to the board.

### **Step 2: Planning for Board Outline**
- With key components like the USB connector and SWD connector placed, you can begin to envision the **PCB outline**.
   - Plan for a rectangular shape with mounting holes at the corners, or design a shape based on the enclosure if there is a specific mechanical fit.

---

## **5. Review and Finalize Initial Placement**

Before proceeding to the routing stage, take a moment to review your initial layout. This is a rough placement, but it’s important to make sure that:
1. **Critical components** like the **USB differential pair** and **SWD** connectors are properly placed and aligned.
2. There is **adequate space** between components for easy routing and soldering.
3. The **silkscreen labels** are clearly visible, making assembly and debugging easier.

### **Step 1: Adjust the Silkscreen**
- Ensure the silkscreen text (component labels and designators) is properly aligned and not overlapping with pads or traces.
   - Use **M** to move the silkscreen text for each component if necessary.

### **Step 2: Double-Check Measurements**
- Use the **measurement tool** to ensure that key distances (e.g., USB trace lengths, space between components) are within acceptable ranges for manufacturability and signal integrity.

### **Step 3: Inspect Layout in 3D**
- Press **ALT + 3** to view the layout in 3D and inspect the overall placement of components.
   - Make sure components are not too close to the edges of the board and that they are properly spaced for ease of assembly.

---

## **Conclusion**

You have now completed the **critical component placement** phase, focusing on sensitive components such as the **USB differential pair** and **SWD connector**. Proper placement ensures clean routing, minimal signal interference, and ease of assembly. The next step is to refine the layout and begin **routing** the PCB, which involves connecting the electrical signals between components with copper traces.

By following these steps, you’ve set the foundation for a well-structured and high-performance PCB design that is ready for the final layout and routing stages.