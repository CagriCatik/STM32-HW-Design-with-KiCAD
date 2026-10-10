"""Generate the Rev B hierarchical schematic for stm32_prototype from a declarative part list.
Every pin gets a short wire stub and a label / power symbol / no-connect at its end, so the
connectivity is fully defined by the `conns` maps below and can be verified via netlist export."""
import math, uuid, sys, os
import sexp, libsym
from sexp import Q

G = 2.54
PROJECT = 'stm32_prototype'
ROOT_UUID = 'be055fee-c3a5-4e5c-a361-2a24d1729bc4'
POWER_NETS = {'+3V3': '+3V3', '+5V': '+5V', 'GND': 'GND', 'VBUS': 'VBUS'}
OUT = sys.argv[1]

def U(): return str(uuid.uuid4())
def f(v): return ('%.4f' % v).rstrip('0').rstrip('.')

FP_R = 'Resistor_SMD:R_0603_1608Metric'
FP_C = 'Capacitor_SMD:C_0603_1608Metric'

# ----------------------------------------------------------------------------------------
class Part:
    def __init__(s, sheet, prefix, lib, sym, value, fp, lcsc, mpn, at, rot=0, conns=None, dnp=False, desc=''):
        s.sheet, s.prefix, s.lib, s.sym, s.value, s.fp, s.lcsc, s.mpn = sheet, prefix, lib, sym, value, fp, lcsc, mpn
        s.at = (at[0] * G, at[1] * G); s.rot = rot; s.conns = conns or {}; s.dnp = dnp; s.desc = desc
        s.ref = None

PARTS = []
def P(*a, **k):
    p = Part(*a, **k); PARTS.append(p); return p
def R(sheet, val, lcsc, mpn, at, n1, n2, rot=0, dnp=False):
    return P(sheet, 'R', 'Device', 'R', val, FP_R, lcsc, mpn, at, rot, {'1': n1, '2': n2}, dnp)
def C(sheet, val, lcsc, mpn, at, n1, n2='GND', rot=0, dnp=False):
    return P(sheet, 'C', 'Device', 'C', val, FP_C, lcsc, mpn, at, rot, {'1': n1, '2': n2}, dnp)
def FLAG(sheet, at, net):
    return P(sheet, '#FLG', 'power', 'PWR_FLAG', 'PWR_FLAG', '', '', '', at, 0, {'1': net})

C100N = ('100n', 'C14663', 'CC0603KRX7R9BB104')
C1U = ('1u', 'C15849', 'CL10A105KB8NNNC')
C10U = ('10u', 'C19702', 'CL10A106KP8NNNC')
C4U7 = ('4.7u', 'C19666', 'CL10A475KO8NNNC')
C10N = ('10n', 'C57112', '0603B103K500NT')
C15P = ('15p', 'C1644', 'CL10C150JB8NNNC')
C4P7 = ('4.7p', 'C1669', '0603CG4R7C500NT')
C4N7 = ('4.7n', 'C53987', '0603B472K500NT')
R10K = ('10k', 'C25804', '0603WAF1002T5E')
R5K1 = ('5.1k', 'C23186', '0603WAF5101T5E')
R1K5 = ('1.5k', 'C22843', '0603WAF1501T5E')
R4K7 = ('4.7k', 'C23162', '0603WAF4701T5E')
R1K = ('1k', 'C21190', '0603WAF1001T5E')
R1M = ('1M', 'C22935', '0603WAF1004T5E')
R0 = ('0R', 'C21189', '0603WAF0000T5E')

# ---------------------------------------------------------------- MCU sheet (A3)
S = 'mcu'
mcu_pins = {n['name']: [] for n in libsym.pins(libsym.flat('MCU_ST_STM32F1', 'STM32F103C8Tx'))}
for n in libsym.pins(libsym.flat('MCU_ST_STM32F1', 'STM32F103C8Tx')):
    mcu_pins[n['name']].append(n['num'])
