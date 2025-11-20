# Finalizing the Design and Generating Manufacturing Files

After completing the PCB layout and ensuring it meets all design rules, the next step is to generate the necessary files for PCB fabrication and assembly.

## Steps to Generate Gerber Files

### Generate Gerber Files

- Access Plot Dialog:
  - In the PCB Editor, go to File > Plot.
  
- Configure Plot Settings:
  - Output Format: Select Gerber.
  - Layers to Plot: Choose all relevant layers, such as:
    - Top Layer
    - Bottom Layer
    - Silk Screen (Top and Bottom)
    - Solder Mask (Top and Bottom)
    - Edge Cuts (Board Outline)
  
- Generate Files:
  - Click Plot to generate the Gerber files for each selected layer.
  
- Generate Drill Files:
  - After plotting the Gerber files, click File > Generate Drill Files.
  - Configure drill settings and generate the necessary drill files (`.drl`) for PCB hole specifications.

> Best Practice: Verify Gerber files using a Gerber viewer before sending them to a manufacturer to ensure all layers and details are correct.

### Bill of Materials (BOM)

- Generate BOM:
  - In the PCB Editor, navigate to Tools > Generate Bill of Materials.
  
- Configure BOM Options:
  - Choose the desired BOM format (e.g., CSV, HTML).
  
- Export BOM:
  - Save the BOM file, which lists all components, their quantities, part numbers, and other relevant details.

> Practical Example: Use the BOM to source components from suppliers, ensuring that all necessary parts are accounted for during assembly.

### Prepare Files for Manufacturer

- Compile All Necessary Files:
  - Ensure that all Gerber files, drill files, BOM, and any additional documentation are organized and ready for submission.
  
- Compress Files:
  - Package all files into a single compressed archive (e.g., ZIP) to facilitate easy upload to the PCB manufacturer.
  
- Select a Manufacturer:
  - Choose a PCB manufacturer (e.g., JLCPCB, PCBWay) and follow their specific submission guidelines.

> Best Practice: Provide clear instructions and verify all file specifications meet the manufacturer’s requirements to avoid fabrication delays.

