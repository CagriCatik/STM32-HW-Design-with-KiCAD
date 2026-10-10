# Customized Footprint Generation

Python scripting in KiCad offers an efficient and flexible way to generate custom footprints for components, especially in cases where non-standard footprints are required or when working with a large number of components that need consistent layout properties. Custom footprints can be critical for designs that have special mounting requirements, mechanical constraints, or non-typical geometries. Automating footprint creation through scripting also ensures accuracy and consistency across multiple components, which can be particularly useful for large or modular designs.

## Why Use Python for Footprint Generation?

Creating footprints manually in KiCad can be time-consuming, especially when dealing with complex designs or large numbers of components. Python scripting allows you to automate this process, ensuring consistency in pad sizes, spacings, and silkscreen markings. With scripting, you can also easily generate variations of a footprint by simply adjusting a few parameters (e.g., number of pins, pad size), which can significantly accelerate the design process for large projects.

## Components of a Custom Footprint
When generating a custom footprint using Python, you typically need to define the following key elements:
1. Pads: The electrical contact points on the footprint. These are essential for defining where the component's leads or terminals will connect to the PCB.
2. Silkscreen Markings: Visual indicators such as component outlines, reference designators, and polarity marks.
3. Courtyard: The area surrounding the component where other components cannot be placed, ensuring clearance for soldering or assembly.
4. Placement of the Footprint: Ensuring the proper alignment of pads, silkscreen, and courtyard with respect to the component's mechanical dimensions.
5. Metadata: Adding reference designators and descriptions for identification and organization within KiCad.

By using Python, all these aspects can be automated and precisely controlled.



## Best Practices for Custom Footprint Generation

When generating custom footprints programmatically, several best practices should be followed to ensure the footprint will work correctly and meet design specifications.

### 1. Follow the Component's Datasheet
The foundation of any good custom footprint is the component's datasheet. All dimensions, including pad sizes, spacings, pin positions, and other geometric constraints, should be derived directly from the datasheet. Incorrect dimensions or assumptions can lead to misaligned components during the assembly process or unreliable electrical connections.

Datasheet-Based Parameters:
- Pad Size: Pad dimensions should be based on the component's terminal size, taking into account soldering and thermal relief considerations.
- Pin Pitch: This is the distance between adjacent pins on the component and should be accurately reflected in the pad spacing on the footprint.
- Component Outline and Courtyard: Ensure that the component outline and courtyard are drawn according to the dimensions specified in the datasheet, providing adequate clearance for placement and soldering.

### 2. Define Pad Layouts Consistently
Consistency is key when creating footprints, especially in designs where multiple similar components are used. By using Python scripting, you can ensure that the same pad layout and spacing rules are applied to all relevant components.

Best Practices:
- Pad Shape and Size: Define pad shapes (e.g., rectangular, circular, or oval) consistently across similar components. Ensure the size is adequate for both the component lead and soldering process.
- Tolerance Considerations: When defining pad size and spacing, include tolerances for assembly to account for variations in manufacturing processes, component size, and solder paste application.
- Alignment of Pads: Maintain consistent alignment for all pads, especially for surface-mount components. Pads should be aligned symmetrically to the component's center to ensure even solder paste application and assembly accuracy.

### 3. Silkscreen and Courtyard Markings
Good silkscreen markings improve the readability and assembly of a PCB. These markings should include clear component outlines, reference designators, and polarity marks where needed. Additionally, the courtyard defines the component's keep-out zone to prevent other components from being placed too close.

Best Practices:
- Polarity and Pin 1 Marking: For components like diodes, LEDs, and polarized capacitors, include clear markings (e.g., arrows, dots) to indicate polarity or the location of Pin 1.
- Component Outline: Use silkscreen to show the physical outline of the component. Ensure that the outline doesn't interfere with pads or vias, as silkscreen over pads can affect solderability.
- Courtyard Clearance: Define the courtyard for each footprint with enough clearance to prevent components from being placed too close. This is particularly important for large components with high thermal dissipation requirements or components that require space for proper soldering.
  
