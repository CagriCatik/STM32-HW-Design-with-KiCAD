# Finalizing Power Supply Layout and Preparing for PCB Routing

In this final stage of component placement, we will complete the layout of the **power supply section**, ensuring proper positioning of the **voltage regulator**, **capacitors**, and **LED indicators**. We'll also prepare the design for **PCB routing** by adjusting connector positions, reviewing the layout for neatness, and adding **mounting holes**.

---

## **1. Laying Out the Power Supply Section**

The power supply is a critical part of the PCB that ensures stable voltage delivery to the entire circuit. Proper placement of components in the power section, such as the **voltage regulator**, **input/output capacitors**, and **power LEDs**, is essential for both functionality and routing efficiency.

### **Step 1: Positioning the Voltage Regulator**
1. **Move the voltage regulator** (e.g., **AMS1117-3.3V**) close to the **USB-C power input** pin (pin 1). This ensures that the incoming power from the USB can easily be routed to the voltage regulator.
   - Use **R** to rotate the voltage regulator if needed, ensuring that the input pin aligns with the power input (VBUS) from the USB connector.
2. Ensure there is enough space around the regulator for **heat dissipation**, especially if it will handle significant current.

### **Step 2: Placing the Input and Output Capacitors**
1. **Place the input capacitor** (e.g., **C10**) close to the **input pin** of the voltage regulator. This capacitor smooths out voltage fluctuations from the USB power source and should be as close as possible to the regulator.
   - Ensure the **ground pin** of the capacitor is close to the ground pin of the regulator to minimize trace length.
2. **Position the output capacitor** (e.g., **C11**) near the **output pin** of the voltage regulator. This capacitor stabilizes the 3.3V output, ensuring smooth power delivery to the microcontroller and other components.
   - Place it inline with the regulator's output pin for easier routing of the 3.3V trace.

### **Step 3: Adding the Power-On LED**
1. **Place the power-on LED** (e.g., **D1**) near the **output of the voltage regulator**, but not too close to sensitive components.
   - The LED is not critical in terms of placement, so position it where it’s visible and accessible for testing.
2. **Position the current-limiting resistor** (e.g., **R6**) inline with the LED. The resistor should be connected to the LED's anode and the 3.3V output.

### **Step 4: Adjusting for Layout Compactness**
1. After placing the components, **review the layout** to make sure the power supply section is **compact** and that the traces between components (especially the capacitors and regulator) are short.
   - Group related components together and check that the **power input and output** lines are easy to route later.
2. Adjust the layout to **avoid overlapping traces** and ensure proper grounding paths.

---

## **2. Handling Remaining Passive Components**

The last component remaining is the **bulk decoupling capacitor** for the microcontroller. This capacitor helps smooth power to the entire circuit and should be placed close to the main power supply route.

### **Step 1: Positioning the Bulk Decoupling Capacitor**
1. **Place the bulk decoupling capacitor** (e.g., **C12**) close to the power traces leading to the microcontroller.
   - This capacitor is less critical in terms of exact placement, but should still be positioned within a reasonable distance from the **microcontroller power input** (3.3V line).
2. Ensure the **ground pin** of the decoupling capacitor has a short connection to the ground plane for optimal performance.

---

## **3. Inspecting the Layout and Preparing for Routing**

Now that all components are placed, we need to review the entire layout and prepare the design for **PCB routing**.

### **Step 1: Inspect the Layout in the 3D Viewer**
1. Press **ALT + 3** or go to **View > 3D Viewer** to inspect the current layout in 3D.
   - Ensure that all components, especially connectors (e.g., **USB-C**) and switches, are positioned correctly. For instance, connectors like the USB-C should hang off the edge slightly for easier access in enclosures.
   - Verify that the **silkscreen labels** are not overlapping with pads, traces, or other components.
   
### **Step 2: Fine-Tune the Placement of Connectors and Components**
1. Adjust the placement of components to ensure everything is **neatly aligned** and there are no **crossing traces** that could complicate routing.
   - **Move connectors** closer to the edges of the board, if necessary, to allow for easy external connections (e.g., **USB-C, UART, SWD**).
   - Make sure that **power and ground connections** are properly aligned with the main power routes.

### **Step 3: Prepare for Routing**
1. Check that **critical traces**, such as **power (3.3V)** and **ground**, are clearly planned and can be routed without crossing other traces.
2. Ensure that **3.3V and GND traces** are easily accessible from the voltage regulator to all necessary components (especially the microcontroller).
   - Use **wide traces** for the power and ground to handle the current and minimize voltage drop.

---

## **4. Adding Mounting Holes and Board Outline**

Before starting the routing process, it’s a good idea to add **mounting holes** and finalize the **board outline**.

### **Step 1: Adding Mounting Holes**
1. Use **Add a Mounting Hole** from the KiCad toolbar to place **mounting holes** in each corner of the PCB.
   - Typical mounting hole sizes are around **3.2mm** for screws, but this depends on the enclosure or mounting method you plan to use.
2. Ensure that the mounting holes are spaced evenly and placed **away from critical components** to avoid interference.

### **Step 2: Drawing the Board Outline**
1. Switch to the **Edge.Cuts layer** (the layer used for defining the board’s outer boundary).
2. Use the **Draw Line tool** to create the **board outline**, ensuring that it is large enough to accommodate all components but not excessively large.
   - The outline should be **slightly larger than the PCB components** for adequate edge clearance, particularly around connectors like **USB-C**.

---

## **5. Final Review Before Routing**

### **Step 1: Conduct a Final Layout Review**
1. Check for any **missing connections** or misplaced components.
2. Use the **3D Viewer** to conduct a final **sanity check**, ensuring that everything fits correctly and that the components are positioned for easy routing and assembly.

### **Step 2: Prepare for Routing**
1. Once everything is in place and checked, you're ready to move on to **PCB routing**, which involves drawing the actual copper traces that connect the components electrically.

---

## **Conclusion**

By completing the layout of the **power supply section** and refining the positioning of passive components, connectors, and decoupling capacitors, we’ve prepared the board for the next stage: **routing the traces**. This process ensures that components are optimally placed for power distribution and signal integrity.

The design is now well-organized and compact, making the routing stage smoother and easier. With mounting holes and the board outline added, the PCB is nearly ready for the final stages of design. Next, you’ll proceed to the **PCB routing phase**, where you’ll connect all the components using copper traces, finalizing the electrical connections that make the PCB functional.