#!/usr/bin/env python3
"""Phase 2 board setup for stm32_prototype Rev B (run with KiCad's bundled Python).

- writes JLCPCB-oriented net classes / minimum rules into the .kicad_pro
- writes stm32_prototype.kicad_dru (custom rules, commented)
- builds the board from the schematic netlist (like "Update PCB from Schematic"):
  footprints, fields, nets, DNP/BOM attributes, symbol links
- draws the Blue-Pill outline (53.34 x 22.86 mm, rounded corners) and places the
  mechanically fixed parts: both 1x20 headers and the USB-C receptacle on the short edge

Only intended for an empty board; afterwards use KiCad's "Update PCB from Schematic" (F8).

  /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 \
      scripts/board_setup.py stm32_prototype
"""
import json, os, re, subprocess, sys, tempfile
import pcbnew

PRJ_DIR = os.path.abspath(sys.argv[1])
NAME = 'stm32_prototype'
KICAD_CLI = os.environ.get('KICAD_CLI', '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli')
FP_ROOT = os.environ.get('KICAD_FP_DIR', '/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints')
MM = pcbnew.FromMM

# Board geometry (Blue Pill footprint: 2x 1x20 headers, 0.6" row spacing)
X0, Y0 = 100.0, 100.0
W, H = 53.34, 22.86
CORNER = 1.0
ROW = 15.24

# ------------------------------------------------------------------ project rules / net classes
def update_project():
    path = os.path.join(PRJ_DIR, NAME + '.kicad_pro')
    d = json.load(open(path))
    base = dict(d['net_settings']['classes'][0])
    def cls(name, **kw):
        c = dict(base, name=name, priority=0); c.update(kw); return c
    d['net_settings']['classes'] = [
        dict(base, name='Default', track_width=0.2, clearance=0.2, via_diameter=0.6, via_drill=0.3),
        cls('Power', track_width=0.5, clearance=0.2, via_diameter=0.8, via_drill=0.4, priority=1),
        cls('USB', track_width=0.3, clearance=0.15, diff_pair_width=0.3, diff_pair_gap=0.15, priority=0),
    ]
    d['net_settings']['netclass_patterns'] = (
        [{'netclass': 'Power', 'pattern': p} for p in ('+5V', '+3V3', 'VBUS', 'VBUS_F', 'GND', 'VDDA', 'VBAT')] +
        [{'netclass': 'USB', 'pattern': p} for p in ('USB_D+', 'USB_D-', 'PA11', 'PA12')])
    ds = d['board']['design_settings']
    ds['rules'].update(min_clearance=0.127, min_track_width=0.127, min_via_diameter=0.5, min_through_hole_diameter=0.3,
                       min_via_annular_width=0.1, min_copper_edge_clearance=0.3, min_hole_to_hole=0.5,
                       min_hole_clearance=0.25, min_silk_clearance=0.0, min_text_height=0.8, min_text_thickness=0.15)
    ds['track_widths'] = [0.0, 0.2, 0.3, 0.5, 0.8]
    ds['via_dimensions'] = [{'diameter': 0.0, 'drill': 0.0}, {'diameter': 0.6, 'drill': 0.3}, {'diameter': 0.8, 'drill': 0.4}]
    ds['diff_pair_dimensions'] = [{'gap': 0.0, 'via_gap': 0.0, 'width': 0.0}, {'gap': 0.15, 'via_gap': 0.25, 'width': 0.3}]
    json.dump(d, open(path, 'w'), indent=2)
    open(path, 'a').write('\n')

DRU = """(version 1)
# JLCPCB 2-layer, 1.6 mm, 1 oz standard capabilities (no extra-cost options).
# Project defaults (net classes) are deliberately more generous: 0.2 mm signal, 0.6/0.3 mm via.

(rule "JLC min track / space"
  (constraint track_width (min 0.127mm))
  (constraint clearance (min 0.127mm)))

(rule "JLC min via (0.3 mm drill, 0.5 mm pad)"
  (condition "A.Type == 'Via'")
  (constraint hole_size (min 0.3mm))
  (constraint via_diameter (min 0.5mm))
  (constraint annular_width (min 0.1mm)))

(rule "JLC PTH annular ring"
  (condition "A.Type == 'Pad' && A.Pad_Type == 'Through-hole'")
  (constraint annular_width (min 0.15mm)))

(rule "JLC copper to board edge"
  (constraint edge_clearance (min 0.3mm)))

(rule "JLC hole to hole"
  (constraint hole_to_hole (min 0.5mm)))

(rule "JLC silkscreen text"
  (layer "?.Silkscreen")
  (constraint text_height (min 0.8mm))
  (constraint text_thickness (min 0.15mm)))

(rule "USB differential pair (12 Mbit/s full speed, keep short and matched)"
  (condition "A.NetClass == 'USB'")
  (constraint diff_pair_gap (opt 0.15mm))
  (constraint skew (max 0.15mm)))
"""

