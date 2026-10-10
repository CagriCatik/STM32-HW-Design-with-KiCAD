#!/usr/bin/env python3
"""Phase 3 placement for stm32_prototype Rev B (format A: Blue-Pill pinout, lengthened board).

Board 76.2 x 22.86 mm. The two 1x20 headers (0.6" row spacing) are centred; the left extension holds
USB-C and the power path, the right extension the debug connectors and Qwiic. The MCU sits in the
strip between the header rows, rotated 180 deg so PA11/PA12 face the USB connector.

Coordinates below are relative to the board's top-left corner (X0, Y0), in mm.

  /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 \
      scripts/place_revb.py stm32_prototype/stm32_prototype.kicad_pcb
"""
import sys
import pcbnew

MM = pcbnew.FromMM
X0, Y0 = 100.0, 100.0
L, H = 76.2, 22.86
CORNER = 1.0
CY = H / 2
ROW = 15.24

# ref: (x, y, rotation)  -- footprint origin position
PLACE = {
    # left extension: USB-C, protection, power path
    'J1': None,                       # flush with the left edge, see below
    'F1': (3.0, 2.0, 0), 'D2': (8.5, 2.0, 0),
    'C14': (11.2, 7.6, 90), 'U3': (15.5, 7.6, 0), 'C15': (19.8, 7.6, 90), 'C16': (21.5, 7.6, 90),
    'U2': (14.5, CY, 0),
    'R7': (1.5, 19.6, 90), 'R8': (3.3, 19.6, 90), 'R9': (5.1, 19.6, 90), 'C13': (6.9, 19.6, 90),
    'D3': (8.7, 19.6, 90), 'R10': (10.5, 19.6, 90),
    # USB series resistors and D+ pull-up between ESD and MCU
    'R4': (20.5, 10.9, 0), 'R5': (20.5, 12.6, 0), 'R6': (20.5, 14.5, 0),
    # MCU and its left-side decoupling (VDD24 top-left, VDD36 bottom-left)
    'U1': (31.0, CY, 180),
    'C4': (23.2, 7.3, 90), 'C1': (24.9, 7.3, 90), 'C2': (24.9, 15.6, 90),
    # right side: VDDA filter, HSE, NRST, BOOT, VBAT, VDD48
    'C6': (37.6, 7.6, 90), 'C7': (39.3, 7.6, 90), 'FB1': (41.0, 7.6, 90),
    'Y1': (39.5, 12.0, 0), 'C8': (43.3, 10.6, 0), 'C9': (43.3, 13.4, 0),
    'C12': (44.6, 7.6, 90), 'R1': (46.6, 7.6, 90), 'R2': (48.3, 7.6, 90),
    'C3': (37.6, 15.6, 90), 'C5': (39.3, 15.6, 90), 'JP1': (42.0, 15.8, 0),
    'Y2': (46.0, 14.5, 90), 'C10': (48.9, 13.4, 0), 'C11': (48.9, 15.6, 0),
    # buttons and user LED
    'SW1': (54.5, 8.55, 0), 'SW2': (54.5, 14.4, 0),
    'D1': (59.6, 8.0, 90), 'R3': (61.3, 8.0, 90),
    # right extension: debug and Qwiic
    'J2': (68.0, 5.8, 90), 'J3': (73.9, 7.62, 0),
    'JP2': (66.0, 12.4, 0), 'R11': (69.6, 11.6, 0), 'R12': (69.6, 13.4, 0),
    'J4': (68.0, 18.0, 0),
}

def outline(board):
    for d in [d for d in board.GetDrawings() if d.GetLayer() == pcbnew.Edge_Cuts]:
        board.Delete(d)
    def seg(a, b):
        s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(MM(0.1))
        s.SetStart(pcbnew.VECTOR2I(MM(a[0]), MM(a[1]))); s.SetEnd(pcbnew.VECTOR2I(MM(b[0]), MM(b[1]))); board.Add(s)
    def arc(c, start):
        s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_ARC); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(MM(0.1))
        s.SetCenter(pcbnew.VECTOR2I(MM(c[0]), MM(c[1]))); s.SetStart(pcbnew.VECTOR2I(MM(start[0]), MM(start[1])))
        s.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T)); board.Add(s)
    r, x1, y1 = CORNER, X0 + L, Y0 + H
    seg((X0 + r, Y0), (x1 - r, Y0)); seg((x1, Y0 + r), (x1, y1 - r))
    seg((x1 - r, y1), (X0 + r, y1)); seg((X0, y1 - r), (X0, Y0 + r))
    arc((x1 - r, Y0 + r), (x1 - r, Y0)); arc((x1 - r, y1 - r), (x1, y1 - r))
    arc((X0 + r, y1 - r), (X0 + r, y1)); arc((X0 + r, Y0 + r), (X0, Y0 + r))

def pads_center(fp):
    xs = [p.GetPosition().x for p in fp.Pads()]; ys = [p.GetPosition().y for p in fp.Pads()]
    return (min(xs) + max(xs)) // 2, (min(ys) + max(ys)) // 2

def main(path):
    board = pcbnew.LoadBoard(path)
    fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
    outline(board)
    for fp in fps.values(): fp.SetLocked(False)
    # headers: centred along the board, pin 20 towards the USB end (orientation kept from board_setup)
    for ref, y in (('J6', CY - ROW / 2), ('J5', CY + ROW / 2)):
        fp = fps[ref]; cx, cy = pads_center(fp)
        fp.Move(pcbnew.VECTOR2I(MM(X0 + L / 2) - cx, MM(Y0 + y) - cy))
    # USB-C: keep orientation, front of courtyard flush with the left edge, centred vertically
    fp = fps['J1']; bb = fp.GetCourtyard(pcbnew.F_CrtYd).BBox()
    fp.Move(pcbnew.VECTOR2I(MM(X0) - bb.GetLeft(), MM(Y0 + CY) - bb.GetCenter().y))
    for ref, v in PLACE.items():
        if v is None: continue
        x, y, rot = v; fp = fps[ref]
        fp.SetOrientationDegrees(rot); fp.SetPosition(pcbnew.VECTOR2I(MM(X0 + x), MM(Y0 + y)))
    missing = set(fps) - set(PLACE) - {'J5', 'J6'}
    assert not missing, missing
    for ref in ('J1', 'J5', 'J6', 'J2', 'J3', 'J4'): fps[ref].SetLocked(True)
    # too dense for designators on every part: keep silk references only on parts the user interacts with
    for ref, fp in fps.items():
        keep = (ref.startswith(('J', 'SW', 'U')) and not ref.startswith('JP')) or ref in ('D1', 'D3')
        fp.Reference().SetVisible(keep)
    board.Save(path)

if __name__ == '__main__':
    main(sys.argv[1])
