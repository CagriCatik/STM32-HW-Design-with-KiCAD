# Footprint Assignment

---

## Rules of thumb

* **Passives:** 0603 is a good default: small, still hand-solderable, and the most common JLCPCB *basic* size.
  Use 0805/1206 for larger capacitance at higher voltage (e.g. 22 µF / 25 V) and 2512 for current-sense resistors.
* **Match the datasheet, not the symbol name.** Check pad numbering against the datasheet pinout, especially for
  transistors, LDOs, ESD arrays and USB-C connectors.
* **Pick the footprint for the actual part number.** Two "SOT-23-6" parts can have different pinouts; two "USB-C"
  connectors have different pad layouts.
* **Exposed pads** (motor drivers, regulators) need the thermal-via variant of the footprint.

---

## Fields for assembly

Every symbol carries:

| Field | Example | Used for |
|---|---|---|
| Footprint | `Capacitor_SMD:C_0603_1608Metric` | PCB |
| LCSC | `C14663` | JLCPCB BOM matching |
| MPN | `CC0603KRX7R9BB104` | ordering elsewhere, documentation |
| DNP (attribute) | – | parts placed on the PCB but not assembled |

Prefer JLCPCB **basic** parts: they have no extra feeder fee. Check the LCSC number in the JLC parts library
before ordering; stock changes.

---

## Footprints used on the RC controller (examples)

| Part | Footprint |
|---|---|
| STM32F103C8T6 | `Package_QFP:LQFP-48_7x7mm_P0.5mm` |
| DRV8870 | `Package_SO:Texas_HSOP-8-1EP_3.9x4.9mm_P1.27mm_ThermalVias` |
| TPS563201 | `Package_TO_SOT_SMD:TSOT-23-6` |
| AP2112K-3.3 | `Package_TO_SOT_SMD:SOT-23-5` |
| USB-C | `Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12` |
| XT30 | `Connector_AMASS:AMASS_XT30UPB-M_1x02_P5.0mm_Vertical` |
| 8 MHz crystal | `Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm` |
| LSM6DS3TR-C | `Package_LGA:LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y` |

---

## Check

After *Update PCB from Schematic*, run the DRC with schematic parity; it reports missing footprints, pad/pin
mismatches and nets that differ between schematic and board:

```bash
kicad-cli pcb drc --schematic-parity stm32_prototype/stm32_prototype.kicad_pcb
```
