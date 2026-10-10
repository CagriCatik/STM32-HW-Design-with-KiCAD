# Netlist Manipulation

Netlist manipulation is a powerful feature that allows designers to dynamically adjust, merge, and analyze the connectivity between components in a PCB design. Python scripting in KiCad enables more advanced control over the netlist, allowing you to optimize routing, improve signal integrity, and handle complex hierarchical designs.

Netlists are essentially the glue that connects all components in your design, describing which pins on each component should be connected to one another. By using Python scripts, designers can manipulate these connections, identify potential design issues, and automate tasks that would be tedious or error-prone if done manually.



## Why Manipulate Netlists with Python?

In complex designs, especially those with hierarchical structures or multi-board systems, manipulating the netlist directly can provide numerous advantages:
- Merging Hierarchical Designs: When working with hierarchical designs, different subsystems may be designed separately. Python scripting can merge multiple netlists, ensuring that connections between different levels of hierarchy are maintained correctly.
- Optimizing Connectivity: Automated netlist manipulation allows you to reassign pins or modify connections to optimize routing strategies, reduce wire lengths, and improve overall board layout.
- Debugging and Analysis: Python can be used to analyze the netlist, detecting potential issues such as redundant connections, shorts, or open circuits. This can be particularly useful in large designs where manually identifying such problems is difficult.
- Version Control and Comparisons: Netlist manipulation scripts can be used to compare different versions of a design, ensuring that changes made between versions are intentional and not the result of errors or oversights.



## Common Use Cases for Netlist Manipulation

### 1. Merging Netlists in Hierarchical Designs
In large projects where different sections of a design are split into separate schematic sheets or developed by different teams, it may be necessary to combine multiple netlists into a single, cohesive netlist. Python scripts can automate this merging process, ensuring that all necessary connections between subsystems are maintained.

Example Use Case:
- A PCB design might have separate netlists for the power supply, the control circuitry, and the sensor interface. By merging these netlists, you ensure all connections between the subsystems are correct before proceeding to layout and routing.

### 2. Netlist Filtering and Analysis
In complex designs, it’s often useful to filter the netlist to focus on specific sections of the design. For example, you may want to extract only the nets associated with power distribution, or isolate analog sections from digital ones for further analysis. Python scripts can quickly perform this filtering and allow for detailed analysis of specific parts of the design.

Example Use Case:
- A designer working on a mixed-signal PCB may need to separate the power nets from the signal nets for further analysis. The power nets can then be analyzed to ensure proper voltage distribution, while the signal nets can be inspected for any potential interference or routing issues.

### 3. Reassigning Pins for Routing Optimization
During the routing phase of PCB design, you may discover that certain components could benefit from having their pins reassigned to different nets in order to simplify routing. Python scripts can automate the process of reassigning pins based on the current routing constraints, helping to reduce wire lengths and improve signal integrity.

Example Use Case:
- In a design with multiple microcontroller GPIOs, a Python script can reassign GPIO pins dynamically to optimize trace lengths and minimize the number of crossing signals, improving the overall quality of the layout.

### 4. Detecting Redundant Connections or Shorts
In complex designs, especially when multiple designers are involved, it’s possible for redundant connections or shorts to occur. Python scripting can be used to analyze the netlist and detect these potential issues before they become costly errors during manufacturing.

Example Use Case:
- A netlist analysis script can check for nets that are connected to the same pin multiple times (redundant connections) or check for shorts between power and ground nets, providing an early warning to the designer.



## Step-by-Step Guide: Implementing Netlist Manipulation with Python

Let’s explore an example where we merge multiple netlists and analyze the merged netlist for any connectivity issues. This example demonstrates how to load and manipulate netlists using Python in KiCad.

### Step 1: Load the Netlists

To start manipulating netlists, you first need to load them into Python. This can be done using the `pcbnew` library, which provides access to the PCB layout and its associated netlist.

The netlist is exported with `kicad-cli` and read as a plain S-expression file; no GUI is needed:

```python
import re, subprocess, sys
from collections import defaultdict

def export_netlist(sch, out="netlist.net", cli="kicad-cli"):
    subprocess.run([cli, "sch", "export", "netlist", "--format", "kicadsexpr", "-o", out, sch], check=True)
    return out

def read_nets(path):
    """Return {net name: [(ref, pin), ...]} from a KiCad S-expression netlist."""
    text = open(path).read()
    nets = defaultdict(list)
    for block in re.findall(r'\(net\s+\(code "\d+"\)\s+\(name "([^"]*)"\)(.*?)\)\s*(?=\(net\s|\)\s*\)\s*$)', text, re.S):
        name, body = block
        nets[name] = re.findall(r'\(ref "([^"]+)"\)\s*\(pin "([^"]+)"\)', body)
    return dict(nets)

def single_node_nets(nets):
    """Nets with only one pin are usually a missing wire (or an intentionally unused pin)."""
    return [n for n, nodes in nets.items() if len(nodes) == 1 and not n.startswith("unconnected-")]

def diff(old, new):
    """Compare two revisions: which nets were added, removed or changed."""
    added = sorted(set(new) - set(old)); removed = sorted(set(old) - set(new))
    changed = sorted(n for n in set(old) & set(new) if sorted(old[n]) != sorted(new[n]))
    return added, removed, changed

nets = read_nets(export_netlist("stm32_prototype/stm32_prototype.kicad_sch"))
print(len(nets), "nets")
```

