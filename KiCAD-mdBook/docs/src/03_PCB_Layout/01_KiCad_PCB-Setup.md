# PCB Layout and Routing Setup in KiCad

In this section, we will begin the process of creating the **PCB layout** for our STM32-based design in KiCad. This involves setting up the **board stack**, configuring **design rules**, defining **track sizes**, and importing the **component footprints** from our schematic. These steps will prepare the board for efficient layout and routing, ensuring manufacturability and signal integrity.

---

## **1. Opening the PCB Layout Editor**

Once you have completed your schematic and assigned footprints to all components, it’s time to transition to the PCB layout stage. To do this:
1. Click the **"Open PCB Editor"** button in the toolbar.
2. You’ll be presented with a new window that is the **PCB Layout Editor** (Board Editor).

At first glance, the PCB editor may seem overwhelming, but it’s structured in a way that allows for methodical layout and routing.

---

## **2. Setting Up the PCB Board Stack**

The **board stack** defines the number of layers and the material properties of the PCB. For simpler designs, such as the STM32 project, a **two-layer board** is sufficient, with the top layer typically used for signal routing and the bottom layer used for a **solid ground plane**.

### **Step 1: Configuring the Board Layers**
1. In the PCB Editor, click the **"Board Setup"** button in the top-left corner to open the **Board Setup window**.
2. In the **Layers** tab, configure the following:
   - **Top Layer (Front Copper)**: This layer is used for signal routing.
   - **Bottom Layer (Back Copper)**: Typically, this is used for a solid ground plane.
   - Leave the default settings for **Silkscreen**, **Solder Mask**, and **Paste layers**.

### **Step 2: Set Ground Plane**
1. Set the **Bottom Copper Layer** as a **solid ground plane**. This allows you to easily connect components to ground by dropping vias from the top layer to the ground plane.
   - To connect a signal to the ground plane, you will use **vias**, which are small holes that connect the top and bottom layers.

### **Step 3: Stack-Up View**
1. Switch to the **Physical Stack-Up** tab to see a visual representation of your PCB stack.
   - You should see the **Top Copper layer**, a **dielectric layer** (insulating material), the **Bottom Copper layer**, and other associated layers like the **Solder Mask** and **Silkscreen**.
   - For a typical 2-layer PCB, the total thickness is usually around **1.6mm**, which is standard for most PCB manufacturers.

---

## **3. Setting Up Design Rules**

Design rules ensure that your PCB can be manufactured within the capabilities of your PCB fabricator. These rules define the **minimum trace width**, **clearance between copper features**, and **via sizes**.

### **Step 1: Understanding Manufacturer Capabilities**
Before setting up design rules, refer to your PCB manufacturer's **design capabilities**. For instance, a manufacturer like **JLCPCB** or **PCBWay** will provide details about:
   - **Minimum trace width** (e.g., 0.2mm or 8 mils).
   - **Minimum clearance between copper features** (e.g., 0.2mm).
   - **Via sizes** (e.g., 0.6mm pad diameter with 0.3mm drill hole).

### **Step 2: Configuring Design Rules in KiCad**
1. In the **Board Setup** window, go to the **Design Rules** tab.
2. Set the following parameters based on your PCB manufacturer's specifications:
   - **Minimum track width**: Set to **0.3mm** (or the value specified by your manufacturer).
   - **Clearance**: Set to **0.3mm** (for copper-to-copper clearances).
   - **Via drill diameter**: Set to **0.3mm** with a **pad diameter** of **0.7mm**.
   - **Annular ring width**: This defines the copper ring around a via.

---

## **4. Pre-Defining Track Sizes**

Track sizes define the width of the copper traces that connect different components. Different traces may need different widths, especially when handling signals vs. power.

### **Step 1: Defining Signal and Power Track Sizes**
1. In the **Predefined Sizes** section of the **Board Setup** window, define track sizes for signals and power:
   - **Signal traces**: Use **0.3mm** width (suitable for general signal routing).
   - **Power traces**: Use **0.5mm** width (for routing VCC or power lines that carry higher current).

### **Step 2: Defining Via Sizes**
- Define the standard via size as:
   - **Pad diameter**: **0.7mm**.
   - **Drill hole diameter**: **0.3mm**.

### **Step 3: Adding Differential Pair Sizes**
If your design includes high-speed signals (such as USB), you will need **differential pairs**:
1. Define the differential pair width and gap:
   - **Trace width**: **0.3mm**.
   - **Gap between traces**: **0.3mm**.
   
**Note**: For USB differential pairs, it's crucial to route the two traces in parallel and keep them as short as possible to maintain signal integrity.

---

## **5. Importing Component Footprints**

Now that the board is set up and design rules are defined, it’s time to import the component footprints from your schematic.

### **Step 1: Importing Footprints**
1. In the PCB Editor, click **"Update PCB from Schematic"** (button with an icon of a wire connecting to a PCB).
2. KiCad will import all the footprints from your schematic onto the PCB layout.

### **Step 2: Arranging Components**
1. After importing, you will see all your component footprints placed outside the board area.
2. Start by **manually arranging** the components on the board:
   - Place components that are **closely related** (such as decoupling capacitors near the microcontroller pins) in their respective areas.
   - Position connectors (e.g., USB, power, SWD) near the edges of the board where they are accessible.

### **Step 3: Preview the Footprints**
1. For each footprint, ensure it has been correctly imported and is aligned with the expected orientation. You can use the **3D View** (Right-click → View Footprint 3D) to visualize how the component will look on the finished PCB.

---

## **6. Preparing for Routing**

Routing is the process of drawing copper traces between the component pads based on the connections (nets) defined in your schematic. Before routing:
1. **Place key components**: Start by positioning critical components like the microcontroller, power supply, and connectors.
2. **Check netlist connections**: Ensure that all components are connected according to your schematic.

Once the components are in place and you’ve double-checked the netlist, you’re ready to start routing.

---

## **Conclusion**

You’ve now set up your **PCB layout** with the correct board stack, design rules, and predefined track sizes. The footprints have been imported and placed on the board. In the next step, you will move on to **routing the PCB**, connecting the various components with copper traces, and finalizing the layout for manufacturing.

This process ensures that your PCB will meet the requirements of your chosen manufacturer while maintaining a clean and functional design.