import pcbnew

def generate_custom_footprint(component_name):
    # Create a new footprint object
    footprint = pcbnew.Footprint()

    # Set footprint properties
    footprint.SetReference(component_name)
    footprint.SetDescription("Custom footprint for " + component_name)

    # Define pad layout and dimensions
    pad_count = 4
    pad_width = 1.0  # in mm
    pad_height = 1.0  # in mm
    pad_spacing = 1.5  # in mm

    # Add pads to the footprint
    for i in range(pad_count):
        pad = pcbnew.D_PAD(footprint)
        pad.SetSize(pcbnew.wxSizeMM(pad_width, pad_height))
        pad.SetPosition(pcbnew.wxPointMM(i * pad_spacing, 0))  # Adjust position for each pad
        footprint.Add(pad)

    # Save the footprint to a file
    footprint_file_path = component_name + ".kicad_mod"
    pcbnew.PCB_IO().FootprintSave(footprint, footprint_file_path)

    print("Custom footprint generated for", component_name)

# Example usage
generate_custom_footprint("CustomComponent")
