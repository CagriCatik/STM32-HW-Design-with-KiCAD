# Boot Configuration, Reset Circuit, and Power Source Setup

This section delves into the remaining key aspects of the STM32 PCB design, including configuring the **reset pin** (NRST), **boot configuration pin** (BOOT0), and ensuring the microcontroller boots correctly. Additionally, we cover how to connect a power source and use basic external components such as resistors and capacitors to stabilize the circuit.

---

## **1. Reset Pin Configuration (NRST)**

The **NRST** pin is the reset pin on the STM32 microcontroller. Resetting the microcontroller clears all internal registers and restarts the device, which can be useful for manual resets or to prevent erratic behavior.

### **Behavior of the NRST Pin**
- The NRST pin uses **inverted logic**, meaning pulling the pin low resets the microcontroller.
- STM32 microcontrollers have an **internal pull-up resistor** on the NRST pin, so in most cases, it does not need to be connected externally to a pull-up resistor.
- However, it is still a good idea to expose this pin in the schematic for potential debugging or future use.

### **Adding a Reset Circuit**
- If you want to add a **manual reset button**, you can connect a **tactile switch** between NRST and ground (GND). Pressing the switch pulls NRST low, resetting the microcontroller.
- For **protection against spurious resets**, it is a best practice to connect a **100nF decoupling capacitor** to NRST, which helps filter noise that could trigger unintended resets.

### **Steps in KiCad:**
1. **Add the Decoupling Capacitor**:
   - Click **Add Symbol** and select a **100nF capacitor** (C value: 100nF).
   - Connect one terminal of the capacitor to NRST and the other to ground.
   
2. **(Optional) Add a Reset Button**:
   - You can add a **tactile switch** between NRST and ground. Place the switch in the schematic by searching for a generic switch in KiCad’s symbol library.

### **Naming the NRST Net**
- In KiCad, each connection (net) should have a clear name for readability and ease of debugging in the PCB layout.
- To name the NRST net:
   - Click **Net Label** from the right toolbar and place a label called `NRST` on the wire connecting to the NRST pin.
   - This ensures that the wire will be identifiable in the PCB layout.

## **2. Boot Pin Configuration (BOOT0)**

The **BOOT0** pin on STM32 microcontrollers allows the device to select between different boot modes, including:
- **Boot from Flash Memory** (default mode to run programs stored in memory).
- **Boot from System Memory** (activates the microcontroller's built-in bootloader for programming via UART, USB, or other interfaces).

### **Why is BOOT0 Important?**
- For regular use, you want the microcontroller to boot from Flash memory. However, for initial programming or re-flashing, the bootloader mode can be useful.
- By controlling BOOT0, you can enable or disable the internal bootloader. When BOOT0 is pulled high (connected to 3.3V), the bootloader mode is enabled. When pulled low (connected to ground), the device boots from Flash.

### **Creating a Boot Configuration Switch**

A **Single-Pole, Dual-Throw (SPDT)** switch is typically used to toggle between high (3.3V) and low (GND) for the BOOT0 pin. This allows you to select the boot mode manually.

### **Steps in KiCad:**
1. **Place an SPDT Switch**:
   - Add a **Single-Pole, Dual-Throw switch** from the symbol library. This switch has a common terminal and can switch between two states (connected to 3.3V or GND).
   - Use the **X** or **Y** keys to flip or rotate the symbol as needed.

2. **Add a Resistor**:
   - Place a **10kΩ pull-down resistor** (R value: 10kΩ) between BOOT0 and ground. This ensures that in the default state, BOOT0 is low, allowing the microcontroller to boot from Flash.

3. **Connect Power and Ground**:
   - Connect one side of the switch to **3.3V** and the other side to **GND** using the wiring tool (**W**).
   - Connect the middle (common) terminal of the switch to the **BOOT0 pin**.

4. **Add Labels for Clarity**:
   - Label the connections on both sides of the switch for clarity:
     - Name the wire connected to BOOT0 as `BOOT0`.
     - Name the side connected to 3.3V as `BOOT HIGH`.
     - Name the side connected to GND as `BOOT LOW`.

### **Why Use a Resistor?**
- The 10kΩ resistor ensures that BOOT0 is pulled to ground (low) when the switch is in the default position, preventing the microcontroller from booting into the bootloader by accident.
- Without this resistor, the state of BOOT0 could float, potentially causing unstable behavior.

### **Final BOOT0 Circuit Overview**
When the switch is in its default state (connected to GND), the microcontroller will boot from Flash memory and run the loaded program. When the switch is toggled to 3.3V, BOOT0 is pulled high, enabling the bootloader for programming.

---

## **3. Adding the Power Source**

To complete the setup for the STM32 microcontroller, a stable **3.3V power supply** is required. This is typically provided by an external voltage regulator if your design is powered by a higher voltage (e.g., 5V or USB).

### **Voltage Regulator Selection**
A common choice for generating 3.3V from 5V is the **AMS1117-3.3** voltage regulator. This linear regulator steps down the voltage while providing sufficient current to power the STM32.

### **Steps in KiCad:**
1. **Add a Voltage Regulator**:
   - Search for and place the **AMS1117-3.3** or any compatible **3.3V linear regulator** symbol from the KiCad library.

2. **Connect Input and Output**:
   - Connect the **input** of the regulator to the 5V power source (e.g., from USB or an external power supply).
   - The **output** should be connected to the 3.3V rail that powers the STM32 microcontroller.

3. **Add Decoupling Capacitors**:
   - Place **10µF capacitors** on both the input and output sides of the regulator for stability. These capacitors should be placed as close to the regulator pins as possible.
   - The capacitors filter out noise and provide stability during voltage fluctuations.

4. **Ground Connections**:
   - Ensure the ground pin of the regulator is connected to the main ground (GND) of the circuit.

---

## **4. Finalizing the Circuit and Testing**

At this point, the essential external circuitry required to boot the STM32 microcontroller has been set up. Here’s a quick checklist to ensure the microcontroller will boot and operate correctly:

### **Checklist for Proper Operation:**
1. **Power Supply**:
   - Ensure the 3.3V power supply is correctly connected to VDD and VBAT pins.
   - Check that decoupling capacitors are placed on all power pins.

2. **Ground Connections**:
   - All ground pins (VSS, VSSA) must be connected to the main ground.

3. **Reset Circuit**:
   - The NRST pin is connected to ground via a decoupling capacitor or a manual reset switch (optional).
   - The NRST net is labeled for clarity.

4. **Boot Configuration**:
   - The BOOT0 pin is connected to a switch that toggles between 3.3V (bootloader) and ground (boot from Flash).
   - A 10kΩ resistor is in place to pull BOOT0 low by default.

5. **Voltage Regulation**:
   - Ensure that the voltage regulator is properly configured with decoupling capacitors for stable power delivery.

---

## **Next Steps: Enhancing the Design**

While the circuit we’ve built will allow the STM32 microcontroller to boot up and function, there are additional components and peripherals you may want to add depending on your application:
- **Crystal Oscillator**: To improve clock accuracy.
- **Communication Interfaces**: Add UART, SPI, I²C, or USB connections for external communication.
- **Programming Headers**: Add SWD/JTAG headers for debugging and firmware flashing.

## **Conclusion**

With this setup, you now have a properly configured STM32 microcontroller circuit that is ready to boot and run your program. This guide provided detailed steps for setting up the reset pin, boot configuration, and power source in KiCad. Moving forward, you can enhance the design with additional components based on your project’s needs.