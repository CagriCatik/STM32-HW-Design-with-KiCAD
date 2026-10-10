#!/bin/zsh
# usage: check.sh <dir>  -> ERC + netlist comparison against expected_nets.json
K=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
D=$1; T=$(dirname $0)
$K sch erc --severity-all --format report -o $D/erc.rpt $D/stm32_prototype.kicad_sch >/dev/null; grep 'ERC messages' $D/erc.rpt; grep -E '^\[' $D/erc.rpt
$K sch export netlist --format kicadsexpr -o $D/new.net $D/stm32_prototype.kicad_sch >/dev/null
cd $T && python3 - $D <<'PY'
import json, sexp, sys
D=sys.argv[1]
exp={k:frozenset(map(tuple,v)) for k,v in json.load(open(D+'/expected_nets.json')).items()}
got={n.split('/')[-1]:frozenset((r,p) for r,p,f in v if not r.startswith('#')) for n,v in sexp.nets(D+'/new.net').items()}
got={k:v for k,v in got.items() if v and not k.startswith('unconnected')}
bad=[k for k,v in exp.items() if got.get(k)!=v]
print('nets: expected',len(exp),'got',len(got),'mismatch',bad)
PY
