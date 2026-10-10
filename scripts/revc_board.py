#!/usr/bin/env python3
"""Rev C (RC-car controller) board setup and placement, run with KiCad's bundled Python.

Builds the board from the schematic netlist (reusing board_setup.py), sets the Rev C net classes,
draws a 70 x 50 mm outline with four M3 holes and places every part (coordinates below, mm from the
board's top-left corner). Only for an empty board.

  /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 \
      scripts/revc_board.py stm32_prototype
"""
import json, os, sys
import pcbnew
sys.argv = [sys.argv[0], sys.argv[1]]
import board_setup as bs

MM = pcbnew.FromMM
bs.W, bs.H, bs.CORNER = 70.0, 50.0, 2.0
X0, Y0 = bs.X0, bs.Y0

# ref: (x, y, rotation) of the footprint origin
PLACE = {
    # mounting holes (M3) in the corners
    'H1': (3.5, 3.5, 0), 'H2': (66.5, 3.5, 0), 'H3': (3.5, 46.5, 0), 'H4': (66.5, 46.5, 0),
    # top edge: servo/ESC outputs, receiver inputs, lights, UART (pin 1 = signal at the top)
    'J4': (10.5, 2.8, 0), 'J5': (14.31, 2.8, 0), 'J6': (18.12, 2.8, 0), 'J7': (21.93, 2.8, 0),
    'J8': (27.5, 2.8, 0), 'J9': (31.31, 2.8, 0), 'J10': (35.12, 2.8, 0),
    'R18': (27.5, 11.5, 90), 'R19': (31.31, 11.5, 90), 'R20': (35.12, 11.5, 90),
    'J11': (41.0, 2.8, 0), 'J12': (44.81, 2.8, 0),
    'Q2': (40.5, 10.8, 0), 'R21': (40.5, 13.8, 0), 'R22': (40.5, 15.6, 0),
    'Q3': (44.6, 10.8, 0), 'R23': (44.6, 13.8, 0), 'R24': (44.6, 15.6, 0),
    'J15': (57.0, 2.8, 0),
    # left edge, top: WS2812 output (5V, DIN, GND) with level shifter, 330R and bulk capacitor
    'J17': (3.0, 9.5, 0), 'C34': (7.0, 11.0, 90), 'U7': (7.5, 17.5, 0), 'R29': (7.5, 21.5, 0), 'C33': (3.5, 20.5, 90),
    # left: battery input, reverse protection, TVS, sense divider
    'J16': (48.5, 2.0, 0),
    'J1': (4.0, 30.0, 0),
    'Q1': (16.0, 30.0, 0), 'R7': (16.0, 26.0, 0),
    'D2': (16.0, 35.6, 0), 'C13': (10.0, 36.6, 0), 'C14': (21.8, 33.0, 90),
    'R8': (10.5, 22.0, 90), 'R9': (12.3, 22.0, 90), 'C15': (14.1, 22.0, 90),
    # 5 V buck (TPS563201), output towards the servo headers
    'U2': (18.0, 17.0, 0), 'R10': (14.0, 14.0, 90), 'C16': (11.5, 17.0, 90), 'C17': (13.9, 17.8, 90),
    'C18': (16.5, 20.5, 0), 'C19': (19.5, 12.8, 0), 'L1': (25.5, 17.0, 0),
    'R11': (21.8, 22.0, 90), 'R12': (23.6, 22.0, 90),
    'C20': (30.0, 16.0, 90), 'C21': (32.2, 16.0, 90), 'C22': (34.4, 16.0, 90), 'C30': (28.0, 27.8, 0),
    'D3': (38.5, 18.5, 0),
    # motor driver, bulk, shunt, terminal on the bottom edge
    'U5': (25.0, 40.0, 180), 'C27': (33.6, 45.6, 0), 'C28': (19.5, 41.5, 90), 'C29': (25.0, 35.8, 0),
    'R17': (31.5, 36.0, 90), 'J3': (11.0, 44.0, 0),
    # MCU, PA11/PA12 facing the USB connector on the right edge
    'U1': (46.0, 31.0, 0),
    'C1': (48.75, 37.8, 0), 'C2': (52.6, 27.3, 90), 'C3': (43.25, 24.2, 0), 'C4': (40.0, 24.2, 0),
    'C5': (36.5, 25.5, 0), 'JP1': (31.0, 21.5, 0),
    'FB1': (38.6, 35.6, 90), 'C6': (36.8, 35.6, 90), 'C7': (35.0, 35.6, 90),
    'Y1': (38.2, 30.3, 0), 'C8': (36.4, 27.3, 0), 'C9': (36.4, 33.0, 0),
    'Y2': (36.5, 22.5, 0), 'C10': (33.6, 22.0, 90), 'C11': (40.3, 21.6, 90),
    'C12': (38.6, 39.0, 90), 'R1': (41.5, 39.6, 0), 'R2': (47.0, 39.6, 0),
    'R3': (55.3, 40.2, 90), 'D1': (53.5, 40.2, 90),
    'SW1': (58.0, 46.5, 0), 'SW2': (50.0, 46.5, 0),
    # USB-C on the right edge, ESD, series R, LDO
    'J2': None, 'U3': (56.0, 33.0, 0), 'R4': (52.6, 30.5, 90), 'R5': (52.6, 33.8, 90), 'R6': (52.6, 37.2, 90),
    'R13': (57.0, 28.5, 0), 'R14': (57.0, 37.5, 0), 'R15': (58.5, 41.0, 90), 'C23': (60.3, 41.0, 90),
    'F1': (56.5, 26.0, 0), 'D4': (56.0, 22.5, 0), 'U4': (50.0, 21.0, 0), 'C24': (52.9, 18.0, 90),
    'C25': (46.8, 23.6, 0), 'C26': (50.2, 24.2, 0), 'R16': (44.0, 21.0, 0), 'D5': (44.0, 19.0, 0),
    # debug, Qwiic (right column), IMU near the board centre line
    'J13': (64.5, 21.0, 0), 'J14': (64.5, 12.0, 0), 'JP2': (58.8, 16.5, 90),
    'R27': (55.5, 14.3, 0), 'R28': (55.5, 16.6, 0),
    'U6': (44.0, 44.5, 0), 'R25': (41.0, 44.5, 90), 'R26': (39.2, 44.5, 90), 'C31': (44.0, 41.6, 0),
    'C32': (44.0, 47.6, 0),
}

