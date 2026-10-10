# Placing the Order

Once all details are selected, review the price breakdown for the boards and any extra services like assembly. If everything looks good, place the order.

By following these steps, you’ve successfully prepared all necessary files to submit your PCB design for manufacturing. After running a design rule check, verifying Gerber files, and adding silkscreen and logos, your design is polished and ready to be sent to a manufacturer for production. Whether you're ordering just a few prototypes or mass production, these steps will ensure a smooth and accurate process.

## Before you pay

- [ ] ERC: 0 errors, 0 warnings
- [ ] DRC with schematic parity: 0 violations, 0 unconnected items
- [ ] Gerbers checked in a viewer (outline, inner planes, drill)
- [ ] BOM: every part matched, stock available
- [ ] Assembly preview: every rotation checked
- [ ] Fabrication files and the design committed together, ideally with a git tag (`rev-c`), so the ordered
      board can always be reproduced

## After ordering

- Keep the order number with the tag in the repository's release notes.
- When the boards arrive, follow the [bring-up checklist](../09_Project/06_Bring-up.md) block by block.
