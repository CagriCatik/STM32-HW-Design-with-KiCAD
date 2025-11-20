# D

## DRC

DRC (Design Rule Check) is an automated verification step in PCB design that validates whether the layout complies with manufacturing and electrical constraints. It checks clearances, trace widths, via dimensions, copper-to-copper spacing, and other rules defined by the PCB fabricator. A complete DRC pass ensures the board can be produced reliably and reduces the risk of shorts, opens, or impedance issues [Verified].

## Decoupling

Decoupling is the use of capacitors placed near power pins to stabilize local supply voltage for an integrated circuit. These capacitors counter rapid current demands that occur during internal switching events, preventing voltage dips and suppressing high-frequency noise. A decoupling capacitor acts as a local charge reservoir, supplying instantaneous current while isolating the device from supply-line inductance.

Decoupling is most effective when the capacitor is placed directly at the IC power pin with minimal trace length. Typical values include 100 nF ceramic capacitors with low ESR for high-frequency suppression, complemented by larger capacitors for lower-frequency transients. Proper decoupling ensures stable MCU operation, reduces electromagnetic interference, and supports consistent logic-level thresholds [Verified].
