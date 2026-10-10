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

## Step 3: Layers for a 4-layer board

For a 4-layer board include the inner copper layers (`In1.Cu`, `In2.Cu`) as well. A complete set:

| Layer | File (Protel extension) |
|---|---|
| F.Cu, In1.Cu, In2.Cu, B.Cu | `.gtl`, `.g1`, `.g2`, `.gbl` |
| F.Mask, B.Mask | `.gts`, `.gbs` |
| F.Paste, B.Paste | `.gtp`, `.gbp` (needed for assembly stencils) |
| F.Silkscreen, B.Silkscreen | `.gto`, `.gbo` |
| Edge.Cuts | `.gm1` |
| Drill (plated / non-plated) | `-PTH.drl`, `-NPTH.drl` |

## Step 4: From the command line

```bash
kicad-cli pcb export gerbers --check-zones --subtract-soldermask \
  -l F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts \
  -o gerber/ stm32_prototype/stm32_prototype.kicad_pcb
kicad-cli pcb export drill --format excellon --excellon-units mm --excellon-separate-th -o gerber/ \
  stm32_prototype/stm32_prototype.kicad_pcb
```

`--check-zones` refills all copper zones first, so the Gerbers never contain outdated pours.
Zip the folder and upload the ZIP.
