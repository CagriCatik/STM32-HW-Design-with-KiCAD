# RC-car controller firmware (Rev C bring-up)

`rc_controller/` is a STM32CubeMX 6.18 project (HAL, CMake) for the Rev C board, generated from
`rc_controller/rc_controller.ioc`. The .ioc itself is produced reproducibly:

```bash
# 1. pins + modes (CubeMX script mode), 2. peripheral parameters, 3. generate, 4. hook in the app
STM32CubeMX -q cubemx_pinout.txt          # replace __OUT__ with this folder first
python3 ioc_params.py rc_controller/rc_controller.ioc
STM32CubeMX -q <script: config load rc_controller.ioc / project generate / exit>
python3 apply_user_code.py rc_controller
```

Clock: 8 MHz HSE × 9 = 72 MHz, USB 48 MHz. TIM2 = servos (50 Hz, 1 µs), TIM3 = motor + lights (20 kHz),
TIM4 = receiver capture (1 µs), I2C2 400 kHz (IMU 0x6A + Qwiic), ADC1 IN4 = battery, USB CDC.

The application (`app/app.c`, copied into the project) blinks PC13, echoes everything received over USB CDC
and prints once per second:

```text
VBAT=7.84V IMU=0x6A RC=1502/1498/0us
```

Commands (one per line): `s1 1200` servo 1..4 pulse in µs, `m 30` motor −100..100 %, `l1 100` light 1..2 in %.

## Build and flash

```bash
export PATH=$HOME/Tools/arm-gnu/arm-gnu-toolchain-15.3.rel2-darwin-arm64-arm-none-eabi/bin:$PATH
cd rc_controller
cmake -S . -B build -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=cmake/gcc-arm-none-eabi.cmake -DCMAKE_BUILD_TYPE=Release
cmake --build build
STM32_Programmer_CLI -c port=SWD -w build/rc_controller.elf -v -rst   # ST-Link on the Cortex-Debug header
```

Bring-up order: power the board from USB only first (servo rail and motor stay off), check that the board
enumerates as a virtual COM port, then connect the battery and check VBAT, then the servos, then the motor.