special = {'VDD': '+3V3', 'VSS': 'GND', 'VSSA': 'GND', 'VDDA': 'VDDA', 'VBAT': 'VBAT', 'NRST': 'NRST',
           'BOOT0': 'BOOT0', 'PB2': 'BOOT1', 'PD0': 'HSE_IN', 'PD1': 'HSE_OUT', 'PA13': 'SWDIO',
           'PA14': 'SWCLK', 'PB3': 'SWO', 'PB6': 'I2C_SCL', 'PB7': 'I2C_SDA'}
u1 = {}
for name, nums in mcu_pins.items():
    for num in nums:
        u1[num] = special.get(name, name)  # remaining GPIOs: net named after the pin
P(S, 'U', 'MCU_ST_STM32F1', 'STM32F103C8Tx', 'STM32F103C8T6', 'Package_QFP:LQFP-48_7x7mm_P0.5mm',
  'C8734', 'STM32F103C8T6', (80, 58), 0, u1)
# decoupling: one 100n per VDD pin + bulk, VBAT
for i in range(3):
    C(S, *C100N, (20 + 5 * i, 95), '+3V3')
C(S, *C4U7, (35, 95), '+3V3')
C(S, *C100N, (45, 95), 'VBAT')
P(S, 'JP', 'Jumper', 'SolderJumper_2_Bridged', 'VBAT=3V3', 'Jumper:SolderJumper-2_P1.3mm_Bridged_RoundedPad1.0x1.5mm',
  '', '', (52, 90), 0, {'1': '+3V3', '2': 'VBAT'})
FLAG(S, (60, 95), 'VBAT')
# VDDA filter: FB1 from +3V3 to VDDA, 10n + 1u on VDDA
P(S, 'FB', 'Device', 'FerriteBead', '600R@100MHz', 'Inductor_SMD:L_0603_1608Metric', 'C1002', 'GZ1608D601TF',
  (20, 75), 0, {'1': '+3V3', '2': 'VDDA'})
C(S, *C10N, (27, 75), 'VDDA')
C(S, *C1U, (33, 75), 'VDDA')
FLAG(S, (39, 75), 'VDDA')
# HSE 8 MHz, CL = 12 pF -> C = 2*(12-4) = 16 pF -> 15 pF
P(S, 'Y', 'Device', 'Crystal_GND24', '8MHz', 'Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm', 'C2682775', 'X32258MOB4SI',
  (25, 22), 0, {'1': 'HSE_IN', '3': 'HSE_OUT', '2': 'GND', '4': 'GND'})
C(S, *C15P, (19, 30), 'HSE_IN')
C(S, *C15P, (31, 30), 'HSE_OUT')
# LSE 32.768 kHz (optional, DNP), CL = 6 pF
P(S, 'Y', 'Device', 'Crystal', '32.768kHz', 'Crystal:Crystal_SMD_3215-2Pin_3.2x1.5mm', 'C95361', 'Q13FC13500049',
  (25, 45), 0, {'1': 'PC14', '2': 'PC15'}, dnp=True)
C(S, *C4P7, (19, 53), 'PC14', dnp=True)
C(S, *C4P7, (31, 53), 'PC15', dnp=True)
# BOOT0: 10k pull-down + push button to 3V3; BOOT1 (PB2) 10k pull-down
R(S, *R10K, (125, 25), 'BOOT0', 'GND')
P(S, 'SW', 'Switch', 'SW_Push', 'BOOT0', 'Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A', 'C318884', 'TS-1187A-B-A-B',
  (135, 18), 0, {'1': '+3V3', '2': 'BOOT0'})
R(S, *R10K, (145, 25), 'BOOT1', 'GND')
# NRST: 100n + reset button
C(S, *C100N, (125, 45), 'NRST')
P(S, 'SW', 'Switch', 'SW_Push', 'RESET', 'Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A', 'C318884', 'TS-1187A-B-A-B',
  (135, 40), 0, {'1': 'NRST', '2': 'GND'})