# ------------------------------------------------------------------ netlist
def tokenize(s):
    return re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()"]+', s)
def parse(s):
    st = [[]]
    for t in tokenize(s):
        if t == '(': st.append([])
        elif t == ')': x = st.pop(); st[-1].append(x)
        else: st[-1].append(t[1:-1] if t.startswith('"') else t)
    return st[0][0]
def kids(n, k): return [c for c in n if isinstance(c, list) and c and c[0] == k]
def kid(n, k):
    r = kids(n, k); return r[0] if r else None

def read_netlist():
    tmp = os.path.join(tempfile.mkdtemp(), 'net.net')
    subprocess.run([KICAD_CLI, 'sch', 'export', 'netlist', '--format', 'kicadsexpr', '-o', tmp,
                    os.path.join(PRJ_DIR, NAME + '.kicad_sch')], check=True, capture_output=True)
    t = parse(open(tmp).read())
    comps = []
    for c in kids(kid(t, 'components'), 'comp'):
        fields = {f[1][1]: (f[2] if len(f) > 2 else '') for f in kids(kid(c, 'fields'), 'field')} if kid(c, 'fields') else {}
        props = {p[1][1]: (p[2][1] if len(p) > 2 else '') for p in kids(c, 'property')}
        sp = kid(c, 'sheetpath')
        comps.append(dict(ref=kid(c, 'ref')[1], value=kid(c, 'value')[1], fp=kid(c, 'footprint')[1],
                          fields=fields, props=props, sheetnames=kid(sp, 'names')[1], sheetstamps=kid(sp, 'tstamps')[1],
                          uuid=kid(c, 'tstamps')[1]))
    nets = []
    for n in kids(kid(t, 'nets'), 'net'):
        nets.append((kid(n, 'name')[1], [(kid(nd, 'ref')[1], kid(nd, 'pin')[1]) for nd in kids(n, 'node')]))
    return comps, nets

# ------------------------------------------------------------------ board
def outline(board):
    def seg(a, b):
        s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(MM(0.1)); s.SetStart(pcbnew.VECTOR2I(MM(a[0]), MM(a[1]))); s.SetEnd(pcbnew.VECTOR2I(MM(b[0]), MM(b[1])))
        board.Add(s)
    def arc(c, start, ang):
        s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_ARC); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(MM(0.1))
        s.SetCenter(pcbnew.VECTOR2I(MM(c[0]), MM(c[1]))); s.SetStart(pcbnew.VECTOR2I(MM(start[0]), MM(start[1])))
        s.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(ang, pcbnew.DEGREES_T)); board.Add(s)
    r, x1, y1 = CORNER, X0 + W, Y0 + H
    seg((X0 + r, Y0), (x1 - r, Y0)); seg((x1, Y0 + r), (x1, y1 - r))
    seg((x1 - r, y1), (X0 + r, y1)); seg((X0, y1 - r), (X0, Y0 + r))
    arc((x1 - r, Y0 + r), (x1 - r, Y0), 90); arc((x1 - r, y1 - r), (x1, y1 - r), 90)
    arc((X0 + r, y1 - r), (X0 + r, y1), 90); arc((X0 + r, Y0 + r), (X0, Y0 + r), 90)

def pad_bbox(fp, numbers=None):
    xs, ys = [], []
    for p in fp.Pads():
        if numbers is None or p.GetNumber() in numbers:
            xs.append(p.GetPosition().x); ys.append(p.GetPosition().y)
    return min(xs), min(ys), max(xs), max(ys)

