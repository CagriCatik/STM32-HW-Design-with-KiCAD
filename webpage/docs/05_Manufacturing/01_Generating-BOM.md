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

## Step 3: BOM in JLCPCB format

JLCPCB's assembly service expects four columns: **Comment** (value), **Designator** (references, comma-separated),
**Footprint** and **LCSC Part #**. Store the LCSC number as a field (`LCSC`) on every symbol, then the BOM can be
exported directly:

```bash
kicad-cli sch export bom --exclude-dnp --ref-range-delimiter "" \
  --fields 'Value,Reference,Footprint,LCSC' --labels 'Comment,Designator,Footprint,LCSC Part #' \
  --group-by 'Value,Footprint,LCSC' -o bom.csv stm32_prototype/stm32_prototype.kicad_sch
```

- `--exclude-dnp` leaves out parts marked *Do not populate* (optional crystal, loose headers).
- `--ref-range-delimiter ""` writes `C1,C2,C3` instead of `C1-C3`, which JLCPCB cannot parse.
- Parts with *Exclude from BOM* (solder jumpers, mounting holes) are skipped automatically.

## Tips

- Prefer JLCPCB **basic** parts (no feeder fee); every *extended* part adds a one-time fee per order.
- Check stock for each LCSC number shortly before ordering.
- Group identical parts (same value, footprint and LCSC number) into one line.

In this repository `scripts/export_fab.sh` produces the BOM together with all other files, see
[Project → Manufacturing](../09_Project/04_Manufacturing.md).
