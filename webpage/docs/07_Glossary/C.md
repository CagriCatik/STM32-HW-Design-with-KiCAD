# C

## CC Pins (USB-C)

Configuration-channel pins of a USB-C connector. A device (sink) places 5.1 kΩ from CC1 and from CC2 to GND; the host only switches VBUS on when it sees these resistors.

## Courtyard

The keep-out outline of a footprint on the F.CrtYd/B.CrtYd layers. The DRC reports overlapping courtyards, which usually means two parts would collide physically.

## CPL (Component Placement List)

The pick-and-place file: reference, X/Y position, side and rotation of every part. JLCPCB uses it with the BOM to assemble the board.

## Crystal Load Capacitance (C_L)

The capacitance a crystal must see to oscillate at its rated frequency. The two load capacitors are chosen as C = 2 · (C_L − C_stray), with C_stray ≈ 3–5 pF from pins and traces.

## CubeMX

ST's configuration and code-generation tool. It assigns pins and peripherals, checks for conflicts, calculates the clock tree and generates HAL initialisation code. Also part of STM32CubeIDE.
