# Ground and Power Routing, Decoupling Capacitors, and Critical Connections

In this section, we'll cover how to proceed with routing for a two-layer PCB. Our focus will be on routing **decoupling capacitors**, the **crystal oscillator**, and other **sensitive components**. Additionally, we will discuss how to properly route **ground and power planes**, ensuring minimal noise and clean signal integrity.

---

## **1. Setting Up the Ground Plane**

For a two-layer board, the **ground plane** is typically placed on the **bottom layer**. This ensures a **low impedance return path** for signals on the top layer, reducing noise and providing a stable reference for sensitive components.

### **Step 1: Creating a Ground Plane**
1. **Select the Bottom Layer**: In KiCad, click on the bottom copper layer.
2. **Create a Ground Fill Zone**:
   - Use the **Add Filled Zone** tool (shortcut: **SHIFT + CTRL + F**) to draw a filled copper area.
   - Choose **GND** as the net for the zone, ensuring that all ground pins are connected to this plane.
   - Set a clearance of **0.3mm** and a minimum trace width of **0.25mm**. This provides enough clearance for manufacturing while maintaining sufficient width for signal and power routing.
   - Enable **thermal relief** for through-hole pads, which makes soldering easier. Set **thermal relief** with a spoke width and clearance of **0.5mm**.
   
   > **Note**: Thermal relief ensures that the ground pads connected to the plane are still easy to solder without creating thermal dissipation issues.
   
3. **Define the Shape**: Start at one corner of the PCB and draw the ground zone, ensuring that the zone encompasses the entire bottom layer.
4. **Fill the Zone**: After defining the area, press **B** to fill the copper plane, creating the ground plane.

### **Step 2: Dropping Vias for Ground**
1. For each **ground pin** on the top layer, use **vias** to connect the ground pin to the ground plane:
   - Route a short ground trace from the pad (using 0.5mm width).
   - Press **V** to place a via that connects the ground trace to the ground plane.
   - Keep vias **slightly spaced** from the ground pad to avoid soldering issues.

2. **Minimizing Ground Loops**: Instead of placing multiple vias from the same ground pin to the plane, ensure that the ground traces are centralized and minimize the number of vias to avoid creating **ground loops**.

---

## **2. Routing Critical Components**

After setting up the ground plane, begin by routing the **critical components**. These include **decoupling capacitors**, **the crystal oscillator**, and **sensitive signals**.

### **Step 1: Routing Decoupling Capacitors**
1. **Track Width**: Use a **0.3mm track width** for routing between the decoupling capacitors and the MCU.
2. **Routing Strategy**:
   - Start by routing from the **power pin** of the MCU to the **decoupling capacitor**.
   - Maintain **maximum spacing** between the decoupling capacitor trace and other signal traces to avoid **crosstalk** and ensure **clean power delivery**.
3. **Wider Traces for Power**:
   - For the capacitor's connection to the **3.3V power rail**, increase the track width to **0.5mm**.
   - Route these wider traces from the decoupling capacitors to the **power puddles** or **power plane** to ensure stable power delivery with minimal voltage drop.

4. **Consistency**: Repeat this process for all decoupling capacitors around the MCU, ensuring they are positioned as **close to the MCU pins** as possible.

### **Step 2: Routing the Crystal Oscillator**
1. **Track Width**: Use **0.3mm tracks** for the oscillator signals.
2. **Maximize Spacing**: Ensure that the signals from **HSE (High-Speed External) in** and **HSE out** are **well-spaced** from each other. This prevents interference between the sensitive clock signals.
3. **Short, Direct Paths**:
   - Keep the traces between the MCU and the crystal **as short as possible**. Shorter traces reduce parasitic inductance and capacitance, ensuring stable clock operation.
   - Route the traces **directly under the crystal** if necessary, avoiding long, winding paths.
4. **Grounding**: Ensure that the ground connections for the crystal oscillator are properly routed to the ground plane, using short vias or direct connections to nearby ground pins.

---

