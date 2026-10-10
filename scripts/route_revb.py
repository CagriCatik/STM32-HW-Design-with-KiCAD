#!/usr/bin/env python3
"""Phase 4 routing for stm32_prototype Rev B.

  route_revb.py dsn   <board> <out.dsn>   export Specctra DSN (2 signal layers, GND as B.Cu plane)
  route_revb.py ses   <board> <in.ses>    import the session, then switch to 4 layers SIG/GND/GND/SIG
  route_revb.py gnd   <board>             final GND pours on F.Cu/B.Cu, fallback vias for any GND pad still
                                          unconnected, stitching vias along the edges
  route_revb.py silk  <board>             hide top designators, pinout + labels on the bottom silkscreen

Run with KiCad's bundled Python. Freerouting in between:
  java -jar freerouting-2.5.0.jar --gui.enabled=false -de out.dsn -do in.ses -mp 100
"""
import math, re, sys
import pcbnew

MM = pcbnew.FromMM
CLEAR = 0.15         # clearance used for the via search (Default and Supply net classes)
VIA_D, VIA_DRILL = 0.6, 0.3
GND_TRACK_W = 0.25   # short pad-to-via stubs; must fit next to 0.5 mm pitch LQFP pins


INNER = (pcbnew.In1_Cu, pcbnew.In2_Cu)


def setup_layers(board):
    """4 layers SIG / GND / GND / SIG (JLC 1.6 mm); inner layers are planes, never routed."""
    board.SetCopperLayerCount(4)
    for L, name in zip(INNER, ('In1.GND', 'In2.GND')):
        board.SetLayerType(L, pcbnew.LT_POWER)
        board.SetLayerName(L, name)


def export_dsn(board, out):
    """Route as a 2-layer job with GND as a B.Cu plane: Freerouting then ties every GND pin to a via.
    (Freerouting cannot route through KiCad's inner power planes; the planes are added after import, where
    every GND via lands on them.)"""
    board.SetCopperLayerCount(2)
    for z in list(board.Zones()):
        board.Delete(z)
    add_zone(board, pcbnew.B_Cu, gnd_net(board), 0)
    fill(board)
    assert pcbnew.ExportSpecctraDSN(board, out)
    t = open(out).read()
    assert '(plane GND' in t
    # Freerouting has no hole-to-hole rule: model 0.6 mm vias as 0.7 mm so via centres stay >= 0.85 mm apart
    t = re.sub(r'\(circle (\S+) 600\)', r'(circle \1 700)', t)
    open(out, 'w').write(t)


def gnd_net(board):
    return board.GetNetInfo().GetNetItem('GND')


def outline_poly(board, inset=0.0):
    box = board.GetBoardEdgesBoundingBox()
    x0, y0, x1, y1 = box.GetLeft(), box.GetTop(), box.GetRight(), box.GetBottom()
    i = MM(inset)
    return [(x0 + i, y0 + i), (x1 - i, y0 + i), (x1 - i, y1 - i), (x0 + i, y1 - i)]


def add_zone(board, layer, net, prio):
    z = pcbnew.ZONE(board)
    z.SetLayer(layer); z.SetNet(net); z.SetAssignedPriority(prio)
    z.SetLocalClearance(MM(0.2)); z.SetMinThickness(MM(0.18))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THT_THERMAL)   # SMD solid, THT with spokes
    z.SetThermalReliefGap(MM(0.3)); z.SetThermalReliefSpokeWidth(MM(0.35))
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    ol = z.Outline(); ol.NewOutline()
    for x, y in outline_poly(board):
        ol.Append(x, y)
    board.Add(z)
    return z


def fill(board):
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())


def copper_items(board):
    items = []
    for fp in board.GetFootprints():
        items += list(fp.Pads())
    items += list(board.GetTracks())
    return items


