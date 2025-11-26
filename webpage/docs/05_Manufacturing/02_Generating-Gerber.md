# Generating Gerber Files

Gerber files are the industry standard format for PCB manufacturing. These files contain the data for each layer of your PCB, such as copper layers, silkscreen, and solder mask.

## Step 1: Export Gerber Files

1. Go to the PCB Layout Editor in KiCad.
2. Click on File > Fabrication Outputs > Gerber Files.
3. Select the Layers to Export:
   - Top and Bottom Copper layers.
   - Solder Mask layers (Top and Bottom).
   - Silkscreen layers (Top and Bottom).
   - Edge Cuts layer (to define the PCB outline).
4. Generate Gerbers: Choose a directory (e.g., Manufacturing folder), and click Plot to generate the Gerber files.

## Step 2: Generate Drill Files

1. After plotting the Gerbers, go back to Fabrication Outputs and select Drill Files.
2. Choose the appropriate format (e.g., Excellon), and generate the drill file that defines all the holes (e.g., for vias and through-hole components).