### 4. Parameterized Footprint Generation
Python scripting allows the creation of parameterized footprints, where key dimensions (e.g., pin count, pad size, or pin pitch) are passed as variables. This approach makes it easier to generate variations of the same component without needing to manually adjust each one.

Example Use Case:
If you're designing footprints for multiple ICs with varying pin counts, you can use a script to automatically adjust the pad layout based on the number of pins, ensuring consistent pad sizing, spacing, and silkscreen markings across all variants.

### 5. Check for Design Rule Compliance
Before integrating a custom footprint into a design, it's essential to ensure that it complies with the design rules (DRC) set for the PCB. Python scripts can help enforce these design rules by checking pad spacing, clearance from the courtyard, and alignment of the footprint with other components on the board.

Best Practices:
- DRC Compliance: After generating the custom footprint, run a design rule check (DRC) to ensure that all pads and outlines comply with the manufacturing constraints and assembly tolerances.
- Manual Verification: Even though scripts generate footprints programmatically, it’s always a good idea to manually verify the dimensions and placement of the pads and silkscreen by checking against the datasheet.



## Step-by-Step Guide for Generating a Custom Footprint with Python

Here’s an example of how to create a custom footprint for a 4-pin component using Python scripting in KiCad:

```python
import os
import pcbnew

def generate_custom_footprint(name, lib_path="my.pretty", pad_count=4, pitch_mm=1.5, pad_mm=(1.0, 1.0)):
    board = pcbnew.BOARD()                      # footprints need a parent board while they are built
    fp = pcbnew.FOOTPRINT(board)
    fp.SetFPID(pcbnew.LIB_ID("my", name))
    fp.SetReference("U**")
    fp.SetValue(name)
    fp.SetLibDescription("Custom footprint for " + name)
    for i in range(pad_count):
        pad = pcbnew.PAD(fp)
        pad.SetNumber(str(i + 1))
        pad.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
        pad.SetShape(pcbnew.PAD_SHAPE_RECT)
        pad.SetLayerSet(pad.SMDMask())
        pad.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(pad_mm[0]), pcbnew.FromMM(pad_mm[1])))
        pad.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(i * pitch_mm), 0))
        fp.Add(pad)
    io = pcbnew.PCB_IO_MGR.FindPlugin(pcbnew.PCB_IO_MGR.KICAD_SEXP)
    io.FootprintSave(os.path.abspath(lib_path), fp)   # writes <lib>.pretty/<name>.kicad_mod
    print("footprint written:", name)

generate_custom_footprint("CustomComponent")
```

Explanation:
- Footprint Creation: We begin by creating a new footprint object and setting the reference (the name of the component) and the description.
- Pad Layout: The pad layout is defined based on the number of pads, their dimensions, and the spacing between them. Sizes and positions are `pcbnew.VECTOR2I` values in internal units (nanometres); `pcbnew.FromMM()` converts from millimetres.
- File Output: The KiCad S-expression plugin writes the footprint into a `.pretty` library folder as `<name>.kicad_mod`. Add the folder to the footprint library table to use it.

!!! note "Tested with KiCad 10"
    Run the script with KiCad's bundled Python (on macOS: `/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3`). Older examples on the web use `D_PAD`, `MODULE`, `wxPoint` and `wxSize`; these names were removed in KiCad 6–8.



## Benefits of Custom Footprint Generation with Python
- Efficiency: Automating the generation of footprints, especially for large or modular designs, saves time and ensures consistency.
- Consistency: When generating multiple footprints with similar layouts, Python scripts ensure that all footprints follow the same layout principles, reducing the risk of errors during placement.
- Flexibility: Scripting allows you to customize each aspect of the footprint, making it easy to adapt designs to specific project requirements or manufacturing constraints.
- Scalability: For projects with numerous components, especially those using custom or unique footprints, Python scripting offers a scalable solution for creating and managing footprints.



By following these best practices and leveraging Python scripting in KiCad, designers can efficiently create accurate and reliable custom footprints that adhere to their project specifications. This automation minimizes errors and increases design quality, making it an essential tool for advanced PCB designers.