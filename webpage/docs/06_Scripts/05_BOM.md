# BOM Generation

Generating a Bill of Materials (BOM) is a critical part of the PCB design process. The BOM lists all the components required to manufacture the PCB, along with quantities, part numbers, and additional information necessary for procurement and assembly. Python scripting in KiCad offers powerful tools to automate BOM generation, ensuring that the BOM is accurate, well-formatted, and tailored to meet the needs of your specific project, assembly house, or procurement system.

Automating the BOM generation process not only saves time but also reduces the chance of errors, especially in complex designs with many components. Python allows you to customize the format, add additional fields like manufacturer part numbers, and integrate with external databases or systems for sourcing components.



## Why Automate BOM Generation?

In any PCB design project, manually generating a BOM can be a time-consuming and error-prone task, particularly for designs that involve a large number of components or frequent revisions. Automating this process with Python scripting ensures consistency, reduces human error, and allows you to easily adapt the BOM format for various requirements. Automating BOM generation has several key benefits:

- Efficiency: Automating the process saves time by reducing manual data entry, especially when dealing with numerous components.
- Accuracy: Automatically extracting information from the design ensures that the BOM accurately reflects the components used in the schematic and layout.
- Customization: You can format the BOM to meet the needs of different stakeholders, such as your assembly house, procurement team, or external suppliers.
- Integration: Python scripts can integrate with external databases, enabling automatic lookup and insertion of part numbers, pricing, availability, and other supplier-related details.
- Update Management: BOM scripts can easily be run whenever there is a design change, ensuring that the BOM is always in sync with the latest version of the design.



## Common Use Cases for BOM Generation

### 1. Generating a Basic BOM

At its simplest, a BOM contains a list of all components used in a design along with their quantities and designators. A Python script can extract this information directly from the design files, ensuring that the BOM accurately reflects the components used in the schematic.

Example:
- A basic BOM for a small design might list the resistors, capacitors, integrated circuits (ICs), and connectors, along with their quantities, descriptions, and designators (e.g., R1, C2, U3).

### 2. Adding Manufacturer Part Numbers and Supplier Information

In most cases, a basic BOM is insufficient for procurement. You need to include manufacturer part numbers, supplier information, and sometimes alternate part options. A Python script can either retrieve this information from a local database or query online APIs to populate these fields.

Example:
- A script could query a component database to automatically fetch the manufacturer part numbers for each resistor and capacitor, or to pull in pricing and availability information from suppliers like Digi-Key or Mouser.

### 3. Customized BOM Formats for Assembly Houses

Different assembly houses may have specific requirements for BOM formatting. Python scripts allow you to generate BOMs that are tailored to these requirements, ensuring that the assembly house has all the information needed to manufacture your board correctly. This can include adding extra fields such as component placement details, package types, and special handling instructions.

Example:
- A Python script can generate a BOM with extra columns for SMT (Surface-Mount Technology) package sizes, special assembly notes, and even placement details (e.g., top or bottom layer of the PCB).

### 4. BOM Grouping and Sorting

In larger designs, grouping components by type (e.g., all resistors together) or sorting them by designator can make the BOM more readable and easier to work with. Python scripts can automate this process, allowing you to organize the BOM in the most logical way for your project.

Example:
- A script could group all resistors and capacitors together, sort them by value, and then list the associated designators for each component. This makes it easier for procurement teams to source parts in bulk.

### 5. Generating Multi-Board BOMs

In designs that involve multiple PCBs or subsystems, generating a unified BOM across all boards can be challenging. Python scripts can automate the merging of BOMs from multiple boards, ensuring that quantities are consolidated, and all necessary components are listed in a single document.

Example:
- For a project involving a main control board and a power distribution board, a script can merge the BOMs from both designs, ensuring that the total number of common components like connectors or resistors is correctly calculated.



## Step-by-Step Guide: Automating BOM Generation with Python

Let’s walk through an example of using Python scripting in KiCad to automate the generation of a detailed BOM that includes basic component information along with manufacturer part numbers and supplier details.

### Step 1: Extract Component Information from the Schematic

The first step in generating a BOM is to extract the relevant information from the schematic. Using KiCad’s `pcbnew` or `eeschema` libraries, you can programmatically access the components and their associated properties.

