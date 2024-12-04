# Adding Mounting Holes, Defining Board Outline, and Preparing for Routing

In this section, we delve into the essential steps of adding **mounting holes**, defining the **board outline**, and adjusting the layout to prepare for PCB routing using KiCad. These procedures are critical for ensuring that your PCB is securely mounted, properly enclosed, and optimized for manufacturing. The following guide provides detailed instructions, practical examples, and best practices to help you achieve a professional and reliable PCB design.

---

## **1. Adding Mounting Holes to the PCB**

Mounting holes play a pivotal role in attaching the PCB to an enclosure or mechanical structure, providing mechanical stability. They are especially crucial in projects that require mounting within cases or during assembly handling.

### **Step 1: Add Mounting Holes to the Schematic**

1. **Open the Schematic Editor:**
   - Launch KiCad and open your project.
   - Navigate to the **Schematic Editor** by clicking on the corresponding icon.

2. **Access the Symbol Library:**
   - Click on the **Add Symbol** tool (usually represented by an op-amp icon or a symbol with a plus sign).
   - In the **Symbol Library** dialog, use the search bar to locate **"Mounting Hole"** symbols.

3. **Select the Appropriate Mounting Hole Symbol:**
   - **Simple Mounting Hole:** A non-electrically connected hole, ideal for mechanical stability without affecting the electrical design.
   - **Mounting Hole with Pad:** Includes a pad that can be tied to ground, beneficial for grounding purposes, such as grounding oscilloscope probes.
   - For this design, select the **simple mounting hole** to avoid unintended electrical connections.

4. **Place Mounting Holes on the Schematic:**
   - Position four mounting holes strategically on the schematic to correspond with the PCB's corners.
   - Ensure that their locations do not interfere with critical components or signal paths.

### **Step 2: Select and Assign Footprint**

1. **Access Mounting Hole Properties:**
   - Double-click each mounting hole symbol to open the **Symbol Properties** dialog.

2. **Assign Footprint:**
   - Click the **Footprint** button to open the **Footprint Library Browser**.
   - Search for a suitable **mounting hole footprint**. Common footprints include:
     - **Mounting Hole M2:** Suitable for small boards requiring minimal space.
     - **Mounting Hole M3:** Provides a larger diameter for increased mechanical strength.
   - Select the appropriate footprint based on your board size and mechanical requirements.

3. **Uniform Footprint Assignment:**
   - Assign the same footprint to all four mounting holes to maintain consistency.
   - Utilize the **copy and paste** functions to replicate the footprint assignment efficiently.

4. **Confirm Footprint Assignment:**
   - Verify that each mounting hole has the correct footprint by reviewing the properties.

### **Step 3: Import Mounting Holes to the PCB Layout**

1. **Save the Schematic:**
   - After placing and assigning footprints to all mounting holes, save your schematic changes.

2. **Open the PCB Editor:**
   - Navigate to the **PCB Editor** by clicking its icon within KiCad.

3. **Update PCB from Schematic:**
   - Click on **Update PCB from Schematic** (often represented by an arrow or synchronization icon).
   - In the **Update PCB** dialog, ensure that the **Mounting Holes** are selected for import.
   - Confirm to import the mounting holes into the PCB layout.

### **Step 4: Positioning Mounting Holes**

1. **Strategic Placement:**
   - Position the mounting holes near the **four corners of the PCB** to provide balanced support.
   - Balanced mounting prevents stress concentration and enhances mechanical stability.

2. **Spacing Considerations:**
   - Ensure even spacing to maintain structural integrity.
   - **Example Placement:**
     - **X-Axis Spacing:** 35mm apart.
     - **Y-Axis Spacing:** 25mm apart.
   - Adjust spacing based on board size and enclosure dimensions.

3. **Avoiding Interference:**
   - Ensure mounting holes do not interfere with component placement or signal paths.
   - Leave adequate clearance around the holes for screw heads and mounting hardware.

### **Step 5: Aligning and Adjusting Mounting Holes**

1. **Utilize Alignment Tools:**
   - Use KiCad's **Align Tools** to ensure precise alignment of mounting holes.
   - Access these tools via the **Tools** menu or relevant keyboard shortcuts.

2. **Grid Adjustment:**
   - Modify the grid size if necessary to achieve finer placement accuracy.
   - Access grid settings through the **View** or **Grid** menu.

3. **Clearance from Critical Components:**
   - Position mounting holes away from sensitive or critical components to prevent mechanical stress from affecting their functionality.
   - **Best Practice:** Maintain a minimum clearance distance (e.g., 5mm) from high-speed or heat-sensitive components.

---

## **2. Removing Unnecessary Silkscreen Labels**

Silkscreen layers provide labels and markings on the PCB, aiding in assembly and troubleshooting. However, unnecessary labels, especially around mounting holes and connectors, can clutter the design and interfere with manufacturing.

### **Step 1: Remove Silkscreen from Mounting Holes**

1. **Edit Mounting Hole Properties:**
   - Double-click each mounting hole in the PCB layout to open its **Footprint Properties**.

