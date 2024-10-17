# Assigning Footprints to Schematic Symbols

In this section, we will walk through the process of assigning footprints to the schematic symbols in KiCad. Each component in your schematic must be linked to a physical footprint that defines its size, shape, and pad configuration on the printed circuit board (PCB). KiCad version 6 provides a robust tool for footprint assignment, offering built-in libraries and the ability to import or create custom footprints.

---

## **1. Opening the Footprint Assignment Tool**

Before proceeding with footprint assignment, ensure that your schematic is complete, well-annotated, and free of electrical errors. Once the schematic is ready:
1. Click the **"Run Footprint Assignment Tool"** button on the toolbar. This opens the **Footprint Assignment Window**.
   - On the **left panel**, you’ll see the list of **available footprint libraries**, which include a wide variety of standard components (resistors, capacitors, ICs, connectors, etc.).
   - The **center panel** shows all the symbols you’ve placed in the schematic, listing each component and its associated symbol name.
   - The **right panel** allows you to select the relevant footprint for each component from the library.

---

## **2. Filtering Footprints by Pins and Libraries**

KiCad offers filtering options to help narrow down your footprint selection:
- **Enable filtering by pin count**: This ensures that the footprint matches the number of pins on the component.
- **Enable library filtering**: This limits the displayed footprints to only those available in the library associated with the selected component symbol.
  
These filters streamline the process by reducing the number of available footprints to those that match your components.

---

## **3. Assigning Footprints to Common Components**

### **Step 1: Capacitors**
1. Select a **ceramic capacitor** (e.g., 100nF or 22µF) from the list.
2. Assign a standard **SMD footprint** such as:
   - **0402** for smaller capacitors (e.g., 100nF).
   - **0603** or **0805** for larger capacitors (e.g., 10µF or 22µF).
3. Double-click the footprint to assign it to the component.

**Note**: The size of the capacitor depends on the required power handling and the capabilities of your PCB assembly method. Smaller sizes (e.g., 0402) are suitable for compact designs but may be harder to hand-solder.

### **Step 2: Resistors**
1. Select a **resistor** (e.g., 1.5kΩ or 10kΩ) from the list.
2. Assign a standard SMD footprint such as **0402**, **0603**, or **0805**.
   - **0402** is commonly used for low-power applications.
   - Larger sizes like **0603** or **0805** are used for components that need higher power dissipation or are easier to solder by hand.
   
**Tip**: If your design doesn't require high power handling, **0402** or **0603** is a safe option for general-purpose resistors.

### **Step 3: LEDs**
1. Select the **LED** symbol from the schematic.
2. Assign a **0603** or **0805** footprint for the LED, depending on the size and brightness you need.
   - For debug LEDs, **0603** is typically sufficient.

### **Step 4: Crystals**
1. Select the **crystal** symbol.
2. Choose a standard **SMD package** like **3.2x2.5mm** (SMD-3225) or **2.5x2.0mm**, depending on the size of the crystal.
3. This footprint typically includes two pads for crystal connections and may also include grounding pads for noise reduction.

### **Step 5: Connectors**
1. Select a **connector** symbol from the schematic (e.g., USB or pin headers).
2. For **USB Micro connectors**, choose a standard **Micro-USB-B** footprint, which is commonly available in KiCad’s connector library.
3. For **pin headers** (used for debugging, UART, I²C, etc.), select a **2.54mm pitch vertical header** (e.g., 1x4 or 2x4 pin headers). You can inspect the 3D model to ensure it matches the physical connector you plan to use.

### **Step 6: AMS1117-3.3 Voltage Regulator**
1. The **AMS1117-3.3** voltage regulator will typically use a **SOT-223** package, which is pre-assigned in KiCad for this symbol.
2. If necessary, you can inspect the footprint in 3D by right-clicking and selecting **View Footprint 3D** to ensure it matches the component you plan to use.

### **Step 7: STM32 Microcontroller**
1. The STM32 microcontroller comes in various packages. The footprint will depend on the package of your microcontroller (e.g., **LQFP64**, **LQFP48**).
2. If not already assigned, search for the correct footprint in the library by filtering based on the package type (e.g., **LQFP64** for a 64-pin package).

---

## **4. Inspecting Footprints**

Before assigning footprints, you can visually inspect them to ensure they match the physical components you plan to use:
1. **Right-click** on a footprint and select **View Footprint 3D**.
   - This opens a 3D model of the footprint, allowing you to check the component's physical layout and ensure it aligns with the expected size and pin configuration.
   
This is especially useful for connectors, where alignment and pin layout are critical.

---

## **5. Applying and Saving Footprint Assignments**

Once you’ve assigned footprints to all components:
1. Click **Apply, Save Schematic & Continue** to save the footprint assignments.
2. Click **OK** to close the **Footprint Assignment** window.

Now, all your schematic symbols have corresponding footprints that will be used when transitioning to the PCB layout phase.

---

## **6. Final Checks Before PCB Layout**

Before moving to PCB layout:
- **Ensure consistency** between component symbols and their assigned footprints.
- Double-check that the **footprint sizes** are appropriate for your PCB manufacturing process. For instance:
  - **Smaller components (0402, 0603)** are better for compact designs but may require advanced assembly techniques.
  - **Larger components (0805, 1206)** are easier to solder by hand and handle more power.

- **Review connectors and special components** (like crystals and regulators) to ensure the footprints are correct and that the component pin configuration matches the footprint.

---

## **7. Conclusion**

By assigning footprints to schematic symbols, you have successfully linked each component in the schematic to its physical counterpart in the PCB layout. This process is essential for translating the logical connections in your schematic into a physical board design. You’re now ready to move on to the **PCB layout and routing** stage, where you will position components, route traces, and finalize the design for manufacturing.

## **Next Step: PCB Layout and Routing**
With the footprints assigned, the next step is to transition to **PCB layout**. In the layout phase, you'll arrange components on the PCB and route the electrical connections, ensuring signal integrity, proper power distribution, and manufacturability.