# Adding Serial Debug Connectors, Power Supply, and Finalizing

This section covers the steps to add **Serial Debug Connectors**, set up the **power supply** using a linear regulator, integrate a **status LED**, and finalize the STM32-based schematic in KiCad. The goal is to create a simple yet functional and robust design that includes UART and I²C connections, proper decoupling, and clean power regulation.

---

## **1. Adding Serial Debug (SWD) and Communication Headers**

Serial Wire Debug (SWD) is essential for programming and debugging STM32 microcontrollers. We will add a **header for SWD connections** to facilitate debugging and program upload. Additionally, we'll break out the **UART** and **I²C** communication interfaces to connectors for external communication.

### **Step 1: Adding SWD Header**
1. **Add Symbol**: Search for **connector** and select a **1x4 male header** (4-pin connector).
2. Place the header in your schematic and align it with the SWD signals.
   - **SWDIO**: Connect to the microcontroller's **PA13**.
   - **SWCLK**: Connect to **PA14**.
   - **VCC**: Connect to the **3.3V power rail**.
   - **GND**: Connect to the **ground**.

3. **Label the Pins**: Use net labels to assign the proper names to each pin, such as **SWDIO**, **SWCLK**, **VCC**, and **GND**.
4. **Note**: SWD connections allow for debugging via an ST-Link or similar device. These connections can be used with **STM32CubeProgrammer** or **OpenOCD** for flashing firmware.

### **Step 2: Adding UART and I²C Headers**
1. **Add UART Header**:
   - Select a **1x4 male header**.
   - Connect **TX** (transmit) to **PA9** and **RX** (receive) to **PA10**.
   - Also connect **VCC** and **GND** to this header to provide power and ground.
   - Label the pins appropriately: **TX**, **RX**, **VCC**, and **GND**.

2. **Add I²C Header**:
   - Select another **1x4 male header**.
   - Connect **SCL** (clock) to **PB6** and **SDA** (data) to **PB7**.
   - Connect **VCC** and **GND** as well.
   - **Add Pull-Up Resistors**: I²C requires pull-up resistors on the clock and data lines to ensure proper signal transmission. Typically, **2.2kΩ resistors** are used, but in this example, we'll use **1.5kΩ** resistors for simplicity. Connect these resistors between **SCL**/**SDA** and **3.3V**.
   - Label the pins **SCL**, **SDA**, **VCC**, and **GND**.

---

## **2. Adding the Power Supply (Linear Regulator)**

The STM32 microcontroller operates at **3.3V**, but USB provides **5V (VBUS)**. To step down the voltage, we will use a **linear voltage regulator** (AMS1117-3.3). This regulator ensures a steady 3.3V output.

### **Step 1: Add the AMS1117-3.3 Regulator**
1. **Add Symbol**: Search for **AMS1117-3.3** and place it in the schematic.
   - **Input (VIN)**: Connect to **VBUS** (the 5V USB power rail).
   - **Output (VOUT)**: Connect to the **3.3V rail** that powers the STM32.
   - **GND**: Connect to the main ground.

### **Step 2: Add Decoupling Capacitors**
Linear regulators require **decoupling capacitors** on both the input and output to stabilize voltage fluctuations:
1. **Input Capacitor**: Place a **22µF capacitor** between **VIN** and **GND**.
2. **Output Capacitor**: Place another **22µF capacitor** between **VOUT** and **GND**.

---

## **3. Adding a Status LED**

To indicate that the system is powered on, we will add a **status LED**. This LED will light up when the regulator outputs 3.3V, providing a simple visual indicator.

### **Step 1: Add the LED**
1. **Add Symbol**: Search for **LED** and place it in the schematic.
   - Connect the **anode** of the LED to the **3.3V rail**.
   - Connect the **cathode** to ground through a current-limiting resistor.

### **Step 2: Add a Current-Limiting Resistor**
1. **Add Symbol**: Search for **resistor** and place it in series with the LED.
2. **Resistor Value**: Use a **1.5kΩ resistor** to limit the current through the LED.
   - Label the resistor as **1K5** (1.5kΩ), which provides approximately **2mA** of current (suitable for most LEDs).

### **LED Voltage and Current**
- The forward voltage drop of a typical **red LED** is around **1.8V**. The current is controlled by the resistor, and for debugging, around **2mA** is sufficient.

---

## **4. Finalizing the Schematic**

After adding the core components (SWD, UART, I²C, Power Supply, and Status LED), the final step is to clean up the schematic and make it ready for PCB layout.

### **Step 1: Group Components and Add Notes**
- **Group related components** (such as the power section, communication headers, and microcontroller pins) together.
- **Use bounding boxes** and label each section clearly (e.g., **Power Supply**, **SWD Debug**, **UART**, **I²C**).
- Add **notes** to the schematic to document key decisions, such as the values of pull-up resistors and the purpose of the LED.

### **Step 2: Add No-Connect (DNC) Flags**
- Unused pins on the STM32 should be marked with **No-Connect (DNC) flags** to prevent errors during the **Electrical Rule Check (ERC)**. To do this:
  - Select the **DNC flag** tool and place it on all unused pins.
  - This practice helps reduce **ERC warnings** and ensures you only focus on the essential pins.

### **Step 3: Run Electrical Rule Check (ERC)**
- After organizing the schematic, run the **Electrical Rule Check (ERC)** to identify any errors or missing connections.
- Fix any errors that are flagged, especially around **power and ground connections** or unconnected signal lines.

---

## **5. Conclusion**

By following these steps, you now have a complete STM32-based schematic that includes:
- **Serial Debug (SWD)**: A header for debugging and programming.
- **UART and I²C headers**: For serial communication with external devices.
- **Power Supply**: A linear regulator to convert 5V from USB to 3.3V for the microcontroller.
- **Status LED**: A visual indicator for debugging and power status.
- **Properly decoupled power lines**: With capacitors on both input and output to stabilize the linear regulator.

This schematic is simple yet functional, providing all the necessary connections to get an STM32 microcontroller up and running. The next step will be to move on to the **PCB layout and routing** stage, where you will place the components on the board and route the connections while considering best practices for differential pair routing (USB), power, and signal integrity.