# Fixing 3D Models and Adjusting Footprints

In this section, we will walk through how to address **missing or incorrect 3D models** and **oversized footprints** in your PCB design using KiCad. These steps are essential for ensuring that your design aligns with real-world components and is suitable for enclosure design, assembly checks, and accurate manufacturing.

---

## **1. Identifying and Resolving 3D Model Issues**

Using the **3D viewer** in KiCad is an effective way to check for potential problems in your PCB layout. The 3D view helps you visualize how your components fit together, ensuring that the footprints and sizes of components are correct. Let’s address two common issues: **missing 3D models** and **oversized footprints**.

### **Step 1: Inspecting the 3D Model**
1. Open the **3D viewer** by pressing **ALT + 3** or clicking **View > 3D Viewer**.
2. Inspect the layout to identify any components that either lack a 3D model or appear incorrectly sized compared to other components.

**Example Problems:**
- Missing 3D model for a USB connector.
- A switch with an **oversized footprint** compared to other components.

---

## **2. Fixing an Oversized Footprint**

Let’s address the issue of an **oversized footprint**. In this example, the **boot zero switch** appears much larger than expected. We’ll modify the footprint in the schematic and update it in the PCB layout.

### **Step 1: Modify the Footprint in the Schematic**
1. **Open the Schematic Editor** and find the component with the problematic footprint (e.g., the boot zero switch).
2. **Double-click** the component to open the properties window.
3. Under **Footprint**, click the **Browse** button to open the footprint selection window.

### **Step 2: Select a New Footprint**
1. In the footprint browser, search for a more appropriate footprint (e.g., a **smaller tactile switch** or a **surface-mount** switch).
   - Example: Select a **smaller tactile switch** footprint, which is more suitable for your design.
2. **Preview the 3D model** to ensure that it matches the desired component size.
3. Once you are satisfied, **double-click** the selected footprint to assign it to the component.

### **Step 3: Update the PCB Layout**
1. After modifying the footprint in the schematic, return to the **PCB Editor**.
2. Click **Update PCB with Changes Made to Schematic** (icon with a wire connecting to the PCB).
3. This updates the PCB layout with the newly selected footprint for the switch.
4. Recheck the footprint in the **3D viewer** to ensure it now fits correctly.

---

## **3. Adding a Missing 3D Model**

A missing 3D model can affect design validation, especially when creating enclosures or performing assembly checks. In this example, the **USB connector** is missing its 3D model, so we’ll add one manually.

### **Step 1: Download the Correct 3D Model**
1. Visit the **manufacturer’s website** for the specific part number of the missing component (e.g., the USB connector).
2. Download the **STEP file** (or other supported 3D format) from the manufacturer's website. Look for the **3D model** in the "Downloads" or "Resources" section.
   - For example, if the connector part number is available, search for the correct model, download it, and save it in your project folder.

### **Step 2: Assign the 3D Model to the Component in KiCad**
1. **Select the component** (e.g., USB connector) in the PCB layout and **double-click** it to open the properties window.
2. Go to the **3D Models** tab and remove the existing model (if any) by clicking **Delete**.
3. Click the **Folder icon** to browse and locate the **STEP file** you downloaded.
   - Navigate to the folder where you saved the model and select it.
4. Once selected, click **OK** to add the 3D model.

### **Step 3: Adjusting the 3D Model Alignment**
After adding the 3D model, you may need to adjust its **position** or **rotation** to ensure it aligns correctly with the footprint on the PCB.

1. In the **3D Models tab**, adjust the **X**, **Y**, and **Z offsets** as needed to position the model correctly.
2. You may also need to adjust the **rotation** of the model to match the orientation of the footprint on the board.
   - For example, try rotating the model by 90 degrees or adjusting the offsets by **trial and error** until the model aligns with the footprint.
3. Use the **3D viewer** to check your adjustments and ensure the model fits correctly.

### **Step 4: Final Check in 3D Viewer**
1. Once the model is positioned correctly, go back to the **3D viewer** and inspect the layout again.
   - Confirm that the USB connector model is now visible and correctly aligned with the footprint.

---

## **4. Finalizing Placement and Ensuring Proper Component Alignment**

Now that the 3D models and footprints are corrected, continue refining your component placement.

### **Step 1: Recheck Component Placement**
1. Return to the **2D PCB layout** and ensure that all components are properly placed.
   - Critical components, such as connectors and switches, should be located near the edges of the board for accessibility.
   - Ensure that components have adequate spacing for soldering and assembly.

### **Step 2: Use the 3D Viewer for Sanity Checks**
1. Frequently check the **3D viewer** during placement to ensure there are no issues with component alignment or interference.
   - This is especially important when designing enclosures or ensuring mechanical clearance for connectors.

### **Step 3: Prepare for Routing**
1. After finalizing the placement, you can move forward with **PCB routing**, ensuring that traces between components are well-organized and optimized for signal integrity.

---

## **Conclusion**

By addressing issues such as **missing 3D models** and **oversized footprints**, you ensure that your PCB design is mechanically accurate and easy to manufacture. Adding 3D models for critical components helps with **enclosure design** and **visual verification**, while properly scaling down footprints ensures that components fit the board and leave room for other important elements.

This detailed process guarantees that the design is ready for further refinement and, eventually, PCB routing. Checking your work frequently in the **3D viewer** ensures that the layout is clean and professional, leading to a successful final product.