# User LED on PC13, low-active: 3V3 -> 1k -> LED -> PC13 (~1.3 mA)
R(S, *R1K, (125, 65), '+3V3', 'LED_USER_A', rot=90)
P(S, 'D', 'Device', 'LED', 'red', 'LED_SMD:LED_0603_1608Metric', 'C2286', 'KT-0603R',
  (135, 65), 180, {'2': 'LED_USER_A', '1': 'PC13'})
# USB series resistors (0R default, 22R optional) and 1.5k D+ pull-up
R(S, *R0, (125, 82), 'USB_D+', 'PA12', rot=90)
R(S, *R0, (125, 90), 'USB_D-', 'PA11', rot=90)
R(S, *R1K5, (140, 88), '+3V3', 'PA12')

# ---------------------------------------------------------------- Power / USB sheet (A4)
S = 'power_usb'
P(S, 'J', 'Connector', 'USB_C_Receptacle_USB2.0_16P', 'USB-C', 'Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12',
  'C165948', 'TYPE-C-31-M-12', (20, 40), 0,
  {'A4': 'VBUS', 'A9': 'VBUS', 'B4': 'VBUS', 'B9': 'VBUS', 'A1': 'GND', 'A12': 'GND', 'B1': 'GND', 'B12': 'GND',
   'A5': 'CC1', 'B5': 'CC2', 'A6': 'USB_D+', 'B6': 'USB_D+', 'A7': 'USB_D-', 'B7': 'USB_D-',
   'A8': 'NC', 'B8': 'NC', 'SH': 'USB_SHIELD'})
R(S, *R5K1, (36, 22), 'CC1', 'GND')
R(S, *R5K1, (41, 22), 'CC2', 'GND')
R(S, *R1M, (10, 60), 'USB_SHIELD', 'GND')
C(S, *C4N7, (14, 60), 'USB_SHIELD')
P(S, 'U', 'Power_Protection', 'USBLC6-2SC6', 'USBLC6-2SC6', 'Package_TO_SOT_SMD:SOT-23-6', 'C7519', 'USBLC6-2SC6',
  (55, 42), 0, {'1': 'USB_D+', '6': 'USB_D+', '3': 'USB_D-', '4': 'USB_D-', '5': 'VBUS', '2': 'GND'})
P(S, 'F', 'Device', 'Polyfuse', '500mA', 'Fuse:Fuse_1206_3216Metric', 'C70077', 'nSMD050-33V',
  (60, 15), 0, {'1': 'VBUS', '2': 'VBUS_F'})
P(S, 'D', 'Device', 'D_Schottky', 'B5819W', 'Diode_SMD:D_SOD-123', 'C8598', 'B5819W SL',
  (68, 22), 180, {'2': 'VBUS_F', '1': '+5V'})
P(S, 'U', 'Regulator_Linear', 'AP2112K-3.3', 'AP2112K-3.3', 'Package_TO_SOT_SMD:SOT-23-5', 'C51118', 'AP2112K-3.3TRG1',
  (90, 22), 0, {'1': '+5V', '3': '+5V', '2': 'GND', '5': '+3V3'})
C(S, *C1U, (80, 30), '+5V')
C(S, *C1U, (100, 30), '+3V3')
C(S, *C10U, (105, 30), '+3V3')
R(S, *R1K, (90, 50), '+3V3', 'LED_PWR_A')
P(S, 'D', 'Device', 'LED', 'red', 'LED_SMD:LED_0603_1608Metric', 'C2286', 'KT-0603R',
  (98, 58), 180, {'2': 'LED_PWR_A', '1': 'GND'})
FLAG(S, (60, 62), 'VBUS')
FLAG(S, (66, 62), '+5V')
FLAG(S, (72, 62), 'GND')

# ---------------------------------------------------------------- Connectors sheet (A4)
S = 'connectors'
P(S, 'J', 'Connector', 'Conn_ARM_JTAG_SWD_10', 'Cortex-Debug', 'Connector_PinHeader_1.27mm:PinHeader_2x05_P1.27mm_Vertical_SMD',
  'C2935458', 'PZ127VS-12-10-H10-A38', (20, 25), 0,
  {'1': '+3V3', '2': 'SWDIO', '3': 'GND', '4': 'SWCLK', '5': 'GND', '6': 'SWO', '8': 'NC', '9': 'GND', '10': 'NRST'})
