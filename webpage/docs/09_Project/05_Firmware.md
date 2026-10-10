# Firmware

The firmware in `firmware/rc_controller/` is a STM32CubeMX 6.18 project (HAL, CMake) with a small bring-up
application. It is meant to test every block of a freshly assembled board.

## CubeMX configuration from scripts

CubeMX can be driven from the command line. Pins and modes are set with a script, the peripheral parameters are
patched into the `.ioc`, then CubeMX generates the code:

```bash
STM32CubeMX -q firmware/cubemx_pinout.txt                       # pins and modes (replace __OUT__ first)
python3 firmware/ioc_params.py firmware/rc_controller/rc_controller.ioc
STM32CubeMX -q <script: config load ... / project generate / exit>
python3 firmware/apply_user_code.py firmware/rc_controller      # hooks the app into USER CODE blocks
```

CubeMX accepted the complete Rev C pin map without conflicts, which confirms the pin assignment chosen in the
schematic.

| Peripheral | Configuration |
|---|---|
| RCC | 8 MHz HSE × 9 = 72 MHz, APB1 36 MHz, USB 48 MHz |
| TIM2 | 4 × PWM, 1 µs tick, 20 ms period (servos, 1500 µs centre) |
| TIM3 | 4 × PWM, 20 kHz (motor IN1/IN2, lights) |
| TIM4 | 3 × input capture, 1 µs tick (receiver pulses) |
| I2C2 | 400 kHz (IMU, Qwiic) |
| ADC1 | IN4 (battery) |
| USART1 | 115200 baud (UART header) |
| USB | Device FS, CDC (virtual COM port) |

## Bring-up application

`firmware/app/app.c` is copied into the project:

- PC13 LED blinks at 1 Hz.
- Everything received over USB CDC is echoed, and once per second the board sends a status line:

```text
VBAT=7.84V IMU=0x6A RC=1502/1498/0us
```

- Commands, one per line:

| Command | Effect |
|---|---|
| `s1 1200` | servo 1–4 pulse in µs (500–2500) |
| `m 30` | motor duty −100…100 %, sign = direction, 0 = coast |
| `l1 100` | light 1–2 brightness in % |

The motor uses slow decay: one input is held high while the other is PWM'd low. Receiver pulses are measured by
capturing the rising edge, switching the channel to falling-edge capture and taking the difference (the F1 timers
cannot capture both edges at once).

## Build and flash

```bash
export PATH=$HOME/Tools/arm-gnu/arm-gnu-toolchain-15.3.rel2-darwin-arm64-arm-none-eabi/bin:$PATH
cd firmware/rc_controller
cmake -S . -B build -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=cmake/gcc-arm-none-eabi.cmake -DCMAKE_BUILD_TYPE=Release
cmake --build build
STM32_Programmer_CLI -c port=SWD -w build/rc_controller.elf -v -rst
```

The release build uses 28 KB of the 64 KB flash and 7.4 KB of the 20 KB RAM.
