#!/usr/bin/env python3
"""Assign 3D models that KiCad 10 does not ship (run with KiCad's bundled Python).

STEP files from LCSC/EasyEDA (fetched with easyeda2kicad by LCSC number) live in stm32_prototype/3dmodels/;
the offsets align them with KiCad's footprints (measured from the pad positions of both footprints).

  python3 scripts/apply_3d_models.py stm32_prototype/stm32_prototype.kicad_pcb
"""
import sys
import pcbnew

# footprint name: (model path, offset x/y/z in mm, rotation z in degrees)
MODELS = {
    # LCSC C165948; EasyEDA pads sit 1.575 mm lower than KiCad's (3D y axis points up)
    'USB_C_Receptacle_HRO_TYPE-C-31-M-12': ('${KIPRJMOD}/3dmodels/USB-C_HRO_TYPE-C-31-M-12.step', (0, 1.575, 0), 180),
    # LCSC C428721; EasyEDA origin between the pins, KiCad origin on pin 1
    'AMASS_XT30UPB-M_1x02_P5.0mm_Vertical': ('${KIPRJMOD}/3dmodels/XT30UPB-M.step', (2.5, 0, 0), 0),
    # LCSC C318884; same pad geometry, centred
    'SW_Push_1P1T_XKB_TS-1187A': ('${KIPRJMOD}/3dmodels/TS-1187A-B-A-B.step', (0, 0, 0), 0),
    # DRV8870 DDA: KiCad ships the HSOP-8 body under a different file name
    'Texas_HSOP-8-1EP_3.9x4.9mm_P1.27mm_ThermalVias':
        ('${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/HSOP-8-1EP_3.9x4.9mm_P1.27mm_EP2.41x3.1mm.step', (0, 0, 0), 0),
}

def apply(board):
    n = 0
    for fp in board.GetFootprints():
        spec = MODELS.get(str(fp.GetFPID().GetLibItemName()))
        if not spec:
            continue
        path, (x, y, z), rz = spec
        fp.Models().clear()
        m = pcbnew.FP_3DMODEL()
        m.m_Filename = path
        m.m_Offset = pcbnew.VECTOR3D(x, y, z)
        m.m_Rotation = pcbnew.VECTOR3D(0, 0, rz)
        m.m_Scale = pcbnew.VECTOR3D(1, 1, 1)
        fp.Models().push_back(m)
        n += 1
    return n

if __name__ == '__main__':
    b = pcbnew.LoadBoard(sys.argv[1])
    print('3D models assigned:', apply(b))
    b.Save(sys.argv[1])
