# Rev B schematic bootstrap

One-off generator that produced the Rev B hierarchical schematic (`mcu`, `power_usb`, `connectors`) from a
declarative part list (`gen.py`). Each pin gets a short wire stub plus a label, power symbol or no-connect flag,
so connectivity is defined only by the `conns` maps and can be checked against the exported netlist.

Once the schematic is edited in the KiCad GUI, the `.kicad_sch` files are the source of truth and this
generator is kept only as a record of the part choices (values, footprints, LCSC/MPN).

```bash
python3 gen.py /tmp/out          # writes sheets + expected_nets.json (needs KiCad 10 symbol libs, macOS path in libsym.py)
cp ../../stm32_prototype/stm32_prototype.kicad_pro /tmp/out/
./check.sh /tmp/out               # ERC + netlist comparison
```
