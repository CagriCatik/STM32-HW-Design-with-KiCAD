# Drawing the Schematic

Creating a schematic is a crucial step that defines how the components of your circuit interconnect.
A well-designed schematic ensures that your PCB functions correctly and is easy to troubleshoot.

## Steps to Draw the Schematic

### Open the Schematic Editor

- Access the Editor:
  - In the Project Manager, click on the Schematic Editor icon (represented by an electronic schematic symbol).
  
- Familiarize with the Interface:
  - The Schematic Editor window opens, displaying a blank canvas where you'll design your circuit.
  - Key areas include the component toolbar, wire tool, and libraries panel.

### Add Components

- Place Symbols:
  - Click on the Place Symbol tool (shortcut key: `A`) in the toolbar.
- Select Components:
  - A Choose Symbol dialog appears. Use the search bar to find components like "STM32" for the microcontroller, "R" for resistors, "C" for capacitors, etc.
- Add to Schematic:
  - Select the desired component and click OK. Click on the schematic canvas to place the component.
- Repeat:
  - Continue adding all necessary components for your STM32-based project.

> Tip: If a required component isn't available in the default libraries, consider:

- Installing Additional Libraries: Use KiCad’s library manager to add more component libraries.
- Creating Custom Symbols: Design custom symbols for unique or proprietary components.

> Best Practice: Label components clearly using consistent naming conventions to enhance readability and ease of reference.

### Connect Components

- Use the Wire Tool:
  - Select the Wire tool (shortcut key: `W`) from the toolbar.
- Create Connections:
  - Click on a component’s pin to start a wire, then click on the destination pin to complete the connection.
- Ensure Proper Connectivity:
  - Double-check that all components are correctly interconnected as per your circuit design.

> Practical Example: Connect the VCC pin of the STM32 microcontroller to a power source symbol, and link the GND pins to the ground symbol to establish common power and ground connections.

### Add Power and Ground Symbols

- Place Power Ports:
  - Click on the Place Power Port tool or search for "VCC" and "GND" symbols in the libraries.
- Position Symbols:
  - Place the power (`VCC`) and ground (`GND`) symbols appropriately on the schematic to serve as common power sources.

> Best Practice: Use global labels for power and ground to simplify connections across different schematic sheets.

### Annotate the Schematic

- Assign Unique Identifiers:
  - Go to Tools > Annotate Schematic.
- Automatic Labeling:
  - KiCad will automatically assign unique identifiers (e.g., `R1`, `U1`, `C1`) to each component.
- Review Annotations:
  - Ensure that each component has a unique and logical identifier to avoid confusion during PCB layout.

> Best Practice: Perform annotation before proceeding to layout to ensure all components are correctly labeled and identifiable.

### Perform Electrical Rule Check (ERC)

- Initiate ERC:
  - Navigate to Tools > Electrical Rules Checker.
- Review Errors and Warnings:
  - KiCad will scan the schematic for connectivity issues, unconnected pins, and other potential errors.
- Resolve Issues:
  - Address any highlighted issues to ensure the schematic is free from electrical conflicts.

> Best Practice: Regularly perform ERC during schematic design to catch and rectify issues early in the design process.