P(S, 'J', 'Connector_Generic', 'Conn_01x04', 'SWD', 'Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical',
  'C2691448', 'PZ254V-11-04P', (20, 55), 0, {'1': '+3V3', '2': 'SWDIO', '3': 'SWCLK', '4': 'GND'})
P(S, 'J', 'Connector_Generic', 'Conn_01x04', 'Qwiic', 'Connector_JST:JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal',
  'C160404', 'SM04B-SRSS-TB(LF)(SN)', (50, 25), 0, {'1': 'GND', '2': '+3V3', '3': 'I2C_SDA', '4': 'I2C_SCL'})
P(S, 'JP', 'Jumper', 'SolderJumper_2_Bridged', 'I2C_PU', 'Jumper:SolderJumper-2_P1.3mm_Bridged_RoundedPad1.0x1.5mm',
  '', '', (50, 45), 0, {'1': '+3V3', '2': 'I2C_PU'})
R(S, *R4K7, (58, 52), 'I2C_PU', 'I2C_SDA')
R(S, *R4K7, (64, 52), 'I2C_PU', 'I2C_SCL')
BP_A = ['PB12', 'PB13', 'PB14', 'PB15', 'PA8', 'PA9', 'PA10', 'PA11', 'PA12', 'PA15', 'SWO', 'PB4', 'PB5',
        'I2C_SCL', 'I2C_SDA', 'PB8', 'PB9', '+5V', 'GND', '+3V3']
BP_B = ['VBAT', 'PC13', 'PC14', 'PC15', 'PA0', 'PA1', 'PA2', 'PA3', 'PA4', 'PA5', 'PA6', 'PA7', 'PB0', 'PB1',
        'PB10', 'PB11', 'NRST', '+3V3', 'GND', 'GND']
P(S, 'J', 'Connector_Generic', 'Conn_01x20', 'Header_A', 'Connector_PinHeader_2.54mm:PinHeader_1x20_P2.54mm_Vertical',
  'C22465880', 'PZ254V-11-20P', (85, 40), 0, {str(i + 1): n for i, n in enumerate(BP_A)}, dnp=True)
P(S, 'J', 'Connector_Generic', 'Conn_01x20', 'Header_B', 'Connector_PinHeader_2.54mm:PinHeader_1x20_P2.54mm_Vertical',
  'C22465880', 'PZ254V-11-20P', (105, 40), 0, {str(i + 1): n for i, n in enumerate(BP_B)}, dnp=True)

NOTES = {
 'mcu': [((10, 108), 'HSE: X32258MOB4SI 8 MHz, C_L = 12 pF. C1 = C2 = 2*(C_L - C_stray) = 2*(12 pF - 4 pF) = 16 pF -> 15 pF C0G.\n'
                     'LSE (DNP): Q13FC13500049 32.768 kHz, C_L = 6 pF -> 2*(6 pF - 4 pF) = 4 pF -> 4.7 pF C0G. C_stray ~ 3-5 pF, verify on bring-up.\n'
                     'USB: 0R series resistors (replace with 22R if needed). 1.5k D+ pull-up to 3V3 (F103 has no internal pull-up).\n'
                     'VBAT tied to 3V3 via solder jumper (cut to run VBAT from a coin cell on the header pin).\n'
                     'User LED on PC13 is low-active (~1.3 mA).')],
 'power_usb': [((10, 75), 'USB-C device, 5 V only: CC1/CC2 each 5.1k to GND (separate resistors). SBU unused.\n'
                          'Shield to GND via 1M || 4.7n. ESD: USBLC6-2SC6 directly behind the connector.\n'
                          'VBUS -> 500 mA PTC -> B5819W -> +5V (diode blocks back-feed from the header 5V pin into the host).\n'
                          'AP2112K-3.3: 600 mA, EN tied to VIN, 1u in / 1u + 10u out (ceramic stable).')],
 'connectors': [((10, 70), 'Blue-Pill compatible headers, 2x 1x20, 2.54 mm, row spacing 15.24 mm. Shipped loose (DNP for assembly).\n'
                           'Header_A: ' + ' '.join(n for n in BP_A) + '\n'
                           'Header_B: ' + ' '.join(n for n in BP_B) + '\n'
                           'Qwiic (JST-SH): 1 GND, 2 3V3, 3 SDA (PB7), 4 SCL (PB6). 4.7k pull-ups, cut JP to remove.\n'
                           'Cortex-Debug 10-pin: VTref, SWDIO (PA13), SWCLK (PA14), SWO (PB3), nRESET. SWD 1x4: 3V3 SWDIO SWCLK GND.')],
}
SHEETS = [('mcu', 'MCU', 'A3', 2), ('power_usb', 'Power_USB', 'A4', 3), ('connectors', 'Connectors', 'A4', 4)]
SHEET_UUID = {s: U() for s, *_ in SHEETS}

