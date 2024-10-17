# Adding Mounting Holes, Defining Board Outline, and Preparing for Routing

In this section, we will go over the process of adding **mounting holes**, defining the **board outline**, and adjusting the layout to prepare for PCB routing. These steps are important for ensuring that your PCB is properly enclosed, can be securely mounted, and has a clear outline for manufacturing.

---

## **1. Adding Mounting Holes to the PCB**

Mounting holes are used to attach the PCB to an enclosure or mechanical structure. These holes provide mechanical stability, especially in projects requiring mounting in cases or for handling during assembly.

### **Step 1: Add Mounting Holes to the Schematic**
1. Open the **Schematic Editor** and go to **Add Symbol**.
2. Search for **Mounting Hole** in the symbol library. There are two common types:
   - **Simple mounting hole**: A hole with no electrical connection.
   - **Mounting hole with pad**: This can be used if you want the mounting hole to be tied to ground, which can be useful for grounding oscilloscope probes.
3. For this design, select the **simple mounting hole** without an electrical connection.
4. Place four mounting holes on the schematic at appropriate locations.

### **Step 2: Select and Assign Footprint**
1. After placing the mounting holes, double-click each one to open the properties.
2. Click the **Footprint button** and search for a suitable **mounting hole footprint** in the library.
   - For a small board, an **M2 or M3 mounting hole** is usually appropriate.
3. Once selected, assign the same footprint to all four mounting holes by copying and pasting them.

### **Step 3: Import Mounting Holes to the PCB Layout**
1. After saving the schematic, go to the **PCB Editor** and click **Update PCB from Schematic**.
2. The four mounting holes will now appear in the PCB layout.

### **Step 4: Positioning Mounting Holes**
1. Position the mounting holes near the **four corners of the board** to provide balanced support.
2. Ensure the holes are spaced evenly and provide good structural integrity.
   - Example: Place the holes **35mm apart in the X direction** and **25mm apart in the Y direction**.

### **Step 5: Aligning and Adjusting Mounting Holes**
1. Use **Align Tools** or adjust the grid size to ensure the holes are aligned and evenly spaced.
2. Ensure the mounting holes are positioned away from any critical components that might be affected by screws or mounts.

---

## **2. Removing Unnecessary Silkscreen Labels**

By default, mounting holes and some connectors may have unnecessary silkscreen labels, which can interfere with the board’s design. These can be removed to clean up the layout.

### **Step 1: Remove Silkscreen from Mounting Holes**
1. Double-click on each mounting hole and edit the **Silkscreen Layer**.
2. Move the **silkscreen labels** (if any) to the **Fabrication Layer** or remove them entirely.

### **Step 2: Adjust Connector Silkscreens**
1. For connectors such as **UART, SWD, and USB**, you may want to remove the generic silkscreen labels (e.g., J1, J2).
2. Instead, replace them with more meaningful labels such as **“USB Connector”**, **“UART”**, or **“SWD Debug”**. This helps during assembly and testing.

---

## **3. Defining the PCB Board Outline**

A properly defined board outline ensures that the PCB will fit within an enclosure or designated space. We will use the **Edge.Cuts layer** to define the shape of the PCB and add rounded corners.

### **Step 1: Switch to Edge.Cuts Layer**
1. In the PCB Editor, switch to the **Edge.Cuts layer** from the right-hand panel.
2. Use the **Draw Line tool** to create the **board outline**. Start by drawing **two horizontal lines** and **two vertical lines** that define the edges of your PCB.

### **Step 2: Determine Board Outline Spacing**
1. The board outline should be at least **3mm away** from the mounting holes to allow space for the screw heads and prevent mechanical interference.
   - Align the outline with the mounting hole patterns so the screws have enough clearance.
   
### **Step 3: Adding Rounded Corners**
1. To create rounded corners, use the **Arc tool**.
   - Select the **center of the mounting hole** and draw an arc between the two perpendicular edges.
2. Repeat this for all four corners to give the PCB a rounded appearance.

### **Step 4: Fine-Tuning Connector Placement**
1. Adjust connectors like **USB** and **SWD** so they are properly aligned with the edge of the board. For example, the **USB-C connector** should be slightly off the edge to ensure proper access when the PCB is placed in an enclosure.
   - Ensure there is enough space for the connectors without compromising structural integrity.
2. Move any other components (e.g., switches) so that they fit within the new board outline.

---

## **4. Adjusting Component Silkscreens and Finalizing Placement**

To ensure a clean and professional layout, adjust silkscreen placement and make final adjustments to the positioning of components before moving on to routing.

### **Step 1: Remove Overlapping Silkscreens**
1. Any component silkscreens that overlap the **board outline** or other components should be moved.
   - For example, the **silkscreen on the USB-C connector** should be removed or edited if it extends past the PCB edge.
2. Edit the **footprint of the component** by double-clicking on it, selecting **Silkscreen**, and removing any unnecessary elements.

### **Step 2: Final 3D View Check**
1. Open the **3D Viewer** by pressing **ALT + 3** to visually inspect the layout.
   - Check if any silkscreens are still overlapping or if components are positioned too close to the edge of the board.
   - Verify that the board outline and mounting holes are correctly placed.

### **Step 3: Move Connectors and Switches**
1. Adjust the position of the **USB connector**, **UART**, **SWD**, and other connectors so they are properly aligned with the board edge.
2. Make sure the components are spaced evenly and that the **switch** protrudes slightly from the edge, making it easier to access.

---

## **5. Conclusion and Next Steps**

You have now completed the process of:
- **Adding mounting holes** and defining their positions.
- **Removing unnecessary silkscreen labels** and improving labeling clarity for easier assembly.
- **Drawing the board outline** with rounded corners and adjusting components to fit within this outline.

The board is now properly structured and visually clean, ready for the next stage, which is **routing the traces**. In this phase, we will connect all the components electrically, ensuring proper signal integrity and power distribution across the PCB.

With the mechanical design elements finalized (mounting holes and board outline), you can now proceed with **fine-tuning the layout** and **PCB routing**.