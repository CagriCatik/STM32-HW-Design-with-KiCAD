<div align="center">

<h2>KiCad and STM32 Hardware Design</h2>

<img src="https://upload.wikimedia.org/wikipedia/commons/5/59/KiCad-Logo.svg" alt="KiCad Logo" width="180">

[![Deploy Docusaurus](https://github.com/CagriCatik/PCB-Design-with-KiCad/actions/workflows/deploy.yml/badge.svg)](https://github.com/CagriCatik/PCB-Design-with-KiCad/actions/workflows/deploy.yml)
![KiCad 10](https://img.shields.io/badge/KiCad-10.0-blue)
[![Documentation](https://img.shields.io/badge/MkDocs-Available-green)](webpage/docs/index.md)
![Last Commit](https://img.shields.io/github/last-commit/CagriCatik/PCB-Design-with-KiCad)

</div>

<div align="center">
This project documents my first complete PCB design journey using KiCad and an STM32 microcontroller. It represents a hands-on, end-to-end dive into schematic design, PCB layout, routing, manufacturing files, and the practical considerations required to make a real, manufacturable embedded board.

The goal was not only to learn KiCad as a professional tool, but to understand what makes a microcontroller board electrically reliable, layout-aware, and production-ready. Every stage reflects actual engineering constraints encountered during the design of a small STM32-based board.

</div>

<details>
<summary><strong>1. Schematic Design</strong></summary>

- [X] STM32 microcontroller fundamentals and decoupling guidance.
- [X] STM32 configuration pin requirements and best practices.
- [ ] Pin-out management using STM32CubeIDE.
- [X] Crystal oscillator circuit design.
- [X] USB interface design for STM32 systems.
- [X] Power supply design and connector selection.
- [X] Electrical Rules Check (ERC), annotation workflow, and validation.
- [X] Component footprint assignment.

</details>

---

<details>
<summary><strong>2. PCB Layout</strong></summary>

- [X] KiCad PCB project setup and configuration.
- [X] Placement strategy for MCU, decoupling capacitors, and crystal components.
- [X] USB and SWD interface layout considerations.
- [X] Updating footprints and integrating 3D models.
- [X] Connector and switch placement.
- [X] Power distribution layout and grounding practices.
- [X] Defining board outline and mechanical mounting features.

</details>

---

<details>
<summary><strong>3. PCB Routing</strong></summary>

- [X] Routing guidelines for decoupling and crystal signals.
- [X] Digital and analog signal routing strategies.
- [X] Power trace routing and current handling considerations.
- [X] Refinement procedures and thorough DRC validation.

</details>

---

<details>
<summary><strong>4. Manufacturing</strong></summary>

- [X] Generating BOM files
- [X] Generating Gerber and Pick/Place files
- [X] Generating Drill files

</details>

---
<details>
<summary><strong>5. Documentation</strong></summary>

This project uses **MkDocs** with **Material Theme** for documentation.

**Prerequisites**

- Python 3.x
- pip

**Install the required packages**

```bash
pip install mkdocs mkdocs-material
```

**To serve the documentation locally**:

```bash
cd webpage
python -m mkdocs serve
```

The site will be available at http://127.0.0.1:8000/.


**To build the static site**:

```bash
cd webpage
python -m mkdocs build
```
</details>

---

<details>
<summary><strong>Rev C – RC-car controller (branch rev-c-rc-car)</strong></summary>

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

---

<details>
<summary><strong>Rev B – changes compared to Rev A</strong></summary>

The KiCad project in `stm32_prototype/` is Rev B, a modernised Blue Pill (KiCad 10, branch `rev-b-usb-c`).

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

---

**Additional Resources**

- This content is aligned with [Learn KiCad V6 and STM32 Hardware Design](https://www.udemy.com/course/learn-kicad-v6-and-stm32-hardware-design/)
- STM32CubeIDE Documentation: [STMicroelectronics Documentation](https://www.st.com/en/development-tools/stm32cubeide.html)
- KiCad Official Documentation: [KiCad Documentation](https://docs.kicad.org/)
- STM32 Community Forums: [ST Community](https://community.st.com/s/)
- USB Design Guidelines: [USB.org Guidelines](https://www.usb.org/documents)