### Step 2: Merge the Netlists

Once the netlists are loaded, you can merge them into a single netlist. This is useful when combining designs from different subsystems or merging hierarchical blocks.

Merging netlists is not a supported workflow: combine designs as hierarchical sheets in the schematic instead.
A useful operation on two netlists is the **comparison of two revisions**:

```python
old = read_nets("rev-b.net")
new = read_nets("rev-c.net")
added, removed, changed = diff(old, new)
print("added:", added)
print("removed:", removed)
print("changed:", changed)
```

### Step 3: Analyze the Merged Netlist

After merging the netlists, it’s important to analyze them to ensure that the merged design is correct. You can use Python to check for connectivity issues, such as shorts, open circuits, or redundant connections.

```python
for net in single_node_nets(nets):
    print("only one pin on net", net, "->", nets[net])
```

Nets with a single pin usually mean a missing wire or a label typo (`USB_DP` vs. `USB_D+`). Shorts cannot be seen in
the netlist, because two nets that touch become one net; check for unexpectedly large nets instead (for example a
signal net that suddenly contains a GND pin).

This simple analysis checks for shorts and open circuits in the merged netlist. If any issues are found, they are printed out, allowing the designer to address them before proceeding with the design.

### Step 4: Reassign Pins for Optimization

In some cases, it may be beneficial to reassign component pins to optimize routing. Python allows you to do this programmatically, reducing the manual effort required to fine-tune the layout.

Pin swaps belong in the schematic: change the labels there and update the PCB (*Tools → Update PCB from
Schematic*, F8). Editing the netlist file directly is overwritten by the next export.

This example script allows you to specify a component and reassign its pins to different nets, optimizing the connectivity for easier routing.



## Best Practices for Netlist Manipulation

### 1. Preserve Hierarchy
When working with hierarchical designs, ensure that netlist manipulation scripts maintain the logical structure of the design. Flattening hierarchical designs can lead to confusion and increase the risk of connectivity errors.

### 2. Backup the Original Netlist
Before performing any manipulation, always back up the original netlist. This ensures that you can revert to the previous state if something goes wrong during the manipulation process.

### 3. Validation After Manipulation
After modifying or merging netlists, it’s essential to validate the netlist by running checks such as design rule checks (DRC), connectivity analysis, and schematic reviews. This ensures that the manipulated netlist adheres to the design’s requirements.

### 4. Modular Approach
If the netlist manipulation involves multiple steps (e.g., merging, pin reassignment, and optimization), it’s best to modularize the script into separate functions. This not only makes the script more readable but also allows for easier debugging and reuse in future projects.

### 5. Maintain Consistent Net Names
When manipulating netlists, ensure that consistent naming conventions are followed, especially when merging netlists from different sources. Inconsistent net names can cause confusion and lead to connectivity issues that are hard to trace.



## Advanced Example: Multi-Board System Netlist Merging

In designs with multiple PCBs that need to communicate, merging netlists from different boards is essential to ensure proper interconnectivity. The following example demonstrates how to merge netlists from two different PCBs in a multi-board system and check for consistency between the interconnects.

```python
def check_interconnects(board1, board2, interconnects):
    """board1/board2: {net: [(ref, pin)]} from read_nets(); interconnects: pairs of net names that must exist on both."""
    for a, b in interconnects:
        if a not in board1 or b not in board2:
            print(f"Interconnect missing: {a} on board 1 / {b} on board 2")
        else:
            print(f"Interconnect present: {a} ({len(board1[a])} pins) <-> {b} ({len(board2[b])} pins)")

check_interconnects(read_nets("main.net"), read_nets("sensor.net"), [("SPI_CLK", "SPI_CLK"), ("GND", "GND")])
```

This script checks that the nets which connect two boards (such as SPI and GND) exist on both sides. Any missing net is flagged for review.



## Conclusion

Python scripting in KiCad provides immense flexibility for manipulating netlists, whether you're working with hierarchical designs, optimizing pin assignments, or ensuring connectivity across multi-board systems. By leveraging Python for netlist manipulation, PCB designers can automate complex tasks, improve design reliability, and streamline the development process. Whether merging designs, filtering nets for analysis, or optimizing component connections, Python offers powerful tools for improving your PCB design workflow.