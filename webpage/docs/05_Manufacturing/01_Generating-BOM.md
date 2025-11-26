# Generating the Bill of Materials

The BOM is a list of all components used in your design. It includes reference designators, component values, footprints, and part numbers. This file is critical for your manufacturer to source the components and assemble your PCB correctly.

## Step 1: Export the BOM

1. Go to the Schematic Editor in KiCad.
2. Click on the BOM Tool:
   - Go to File > Fabrication Outputs > Bill of Materials.
   - Specify the desired format for the BOM (e.g., CSV, XML).
   - Choose a location for the BOM, typically in a 'Manufacturing' folder for easy access.
   - Click Generate to export the file.

## Step 2: Review the BOM

- Open the BOM file in your preferred software (e.g., Excel or a text editor).
- The BOM typically includes the following columns:
  - Reference Designators: Lists components by their reference (e.g., R1, C2).
  - Quantities: How many of each component are needed.
  - Values: The value of the component (e.g., 10kΩ resistor).
  - Footprints: The package type (e.g., 0603, SOT-23).
  - Descriptions: Short description of the component (e.g., resistor, capacitor).
  
- Add Manufacturer Part Numbers: Make sure to populate the Manufacturer and Part Number columns for each component. This ensures the assembly house uses the correct parts.
- Remove Non-Assembled Items: Remove items like mounting holes that don’t need assembly.