```python
import pcbnew

def extract_components():
    board = pcbnew.GetBoard()
    components = board.GetModules()

    bom_data = []

    for component in components:
        ref = component.GetReference()
        value = component.GetValue()
        footprint = component.GetFPID().GetLibItemName()
        quantity = 1  # Default to 1 for each component

        bom_data.append({
            'Reference': ref,
            'Value': value,
            'Footprint': footprint,
            'Quantity': quantity
        })

    return bom_data
```

### Step 2: Add Manufacturer and Supplier Information

Once you have the basic component data, you can extend the script to include additional fields such as manufacturer part numbers and supplier details. These can be retrieved from a local database or external sources.

```python
def add_supplier_info(bom_data):
    for component in bom_data:
        # Example: Add manufacturer and supplier information
        if component['Value'] == '10k':
            component['Manufacturer Part Number'] = 'RES-10K-1%_0805'
            component['Supplier'] = 'Digi-Key'
            component['Supplier Part Number'] = '311-10K-RC'
        else:
            component['Manufacturer Part Number'] = 'Unknown'
            component['Supplier'] = 'Unknown'

    return bom_data
```

### Step 3: Export the BOM to a CSV File

The final step is to export the BOM to a CSV file or another format that matches the requirements of your assembly house or procurement system. CSV is a common format that can be easily imported into most procurement tools.

```python
import csv

def export_bom_to_csv(bom_data, filename='bom.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=bom_data[0].keys())
        writer.writeheader()
        for component in bom_data:
            writer.writerow(component)

    print(f"BOM exported to {filename}")
```

### Step 4: Running the Script

After writing the script, you can run it directly from KiCad’s Python scripting console or from an external Python environment. This will generate a BOM with all the necessary fields.

```python
# Generate the BOM
bom_data = extract_components()

# Add manufacturer and supplier information
bom_data = add_supplier_info(bom_data)

# Export to CSV
export_bom_to_csv(bom_data, 'my_custom_bom.csv')
```



## Best Practices for BOM Generation

### 1. Include Manufacturer Part Numbers
The inclusion of manufacturer part numbers is critical for ensuring that the correct components are sourced during procurement. This reduces the chance of errors and ensures that the parts ordered are exactly what was specified in the design.

### 2. Group and Sort Components
For easier reading and to facilitate bulk ordering, group similar components together (e.g., group all resistors or capacitors). Sorting the components by designator or value can also make it easier for the procurement team to process the BOM.

### 3. Tailor the BOM Format for Different Stakeholders
Different stakeholders (assembly houses, procurement teams, or suppliers) may have varying requirements for BOM formats. Use Python scripts to customize the format of the BOM to meet these specific needs. For example, assembly houses may need details on component placement, while procurement teams need supplier information.

### 4. Update the BOM Regularly
During the design process, components may change due to availability, cost, or design revisions. Automate the generation of BOMs at every major design milestone to ensure that the BOM always reflects the most current version of the design.

### 5. Version Control for BOMs
Treat your BOM as a key project document and place it under version control alongside your PCB design files. This ensures that changes to the design are always accompanied by an updated BOM, reducing the risk of version mismatches.



## Advanced Example: Multi-Board BOM Generation

In projects with multiple PCBs, generating a single, unified BOM can streamline the procurement process. The following script demonstrates how to combine BOMs from multiple boards and generate a consolidated BOM.

```python
def merge_boms(boms):
    merged_bom = {}
    
    for bom in boms:
        for component in bom:
            ref = component['Reference']
            if ref in merged_bom:
                merged_bom[ref]['Quantity'] += component['Quantity']
            else:
                merged_bom[ref] = component
    
    return list(merged_bom.values())

# Example usage
board1_bom = extract_components_from_board('board1.kicad_pcb')
board2_bom = extract_components_from_board('

board2.kicad_pcb')

merged_bom = merge_boms([board1_bom, board2_bom])
export_bom_to_csv(merged_bom, 'merged_bom.csv')
```

This script consolidates components from two different PCBs, merging them into a single BOM. The `merge_boms` function ensures that quantities are updated correctly, and the resulting BOM can be exported in the desired format.



## Conclusion

Automating the generation of BOMs using Python in KiCad significantly improves the accuracy, efficiency, and flexibility of your design process. Whether generating simple BOMs for small designs or complex, multi-board BOMs with detailed supplier information, Python scripting provides a powerful toolset for customizing and optimizing this critical step in PCB design. By following best practices and leveraging Python’s capabilities, you can ensure that your BOM is always accurate, up-to-date, and tailored to the specific needs of your project and stakeholders.