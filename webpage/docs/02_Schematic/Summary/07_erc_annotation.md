# ERC and Annotation

---

## Annotation

Annotation gives every symbol a unique reference (R1, C12, U3 …).

* Annotate once the schematic is complete, sorted by sheet and position, so related parts get neighbouring numbers.
* Keep references without gaps; they appear in the BOM, the pick-and-place file and on the silkscreen.
* Power symbols and PWR_FLAGs get `#PWR` / `#FLG` references automatically and do not appear on the board.

---

## Electrical Rules Check

The ERC checks the schematic for connection errors. Typical findings and fixes:

| Message | Meaning | Fix |
|---|---|---|
| *Input power pin not driven* | a power input (VDD, VIN) has no power output on its net | add a **PWR_FLAG** to that net (battery input, connector, diode outputs) |
| *Pin not connected* | an unused pin is open | add a **no-connect flag** only if the pin is really unused |
| *Pins of type Power output and Power output are connected* | two regulators drive one net | check the design; a PWR_FLAG on a net that already has a regulator output also causes this |
| *Bidirectional and Power output connected* | a strap pin tied directly to a flagged rail | use a pull resistor (e.g. IMU address pin) or accept as a documented waiver |
| *Symbol doesn't match copy in library* | the schematic's cached symbol differs from the library | update the symbol from the library or ignore if intended |

---

## Command line

```bash
kicad-cli sch erc --severity-all --exit-code-violations stm32_prototype/stm32_prototype.kicad_sch
```

`--exit-code-violations` makes the command fail on any error or warning, so it can run in CI (see
`.github/workflows/hw-check.yml`).

---

## Goal

**0 errors and 0 warnings.** If a warning is intentionally kept, document why next to the design (for example in
`docs/erc_waivers.md`) so the next reviewer does not have to investigate it again.
