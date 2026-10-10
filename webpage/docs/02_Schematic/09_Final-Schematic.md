# Final Schematic

The schematic of the board in this repository (Rev C, RC-car controller) is hierarchical. Each tab shows one sheet;
the explanation of every block is on [Project → Schematic](../09_Project/02_Schematic.md).

=== "Root"
    ![Root sheet](../assets/schematic/revc_root.svg)

=== "MCU"
    The STM32F103C8T6 with decoupling, VDDA filter, 8 MHz crystal, BOOT0/RESET buttons, user LED and the USB
    series resistors with the 1.5 kΩ D+ pull-up.

    ![MCU sheet](../assets/schematic/revc_mcu.svg)

=== "Power"
    Battery input with reverse protection and TVS, battery sense divider, 5 V / 3 A buck converter, USB-C with
    CC resistors and ESD protection, Schottky OR of servo rail and USB, 3.3 V LDO, power LED.

    ![Power sheet](../assets/schematic/revc_power.svg)

=== "Drive"
    DRV8870 motor driver with current limit, servo/ESC outputs, receiver inputs and light outputs.

    ![Drive sheet](../assets/schematic/revc_drive.svg)

=== "IO"
    Cortex-Debug connector, LSM6DS3TR-C IMU, Qwiic, UART, expansion header and mounting holes.

    ![IO sheet](../assets/schematic/revc_io.svg)

The schematic as one PDF: `stm32_prototype/production/rev-c/stm32_prototype_rev-c_schematic.pdf`.

## How the chapters map to the sheets

| Chapter | Where on the board |
|---|---|
| [Decoupling](01_STM32_uC_Decoupling.md) | MCU sheet: C1–C7, FB1 |
| [Configuration Pins](02_STM32_Configuration_Pins.md) | MCU sheet: BOOT0/BOOT1 pull-downs, buttons, NRST capacitor |
| [Pin-Out](03_Pin-Out_STM32CubeIDE.md) | MCU sheet labels; `firmware/rc_controller/rc_controller.ioc` |
| [Crystal Circuitry](04_Crystal-Circuitry.md) | MCU sheet: Y1, C8, C9 (Y2 optional) |
| [USB](05_USB.md) | Power sheet: J2, U3, R13–R15; MCU sheet: R4–R6 |
| [Power Supply & Connectors](06_Power-Supply-Connectors.md) | Power and IO sheets |
| [ERC & Annotation](07_ERC-Annotation.md) | whole design: 0 errors, 0 warnings |
| [Footprint Assignment](08_Footprint-Assignment.md) | every symbol has Footprint, LCSC and MPN |
