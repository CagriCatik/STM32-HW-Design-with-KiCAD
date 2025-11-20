# B

## Bulk Decoupling

Bulk decoupling is the use of high-value capacitors placed near the power entry point or major load nodes to stabilize the supply rail. These capacitors absorb low-frequency load transients and prevent large voltage droop when multiple devices switch simultaneously. Bulk decoupling complements local high-frequency decoupling capacitors by providing energy storage at lower frequencies [Verified].

## BOOT0 & BOOT1

BOOT0 and BOOT1 are configuration pins used on many microcontrollers, notably STM32 devices, to select the boot mode during reset. They determine whether the MCU starts from user flash, system memory (for programming), or SRAM. Correct pull-up or pull-down resistors ensure deterministic boot behavior and avoid unintended entry into system bootloader modes [Verified].

## Buck-Converter

A buck converter is a DC-DC switching regulator that steps down a higher input voltage to a lower output voltage with high efficiency. It uses a high-speed switching element, diode or synchronous MOSFET, inductor, and output capacitor to regulate voltage via pulse-width modulation. Layout requires tight switching loops, minimized parasitics, and proper grounding to reduce electromagnetic interference and ensure stable regulation [Verified].
