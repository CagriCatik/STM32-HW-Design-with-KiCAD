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

## Step 3: JLCPCB format and rotations

JLCPCB expects the columns **Designator, Mid X, Mid Y, Layer, Rotation**. KiCad's CSV export uses Ref, PosX, PosY,
Rot, Side, so the header has to be renamed:

```bash
kicad-cli pcb export pos --format csv --units mm --side both --exclude-dnp -o pos.csv stm32_prototype/stm32_prototype.kicad_pcb
```

The zero orientation of some packages differs between KiCad and JLCPCB's part library. Common offsets used by the
KiCad-to-JLC tools:

| Package | Offset |
|---|---|
| LQFP, QFN, SOIC, HSOP | +270° |
| SOT-23, TSOT-23, SOT-223 | +180° |
| SOD-123, 0603/0805 passives | 0° |

!!! warning
    These offsets are starting points. Always check the result in JLCPCB's 3D assembly preview before ordering;
    the preview lets you rotate a part that sits wrong.

Leave out parts that are not assembled: solder jumpers, mounting holes, DNP parts.
`scripts/export_fab.sh` does the renaming, the offsets and the filtering.