def update_project():
    path = os.path.join(bs.PRJ_DIR, bs.NAME + '.kicad_pro')
    d = json.load(open(path))
    base = dict(d['net_settings']['classes'][0])
    def cls(name, **kw):
        c = dict(base, name=name, priority=0); c.update(kw); return c
    d['net_settings']['classes'] = [
        dict(base, name='Default', track_width=0.2, clearance=0.15, via_diameter=0.6, via_drill=0.3),
        # battery, motor and servo rail: up to ~3.5 A; 0.8 mm outer copper + pours (IPC-2152: ~2.8 A at 10 K)
        cls('HighCurrent', track_width=0.8, clearance=0.2, via_diameter=0.8, via_drill=0.4, priority=1),
        cls('Power', track_width=0.5, clearance=0.2, via_diameter=0.8, via_drill=0.4, priority=2),
        cls('Supply', track_width=0.3, clearance=0.15, via_diameter=0.6, via_drill=0.3, priority=3),
        cls('USB', track_width=0.3, clearance=0.15, diff_pair_width=0.3, diff_pair_gap=0.15, priority=4),
    ]
    d['net_settings']['netclass_patterns'] = (
        [{'netclass': 'HighCurrent', 'pattern': p} for p in ('VBAT', '*VBAT_RAW', 'V5_SERVO', '*BUCK_SW',
                                                             '*MOTOR_A', '*MOTOR_B', '*MOTOR_ISEN')] +
        [{'netclass': 'Power', 'pattern': p} for p in ('+5V', 'VBUS', '*/VBUS_F')] +
        [{'netclass': 'Supply', 'pattern': p} for p in ('+3V3', 'GND', '*/VDDA', '*VBAT_RTC')] +
        [{'netclass': 'USB', 'pattern': p} for p in ('USB_D+', 'USB_D-', 'PA11', 'PA12')])
    ds = d['board']['design_settings']
    ds['track_widths'] = [0.0, 0.2, 0.3, 0.5, 0.8, 1.2]
    json.dump(d, open(path, 'w'), indent=2)
    open(path, 'a').write('\n')

def place(board, _fps=None):
    fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
    for ref, v in PLACE.items():
        if v is None: continue
        x, y, r = v; fp = fps[ref]
        fp.SetOrientationDegrees(r); fp.SetPosition(pcbnew.VECTOR2I(MM(X0 + x), MM(Y0 + y)))
    # USB-C: mouth flush with the right edge, centred on the MCU's USB pins
    fp = fps['J2']
    for ang in (0, 90, 180, 270):
        fp.SetOrientationDegrees(ang)
        sx = sum(p.GetPosition().x for p in fp.Pads() if p.GetNumber().startswith(('A', 'B'))) / 16
        if sx < fp.GetPosition().x - MM(1): break
    bb = fp.GetCourtyard(pcbnew.F_CrtYd).BBox()
    fp.Move(pcbnew.VECTOR2I(MM(X0 + bs.W) - bb.GetRight(), MM(Y0 + 33.0) - bb.GetCenter().y))
    missing = set(fps) - set(PLACE)
    assert not missing, missing
    for ref in ('J1', 'J2', 'J3', 'H1', 'H2', 'H3', 'H4'): fps[ref].SetLocked(True)

if __name__ == '__main__':
    update_project()
    open(os.path.join(bs.PRJ_DIR, bs.NAME + '.kicad_dru'), 'w').write(bs.DRU)
    bs.place_fixed = place
    print('footprints:', bs.build_board())
    import apply_3d_models   # 3D models KiCad does not ship (stored in stm32_prototype/3dmodels)
    path = os.path.join(bs.PRJ_DIR, bs.NAME + '.kicad_pcb')
    b = pcbnew.LoadBoard(path); apply_3d_models.apply(b); b.Save(path)
