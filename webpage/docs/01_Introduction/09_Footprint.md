# Assigning Footprints to Components

Each schematic symbol corresponds to a physical component on the PCB. Assigning accurate footprints ensures that components fit correctly on the PCB and function as intended.

## Steps to Assign Footprints

### Open the Footprint Assignment Tool

- **Access the Tool:**
  - In the Schematic Editor, navigate to Tools > Assign Footprints.
- **Footprint Assignment Window:**
  - This window displays a list of all components in your schematic alongside their assigned footprints.

### Select Footprints

- **Choose Appropriate Footprints:**
  - For each component, select a footprint that matches its physical specifications.
- **Example Assignments:**
  - STM32 Microcontroller:
    - Choose a footprint matching the specific package type, such as `LQFP48`, from the footprint libraries.
  - Resistors and Capacitors:
    - Assign standard footprints like `Resistor_SMD:R_0805` or `Capacitor_SMD:C_0603`.
- **Custom Footprints:**
  - If a suitable footprint isn't available, create or import a custom footprint to match your component's specifications.

> **Best Practice:** Verify component datasheets to ensure footprint accuracy, preventing manufacturing issues and ensuring reliable soldering.

### Confirm Footprint Assignments

- **Review Selections:**
  - Ensure each component has an appropriate footprint assigned.
- **Finalize Assignments:**
  - Click OK to apply the footprint assignments and return to the Schematic Editor.

> **Practical Example:** For the STM32 microcontroller in an `LQFP48` package, verify that the footprint includes all 48 pins with correct spacing and pad sizes as per the manufacturer's datasheet.
