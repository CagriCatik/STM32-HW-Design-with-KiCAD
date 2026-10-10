# Manufacturing Data

All fabrication and assembly files are produced by one script that only uses `kicad-cli`:

```bash
scripts/export_fab.sh            # writes stm32_prototype/production/rev-c/
```

| File | Content |
|---|---|
| `stm32_prototype_rev-c_gerber.zip` | Gerbers for 4 copper layers, masks, paste, silkscreens, outline + Excellon drill files |
| `stm32_prototype_rev-c_bom.csv` | BOM in JLCPCB format: Comment, Designator, Footprint, LCSC Part # |
| `stm32_prototype_rev-c_cpl.csv` | Pick-and-place in JLCPCB format: Designator, Mid X, Mid Y, Layer, Rotation |
| `stm32_prototype_rev-c_schematic.pdf` | Schematic, all sheets |
| `stm32_prototype_rev-c_top.png`, `_bottom.png` | 3D renders |
| `stm32_prototype_rev-c.step` | 3D model for mechanical checks |

Parts marked DNP (optional 32.768 kHz crystal, expansion header) and the solder jumpers are left out of BOM and CPL.

## Rotation offsets

JLCPCB's library orientation differs from KiCad's for some packages. The script applies the offsets used by the
common KiCad-to-JLC tools: LQFP and SOIC/HSOP +270°, SOT-23/TSOT-23 +180°, JST-SH +180°.

!!! warning "Check the assembly preview"
    Upload BOM and CPL in the JLCPCB order page and check every IC, transistor, electrolytic capacitor and
    connector in the 3D preview before ordering. Correct rotations directly in JLC's preview or in the `ROT` table
    of `scripts/export_fab.sh`.

## Ordering at JLCPCB

1. Upload the Gerber ZIP. JLCPCB detects 4 layers and about 70 × 50 mm.
2. Keep the defaults: FR-4, 1.6 mm, 1 oz outer copper, standard 4-layer stack-up (JLC04161H-7628).
3. Enable *PCB Assembly*, top side, upload BOM and CPL.
4. Check the part matching: all parts have LCSC numbers; the pin headers are through-hole and can be deselected to
   solder them yourself.
5. Check the 3D preview (see above), then order.

## Continuous integration

`.github/workflows/hw-check.yml` runs ERC and DRC (with schematic parity) in a KiCad 10 container on every push. For
tags `rev-*` it also runs `scripts/export_fab.sh` and attaches the fabrication data as a build artifact.