## **3. Routing USB Differential Pair and Other Signals**

Next, focus on routing the **USB differential pair** and other important signals like **SWD** and **UART**.

### **Step 1: Routing the USB Differential Pair**
1. **Differential Pair Tool**:
   - Use KiCad’s **Route Differential Pair** tool for the USB D+ and D- signals.
   - Select the **track width** and **spacing** that were defined earlier (e.g., **0.3mm width** with **0.3mm spacing**).
   
2. **Keep the Pair Together**:
   - Start routing from the MCU's USB pins and route directly to the USB connector.
   - Keep the traces **parallel** and **close together**. This ensures that they behave as a differential pair and maintain the required impedance.
   
3. **Avoid Length Mismatch**:
   - Ensure that both traces in the differential pair are of **equal length**. Any mismatch can lead to signal degradation, especially in high-speed USB signals.

### **Step 2: Routing SWD and UART**
1. **SWD (Serial Wire Debug)**:
   - Use **0.3mm tracks** for the **SWD clock** and **SWDIO** signals.
   - Keep these traces as **short** and **direct** as possible, and avoid placing them near high-speed signals like USB.
   
2. **UART Signals**:
   - Similarly, route **TX** and **RX** traces using 0.3mm track width.
   - Ensure that the traces run directly to the UART header with **adequate spacing** from other signals to avoid interference.

### **Step 3: Avoiding Crosstalk**
1. **Signal Isolation**:
   - When routing multiple signals, ensure that **critical traces** (e.g., USB, UART) are spaced well away from **high-current power traces**.
   - Avoid running traces in parallel for long distances, as this can increase crosstalk between them.
   
2. **Minimize Layer Crossovers**:
   - Keep traces on the same layer where possible to minimize the need for vias. Every via introduces **additional impedance**, which can affect high-speed signals.

---

## **4. Finalizing Power and Ground Routing**

Once the critical components and signals are routed, finalize the routing for **power** and **ground connections**.

### **Step 1: Power Puddle Creation**
1. **Create Power Puddles**:
   - For the **3.3V** and **Vbus** power rails, create **large copper pours** (puddles) on the **top layer**.
   - Use the **Add Filled Zone** tool to draw copper areas connected to the power nets. These puddles will help distribute power efficiently across the board.
   
2. **Avoid Cutting the Ground Plane**:
   - Minimize cuts in the ground plane by ensuring that power puddles and traces do not disrupt the continuity of the bottom ground layer.
   
### **Step 2: Routing Power Traces**
1. **Use Wide Traces**:
   - For the **3.3V power rail**, use **wide traces** (0.5mm or greater) to carry current across the board. This helps to reduce voltage drops and ensures stable power delivery.
   
2. **Short Power Jumps**:
   - If a trace needs to jump between layers, use **larger vias** to minimize resistance and ensure adequate current flow. Keep the length of power traces short to avoid excessive voltage drop.

### **Step 3: Grounding Sensitive Components**
1. **Ground Critical Components**:
   - Ensure that **decoupling capacitors**, the **crystal oscillator**, and the **USB connector** are all properly grounded to the bottom ground plane via short, direct paths.

---

## **5. Completing the Layout**

Now that the critical components and signals are routed, the layout is nearing completion. Ensure that:
1. **All components** are properly connected, and all signals are routed with **adequate spacing**.
2. **Power and ground traces** are wide and well-connected to ensure **low impedance paths**.
3. **Thermal reliefs** are in place for easy soldering.

## **6. Next Steps**

With the layout and routing complete, the next steps are:
1. **Check for design rule violations** using KiCad’s **Design Rule Check (DRC)** tool.
2. **Inspect the layout in 3D** using the 3D viewer to ensure that everything is aligned and properly placed.
3. **Finalize the layout** by reviewing any remaining signals, ensuring proper clearances, and adding **labels** to the silkscreen for clarity.

By following these steps, you will ensure a high-quality PCB design with **clean signal routing**, **stable power delivery**, and **minimal noise**.