# ---------------------------------------------------------------- annotation
counters = {}
for sheet, *_ in SHEETS:
    for p in PARTS:
        if p.sheet != sheet: continue
        counters[p.prefix] = counters.get(p.prefix, 0) + 1
        p.ref = '%s%d' % (p.prefix, counters[p.prefix])

# ---------------------------------------------------------------- geometry
def rot(x, y, r):
    a = math.radians(r); return (x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a))
def pin_geo(p, pin):
    rx, ry = rot(pin['x'], pin['y'], p.rot)
    pt = (round(p.at[0] + rx, 2), round(p.at[1] - ry, 2))
    ox, oy = rot(-math.cos(math.radians(pin['a'])), -math.sin(math.radians(pin['a'])), p.rot)
    d = (round(ox), round(-oy))
    return pt, d
DIR_ANGLE = {(1, 0): 0, (0, -1): 90, (-1, 0): 180, (0, 1): 270}
GND_ROT = {(0, 1): 0, (1, 0): 90, (0, -1): 180, (-1, 0): 270}
UP_ROT = {(0, -1): 0, (-1, 0): 90, (0, 1): 180, (1, 0): 270}

net_sheets = {}
for p in PARTS:
    for n in p.conns.values(): net_sheets.setdefault(n, set()).add(p.sheet)

def eff(hide=False, justify=None):
    e = ['effects', ['font', ['size', '1.27', '1.27']]]
    if justify: e.append(['justify'] + justify)
    if hide: e.append(['hide', 'yes'])
    return e
def prop(name, val, at, hide=False, ang=0):
    return ['property', Q(name), Q(val), ['at', f(at[0]), f(at[1]), str(ang)], eff(hide)]

pwr_count = [0]
def power_sym(net, pt, d, sheet_items, sheet_path, libs):
    sym = POWER_NETS[net]
    r = GND_ROT[d] if net == 'GND' else UP_ROT[d]
    pwr_count[0] += 1
    return symbol_inst('power', sym, '#PWR%02d' % pwr_count[0], net, pt, r, {'1'}, sheet_path, libs,
                       extra=[], hide_ref=True)

def symbol_inst(lib, sym, ref, value, at, r, pinnums, sheet_path, libs, extra=(), fp='', dnp=False, hide_ref=False,
                lcsc=None, mpn=None):
    libs.add((lib, sym))
    n = ['symbol', ['lib_id', Q('%s:%s' % (lib, sym))], ['at', f(at[0]), f(at[1]), str(r)], ['unit', '1'],
         ['exclude_from_sim', 'no'], ['in_bom', 'no' if (ref.startswith('#') or lcsc == '') else 'yes'],
         ['on_board', 'no' if ref.startswith('#') else 'yes'], ['dnp', 'yes' if dnp else 'no'], ['uuid', Q(U())],
         ['property', Q('Reference'), Q(ref), ['at', f(at[0] + 2.54), f(at[1] - 1.27), '0'], eff(hide_ref, ['left'])],
         ['property', Q('Value'), Q(value), ['at', f(at[0] + 2.54), f(at[1] + 1.27), '0'], eff(False, ['left'])],
         prop('Footprint', fp, at, True), prop('Datasheet', '', at, True), prop('Description', '', at, True)]
    if lcsc is not None: n.append(prop('LCSC', lcsc, at, True))
    if mpn is not None: n.append(prop('MPN', mpn, at, True))
    for pn in sorted(pinnums): n.append(['pin', Q(pn), ['uuid', Q(U())]])
    n.append(['instances', ['project', Q(PROJECT), ['path', Q(sheet_path), ['reference', Q(ref)], ['unit', '1']]]])
    return n

