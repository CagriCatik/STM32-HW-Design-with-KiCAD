# Submitting the Files for PCB Manufacturing

Once your design files are checked and ready, you can upload them to your PCB manufacturer’s website for production.

## Step 1: Upload Gerbers to Manufacturer

1. Go to the manufacturer’s website (e.g., JLCPCB or any other PCB fab service).
2. Choose the quote/ordering tool and upload your Gerber ZIP file (which contains all the Gerber files and drill files).
3. Check Gerber Files: Most manufacturers have an integrated Gerber viewer to visually inspect the files before confirming the order.

## Step 2: Specify Board Details

- Choose your desired PCB material (e.g., FR-4 fiberglass).
- Select the number of layers (usually 2 layers for simple designs).
- Specify the PCB color, finish type (e.g., HASL lead-free, ENIG), and board thickness.
- Choose the number of boards you want to order.

## Step 3: Optional PCB Assembly

- If you want the board fully assembled, you can upload the Bill of Materials (BOM) and Pick-and-Place file.
- Choose the side for assembly (e.g., Top, Bottom, or Both).

## JLCPCB settings for this project

| Option | Value |
|---|---|
| Layers | 4 (detected from the Gerbers) |
| Thickness | 1.6 mm |
| Outer copper | 1 oz |
| Stack-up | JLC04161H-7628 (default) |
| Surface finish | HASL lead-free or ENIG |
| Assembly | top side, upload BOM + CPL |

After uploading BOM and CPL, JLCPCB matches every line to an LCSC part. Check:

- every line is matched and in stock,
- through-hole headers: assemble them or deselect them and solder them yourself,
- the 3D preview: pin-1 markers of ICs, polarity of diodes, LEDs and electrolytic capacitors, connector openings
  towards the board edge.
