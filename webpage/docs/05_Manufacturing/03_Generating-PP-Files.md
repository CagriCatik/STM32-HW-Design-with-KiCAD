# Generating Component Placement (Pick-and-Place) Files

The component placement file tells the manufacturer where to place each component on the PCB. It includes coordinates and orientations.

## Step 1: Export the Placement File

1. In the PCB Layout Editor, go to File > Fabrication Outputs > Footprint Position File.
2. Choose the format (e.g., CSV) and select mm for units.
3. Save the file in your Manufacturing folder.

## Step 2: Review the Placement File

- The placement file includes:
  - Reference Designators: The same designators used in the BOM (e.g., R1, C2).
  - X and Y coordinates: Where on the PCB the component is located.
  - Rotation: The component’s orientation.
  - Layer: Specifies if the component is on the top or bottom of the board.