2. **Modify Silkscreen Layer:**
   - Navigate to the **Silkscreen Layer** settings within the footprint.
   - **Option 1:** Move silkscreen labels to the **Fabrication Layer** if they serve a reference purpose.
   - **Option 2:** Remove silkscreen labels entirely to declutter the PCB.

3. **Confirm Changes:**
   - Save the changes to each mounting hole footprint.
   - Verify that silkscreen labels around mounting holes are no longer present or have been relocated appropriately.

### **Step 2: Adjust Connector Silkscreens**

1. **Identify Connectors with Generic Labels:**
   - Locate connectors such as **UART**, **SWD**, and **USB** that may have generic labels like **J1**, **J2**, etc.

2. **Edit Connector Labels:**
   - Double-click each connector to open its **Footprint Properties**.
   - Access the **Silkscreen** layer.

3. **Replace Generic Labels:**
   - Substitute generic labels with descriptive names to enhance clarity.
     - **Example Replacements:**
       - **J1 → USB Connector**
       - **J2 → UART Interface**
       - **J3 → SWD Debug Port**
   - This practice facilitates easier assembly, testing, and troubleshooting by clearly identifying each connector's function.

4. **Maintain Consistency:**
   - Ensure that all connectors are uniformly labeled across the PCB to avoid confusion.

---

## **3. Defining the PCB Board Outline**

A well-defined board outline is crucial for ensuring that the PCB fits within its intended enclosure and meets manufacturing specifications. The **Edge.Cuts layer** in KiCad is used to define the physical boundaries and shape of the PCB, including any rounded corners or specific contours.

### **Step 1: Switch to Edge.Cuts Layer**

1. **Access Edge.Cuts Layer:**
   - In the **PCB Editor**, locate the **Layer Selection Panel** typically found on the right side.
   - Select the **Edge.Cuts** layer to begin drawing the board outline.

2. **Initiate Board Outline Drawing:**
   - Use the **Draw Line** tool (usually represented by a line icon) to start defining the PCB's edges.
   - Begin by drawing **two horizontal lines** and **two vertical lines** that outline the primary dimensions of the PCB.

### **Step 2: Determine Board Outline Spacing**

1. **Maintain Clearance from Mounting Holes:**
   - Ensure that the board outline is at least **3mm away** from all mounting holes.
   - This clearance prevents mechanical interference from screw heads and mounting hardware.

2. **Align Outline with Mounting Pattern:**
   - Position the outline to align with the mounting hole pattern, ensuring sufficient clearance around each hole.
   - **Example Alignment:**
     - If mounting holes are placed at (0,0), (35,0), (35,25), and (0,25) mm, adjust the board edges accordingly to maintain the 3mm clearance.

3. **Consider Enclosure Dimensions:**
   - Verify that the board outline accommodates the internal dimensions of the intended enclosure.
   - Allow additional space if necessary for cable management or additional components.

### **Step 3: Adding Rounded Corners**

1. **Use the Arc Tool for Rounded Corners:**
   - Select the **Arc Tool** from the drawing tools palette.
   - Click to place the center point of the arc at the **corner intersection** of the horizontal and vertical lines.

2. **Create Smooth Transitions:**
   - Draw an arc that smoothly connects the two perpendicular edges, replacing the sharp corner with a rounded one.
   - **Radius Consideration:** Choose a radius that maintains structural integrity without excessively reducing the PCB area (e.g., 5mm radius).

3. **Repeat for All Corners:**
   - Apply the same method to all four corners to achieve a uniform rounded appearance.
   - Ensure that all arcs are symmetrical and consistent in size.

4. **Review the Board Outline:**
   - Inspect the rounded corners for accuracy and smoothness.
   - Make adjustments as necessary to ensure that the outline meets design specifications.

### **Step 4: Fine-Tuning Connector Placement**

1. **Align Connectors with Board Edge:**
   - Position connectors like **USB** and **SWD** so that they are slightly offset from the board edge.
   - **Example:** Place a **USB-C connector** with part of it extending beyond the edge to ensure accessibility when housed in an enclosure.

2. **Ensure Sufficient Access:**
   - Verify that connectors protrude adequately for user interaction without hindering enclosure closure.
   - **Best Practice:** Maintain a minimum clearance (e.g., 2mm) between the connector and the board edge to prevent interference.

3. **Adjust Component Placement:**
   - Relocate other components, such as switches or LEDs, to fit within the newly defined board outline.
   - Ensure that all components are accessible and do not overlap with the board's edges or other critical features.

4. **Validate Clearance:**
   - Use KiCad's **Design Rule Checker (DRC)** to ensure that all components and connectors have adequate clearance from the board edges and each other.

---

## **4. Adjusting Component Silkscreens and Finalizing Placement**

A clean and professional PCB layout requires meticulous adjustment of silkscreen elements and final placement refinements before routing. This ensures that the PCB is not only functional but also aesthetically pleasing and manufacturable.

### **Step 1: Remove Overlapping Silkscreens**