def lib_symbols(libs):
    out = ['lib_symbols']
    for lib, sym in sorted(libs):
        node = libsym.flat(lib, sym)
        out.append(['symbol', Q('%s:%s' % (lib, sym))] + node[2:])
    return out

def build_sheet(sheet, paper):
    items, libs = [], set()
    path = '/%s/%s' % (ROOT_UUID, SHEET_UUID[sheet])
    for p in [p for p in PARTS if p.sheet == sheet]:
        pins = libsym.pins(libsym.flat(p.lib, p.sym))
        nums = {pin['num'] for pin in pins}
        unknown = set(p.conns) - nums
        assert not unknown, (p.ref, unknown)
        items.append(symbol_inst(p.lib, p.sym, p.ref, p.value, p.at, p.rot, nums, path, libs, fp=p.fp, dnp=p.dnp,
                                 hide_ref=p.ref.startswith('#'), lcsc=None if p.ref.startswith('#') else p.lcsc,
                                 mpn=None if p.ref.startswith('#') else p.mpn))
        done = {}
        for pin in pins:
            if pin['num'] not in p.conns:
                assert pin['etype'] == 'no_connect', ('unassigned pin', p.ref, pin['num'], pin['name'])
                continue
            net = p.conns[pin['num']]
            pt, d = pin_geo(p, pin)
            if pt in done:
                assert done[pt] == net, ('stacked pin conflict', p.ref, pin['num']); continue
            done[pt] = net
            if net == 'NC':
                items.append(['no_connect', ['at', f(pt[0]), f(pt[1])], ['uuid', Q(U())]]); continue
            end = (round(pt[0] + d[0] * 2 * G, 2), round(pt[1] + d[1] * 2 * G, 2))
            items.append(['wire', ['pts', ['xy', f(pt[0]), f(pt[1])], ['xy', f(end[0]), f(end[1])]],
                          ['stroke', ['width', '0'], ['type', 'default']], ['uuid', Q(U())]])
            if net in POWER_NETS:
                items.append(power_sym(net, end, d, items, path, libs))
            else:
                ang = DIR_ANGLE[d]
                just = ['right'] if ang in (180, 270) else ['left']
                if len(net_sheets[net]) > 1:
                    items.append(['global_label', Q(net), ['shape', 'bidirectional'],
                                  ['at', f(end[0]), f(end[1]), str(ang)], ['fields_autoplaced', 'yes'], eff(justify=just),
                                  ['uuid', Q(U())],
                                  ['property', Q('Intersheetrefs'), Q('${INTERSHEET_REFS}'),
                                   ['at', f(end[0]), f(end[1]), '0'], eff(hide=True)]])
                else:
                    items.append(['label', Q(net), ['at', f(end[0]), f(end[1]), str(ang)], ['fields_autoplaced', 'yes'],
                                  eff(justify=just + ['bottom']), ['uuid', Q(U())]])
    for (gx, gy), text in NOTES.get(sheet, []):
        items.append(['text', Q(text.replace('\n', '\\n')), ['exclude_from_sim', 'no'], ['at', f(gx * G), f(gy * G), '0'],
                      eff(justify=['left', 'top']), ['uuid', Q(U())]])
    title = dict(SHEETS_TITLES)[sheet]
    doc = ['kicad_sch', ['version', '20250114'], ['generator', Q('eeschema')], ['generator_version', Q('9.0')],
           ['uuid', Q(SHEET_FILE_UUID[sheet])], ['paper', Q(paper)],
           ['title_block', ['title', Q(title)], ['date', Q('2026-10-10')], ['rev', Q('B')], ['company', Q('Cagri Catik')]],
           lib_symbols(libs)] + items + [['embedded_fonts', 'no']]
    return doc

