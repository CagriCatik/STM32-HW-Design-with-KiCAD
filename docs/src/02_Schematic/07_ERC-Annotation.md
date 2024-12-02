# Sectioning, Annotating, and Finalizing the Schematic

In this section, we will walk through the process of **organizing**, **annotating**, and **finalizing** the schematic in KiCad to ensure it is both readable and professional. This includes dividing the schematic into sections, adding annotations, assigning designators, and preparing the schematic for PCB layout. Properly organizing your schematic not only helps with readability but also ensures a smooth transition to PCB layout, assembly, and debugging in the future.

---

## **1. Sectioning the Schematic into Readable Parts**

A clear and organized schematic is critical for ensuring readability, especially in more complex designs. Sectioning the schematic into distinct blocks improves understanding for future reference or for others who may need to review or work on the design.

### **Step 1: Draw Bounding Boxes Around Sections**
1. In KiCad, use the **"Connected Graphic Lines Tool"** from the right toolbar to draw **bounding boxes** around different functional sections of the schematic.
   - **Power Supply Section**: Include all components related to voltage regulation, such as the linear regulator (AMS1117), input/output capacitors, and any associated circuitry.
   - **Microcontroller Section**: Include the STM32 microcontroller, decoupling capacitors, and any essential connections (e.g., crystal oscillator, USB circuit).
   - **Communication Interfaces**: Include UART, I²C, and SWD debug connectors.

   This helps visually distinguish different functional blocks, making it easier to navigate and understand the schematic.

### **Step 2: Add Text Annotations**
1. Select the **"Add Text" tool** and add titles to each section:
   - Label the sections, for example: **"Power Supply"**, **"Microcontroller"**, and **"USB Circuitry"**.
   - Use larger, bold text for titles to make them stand out.
   - To adjust text size, double-click the text and increase the font size as needed.

This will give each section a clear title, making the schematic easier to follow.

---

## **2. Adding a Title Block**

To make the schematic more professional and standardized, it is important to include a **title block**. This provides information about the project, author, revision, and other useful metadata.

### **Step 1: Editing the Title Block**
1. Click the **Page Settings** button (it looks like a sheet of paper) on the toolbar.
2. In the **Page Settings** window, fill in the following fields:
   - **Title**: Name of the project (e.g., "STM32 Demo PCB").
   - **Revision**: Use a meaningful revision number (e.g., "v0.1").
   - **Company Name**: If applicable, add your company or project name.
   - **Date**: Automatically fills in the current date or enter it manually.
3. Click **OK** to apply.

The title block will now appear at the bottom of your schematic page, giving it a more professional appearance, especially if this schematic is part of a multi-page design.

---

## **3. Adding Comments and Notes**

Annotations are critical in explaining design choices and providing context for future reference. Adding comments helps others (and your future self) understand why certain values were chosen or why specific components were used.

### **Step 1: Add Design Explanations**
1. Use the **"Add Text" tool** to provide important information on component choices, design decisions, or notes.
   - For example, you can explain why the **10 pF capacitors** were chosen for the crystal oscillator by writing something like: "Calculated based on crystal load capacitance of 10 pF and stray capacitance of 5 pF."
   - For the **1.5kΩ resistor** on the USB D+ line: "Pull-up resistor for USB detection as per STM32 application note AN4879."

Adding these notes helps ensure that anyone reviewing the schematic understands the reasoning behind your choices.

### **Step 2: Highlight Critical Areas**
- For critical connections (e.g., **VBUS power input**, **SWD connections**), add short comments explaining their purpose and behavior.
- Label important pins such as **VCC**, **GND**, **UART_TX**, **I2C_SCL**, etc., to make routing in the PCB layout phase easier.

---

## **4. Annotating Designators**

Designators (e.g., **C1**, **R2**, **U1**) are required for each component in the schematic so that they can be correctly identified during PCB layout and manufacturing. You can assign designators manually or let KiCad handle this automatically.

### **Step 1: Automatic Annotation**
1. In the toolbar, click the **Annotate Schematic Symbols** button (symbol with an "A").
2. In the **Annotate Schematic** dialog, select which schematic sheets to annotate and the order in which designators should be assigned.
   - For example, you may want to annotate by **X/Y position** to maintain a logical flow in your schematic (top-to-bottom, left-to-right).
3. Click **Annotate** to let KiCad assign the designators.

### **Step 2: Manual Annotation (if needed)**
- If you prefer manual annotation for more control over the designator sequence:
   - Double-click each component's designator (e.g., "C?") and type the appropriate value manually (e.g., "C1", "R1", etc.).
   - This method is useful if you want more control over how components are grouped logically in the design.

---

## **5. Running Electrical Rules Check (ERC)**

Before moving to the PCB layout phase, it is essential to check for any electrical issues or missing connections.

### **Step 1: Run ERC**
1. Click the **Electrical Rules Check (ERC)** button in the toolbar (symbol with a checkmark).
2. Run the ERC to check for potential issues like:
   - Unconnected pins.
   - Power input without a defined power source.
   - Incorrect connections between pins of different types (e.g., output to output).

### **Step 2: Fix Errors and Warnings**
- If errors are reported, such as power flags not being properly assigned:
   - Add a **Power Flag** symbol (found in the **Power Ports** section) to the VBUS or other power lines to define them as power sources.
- Warnings such as floating pins on connectors (which are intentional) can be resolved by adding **No-Connect (DNC)** flags to those pins.

Run ERC again to ensure there are no remaining errors or critical warnings.

---

## **6. Assigning Footprints to Components**

After annotating the schematic, you need to assign **footprints** to each component. Footprints represent the physical dimensions and pin configurations of components on the PCB.

### **Step 1: Assign Footprints**
1. Click the **Assign Footprints to Symbols** button (icon of a footprint).
2. In the **Footprint Assignment** window, assign the appropriate footprint to each component based on its physical characteristics (e.g., **SMD capacitor footprint**, **DIP or TQFP package** for the microcontroller).
   - Example: For the **AMS1117-3.3 regulator**, choose the appropriate **SOT-223 footprint**.
   - Example: For **decoupling capacitors**, choose the correct **0805** or **0603** package, depending on your design's specifications.

### **Step 2: Verify Footprint Assignments**
- Verify that each component has been assigned the correct footprint, particularly for critical components like the microcontroller, connectors, and voltage regulator.
- Ensure that the **package size** matches the available space on your PCB design.

---

## **7. Conclusion**

By sectioning the schematic, adding annotations, and performing proper checks, you ensure that your design is not only functional but also clear and professional. The next step will be to **transition from schematic design to PCB layout**, where you will place components, route connections, and prepare the board for manufacturing. Key takeaways from this section:
- **Sectioning** the schematic improves readability and future maintenance.
- **Annotations** provide important context for design choices.
- **Designators** and **footprints** ensure correct placement and assembly.
- Running **ERC** ensures the electrical sanity of your schematic.

With this foundation, you're ready to move on to PCB layout and ensure a smooth, organized design process.