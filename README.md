<div align="center">

<h2>KiCad and STM32 Hardware Design</h2>

<img src="https://upload.wikimedia.org/wikipedia/commons/5/59/KiCad-Logo.svg" alt="KiCad Logo" width="180">

[![Deploy Docusaurus](https://github.com/CagriCatik/PCB-Design-with-KiCad/actions/workflows/deploy.yml/badge.svg)](https://github.com/CagriCatik/PCB-Design-with-KiCad/actions/workflows/deploy.yml)
![KiCad 9](https://img.shields.io/badge/KiCad-9.0-blue)
[![Documentation](https://img.shields.io/badge/Docusaurus-Available-green)](https://cagricatik.github.io/STM32-HW-Design-with-KiCAD/)

<!-- Extra Badges -->
![Last Commit](https://img.shields.io/github/last-commit/CagriCatik/PCB-Design-with-KiCad)
![Issues](https://img.shields.io/github/issues/CagriCatik/PCB-Design-with-KiCad)
![Pull Requests](https://img.shields.io/github/issues-pr/CagriCatik/PCB-Design-with-KiCad)
![Stars](https://img.shields.io/github/stars/CagriCatik/PCB-Design-with-KiCad?style=social)

</div>

<div align="center">
This project documents my first complete PCB design journey using KiCad and an STM32 microcontroller. It represents a hands-on, end-to-end dive into schematic design, PCB layout, routing, manufacturing files, and the practical considerations required to make a real, manufacturable embedded board.

The goal was not only to learn KiCad as a professional tool, but to understand what makes a microcontroller board electrically reliable, layout-aware, and production-ready. Every stage reflects actual engineering constraints encountered during the design of a small STM32-based board.
</div>

<details>
<summary><strong>1. Schematic Design</strong></summary>

- [x] STM32 microcontroller fundamentals and decoupling guidance.
- [x] STM32 configuration pin requirements and best practices.
- [ ] Pin-out management using STM32CubeIDE.
- [ ] Crystal oscillator circuit design.
- [ ] USB interface design for STM32 systems.
- [ ] Power supply design and connector selection.
- [ ] Electrical Rules Check (ERC), annotation workflow, and validation.
- [ ] Component footprint assignment.

</details>

---

<details>
<summary><strong>2. PCB Layout</strong></summary>

- [ ] KiCad PCB project setup and configuration.
- [ ] Placement strategy for MCU, decoupling capacitors, and crystal components.
- [ ] USB and SWD interface layout considerations.
- [ ] Updating footprints and integrating 3D models.
- [ ] Connector and switch placement.
- [ ] Power distribution layout and grounding practices.
- [ ] Defining board outline and mechanical mounting features.

</details>

---
<details>
<summary><strong>3. PCB Routing</strong></summary>

- [ ] Routing guidelines for decoupling and crystal signals.
- [ ] Digital and analog signal routing strategies.
- [ ] Power trace routing and current handling considerations.
- [ ] Refinement procedures and thorough DRC validation.

</details>

---

<details>
<summary><strong>4. Manufacturing</strong></summary>

- [ ] Generating BOM files
- [ ] Generating Gerber and Pick/Place files
- [ ] Generating Drill files

</details>

---

**Additional Resources**

- This content is aligned with [Learn KiCad V6 and STM32 Hardware Design](https://www.udemy.com/course/learn-kicad-v6-and-stm32-hardware-design/)
- STM32CubeIDE Documentation: [STMicroelectronics Documentation](https://www.st.com/en/development-tools/stm32cubeide.html)
- KiCad Official Documentation: [KiCad Documentation](https://docs.kicad.org/)
- STM32 Community Forums: [ST Community](https://community.st.com/s/)
- USB Design Guidelines: [USB.org Guidelines](https://www.usb.org/documents)