SHEETS_TITLES = [('mcu', 'STM32F103C8T6 core'), ('power_usb', 'USB-C and power supply'), ('connectors', 'Connectors')]
SHEET_FILE_UUID = {s: U() for s, *_ in SHEETS}

def build_root():
    items = []
    for i, (s, name, paper, page) in enumerate(SHEETS):
        x, y, w, h = 40 + i * 60, 50, 40, 25
        items.append(['sheet', ['at', f(x), f(y)], ['size', f(w), f(h)], ['exclude_from_sim', 'no'], ['in_bom', 'yes'],
                      ['on_board', 'yes'], ['dnp', 'no'], ['fields_autoplaced', 'yes'],
                      ['stroke', ['width', '0.1524'], ['type', 'solid']], ['fill', ['color', '0', '0', '0', '0.0000']],
                      ['uuid', Q(SHEET_UUID[s])],
                      ['property', Q('Sheetname'), Q(name), ['at', f(x), f(y - 0.7), '0'], eff(justify=['left', 'bottom'])],
                      ['property', Q('Sheetfile'), Q(s + '.kicad_sch'), ['at', f(x), f(y + h + 0.6), '0'],
                       eff(justify=['left', 'top'])],
                      ['instances', ['project', Q(PROJECT), ['path', Q('/' + ROOT_UUID), ['page', Q(str(page))]]]]])
    note = ('STM32 Prototype Rev B (Blue-Pill compatible)\\n'
            'D1 STM32F103C8T6 | D2 USB-C 2.0 device | D3 AP2112K-3.3 | D4 USBLC6-2SC6 + 500 mA PTC\\n'
            'D5 Cortex-Debug 10-pin + SWD 1x4 | D6 Qwiic I2C1 (PB6/PB7) 4.7k | D7 RESET + BOOT0 buttons\\n'
            'D8 power LED + PC13 user LED | D9 LSE 32.768 kHz (DNP) | D10 Blue-Pill format | D11 2 layers 1.6 mm\\n'
            'D12 0603, JLC basic parts preferred | D13 JLCPCB assembly, LCSC field on every part')
    items.append(['text', Q(note), ['exclude_from_sim', 'no'], ['at', '40', '100', '0'], eff(justify=['left', 'top']),
                  ['uuid', Q(U())]])
    return ['kicad_sch', ['version', '20250114'], ['generator', Q('eeschema')], ['generator_version', Q('9.0')],
            ['uuid', Q(ROOT_UUID)], ['paper', Q('A4')],
            ['title_block', ['title', Q('STM32 Prototype (Blue Pill) Rev B')], ['date', Q('2026-10-10')], ['rev', Q('B')],
             ['company', Q('Cagri Catik')]],
            ['lib_symbols']] + items + [['sheet_instances', ['path', Q('/'), ['page', Q('1')]]], ['embedded_fonts', 'no']]

os.makedirs(OUT, exist_ok=True)
for s, name, paper, page in SHEETS:
    open(os.path.join(OUT, s + '.kicad_sch'), 'w').write(sexp.dump(build_sheet(s, paper)) + '\n')
open(os.path.join(OUT, PROJECT + '.kicad_sch'), 'w').write(sexp.dump(build_root()) + '\n')

# expected netlist for verification
import json
exp = {}
for p in PARTS:
    if p.ref.startswith('#'): continue
    for pin, net in p.conns.items():
        if net != 'NC': exp.setdefault(net, set()).add((p.ref, pin))
json.dump({k: sorted(v) for k, v in exp.items()}, open(os.path.join(OUT, 'expected_nets.json'), 'w'), indent=0)
print('\n'.join('%-5s %-12s %-10s %s%s' % (p.ref, p.value, p.lcsc, p.fp.split(':')[-1], ' DNP' if p.dnp else '')
                for p in PARTS if not p.ref.startswith('#')))
