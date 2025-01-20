# Generating the Bill of Materials, Gerber Files, and Placing an Order

Once the layout and routing are completed, the next step is to generate the Bill of Materials (BOM), Gerber files, and component placement files. These are essential for manufacturing and assembly. Here's a detailed guide on how to prepare these files and place your order with a PCB manufacturer.

---

## 1. Generating the Bill of Materials (BOM)

The BOM is a list of all components used in your design. It includes reference designators, component values, footprints, and part numbers. This file is critical for your manufacturer to source the components and assemble your PCB correctly.

### Step 1: Export the BOM
1. Go to the Schematic Editor in KiCad.
2. Click on the BOM Tool:
   - Go to File > Fabrication Outputs > Bill of Materials.
   - Specify the desired format for the BOM (e.g., CSV, XML).
   - Choose a location for the BOM, typically in a 'Manufacturing' folder for easy access.
   - Click Generate to export the file.

### Step 2: Review the BOM
- Open the BOM file in your preferred software (e.g., Excel or a text editor).
- The BOM typically includes the following columns:
  - Reference Designators: Lists components by their reference (e.g., R1, C2).
  - Quantities: How many of each component are needed.
  - Values: The value of the component (e.g., 10kΩ resistor).
  - Footprints: The package type (e.g., 0603, SOT-23).
  - Descriptions: Short description of the component (e.g., resistor, capacitor).
  
- Add Manufacturer Part Numbers: Make sure to populate the Manufacturer and Part Number columns for each component. This ensures the assembly house uses the correct parts.
- Remove Non-Assembled Items: Remove items like mounting holes that don’t need assembly.

---

## 2. Generating Gerber Files

Gerber files are the industry standard format for PCB manufacturing. These files contain the data for each layer of your PCB, such as copper layers, silkscreen, and solder mask.

### Step 1: Export Gerber Files
1. Go to the PCB Layout Editor in KiCad.
2. Click on File > Fabrication Outputs > Gerber Files.
3. Select the Layers to Export:
   - Top and Bottom Copper layers.
   - Solder Mask layers (Top and Bottom).
   - Silkscreen layers (Top and Bottom).
   - Edge Cuts layer (to define the PCB outline).
4. Generate Gerbers: Choose a directory (e.g., Manufacturing folder), and click Plot to generate the Gerber files.

### Step 2: Generate Drill Files
1. After plotting the Gerbers, go back to Fabrication Outputs and select Drill Files.
2. Choose the appropriate format (e.g., Excellon), and generate the drill file that defines all the holes (e.g., for vias and through-hole components).

---

## 3. Generating Component Placement (Pick-and-Place) Files

The component placement file tells the manufacturer where to place each component on the PCB. It includes coordinates and orientations.

### Step 1: Export the Placement File
1. In the PCB Layout Editor, go to File > Fabrication Outputs > Footprint Position File.
2. Choose the format (e.g., CSV) and select mm for units.
3. Save the file in your Manufacturing folder.

### Step 2: Review the Placement File
- The placement file includes:
  - Reference Designators: The same designators used in the BOM (e.g., R1, C2).
  - X and Y coordinates: Where on the PCB the component is located.
  - Rotation: The component’s orientation.
  - Layer: Specifies if the component is on the top or bottom of the board.

---

## 4. Checking Gerber Files Before Submission

Before submitting the Gerber files to your manufacturer, it’s important to visually check them using a Gerber Viewer to ensure everything looks correct.

### Step 1: Open Gerber Files in a Viewer
1. In KiCad, you can use the Gerber Viewer by going to File > Gerber Viewer.
2. Load all the Gerber files from your Manufacturing folder.

### Step 2: Inspect Each Layer
- Copper Layers: Verify that the copper traces, pads, and connections are correct.
- Silkscreen: Check that all text and labels are placed correctly and not overlapping with any pads.
- Solder Mask: Ensure that the solder mask openings are aligned with the component pads.
- Edge Cuts: Verify that the board outline is correct and matches your intended dimensions.

---

## 5. Submitting the Files for PCB Manufacturing

Once your design files are checked and ready, you can upload them to your PCB manufacturer’s website for production.

### Step 1: Upload Gerbers to Manufacturer
1. Go to the manufacturer’s website (e.g., JLCPCB or any other PCB fab service).
2. Choose the quote/ordering tool and upload your Gerber ZIP file (which contains all the Gerber files and drill files).
3. Check Gerber Files: Most manufacturers have an integrated Gerber viewer to visually inspect the files before confirming the order.

### Step 2: Specify Board Details
- Choose your desired PCB material (e.g., FR-4 fiberglass).
- Select the number of layers (usually 2 layers for simple designs).
- Specify the PCB color, finish type (e.g., HASL lead-free, ENIG), and board thickness.
- Choose the number of boards you want to order.

### Step 3: Optional PCB Assembly
- If you want the board fully assembled, you can upload the Bill of Materials (BOM) and Pick-and-Place file.
- Choose the side for assembly (e.g., Top, Bottom, or Both).

---

## 6. Placing the Order

Once all details are selected, review the price breakdown for the boards and any extra services like assembly. If everything looks good, place the order.

---

## Conclusion

By following these steps, you’ve successfully prepared all necessary files to submit your PCB design for manufacturing. After running a design rule check, verifying Gerber files, and adding silkscreen and logos, your design is polished and ready to be sent to a manufacturer for production. Whether you're ordering just a few prototypes or mass production, these steps will ensure a smooth and accurate process.