def move_pads_center(fp, cx, cy, numbers=None):
    x0, y0, x1, y1 = pad_bbox(fp, numbers)
    fp.Move(pcbnew.VECTOR2I(MM(cx) - (x0 + x1) // 2, MM(cy) - (y0 + y1) // 2))

def place_fixed(board, fps):
    cy = Y0 + H / 2
    # headers along the long edges; pin 20 (3V3/GND) next to the USB end (left), like the Blue Pill
    for ref, y in (('J6', cy - ROW / 2), ('J5', cy + ROW / 2)):
        fp = fps[ref]; fp.SetOrientationDegrees(90)
        x0, _, x1, _ = pad_bbox(fp)
        p1 = [p for p in fp.Pads() if p.GetNumber() == '1'][0].GetPosition().x
        if p1 < (x0 + x1) // 2: fp.SetOrientationDegrees(270)  # pin 1 must be on the right (far from USB)
        move_pads_center(fp, X0 + W / 2, y)
    # USB-C on the left short edge, mouth facing -x, shell front flush with the edge
    fp = fps['J1']
    for ang in (0, 90, 180, 270):
        fp.SetOrientationDegrees(ang)
        sx = sum(p.GetPosition().x for p in fp.Pads() if p.GetNumber().startswith(('A', 'B'))) / 16
        cx = fp.GetPosition().x
        if sx > cx + MM(1): break   # signal pads behind (to the right of) the shell centre -> mouth faces left
    bb = fp.GetCourtyard(pcbnew.F_CrtYd).BBox() if fp.GetCourtyard(pcbnew.F_CrtYd).OutlineCount() else fp.GetBoundingBox(False)
    fp.Move(pcbnew.VECTOR2I(MM(X0) - bb.GetLeft(), MM(cy) - bb.GetCenter().y))

def build_board():
    comps, nets = read_netlist()
    path = os.path.join(PRJ_DIR, NAME + '.kicad_pcb')
    board = pcbnew.LoadBoard(path)
    assert len(board.GetFootprints()) == 0, 'board already has footprints; use Update PCB from Schematic instead'
    board.SetCopperLayerCount(2)
    ds = board.GetDesignSettings()
    ds.SetBoardThickness(MM(1.6))

    netitems = {}
    for name, _ in nets:
        ni = pcbnew.NETINFO_ITEM(board, name); board.Add(ni); netitems[name] = ni
    padnet = {(r, p): name for name, nodes in nets for r, p in nodes}

    fps = {}
    loose = [0, 0]
    for c in comps:
        lib, fpname = c['fp'].split(':')
        fp = pcbnew.FootprintLoad(os.path.join(FP_ROOT, lib + '.pretty'), fpname)
        fp.SetFPIDAsString(c['fp'])
        fp.SetReference(c['ref']); fp.SetValue(c['value'])
        for k, v in list(c['fields'].items()) + [('Datasheet', c['props'].get('Datasheet', '')),
                                                  ('Description', c['props'].get('Description', ''))]:
            if k in ('Footprint', 'Sheetname', 'Sheetfile'): continue
            fp.SetField(k, v)
            fp.GetField(k).SetVisible(False)
        fp.SetPath(pcbnew.KIID_PATH(c['sheetstamps'] + c['uuid']))
        fp.SetSheetname(c['sheetnames'].strip('/').split('/')[-1] if c['sheetnames'] != '/' else '')
        fp.SetSheetfile(dict(MCU='mcu.kicad_sch', Power_USB='power_usb.kicad_sch',
                             Connectors='connectors.kicad_sch').get(fp.GetSheetname(), NAME + '.kicad_sch'))
        attrs = fp.GetAttributes()
        if 'dnp' in c['props']: attrs |= pcbnew.FP_DNP
        if 'exclude_from_bom' in c['props']: attrs |= pcbnew.FP_EXCLUDE_FROM_BOM
        fp.SetAttributes(attrs)
        for pad in fp.Pads():
            n = padnet.get((c['ref'], pad.GetNumber()))
            if n: pad.SetNet(netitems[n])
        # parking lot below the board for everything that is placed in phase 3
        col, row = loose[0] % 10, loose[0] // 10; loose[0] += 1
        fp.SetPosition(pcbnew.VECTOR2I(MM(X0 + col * 13), MM(Y0 + H + 15 + row * 13)))
        board.Add(fp); fps[c['ref']] = fp

    place_fixed(board, fps)
    for ref in ('J1', 'J5', 'J6'):
        fps[ref].SetLocked(True)
    outline(board)
    board.Save(path)
    return len(comps)

if __name__ == '__main__':
    update_project()
    open(os.path.join(PRJ_DIR, NAME + '.kicad_dru'), 'w').write(DRU)
    print('footprints placed:', build_board())