1. **Identify Overlapping Silkscreens:**
   - Inspect the PCB layout for any silkscreen elements that overlap with the **board outline** or other components.
   - Common culprits include labels on connectors like the **USB-C connector**.

2. **Edit Component Footprints:**
   - Double-click on the affected component to open its **Footprint Properties**.
   - Navigate to the **Silkscreen Layer** settings.

3. **Modify or Remove Silkscreen Elements:**
   - **Option 1:** Relocate silkscreen labels to a less congested area within the PCB.
   - **Option 2:** Remove unnecessary silkscreen elements entirely to declutter the layout.

4. **Ensure Compliance with Design Rules:**
   - Verify that the removal or relocation of silkscreen elements does not violate any design rules or obscure critical information.

### **Step 2: Final 3D View Check**

1. **Access 3D Viewer:**
   - Press **ALT + 3** or navigate to the **View** menu and select **3D Viewer** to open the 3D visualization of your PCB.

2. **Inspect Silkscreen and Component Placement:**
   - Rotate and zoom into different areas to ensure that silkscreens do not overlap with the board edges or interfere with component placements.
   - Look for any components positioned too close to the PCB edges that might affect manufacturability or assembly.

3. **Verify Board Outline and Mounting Holes:**
   - Ensure that the board outline is accurately represented and that mounting holes are correctly placed and sized.
   - Confirm that mounting holes do not interfere with any components or traces.

4. **Make Necessary Adjustments:**
   - Return to the **PCB Editor** to adjust any components or silkscreen elements that do not meet the desired criteria.
   - Repeat the 3D view check until the layout meets all visual and functional requirements.

### **Step 3: Move Connectors and Switches**

1. **Adjust Connector Positions:**
   - Reposition connectors such as **USB**, **UART**, and **SWD** to align properly with the board edges.
   - Ensure that connectors are easily accessible and do not obstruct other components.

2. **Optimize Switch Placement:**
   - Position switches so that they protrude slightly from the board edge, facilitating easy access.
   - Verify that switches are not obstructed by the enclosure or other mechanical structures.

3. **Ensure Even Spacing:**
   - Distribute components evenly across the PCB to balance the layout and reduce potential signal interference.
   - Maintain consistent spacing between connectors and other peripherals to enhance the PCB's usability.

4. **Confirm Alignment with Board Outline:**
   - Ensure that all moved connectors and switches are within the defined board outline and do not extend beyond permissible boundaries.
   - Use alignment tools to maintain precision in component placement.

5. **Final Component Check:**
   - Review all components to ensure they are correctly oriented and positioned for optimal performance and manufacturability.
   - Ensure that connectors align with their respective headers or external interfaces.

---

## **5. Conclusion and Next Steps**

Congratulations! You have successfully completed the critical steps of:

- **Adding Mounting Holes:** Implemented four strategically placed mounting holes to ensure mechanical stability and secure attachment within enclosures.
- **Removing Unnecessary Silkscreen Labels:** Cleared clutter from the silkscreen layer, enhancing the PCB's readability and manufacturability.
- **Defining the Board Outline:** Crafted a precise board outline with rounded corners, ensuring compatibility with enclosures and maintaining structural integrity.
- **Adjusting Component Placement:** Fine-tuned the placement of connectors and switches, ensuring accessibility and optimal layout before routing.

The PCB is now well-structured and visually clean, setting a solid foundation for the next phase: **Routing the Traces**. In this upcoming stage, you will connect all the components electrically, ensuring proper signal integrity and power distribution across the PCB.

### **Next Steps: Routing the Traces**

1. **Plan the Routing Path:**
   - Identify critical signal paths and prioritize routing based on signal integrity and minimal interference.
   
2. **Utilize Routing Tools:**
   - Leverage KiCad’s automatic and manual routing tools to create efficient and clean trace layouts.

3. **Implement Best Practices:**
   - Follow routing best practices such as maintaining adequate trace widths, minimizing via usage, and ensuring proper grounding.

4. **Perform Design Rule Checks (DRC):**
   - Continuously run DRCs to identify and rectify any routing issues or violations before finalizing the design.

With the mechanical design elements finalized, you are now poised to transition into fine-tuning the layout and meticulously routing the PCB traces to complete your professional PCB design.

---

## **Best Practices Summary**

- **Consistent Footprint Assignment:** Use uniform footprints for mounting holes to maintain consistency and simplify the manufacturing process.
- **Clear Silkscreen Labels:** Use descriptive labels for connectors and critical components to facilitate easier assembly and troubleshooting.
- **Adequate Clearance:** Ensure sufficient spacing between mounting holes, components, and the board outline to prevent mechanical and electrical interference.
- **Precision in Alignment:** Utilize KiCad’s alignment and grid tools to achieve precise component placement and board outline definition.
- **Visual Verification:** Regularly use the 3D Viewer to inspect the PCB layout for any visual inconsistencies or placement issues.
- **Iterative Review:** Continuously review and adjust the layout throughout the design process to ensure adherence to design specifications and best practices.

By adhering to these best practices, you ensure that your PCB design is not only functionally robust but also manufacturable and aesthetically pleasing.