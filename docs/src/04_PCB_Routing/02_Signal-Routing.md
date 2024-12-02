# Routing USB Differential Pair and Fine-Tuning Signal Layout

In this section, we'll dive into **routing the USB differential pair**, **adjusting the placement of components like pull-up resistors**, and ensuring proper **spacing for signal traces** like **UART** and **SWD**. Finally, we'll route the **power and ground connections** to complete the PCB layout.

---

## **1. Routing the USB Differential Pair**

### **Step 1: Understanding the Importance of the Differential Pair**
In high-speed designs, the **USB differential pair** (D+ and D-) needs to be routed in a way that maintains **controlled impedance** to ensure signal integrity. While on two-layer PCBs, it can be challenging to meet the strict specifications for **USB 2.0**, keeping the differential traces short and parallel helps mitigate potential issues. The goal is to maintain a **consistent spacing** between D+ and D- and avoid length mismatches.

### **Step 2: Using the Differential Pair Tool**
1. **Labeling**: Ensure that you’ve properly labeled your **D+** and **D-** nets in KiCad as differential pairs.
2. **Routing**:
   - Select the **Route Differential Pair** tool in KiCad.
   - Start routing from the MCU’s **USB D+ and D-** pins and trace these lines to the corresponding pins on the **USB-C connector**.
   - The **track width** and **spacing** should have been predefined earlier (e.g., **0.3mm width** and **0.3mm spacing**).
   - Keep the traces **parallel** to each other throughout the routing process. In your design, the placement of the MCU and the USB connector has allowed for a **straight and direct** routing, which is ideal.

3. **Final Adjustment**:
   - The pull-up resistor (R3) on the **D+** line needs to be placed **in-line** with the trace.
   - Adjust the placement of the resistor slightly so that it does not interfere with the differential pair. You can move it closer to the trace without obstructing the differential pair's flow.

### **Step 3: Checking the Differential Pair**
1. Once routed, check for **equal trace lengths** by selecting both D+ and D- traces and ensuring they are balanced. Length mismatches can cause signal skew.
2. Use the **3D viewer** (shortcut: **ALT + 3**) to visually inspect the differential pair and confirm the layout looks clean and unobstructed.

---

## **2. Routing Other Signal Traces: SWD, UART, and Boot Zero**

### **Step 1: Routing SWD (Serial Wire Debug)**
1. For **SWD clock (SWCLK)** and **SWDIO** signals, use a **0.3mm track width**.
2. Ensure that the **clock signal** is spaced away from other high-speed signals to minimize interference.
   - Start from the MCU’s **SWCLK** pin and route directly to the **SWD header**. Give it enough spacing to avoid crosstalk with nearby signals.
   - Similarly, route **SWDIO** directly, avoiding interference from power traces or other high-speed signals like USB.

### **Step 2: Routing UART Signals**
1. Start routing **TX** and **RX** traces from the MCU to the **UART connector**:
   - Use **0.3mm track width** for both signals.
   - Ensure that the **TX** and **RX** traces are not running parallel for long distances with other sensitive signals to avoid **crosstalk**.

2. **Fine-Tuning the Layout**:
   - After routing the traces, verify the layout by checking that each trace is properly spaced from one another.
   - Use the **3D viewer** to confirm that no traces overlap or interfere with components like **capacitors** or **resistors**.

### **Step 3: Routing Boot Zero and Other Configuration Signals**
1. For **Boot Zero (BOOT0)**, the routing process is straightforward:
   - Route **BOOT0** from the MCU to the **resistor** and **switch** in series. Use **0.3mm track width**.
   - Ensure proper clearance between the trace and adjacent components, giving it enough space to avoid any interference from other signals or power traces.

---

## **3. Adjusting Layout for Power and Ground Routing**

Now that we’ve routed the critical signals, we’ll finalize the **power** and **ground** connections.

### **Step 1: Ground Routing Using Vias**
1. **Ground Plane on the Bottom Layer**:
   - With the ground plane already placed on the **bottom layer**, route any **ground pins** on the top layer directly to the ground plane using **vias**.
   - For each ground pad, drop a **via** near the pad (but not too close to avoid soldering issues).
   - Use **larger vias** (e.g., 0.4mm) for power pins to ensure low resistance.

2. **Minimizing Cuts in the Ground Plane**:
   - Ensure that you **minimize the number of cuts** in the ground plane by keeping vias and traces on the top layer whenever possible.

### **Step 2: Power Routing with Power Puddles**
1. **Power Puddles**:
   - For the **3.3V rail**, create **large power puddles** in the top layer near the MCU, ensuring all components requiring 3.3V are connected efficiently.
   - Use the **Add Filled Zone** tool to create **copper pours** that provide a low-impedance path for the 3.3V supply.

2. **Wide Power Traces**:
   - Route **wide power traces** (0.5mm or larger) from the **voltage regulator** to the **3.3V power puddles**.
   - Ensure that these power traces are **short and direct**, avoiding excessive length that might cause voltage drops.
   
3. **Routing the 3.3V Supply**:
   - Use **0.5mm tracks** to route power from the **voltage regulator’s output capacitor** to each **3.3V power pin**.
   - Where necessary, drop **vias** to jump between layers, but minimize the number of jumps to maintain the integrity of the power distribution.

---

## **4. Finalizing Ground and Power Connections**

After routing all the critical signals, USB, and power, the last step is to **fine-tune the ground and power connections** to ensure all pads and components are properly connected.

### **Step 1: Using Power Puddles for Ground and Power**
1. If needed, use the **Fill Zone** tool to create additional copper pours for **ground** and **power** traces, ensuring that all components have solid connections to their respective nets.
2. **Minimize power trace lengths** to reduce potential **voltage drops** or **EMI** issues. Where long traces are unavoidable, ensure that they are wide enough to carry the required current.

### **Step 2: Checking Thermal Reliefs and Ground Continuity**
1. Ensure that all ground pads connected to the **ground plane** have **thermal reliefs**. These are especially important for through-hole components to prevent heat dissipation issues during soldering.
2. **Run a Design Rule Check (DRC)** to verify that there are no **unconnected ground pads** or power pins. The DRC will help catch any errors before finalizing the layout.

---

## **5. Final Review of Layout**

Before moving on to the final steps of generating manufacturing files, review the entire layout.

### **Step 1: 3D Viewer Inspection**
1. Use the **3D viewer** to visually inspect the layout. Check that:
   - **USB differential pair** is correctly routed.
   - No traces are overlapping components or interfering with silkscreen.
   - **Power and ground** connections are correct, and no ground plane is fragmented.

### **Step 2: Final Adjustments**
1. Adjust any remaining silkscreen labels and verify that all **net labels** are clear.
2. Ensure that all **vias** and **pads** are properly placed and spaced according to design specifications.

---

## **6. Next Steps: Finalizing the Design**

After routing is complete, follow these next steps to finalize the design:
1. **Electrical Rule Check (ERC)**: Run the ERC to verify that all components are connected correctly and that there are no missing or floating nets.
2. **Generate Gerber Files**: Once the design passes all checks, generate the **Gerber files** for manufacturing.
3. **Submit to PCB Fabrication**: Use the Gerber files to submit the design to a PCB manufacturer for production.

This concludes the routing and layout process, ensuring that all **critical signals**, **power**, and **ground connections** are clean and efficient. The PCB is now ready for the final stages before manufacturing.