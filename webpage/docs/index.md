# STM32 Hardware Design with KiCad

A practical course on designing STM32 hardware with KiCad 10, from the first schematic symbol to a manufactured,
assembled board, and a complete project built along the way: an **STM32 RC-car controller**.

![RC controller Rev C](assets/pcb/revc_top.png)

## How this site is organised

| Chapter | What you learn |
|---|---|
| [Introduction](01_Introduction/01_Introduction.md) | goals, tools, the overall workflow from project setup to programming |
| [Schematic Design](02_Schematic/01_STM32_uC_Decoupling.md) | decoupling, boot and reset pins, pin-out, crystal, USB, power, ERC, footprints |
| [PCB Layout](03_PCB_Layout/01_KiCad_PCB-Setup.md) | board setup, placement of decoupling, crystal, USB/SWD, connectors and power |
| [PCB Routing](04_PCB_Routing/01_Decoupling-Capacitors-Crystal-Routing.md) | routing order, signal and power routing, DRC |
| [Manufacturing](05_Manufacturing/01_Generating-BOM.md) | BOM, Gerbers, pick-and-place, checks and ordering at JLCPCB |
| [Project – RC Controller](09_Project/01_Overview.md) | the board in this repository: schematic, layout, manufacturing data, firmware, bring-up |
| [Scripts](06_Scripts/01_Automated_Design.md) | automating KiCad with Python and `kicad-cli` |
| [Glossary](07_Glossary/A.md) | short definitions of the terms used |

The course chapters explain each building block in general terms. Where the board in this repository uses a
different part or value, an **"In this project"** box links to the project chapter.

## The project at a glance

- STM32F103C8T6 at 72 MHz, 8 MHz crystal, USB-C (virtual COM port), Cortex-Debug connector
- 2S–3S LiPo input with reverse protection, 5 V / 3 A buck converter for servos
- DRV8870 brushed motor driver, 4 servo/ESC outputs, 3 receiver inputs, 2 light outputs
- LSM6DS3TR-C IMU, Qwiic, UART, expansion header
- 70 × 50 mm, 4 layers, assembled by JLCPCB; every step is scripted and reproducible

## Why STM32 instead of Arduino?

- **Performance:** 32-bit Cortex-M at 72 MHz with more memory and many more peripherals.
- **Real-time control:** advanced timers, DMA and interrupts, exactly what motor and servo control need.
- **Connectivity:** USB, CAN, several UART, I²C and SPI interfaces on chip.
- **Professional relevance:** the same parts and tools are used in industrial products.
- **Cost:** a bare MCU on your own board is cheaper and smaller than a development board once you move beyond
  prototyping.

## Prerequisites

- KiCad 10, STM32CubeMX, an ST-Link (V2 clone or V3)
- Basic electronics: Ohm's law, what a capacitor and a regulator do
- Optional: Python 3 for the automation chapter

The sources of this site and of the board are on GitHub:
[CagriCatik/STM32-HW-Design-with-KiCAD](https://github.com/CagriCatik/STM32-HW-Design-with-KiCAD).