def free(board, items, pos, radius, layers, ignore_net):
    """True if a circle of `radius` at pos keeps CLEAR to all foreign copper on `layers`."""
    for it in items:
        if it.GetNetCode() == ignore_net and ignore_net != 0:
            continue
        if not any(it.IsOnLayer(l) for l in layers):
            continue
        if it.HitTest(pos, int(radius + MM(CLEAR))):
            return False
    # keep away from the board edge
    box = board.GetBoardEdgesBoundingBox()
    m = int(radius + MM(0.4))
    return box.GetLeft() + m < pos.x < box.GetRight() - m and box.GetTop() + m < pos.y < box.GetBottom() - m


def segment_free(board, items, a, b, w, ignore_net, own_pad=None):
    n = max(2, int(math.hypot(b.x - a.x, b.y - a.y) / MM(0.1)))
    for i in range(1, n):
        p = pcbnew.VECTOR2I(a.x + (b.x - a.x) * i // n, a.y + (b.y - a.y) * i // n)
        if own_pad is not None and own_pad.HitTest(p, 0):
            continue   # still on the pad's own copper
        if not free(board, items, p, w / 2, [pcbnew.F_Cu], ignore_net):
            return False
    return True


def unconnected_gnd_pads(board):
    board.BuildConnectivity()
    conn = board.GetConnectivity()
    gnd = gnd_net(board).GetNetCode()
    pads = []
    for fp in board.GetFootprints():
        for p in fp.Pads():
            if p.GetNetCode() != gnd or p.GetAttribute() != pcbnew.PAD_ATTRIB_SMD:
                continue
            # an SMD pad is fine if its connected item set contains a via or a THT pad or the B.Cu zone
            linked = conn.GetConnectedItems(p)
            if not any(isinstance(i, pcbnew.PCB_VIA) or
                       (isinstance(i, pcbnew.PAD) and i.GetAttribute() == pcbnew.PAD_ATTRIB_PTH) or
                       (isinstance(i, pcbnew.ZONE) and i.GetLayer() == pcbnew.B_Cu) for i in linked):
                pads.append(p)
    return pads


def add_via(board, net, pos):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(pos); v.SetWidth(MM(VIA_D)); v.SetDrill(MM(VIA_DRILL)); v.SetNet(net)
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    board.Add(v)
    return v


def add_track(board, net, a, b, w):
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(a); t.SetEnd(b); t.SetWidth(MM(w)); t.SetLayer(pcbnew.F_Cu); t.SetNet(net)
    board.Add(t)


def holes_ok(board, pos, min_center=0.85):
    """JLC: 0.5 mm hole-to-hole between different nets -> 0.85 mm centre distance for 0.3/0.35 mm drills."""
    for t in board.GetTracks():
        if isinstance(t, pcbnew.PCB_VIA) and math.hypot(t.GetPosition().x - pos.x, t.GetPosition().y - pos.y) < MM(min_center):
            return False
    for fp in board.GetFootprints():
        for p in fp.Pads():
            if p.HasHole() and math.hypot(p.GetPosition().x - pos.x, p.GetPosition().y - pos.y) < \
                    MM(min_center) + p.GetDrillSize().x / 2:
                return False
    return True


def via_for_pad(board, pad, items):
    net = gnd_net(board); code = net.GetNetCode()
    c = pad.GetPosition(); fpc = pad.GetParentFootprint().GetPosition()
    away = math.atan2(c.y - fpc.y, c.x - fpc.x) if (c.x, c.y) != (fpc.x, fpc.y) else 0.0
    # elongated pads (e.g. LQFP pins): first try straight along the pad axis, outwards then inwards
    sz = pad.GetSize(pcbnew.F_Cu)
    bases = []
    if sz.x != sz.y:
        ax = math.radians(-pad.GetOrientationDegrees()) + (math.pi / 2 if sz.y > sz.x else 0)
        out_ = ax if math.cos(ax - away) > 0 else ax + math.pi
        bases = [out_, out_ + math.pi]
        if len(pad.GetParentFootprint().Pads()) > 16:
            bases.reverse()   # IC: put the via under the package so the signal escape stays free
    angles = bases + [away + (k + 1) // 2 * (1 if k % 2 else -1) * math.pi / 8 for k in range(16)]
    for dist in (0.9, 1.1, 1.3, 1.6, 2.0, 2.4):
        for a in angles:
            p = pcbnew.VECTOR2I(int(c.x + MM(dist) * math.cos(a)), int(c.y + MM(dist) * math.sin(a)))
            if holes_ok(board, p) and free(board, items, p, MM(VIA_D) / 2, [pcbnew.F_Cu, pcbnew.B_Cu], code) and \
               segment_free(board, items, c, p, MM(GND_TRACK_W), code, pad):
                add_track(board, net, c, p, GND_TRACK_W)
                v = add_via(board, net, p)
                items.append(v)
                return True
    return False


def stitch_edges(board, pitch=3.0):
    net = gnd_net(board); code = net.GetNetCode()
    items = copper_items(board)
    pts = []
    for x, y in outline_poly(board, inset=1.2):
        pts.append((x, y))
    added = 0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        n = int(math.hypot(x1 - x0, y1 - y0) / MM(pitch))
        for i in range(n + 1):
            p = pcbnew.VECTOR2I(int(x0 + (x1 - x0) * i / max(n, 1)), int(y0 + (y1 - y0) * i / max(n, 1)))
            if holes_ok(board, p) and free(board, items, p, MM(VIA_D) / 2 + MM(0.3), [pcbnew.F_Cu, pcbnew.B_Cu], code):
                items.append(add_via(board, net, p)); added += 1
    return added


def link_to_gnd(board, pad, items, reach=4.0):
    """Fallback: straight F.Cu track from the pad to the nearest GND via or THT GND pad."""
    net = gnd_net(board); code = net.GetNetCode(); c = pad.GetPosition()
    targets = [v.GetPosition() for v in board.GetTracks() if isinstance(v, pcbnew.PCB_VIA) and v.GetNetCode() == code]
    targets += [p.GetPosition() for fp in board.GetFootprints() for p in fp.Pads()
                if p.GetNetCode() == code and p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH]
    targets.sort(key=lambda q: math.hypot(q.x - c.x, q.y - c.y))
    for q in targets:
        if math.hypot(q.x - c.x, q.y - c.y) > MM(reach):
            break
        if segment_free(board, items, c, q, MM(GND_TRACK_W), code, pad):
            add_track(board, net, c, q, GND_TRACK_W)
            return True
    return False


def fix_narrow_tracks(board, min_w=0.15):
    n = 0
    for t in board.GetTracks():
        if not isinstance(t, pcbnew.PCB_VIA) and t.GetWidth() < MM(min_w):
            t.SetWidth(MM(min_w)); n += 1
    return n


def stitch_islands(board, step=0.25):
    """Connect GND fill islands that are not tied to the main plane: union-find over F.Cu/B.Cu islands
    joined by vias and THT pads, then drop a via where an orphan island overlaps the main group."""
    net = gnd_net(board); code = net.GetNetCode()
    zones = {z.GetLayer(): z for z in board.Zones() if z.GetNetCode() == code}
    isl = []   # (layer, SHAPE_POLY_SET)
    for L, z in zones.items():
        fp = z.GetFilledPolysList(L)
        for i in range(fp.OutlineCount()):
            s = pcbnew.SHAPE_POLY_SET(); s.AddOutline(fp.Outline(i)); isl.append((L, s))
    parent = list(range(len(isl)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    links = [v.GetPosition() for v in board.GetTracks() if isinstance(v, pcbnew.PCB_VIA) and v.GetNetCode() == code]
    links += [p.GetPosition() for fp in board.GetFootprints() for p in fp.Pads()
              if p.GetNetCode() == code and p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH]
    for q in links:
        hit = [i for i, (L, s) in enumerate(isl) if s.Contains(q)]
        for i in hit[1:]:
            parent[find(i)] = find(hit[0])
    groups = {}
    for i in range(len(isl)):
        groups.setdefault(find(i), []).append(i)
    main = max(groups.values(), key=lambda g: sum(isl[i][1].Area() for i in g))
    items = copper_items(board); added = 0
    for g in groups.values():
        if g is main:
            continue
        done = False
        for i in g:
            L, s = isl[i]
            others = [isl[j][1] for j in range(len(isl)) if isl[j][0] != L and find(j) != find(i)]
            bb = s.BBox(); y = bb.GetTop()
            while y < bb.GetBottom() and not done:
                x = bb.GetLeft()
                while x < bb.GetRight():
                    p = pcbnew.VECTOR2I(int(x), int(y))
                    if s.Contains(p) and any(o.Contains(p) for o in others) and holes_ok(board, p) and \
                            free(board, items, p, MM(VIA_D) / 2, [pcbnew.F_Cu, pcbnew.B_Cu], code):
                        items.append(add_via(board, net, p)); added += 1; done = True; break
                    x += MM(step)
                y += MM(step)
            if done:
                break
    return added, len(groups) - 1


HEADER_A = ['PB12', 'PB13', 'PB14', 'PB15', 'PA8', 'PA9', 'PA10', 'PA11', 'PA12', 'PA15', 'PB3', 'PB4', 'PB5',
            'PB6', 'PB7', 'PB8', 'PB9', '5V', 'GND', '3V3']
HEADER_B = ['VB', 'PC13', 'PC14', 'PC15', 'PA0', 'PA1', 'PA2', 'PA3', 'PA4', 'PA5', 'PA6', 'PA7', 'PB0', 'PB1',
            'PB10', 'PB11', 'RST', '3V3', 'GND', 'GND']


def silk(board):
    if board.FindFootprintByReference('U5') is not None:   # Rev C RC-car controller
        return silk_revc(board)
    return silk_revb(board)


def silk_revc(board):
    """Rev C: top designators hidden; connector functions and pin order on the bottom silkscreen."""
    for d in [d for d in board.GetDrawings() if d.GetLayer() == pcbnew.B_SilkS]:
        board.Delete(d)
    for fp in board.GetFootprints():
        fp.Reference().SetVisible(False)
    fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
    def text(s, x, y, rot=0, h=0.8):
        t = pcbnew.PCB_TEXT(board); t.SetText(s); t.SetLayer(pcbnew.B_SilkS); t.SetMirrored(True)
        t.SetTextSize(pcbnew.VECTOR2I(MM(h), MM(h))); t.SetTextThickness(MM(0.15))
        t.SetPosition(pcbnew.VECTOR2I(x, y)); t.SetTextAngleDegrees(rot)
        t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER); t.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
        board.Add(t)
    def under(ref, s, dy=8.8):   # below a vertical pin header (pin 1 at the top)
        q = fps[ref].GetPosition(); text(s, q.x, q.y + MM(dy))
    for i in range(4): under('J%d' % (4 + i), 'S%d' % (i + 1))
    for i in range(3): under('J%d' % (8 + i), 'R%d' % (i + 1))
    under('J11', 'L1', 6.3); under('J12', 'L2', 6.3)
    q = fps['J4'].GetPosition(); text('S', q.x - MM(2.2), q.y); text('+', q.x - MM(2.2), q.y + MM(2.54))
    text('-', q.x - MM(2.2), q.y + MM(5.08))
    q = fps['J15'].GetPosition()
    for i, s in enumerate(('GND', '5V', 'TX', 'RX')):
        text(s, q.x - MM(3.0), q.y + MM(2.54 * i), 0, 0.8)
    box = board.GetBoardEdgesBoundingBox()
    q = fps['J1'].GetPosition(); text('- BATT +', q.x + MM(2.5), q.y - MM(4.2))
    text('2S-3S LiPo', q.x + MM(2.5), q.y + MM(4.2))
    q = fps['J3'].GetPosition(); text('MOTOR', q.x + MM(1.75), q.y - MM(5.0))
    for s, ref in (('SWD', 'J13'), ('QWIIC', 'J14'), ('USB-C', 'J2'), ('BOOT0', 'SW1'), ('RESET', 'SW2'),
                   ('EXPANSION', 'J16')):
        q = fps[ref].GetPosition()
        if ref == 'J16':
            text(s, q.x + MM(1.27), q.y + MM(12.2))
        else:
            text(s, q.x, q.y)
    text('STM32 RC controller Rev C', box.GetCenter().x - MM(2), box.GetCenter().y, 0, 1.0)


def silk_revb(board):
    """Top designators hidden (board too dense); pinout and labels printed on the bottom silkscreen."""
    for d in [d for d in board.GetDrawings() if d.GetLayer() == pcbnew.B_SilkS]:
        board.Delete(d)
    for fp in board.GetFootprints():
        fp.Reference().SetVisible(False)
    def text(s, x, y, rot=0, h=0.8):
        t = pcbnew.PCB_TEXT(board); t.SetText(s); t.SetLayer(pcbnew.B_SilkS); t.SetMirrored(True)
        t.SetTextSize(pcbnew.VECTOR2I(MM(h), MM(h))); t.SetTextThickness(MM(0.15))
        t.SetPosition(pcbnew.VECTOR2I(x, y)); t.SetTextAngleDegrees(rot)
        t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER); t.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
        board.Add(t)
    fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
    for ref, names, sign in (('J6', HEADER_B, 1), ('J5', HEADER_A, -1)):   # J6 top row, J5 bottom row
        for p in fps[ref].Pads():
            q = p.GetPosition(); n = names[int(p.GetNumber()) - 1]
            text(n, q.x, q.y + sign * MM(1.25 + 0.42 * len(n) + 0.3), 90)
    box = board.GetBoardEdgesBoundingBox(); cy = box.GetCenter().y
    text('STM32F103 Rev B  Blue-Pill pinout', box.GetCenter().x - MM(10), cy, 0, 1.0)
    q = fps['SW1'].GetPosition(); text('BOOT0', q.x, cy - MM(1.4))
    q = fps['SW2'].GetPosition(); text('RESET', q.x, cy + MM(1.4))
    q = fps['J3'].GetPosition(); text('SWD', q.x - MM(1.9), cy, 90)
    for s, ref in (('DEBUG', 'J2'), ('QWIIC', 'J4'), ('USB-C', 'J1')):
        q = fps[ref].GetPosition(); text(s, q.x, q.y)


def gnd(board):
    net = gnd_net(board)
    for z in list(board.Zones()):
        board.Delete(z)
    for L in (pcbnew.F_Cu,) + INNER + (pcbnew.B_Cu,):
        add_zone(board, L, net, 0)
    fill(board)
    items = copper_items(board)
    missing = []
    for p in unconnected_gnd_pads(board):
        if not (via_for_pad(board, p, items) or link_to_gnd(board, p, items)):
            missing.append('%s-%s' % (p.GetParentFootprint().GetReference(), p.GetNumber()))
    stitched = stitch_edges(board)
    fill(board)
    for _ in range(4):   # merging two orphans may still leave them apart from the main plane
        islands = stitch_islands(board)
        fill(board)
        if islands[0] == 0:
            break
    print('orphan GND islands / vias added:', islands[1], '/', islands[0])
    print('stitching vias:', stitched, '| GND pads without via:', missing)


if __name__ == '__main__':
    cmd, path = sys.argv[1], sys.argv[2]
    board = pcbnew.LoadBoard(path)
    if cmd == 'dsn':
        export_dsn(board, sys.argv[3]); sys.exit(0)
    if cmd == 'ses':
        assert pcbnew.ImportSpecctraSES(board, sys.argv[3])
        setup_layers(board)
        print('widened narrow tracks:', fix_narrow_tracks(board))
        for v in board.GetTracks():   # undo the 0.7 mm keep-out model
            if isinstance(v, pcbnew.PCB_VIA) and v.GetWidth(pcbnew.F_Cu) == MM(0.7):
                v.SetWidth(MM(VIA_D))
    elif cmd == 'silk':
        silk(board)
    elif cmd == 'gnd':
        gnd(board)
    board.Save(path)
