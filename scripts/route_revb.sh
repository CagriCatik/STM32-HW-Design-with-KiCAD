#!/bin/zsh
# Phase 4: autoroute stm32_prototype Rev B with Freerouting, convert to 4 layers, GND pours, silkscreen, DRC.
# Needs KiCad 10 and Freerouting 2.5 + Java 25 (FREEROUTING_DIR, default ~/Tools/freerouting).
set -e
ROOT=${0:A:h:h}
B=$ROOT/stm32_prototype/stm32_prototype.kicad_pcb
FR=${FREEROUTING_DIR:-$HOME/Tools/freerouting}
PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
K=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
T=$(mktemp -d)
$PY $ROOT/scripts/route_revb.py dsn $B $T/board.dsn
RULES=(); [ -f $T/board.rules ] && RULES=(-dr $T/board.rules)
$FR/jre/Contents/Home/bin/java -Djava.awt.headless=true -jar $FR/freerouting-2.5.0.jar \
    --gui.enabled=false -de $T/board.dsn $RULES -do $T/board.ses -mp 150 -l en > $T/freerouting.log 2>&1
grep -E 'could not be routed|unrouted connection' $T/freerouting.log || true
$PY $ROOT/scripts/route_revb.py ses $B $T/board.ses
$PY $ROOT/scripts/route_revb.py gnd $B
$PY $ROOT/scripts/route_revb.py silk $B
$K pcb drc --severity-all --schematic-parity --exit-code-violations -o $T/drc.rpt $B
echo "log + report in $T"
