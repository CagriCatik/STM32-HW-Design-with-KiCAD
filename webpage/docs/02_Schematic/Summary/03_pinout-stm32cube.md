# Pin-Out and STM32CubeIDE

This section explains how to define the functional pin-out of the STM32F103C8Tx using STM32CubeIDE and how to transfer that pin configuration back into the KiCad schematic. The goal is to establish a clean, predictable mapping between firmware configuration and PCB layout, ensuring that the final board supports USB, SWD debugging, an external crystal, and general-purpose headers.

STM32CubeIDE provides an Eclipse-based development environment with integrated graphical pin configuration. This makes it easier to select peripherals, assign functions to pins, and validate pin conflicts without manually cross-referencing the datasheet.

---

## Creating a New STM32CubeIDE Project

Start STM32CubeIDE and create a new project:

1. Select **File → New → STM32 Project**.
2. In the MCU selector, enter the part number:
   **STM32F103C8Tx**
3. CubeIDE displays package type, flash/RAM size, maximum frequency, available peripherals, and supported interfaces.
4. Confirm the part selection and enter a project name.
5. Open the MCU configuration view, which shows a top-down representation of the chip with all pins exposed.

This graphical interface allows you to assign functionality by clicking the pin directly or selecting peripherals from the left-hand configuration panel.

---

## Understanding the Pin-Out View

The pin-out view shows all MCU pins around the package outline, including:

* VDD, VDDA, VSS, VSSA power pins
* BOOT0 configuration pin
* NRST reset pin
* All GPIO-capable ports (PAx, PBx, PCx, PDx)

Your previously wired schematic connections become visible here, allowing you to ensure consistency between electrical design and firmware configuration.

Pin functionality can be defined in several ways:

* Clicking directly on a pin to assign a function
* Selecting peripherals from the left sidebar (recommended)
* Reading the datasheet (only if familiar with STM32 pin multiplexing)

The preferred method is to enable peripherals via the sidebar, letting CubeIDE automatically configure the related pins.

---

## Selecting Debug, Crystal, and USB Functions

Since the goal is a generic, development-friendly board, only essential peripherals are enabled.

### SWD Debug Interface (SWCLK / SWDIO)

Navigate to **System Core → SYS → Debug** and select:

**Serial Wire**

This assigns:

* **PA13** → SWDIO
* **PA14** → SWCLK

These are required for programming and debugging through an ST-Link.

### External High-Speed Crystal (HSE)

Navigate to **RCC → High Speed Clock (HSE)** and enable:

**Crystal/Ceramic Resonator**

CubeIDE assigns:

* **PD0** → HSE_IN
* **PD1** → HSE_OUT

These will later connect to the external 8 MHz crystal on the PCB.

### USB Full-Speed Device

Navigate to **Connectivity → USB → Device FS**

CubeIDE assigns:

* **PA11** → USB_DM
* **PA12** → USB_DP

These form the USB differential pair for USB-C connection.

Additional USB middleware classes (CDC, MSC, Audio, HID, DFU) can be enabled later under **Middleware → USB Device**.

---

## Clock Configuration

Under the **Clock Configuration** tab, you can:

* Set the external crystal frequency
* Choose the target system clock frequency
* Let CubeIDE automatically compute PLL settings

This ensures your firmware matches the electrical characteristics you have implemented in the schematic.

---

## Transferring the Pin-Out to KiCad

Once the pin mapping is complete, the same assignments must be applied to the schematic.

For example:

* **PD0** → HSE_IN
* **PD1** → HSE_OUT
* **PA13/PA14** → SWDIO/SWCLK
* **PA11/PA12** → USB_DM/USB_DP

Add net labels such as:

```
HSE_IN  
HSE_OUT  
USB_DP  
USB_DM  
SWDIO  
SWCLK  
```

This ensures:

* KiCad recognizes differential pairs (e.g., USB_DP / USB_DM)
* Pins are clearly identified during routing
* The firmware configuration matches the hardware exactly

KiCad treats differential pairs correctly when named with a shared prefix and **+ / -** suffix. For USB, this is:

```
USB_DP  
USB_DM
```

These will later be routed as a matched impedance pair.

---

## Result

After completing the configuration:

* The crystal pins are defined and labeled
* The SWD interface pins are reserved
* The USB differential pair is assigned
* All remaining pins can be routed to headers for general I/O
* The schematic and CubeIDE configuration remain synchronized

This provides a clean foundation for the final PCB layout and ensures the firmware and hardware designs evolve consistently.
