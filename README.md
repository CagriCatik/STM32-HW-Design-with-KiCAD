<div align="center">

<h2>STM32 Hardware Design with KiCad</h2>

[![Hardware check](https://github.com/CagriCatik/STM32-HW-Design-with-KiCAD/actions/workflows/hw-check.yml/badge.svg)](https://github.com/CagriCatik/STM32-HW-Design-with-KiCAD/actions/workflows/hw-check.yml)
[![Deploy docs](https://github.com/CagriCatik/STM32-HW-Design-with-KiCAD/actions/workflows/deploy.yml/badge.svg)](https://github.com/CagriCatik/STM32-HW-Design-with-KiCAD/actions/workflows/deploy.yml)
![KiCad 10](https://img.shields.io/badge/KiCad-10.0-blue)
[![Documentation](https://img.shields.io/badge/docs-Zensical-green)](https://cagricatik.github.io/STM32-HW-Design-with-KiCAD/)
![Last Commit](https://img.shields.io/github/last-commit/CagriCatik/STM32-HW-Design-with-KiCAD)

<img src="webpage/docs/assets/pcb/revc_top.png" alt="STM32 RC controller, Rev C" width="640">

</div>

A hands-on, end-to-end STM32 hardware project in KiCad 10: schematic, PCB layout, routing, manufacturing data,
firmware and documentation. It started as a course exercise (a minimal STM32F103 board) and grew into a complete,
manufacturable **controller for an RC car**.

The goal is not only to learn KiCad, but to understand what makes a microcontroller board electrically reliable,
layout-aware and production-ready, and to keep every step reproducible with scripts.

## The board (Rev C)

- STM32F103C8T6 at 72 MHz (8 MHz crystal), USB-C virtual COM port, Cortex-Debug connector
- 2S–3S LiPo input on XT30 with reverse protection, TPS563201 5 V / 3 A servo rail, AP2112K 3.3 V
- DRV8870 brushed motor driver (3.3 A limit), 4 servo/ESC outputs, 3 receiver inputs, 2 light outputs
- LSM6DS3TR-C IMU, Qwiic, UART header, 2×5 expansion header
- 70 × 50 mm, 4 layers (solid GND plane), four M3 holes, JLCPCB assembly with an LCSC number on every part
- ERC 0/0, DRC 0 violations / 0 unconnected / 0 schematic-parity issues, checked in CI

Full description: [Project chapter of the documentation](webpage/docs/09_Project/01_Overview.md).

<details>
<summary><strong>Rev C – blocks and pin map</strong></summary>

Rev C turns the board into a complete controller for an RC car on one 70 × 50 mm, 4-layer PCB with four M3 holes.

| Block | Parts | MCU pins |
|---|---|---|
| Battery | 2S–3S LiPo on XT30, AO4407A reverse protection, SMAJ15A TVS, voltage sense 33k/10k | PA4 (ADC) |
| Servo rail | TPS563201 buck, 5.07 V / 3 A for servos and receiver | – |
| Logic supply | servo rail or USB-C (each via B5819W) → AP2112K-3.3 | – |
| Motor | DRV8870 brushed motor driver, 3.3 A current limit (0.1 Ω shunt), screw terminal | PA6/PA7 (TIM3 CH1/2) |
| Servo / ESC outputs | 4 × 3-pin (S, 5 V, GND) | PA0–PA3 (TIM2 CH1–4) |
| Receiver inputs | 3 × 3-pin, 1k series, powered from the servo rail | PB6–PB8 (TIM4 CH1–3, 5 V tolerant) |
| Lights | 2 × AO3400A low-side outputs (LED+ = 5 V) | PB0/PB1 (TIM3 CH3/4) |
| IMU | LSM6DS3TR-C, I²C 0x6A, INT1/INT2 | PB10/PB11 (I2C2), PB12/PB13 |
| Other | USB-C, Cortex-Debug 10-pin, Qwiic, UART header, 2×5 expansion, user LED PC13 | |

Stack-up: F.Cu signals / In1 solid GND / In2 signals + GND fill / B.Cu signals + GND fill.
DRC: 0 violations, 0 unconnected, 0 schematic parity issues. Fabrication data: `stm32_prototype/production/rev-c/`.

Notes: the DRV8870 needs ≥ 6.5 V (it locks out on an empty 2S pack). When an ESC is plugged into a servo
output, disconnect its BEC red wire – the board already supplies 5 V.

```bash
python3 scripts/revc_schematic/gen.py <dir>   # schematic generator (+ check.sh)
scripts/route_revb.sh                         # autoroute (Freerouting) + GND pours + DRC
scripts/export_fab.sh                         # Gerber/drill/BOM/CPL/PDF/STEP for rev-c
```

</details>

## Repository layout

```text
stm32_prototype/          KiCad 10 project (schematic sheets, PCB, rules, project symbol library)
  production/rev-c/       Gerber ZIP, BOM, CPL, schematic PDF, renders, STEP
scripts/                  schematic generator, board setup, placement, routing, fabrication export
firmware/                 STM32CubeMX project (rc_controller) and the bring-up application
webpage/                  documentation site, built with Zensical (course + project chapter)
datasheets/               datasheets used during the design
.github/workflows/        hw-check.yml (ERC/DRC, fab data on tags), deploy.yml (docs)
```

## Quick start

```bash
# open the design
open stm32_prototype/stm32_prototype.kicad_pro            # KiCad 10

# checks (the same ones CI runs)
kicad-cli sch erc --severity-all --exit-code-violations stm32_prototype/stm32_prototype.kicad_sch
kicad-cli pcb drc --severity-all --exit-code-violations --schematic-parity stm32_prototype/stm32_prototype.kicad_pcb

# fabrication data for JLCPCB
scripts/export_fab.sh

# firmware (Arm GNU toolchain on PATH)
cd firmware/rc_controller && cmake -S . -B build -G "Unix Makefiles" \
  -DCMAKE_TOOLCHAIN_FILE=cmake/gcc-arm-none-eabi.cmake -DCMAKE_BUILD_TYPE=Release && cmake --build build

# documentation
pip install -r requirements.txt && cd webpage && zensical serve   # http://127.0.0.1:8000
```

Before ordering, check the part rotations in JLCPCB's assembly preview, then follow the
[bring-up checklist](webpage/docs/09_Project/06_Bring-up.md).

## Revisions

| Rev | Content | Where |
|---|---|---|
| A | Course schematic: STM32F103, crystal, decoupling; no layout | `main` history |
| B | Blue-Pill-compatible board: USB-C, ESD, AP2112K, Cortex-Debug, Qwiic, 76.2 × 22.86 mm | branch `rev-b-usb-c` |
| C | RC-car controller (this README) | branch `rev-c-rc-car` |

<details>
<summary><strong>Rev B – changes compared to Rev A</strong></summary>

Rev B is a modernised, Blue-Pill-compatible board (branch `rev-b-usb-c`); Rev C builds on it.

| Area | Rev A | Rev B |
|---|---|---|
| Schematic | single sheet, 15 of 16 parts without footprint | hierarchical sheets `mcu`, `power_usb`, `connectors`; footprint, LCSC and MPN on every part |
| USB | USB Micro | USB-C 2.0 device (5.1k CC resistors), USBLC6-2SC6 ESD, 500 mA PTC |
| Regulator | AMS1117-3.3 | AP2112K-3.3 (250 mV dropout, ceramic stable), Schottky against back-feeding |
| Clock | 16 MHz, 10 pF | 8 MHz (CubeMX default), 15 pF from C = 2·(C_L − C_stray); optional 32.768 kHz LSE (DNP) |
| Reset/boot | slide switch, R1 without value, BOOT1 floating | RESET + BOOT0 buttons, 10k pull-downs on BOOT0 and BOOT1, 100 nF on NRST (was 100 µF) |
| Analog supply | VDDA tied to 3V3 before the ferrite | VDDA on its own net behind FB1 with 10 nF + 1 µF |
| Debug / I²C | 1×4 SWD | Cortex-Debug 10-pin + 1×4 SWD, Qwiic (PB6/PB7) with cuttable 4.7k pull-ups |
| Board | – | 76.2 × 22.86 mm, Blue-Pill header pinout (0.6" rows), 4 layers SIG/GND/GND/SIG, JLCPCB rules |
| Output | – | Gerber/drill/BOM/CPL/PDF/STEP in `stm32_prototype/production/rev-b`, CI ERC + DRC |

Reproducible steps (KiCad 10 on macOS; paths in the scripts):

```bash
scripts/export_fab.sh                 # fabrication data via kicad-cli
scripts/route_revb.sh                 # re-route with Freerouting (needs Java 25 + freerouting 2.5)
```

</details>

## Course progress

<details>
<summary><strong>Checklist</strong></summary>

**1. Schematic design**

- [X] STM32 microcontroller fundamentals and decoupling guidance
- [X] STM32 configuration pin requirements and best practices
- [X] Pin-out management with STM32CubeMX (`firmware/rc_controller/rc_controller.ioc`)
- [X] Crystal oscillator circuit design
- [X] USB interface design for STM32 systems
- [X] Power supply design and connector selection
- [X] ERC, annotation workflow and validation
- [X] Component footprint assignment

**2. PCB layout**

- [X] KiCad PCB project setup and configuration
- [X] Placement of MCU, decoupling capacitors and crystal
- [X] USB and SWD interface layout
- [X] Footprints and 3D models
- [X] Connector and switch placement
- [X] Power distribution and grounding
- [X] Board outline and mounting holes

**3. PCB routing**

- [X] Decoupling and crystal routing
- [X] Signal routing
- [X] Power routing and current handling
- [X] Refinement and DRC

**4. Manufacturing**

- [X] BOM, Gerber, drill and pick-and-place files
- [ ] JLCPCB assembly preview checked
- [ ] Boards ordered and brought up

**5. Firmware**

- [X] CubeMX configuration and bring-up application (builds)
- [ ] Tested on hardware

</details>

## Resources

- Course this project started from: [Learn KiCad V6 and STM32 Hardware Design](https://www.udemy.com/course/learn-kicad-v6-and-stm32-hardware-design/) (KiCad 6; this repository uses KiCad 10)
- [KiCad documentation](https://docs.kicad.org/) and [kicad-cli reference](https://docs.kicad.org/master/en/cli/cli.html)
- [STM32CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html), [STM32F103C8 datasheet](datasheets/datasheet_stm32f103c8.pdf)
- ST application notes: AN2867 (oscillator design), AN4879 (USB hardware and PCB guidelines)
- [JLCPCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities) and [parts library](https://jlcpcb.com/parts)
