# Checking Gerber Files Before Submission

Before submitting the Gerber files to your manufacturer, it’s important to visually check them using a Gerber Viewer to ensure everything looks correct.

## Step 1: Open Gerber Files in a Viewer

1. In KiCad, you can use the Gerber Viewer by going to File > Gerber Viewer.
2. Load all the Gerber files from your Manufacturing folder.

## Step 2: Inspect Each Layer

- Copper Layers: Verify that the copper traces, pads, and connections are correct.
- Silkscreen: Check that all text and labels are placed correctly and not overlapping with any pads.
- Solder Mask: Ensure that the solder mask openings are aligned with the component pads.
- Edge Cuts: Verify that the board outline is correct and matches your intended dimensions.

## Step 3: What to look for

- **Board outline:** closed contour, correct size (the job file `*-job.gbrjob` lists the size and layer count).
- **Inner layers:** a ground plane should be one continuous area with only the clearance holes around vias.
- **Solder mask:** every pad has an opening; vias are covered (tented) unless they are test points.
- **Silkscreen:** no text over pads (KiCad's DRC warns about it), readable size (≥ 0.8 mm high, 0.15 mm line).
- **Drill files:** plated holes for through-hole parts and vias, non-plated holes for mounting holes and
  connector pegs.

## Step 4: Renders as a second check

```bash
kicad-cli pcb render --side top --quality high -o top.png stm32_prototype/stm32_prototype.kicad_pcb
kicad-cli pcb render --side bottom --quality high -o bottom.png stm32_prototype/stm32_prototype.kicad_pcb
```

The 3D render quickly shows wrong orientations, parts off the board or a missing silkscreen. Footprints without a
3D model (some connectors and buttons in the KiCad library) appear as bare pads only.
