#!/usr/bin/env bash
# Phase 5: JLCPCB fabrication + assembly data for stm32_prototype Rev B, using only kicad-cli (+ python3 for CSV).
#   scripts/export_fab.sh [output-dir]      default: stm32_prototype/production/rev-b
# KICAD_CLI may point to another kicad-cli (CI container: plain "kicad-cli").
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
P=$ROOT/stm32_prototype
NAME=stm32_prototype
OUT=${1:-$P/production/rev-b}
K=${KICAD_CLI:-/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli}
[ -x "$K" ] || K=kicad-cli

rm -rf $OUT && mkdir -p $OUT/gerber
PCB=$P/$NAME.kicad_pcb
SCH=$P/$NAME.kicad_sch

# Gerbers (4 layers) + Excellon drill, zipped for upload
$K pcb export gerbers --check-zones --subtract-soldermask \
   -l F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts \
   -o $OUT/gerber $PCB
$K pcb export drill --format excellon --excellon-units mm --excellon-separate-th \
   --generate-map --map-format gerberx2 -o $OUT/gerber/ $PCB
python3 -c "import shutil,sys; shutil.make_archive(sys.argv[1], 'zip', sys.argv[2])" $OUT/${NAME}_rev-b_gerber $OUT/gerber

# BOM in JLC format; DNP parts and solder jumpers (excluded from BOM) are left out
$K sch export bom --exclude-dnp --ref-range-delimiter "" \
   --fields 'Value,Reference,Footprint,LCSC' --labels 'Comment,Designator,Footprint,LCSC Part #' \
   --group-by 'Value,Footprint,LCSC' --sort-field Reference -o $OUT/${NAME}_rev-b_bom.csv $SCH

# Pick & place in JLC format with rotation offsets
$K pcb export pos --format csv --units mm --side both --exclude-dnp -o $OUT/pos_kicad.csv $PCB
python3 - $OUT/pos_kicad.csv $OUT/${NAME}_rev-b_cpl.csv <<'PY'
import csv, re, sys
# JLC's library orientation differs from KiCad's for some packages (values used by the common
# KiCad->JLC tools). Check every one of these in JLC's assembly preview before ordering.
ROT = [(r'^LQFP-', 270), (r'^SOT-23', 180), (r'^SOT-223', 180), (r'^D_SOD-123', 0),
       (r'^USB_C_Receptacle_HRO_TYPE-C-31-M-12', 0), (r'^JST_SH_SM04B', 180)]
rows = list(csv.DictReader(open(sys.argv[1])))
with open(sys.argv[2], 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation'])
    for r in rows:
        if r['Ref'].startswith('JP'):          # solder jumpers are copper only
            continue
        fp = r['Package']; rot = float(r['Rot'])
        for pat, off in ROT:
            if re.match(pat, fp):
                rot = (rot + off) % 360; break
        w.writerow([r['Ref'], r['PosX'] + 'mm', r['PosY'] + 'mm', 'Top' if r['Side'] == 'top' else 'Bottom', '%g' % rot])
PY
rm $OUT/pos_kicad.csv

# Documentation: schematic PDF, 3D renders, STEP
$K sch export pdf -o $OUT/${NAME}_rev-b_schematic.pdf $SCH
$K pcb render --side top --width 2400 --height 1000 --zoom 2.2 --quality high -o $OUT/${NAME}_rev-b_top.png $PCB >/dev/null
$K pcb render --side bottom --width 2400 --height 1000 --zoom 2.2 --quality high -o $OUT/${NAME}_rev-b_bottom.png $PCB >/dev/null
$K pcb export step --subst-models --force -o $OUT/${NAME}_rev-b.step $PCB >/dev/null
echo "fabrication data in $OUT"
