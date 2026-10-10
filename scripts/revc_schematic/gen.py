"""Generate the Rev C (RC-car controller) hierarchical schematic for stm32_prototype from a declarative part list.

Every pin gets a short wire stub and a label / power symbol / no-connect at its end, so connectivity is fully
defined by the `conns` maps below and is verified against the exported netlist (check.sh).
Also writes the project symbol library rcboard.kicad_sym (DRV8870, AO4407A) and sym-lib-table.

  python3 gen.py <out-dir>
"""
import math, uuid, sys, os, json
import sexp, libsym
from sexp import Q

G = 2.54
PROJECT = 'stm32_prototype'
ROOT_UUID = 'be055fee-c3a5-4e5c-a361-2a24d1729bc4'
POWER_NETS = {'+3V3': '+3V3', '+5V': '+5V', 'GND': 'GND', 'VBUS': 'VBUS'}
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

_ns, _n = uuid.UUID('6f1c9a52-3d0e-4c39-9a51-2b7f0c8e4d11'), [0]
def U():
    """Deterministic UUIDs: regenerating the same design keeps symbol/footprint links stable."""
    _n[0] += 1
    return str(uuid.uuid5(_ns, 'revc-%d' % _n[0]))
def f(v): return ('%.4f' % v).rstrip('0').rstrip('.')

FP_R = 'Resistor_SMD:R_0603_1608Metric'
FP_C = 'Capacitor_SMD:C_0603_1608Metric'

# ---------------------------------------------------------------- project symbol library
def box_symbol(name, ref, footprint, datasheet, desc, left=(), right=(), top=(), bottom=(), w=7.62):
    """Simple rectangle symbol. Pin lists: (number, name, electrical type)."""
    h = max(len(left), len(right), 2) * 2.54 / 2 + 2.54
    pins = []
    def pin(num, nm, et, x, y, a):
        pins.append(['pin', et, 'line', ['at', f(x), f(y), str(a)], ['length', '2.54'],
                     ['name', Q(nm), ['effects', ['font', ['size', '1.27', '1.27']]]],
                     ['number', Q(num), ['effects', ['font', ['size', '1.27', '1.27']]]]])
    for i, (num, nm, et) in enumerate(left):
        pin(num, nm, et, -w - 2.54, h - 2.54 - i * 2.54, 0)
    for i, (num, nm, et) in enumerate(right):
        pin(num, nm, et, w + 2.54, h - 2.54 - i * 2.54, 180)
    for i, (num, nm, et) in enumerate(top):
        pin(num, nm, et, -2.54 * (len(top) - 1) / 2 + i * 2.54, h + 2.54, 270)
    for i, (num, nm, et) in enumerate(bottom):
        pin(num, nm, et, -2.54 * (len(bottom) - 1) / 2 + i * 2.54, -h - 2.54, 90)
    def p(k, v, y, hide=False):
        e = ['effects', ['font', ['size', '1.27', '1.27']]]
        if hide: e.append(['hide', 'yes'])
        return ['property', Q(k), Q(v), ['at', '0', f(y), '0'], e]
    return ['symbol', Q(name), ['pin_names', ['offset', '1.016']], ['exclude_from_sim', 'no'], ['in_bom', 'yes'],
            ['on_board', 'yes'], p('Reference', ref, h + 5.08), p('Value', name, -h - 5.08),
            p('Footprint', footprint, 0, True), p('Datasheet', datasheet, 0, True), p('Description', desc, 0, True),
            ['symbol', Q(name + '_0_1'), ['rectangle', ['start', f(-w), f(h)], ['end', f(w), f(-h)],
                                           ['stroke', ['width', '0.254'], ['type', 'default']],
                                           ['fill', ['type', 'background']]]],
            ['symbol', Q(name + '_1_1')] + pins, ['embedded_fonts', 'no']]

RCLIB = ['kicad_symbol_lib', ['version', '20241209'], ['generator', Q('rcboard_gen')], ['generator_version', Q('9.0')],
    box_symbol('DRV8870', 'U', 'Package_SO:Texas_HSOP-8-1EP_3.9x4.9mm_P1.27mm_ThermalVias',
               'https://www.ti.com/lit/ds/symlink/drv8870.pdf', '3.6 A brushed DC motor driver, 6.5-45 V, current regulation',
               left=[('5', 'VM', 'power_in'), ('3', 'IN1', 'input'), ('2', 'IN2', 'input'), ('4', 'VREF', 'input')],
               right=[('6', 'OUT1', 'output'), ('8', 'OUT2', 'output'), ('7', 'ISEN', 'passive')],
               bottom=[('1', 'GND', 'power_in'), ('9', 'EP', 'passive')]),
    box_symbol('AO4407A', 'Q', 'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',
               'https://www.aosmd.com/pdfs/datasheet/AO4407A.pdf', '-30 V -12 A P-channel MOSFET, SO-8',
               left=[('4', 'G', 'input')], top=[('5', 'D', 'passive'), ('6', 'D', 'passive'), ('7', 'D', 'passive'),
                                                ('8', 'D', 'passive')],
               bottom=[('1', 'S', 'passive'), ('2', 'S', 'passive'), ('3', 'S', 'passive')], w=5.08),
]
open(os.path.join(OUT, 'rcboard.kicad_sym'), 'w').write(sexp.dump(RCLIB) + '\n')
open(os.path.join(OUT, 'sym-lib-table'), 'w').write(
    '(sym_lib_table\n  (version 7)\n  (lib (name "rcboard")(type "KiCad")(uri "${KIPRJMOD}/rcboard.kicad_sym")'
    '(options "")(descr "RC controller board symbols"))\n)\n')
libsym.EXTRA['rcboard'] = os.path.join(OUT, 'rcboard.kicad_sym')

# ---------------------------------------------------------------- part model
class Part:
    def __init__(s, sheet, prefix, lib, sym, value, fp, lcsc, mpn, at, rot=0, conns=None, dnp=False):
        s.sheet, s.prefix, s.lib, s.sym, s.value, s.fp, s.lcsc, s.mpn = sheet, prefix, lib, sym, value, fp, lcsc, mpn
        s.at = (at[0] * G, at[1] * G); s.rot = rot; s.conns = conns or {}; s.dnp = dnp
        s.ref = None

PARTS = []
def P(*a, **k):
    p = Part(*a, **k); PARTS.append(p); return p
def R(sheet, val, lcsc, mpn, at, n1, n2, rot=0, dnp=False, fp=FP_R):
    return P(sheet, 'R', 'Device', 'R', val, fp, lcsc, mpn, at, rot, {'1': n1, '2': n2}, dnp)
def C(sheet, val, lcsc, mpn, at, n1, n2='GND', rot=0, dnp=False, fp=FP_C):
    return P(sheet, 'C', 'Device', 'C', val, fp, lcsc, mpn, at, rot, {'1': n1, '2': n2}, dnp)
def CP(sheet, at, n1, n2='GND'):
    return P(sheet, 'C', 'Device', 'C_Polarized', '100u 25V', 'Capacitor_SMD:CP_Elec_6.3x7.7', 'C72477',
             'RVT1E101M0607', at, 0, {'1': n1, '2': n2})
def FLAG(sheet, at, net):
    return P(sheet, '#FLG', 'power', 'PWR_FLAG', 'PWR_FLAG', '', '', '', at, 0, {'1': net})
def HDR(sheet, n, value, at, nets, lcsc, mpn, dnp=False, rot=0):
    fp = 'Connector_PinHeader_2.54mm:PinHeader_1x%02d_P2.54mm_Vertical' % n
    return P(sheet, 'J', 'Connector_Generic', 'Conn_01x%02d' % n, value, fp, lcsc, mpn, at, rot,
             {str(i + 1): x for i, x in enumerate(nets)}, dnp)

C100N = ('100n', 'C14663', 'CC0603KRX7R9BB104')
C1U = ('1u', 'C15849', 'CL10A105KB8NNNC')
C10U = ('10u', 'C19702', 'CL10A106KP8NNNC')
C4U7 = ('4.7u', 'C19666', 'CL10A475KO8NNNC')
C10N = ('10n', 'C57112', '0603B103K500NT')
C15P = ('15p', 'C1644', 'CL10C150JB8NNNC')
C4P7 = ('4.7p', 'C1669', '0603CG4R7C500NT')
C4N7 = ('4.7n', 'C53987', '0603B472K500NT')
C10U25 = ('10u 25V', 'C15850', 'CL21A106KAYNNNE')       # 0805
C22U25 = ('22u 25V', 'C45783', 'CL21A226MAQNNNE')       # 0805
C22U25L = ('22u 25V', 'C12891', 'CL31A226KAHNNNE')      # 1206
FP_C0805, FP_C1206 = 'Capacitor_SMD:C_0805_2012Metric', 'Capacitor_SMD:C_1206_3216Metric'
R10K = ('10k', 'C25804', '0603WAF1002T5E')
R5K1 = ('5.1k', 'C23186', '0603WAF5101T5E')
R1K5 = ('1.5k', 'C22843', '0603WAF1501T5E')
R4K7 = ('4.7k', 'C23162', '0603WAF4701T5E')
R1K = ('1k', 'C21190', '0603WAF1001T5E')
R1M = ('1M', 'C22935', '0603WAF1004T5E')
R0 = ('0R', 'C21189', '0603WAF0000T5E')
R56K = ('56k', 'C23206', '0603WAF5602T5E')
R33K = ('33k', 'C4216', '0603WAF3302T5E')
R100K = ('100k', 'C25803', '0603WAF1003T5E')
R100 = ('100R', 'C22775', '0603WAF1000T5E')
LED_RED = ('red', 'C2286', 'KT-0603R')
HDR3 = ('C49257', '2.54-1*3P')
HDR2 = ('C492401', 'PZ254V-11-02P')

# ================================================================ MCU sheet (A3)
S = 'mcu'
mcu_pins = {}
for n in libsym.pins(libsym.flat('MCU_ST_STM32F1', 'STM32F103C8Tx')):
    mcu_pins.setdefault(n['name'], []).append(n['num'])
special = {'VDD': '+3V3', 'VSS': 'GND', 'VSSA': 'GND', 'VDDA': 'VDDA', 'VBAT': 'VBAT_RTC', 'NRST': 'NRST',
           'BOOT0': 'BOOT0', 'PB2': 'BOOT1', 'PD0': 'HSE_IN', 'PD1': 'HSE_OUT', 'PA13': 'SWDIO', 'PA14': 'SWCLK',
           'PB3': 'SWO',
           # RC car functions
           'PA0': 'SERVO1', 'PA1': 'SERVO2', 'PA2': 'SERVO3', 'PA3': 'SERVO4',      # TIM2 CH1-4
           'PA4': 'VBAT_SENSE',                                                         # ADC12_IN4
           'PA6': 'MOTOR_IN1', 'PA7': 'MOTOR_IN2',                                      # TIM3 CH1/CH2
           'PB0': 'LIGHT1', 'PB1': 'LIGHT2',                                            # TIM3 CH3/CH4
           'PB6': 'RC_IN1', 'PB7': 'RC_IN2', 'PB8': 'RC_IN3',                           # TIM4 CH1-3, 5 V tolerant
           'PA9': 'UART_TX', 'PA10': 'UART_RX',                                         # USART1
           'PB10': 'I2C_SCL', 'PB11': 'I2C_SDA',                                        # I2C2
           'PB12': 'IMU_INT1', 'PB13': 'IMU_INT2'}
u1 = {num: special.get(name, name) for name, nums in mcu_pins.items() for num in nums}
P(S, 'U', 'MCU_ST_STM32F1', 'STM32F103C8Tx', 'STM32F103C8T6', 'Package_QFP:LQFP-48_7x7mm_P0.5mm',
  'C8734', 'STM32F103C8T6', (80, 58), 0, u1)
for i in range(3):
    C(S, *C100N, (20 + 5 * i, 95), '+3V3')
C(S, *C4U7, (35, 95), '+3V3')
C(S, *C100N, (45, 95), 'VBAT_RTC')
P(S, 'JP', 'Jumper', 'SolderJumper_2_Bridged', 'VBAT=3V3', 'Jumper:SolderJumper-2_P1.3mm_Bridged_RoundedPad1.0x1.5mm',
  '', '', (52, 90), 0, {'1': '+3V3', '2': 'VBAT_RTC'})
FLAG(S, (60, 95), 'VBAT_RTC')
P(S, 'FB', 'Device', 'FerriteBead', '600R@100MHz', 'Inductor_SMD:L_0603_1608Metric', 'C1002', 'GZ1608D601TF',
  (20, 75), 0, {'1': '+3V3', '2': 'VDDA'})
C(S, *C10N, (27, 75), 'VDDA')
C(S, *C1U, (33, 75), 'VDDA')
FLAG(S, (39, 75), 'VDDA')
P(S, 'Y', 'Device', 'Crystal_GND24', '8MHz', 'Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm', 'C2682775', 'X32258MOB4SI',
  (25, 22), 0, {'1': 'HSE_IN', '3': 'HSE_OUT', '2': 'GND', '4': 'GND'})
C(S, *C15P, (19, 30), 'HSE_IN')
C(S, *C15P, (31, 30), 'HSE_OUT')
P(S, 'Y', 'Device', 'Crystal', '32.768kHz', 'Crystal:Crystal_SMD_3215-2Pin_3.2x1.5mm', 'C95361', 'Q13FC13500049',
  (25, 45), 0, {'1': 'PC14', '2': 'PC15'}, dnp=True)
C(S, *C4P7, (19, 53), 'PC14', dnp=True)
C(S, *C4P7, (31, 53), 'PC15', dnp=True)
R(S, *R10K, (125, 25), 'BOOT0', 'GND')
P(S, 'SW', 'Switch', 'SW_Push', 'BOOT0', 'Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A', 'C318884', 'TS-1187A-B-A-B',
  (135, 18), 0, {'1': '+3V3', '2': 'BOOT0'})
R(S, *R10K, (145, 25), 'BOOT1', 'GND')
C(S, *C100N, (125, 45), 'NRST')
P(S, 'SW', 'Switch', 'SW_Push', 'RESET', 'Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A', 'C318884', 'TS-1187A-B-A-B',
  (135, 40), 0, {'1': 'NRST', '2': 'GND'})
R(S, *R1K, (125, 65), '+3V3', 'LED_USER_A', rot=90)
P(S, 'D', 'Device', 'LED', 'red', 'LED_SMD:LED_0603_1608Metric', 'C2286', 'KT-0603R',
  (135, 65), 180, {'2': 'LED_USER_A', '1': 'PC13'})
R(S, *R0, (125, 82), 'USB_D+', 'PA12', rot=90)
R(S, *R0, (125, 90), 'USB_D-', 'PA11', rot=90)
R(S, *R1K5, (140, 88), '+3V3', 'PA12')

# ================================================================ Power sheet (A3)
S = 'power'
# battery input: XT30 (pad 1 = -, pad 2 = +), P-MOSFET reverse protection, TVS, bulk, sense divider
P(S, 'J', 'Connector_Generic', 'Conn_01x02', 'XT30 battery 2S-3S', 'Connector_AMASS:AMASS_XT30UPB-M_1x02_P5.0mm_Vertical',
  'C428721', 'XT30UPB-M', (12, 20), 0, {'1': 'GND', '2': 'VBAT_RAW'})
P(S, 'Q', 'rcboard', 'AO4407A', 'AO4407A', 'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm', 'C16072', 'AO4407A',
  (35, 22), 0, {'5': 'VBAT_RAW', '6': 'VBAT_RAW', '7': 'VBAT_RAW', '8': 'VBAT_RAW', '1': 'VBAT', '2': 'VBAT', '3': 'VBAT',
                '4': 'Q_REV_G'})
R(S, *R10K, (22, 36), 'Q_REV_G', 'GND')
P(S, 'D', 'Device', 'D', 'SMAJ15A', 'Diode_SMD:D_SMA', 'C353478', 'SMAJ15A', (52, 28), 90, {'1': 'VBAT', '2': 'GND'})
C(S, *C22U25L, (60, 28), 'VBAT', fp=FP_C1206)
C(S, *C22U25L, (66, 28), 'VBAT', fp=FP_C1206)
FLAG(S, (52, 14), 'VBAT')
R(S, *R33K, (76, 22), 'VBAT', 'VBAT_SENSE')
R(S, *R10K, (76, 36), 'VBAT_SENSE', 'GND')
C(S, *C100N, (84, 36), 'VBAT_SENSE')
# 5 V / 3 A buck for servos and receiver: TPS563201, Vout = 0.768 V * (1 + 56k/10k) = 5.07 V
P(S, 'U', 'Regulator_Switching', 'TPS563201', 'TPS563201', 'Package_TO_SOT_SMD:TSOT-23-6', 'C116592', 'TPS563201DDCR',
  (118, 24), 0, {'1': 'GND', '2': 'BUCK_SW', '3': 'VBAT', '4': 'BUCK_FB', '5': 'BUCK_EN', '6': 'BUCK_BST'})
R(S, *R100K, (100, 14), 'VBAT', 'BUCK_EN')
C(S, *C10U25, (96, 32), 'VBAT', fp=FP_C0805)
C(S, *C10U25, (101, 32), 'VBAT', fp=FP_C0805)
C(S, *C100N, (106, 32), 'VBAT')
C(S, *C100N, (132, 12), 'BUCK_BST', 'BUCK_SW')
P(S, 'L', 'Device', 'L', '3.3u', 'Inductor_SMD:L_Sunlord_SWPA6045S', 'C83456', 'SWPA6045S3R3MT',
  (140, 24), 90, {'1': 'BUCK_SW', '2': 'V5_SERVO'})
R(S, *R56K, (150, 30), 'V5_SERVO', 'BUCK_FB')
R(S, *R10K, (150, 42), 'BUCK_FB', 'GND')
C(S, *C22U25, (158, 32), 'V5_SERVO', fp=FP_C0805)
C(S, *C22U25, (163, 32), 'V5_SERVO', fp=FP_C0805)
C(S, *C22U25, (168, 32), 'V5_SERVO', fp=FP_C0805)
# logic 5 V = servo rail OR USB, each through a Schottky (USB never feeds servos, buck never back-fed)
P(S, 'D', 'Device', 'D_Schottky', 'B5819W', 'Diode_SMD:D_SOD-123', 'C8598', 'B5819W SL',
  (150, 60), 180, {'2': 'V5_SERVO', '1': '+5V'})
# USB-C device
P(S, 'J', 'Connector', 'USB_C_Receptacle_USB2.0_16P', 'USB-C', 'Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12',
  'C165948', 'TYPE-C-31-M-12', (20, 80), 0,
  {'A4': 'VBUS', 'A9': 'VBUS', 'B4': 'VBUS', 'B9': 'VBUS', 'A1': 'GND', 'A12': 'GND', 'B1': 'GND', 'B12': 'GND',
   'A5': 'CC1', 'B5': 'CC2', 'A6': 'USB_D+', 'B6': 'USB_D+', 'A7': 'USB_D-', 'B7': 'USB_D-',
   'A8': 'NC', 'B8': 'NC', 'SH': 'USB_SHIELD'})
R(S, *R5K1, (36, 62), 'CC1', 'GND')
R(S, *R5K1, (41, 62), 'CC2', 'GND')
R(S, *R1M, (10, 100), 'USB_SHIELD', 'GND')
C(S, *C4N7, (14, 100), 'USB_SHIELD')
P(S, 'U', 'Power_Protection', 'USBLC6-2SC6', 'USBLC6-2SC6', 'Package_TO_SOT_SMD:SOT-23-6', 'C7519', 'USBLC6-2SC6',
  (55, 82), 0, {'1': 'USB_D+', '6': 'USB_D+', '3': 'USB_D-', '4': 'USB_D-', '5': 'VBUS', '2': 'GND'})
P(S, 'F', 'Device', 'Polyfuse', '500mA', 'Fuse:Fuse_1206_3216Metric', 'C70077', 'nSMD050-33V',
  (75, 60), 0, {'1': 'VBUS', '2': 'VBUS_F'})
P(S, 'D', 'Device', 'D_Schottky', 'B5819W', 'Diode_SMD:D_SOD-123', 'C8598', 'B5819W SL',
  (85, 66), 180, {'2': 'VBUS_F', '1': '+5V'})
P(S, 'U', 'Regulator_Linear', 'AP2112K-3.3', 'AP2112K-3.3', 'Package_TO_SOT_SMD:SOT-23-5', 'C51118', 'AP2112K-3.3TRG1',
  (110, 66), 0, {'1': '+5V', '3': '+5V', '2': 'GND', '5': '+3V3'})
C(S, *C1U, (100, 74), '+5V')
C(S, *C1U, (120, 74), '+3V3')
C(S, *C10U, (125, 74), '+3V3')
R(S, *R1K, (110, 90), '+3V3', 'LED_PWR_A')
P(S, 'D', 'Device', 'LED', 'red', 'LED_SMD:LED_0603_1608Metric', 'C2286', 'KT-0603R',
  (118, 98), 180, {'2': 'LED_PWR_A', '1': 'GND'})
FLAG(S, (60, 105), 'VBUS')
FLAG(S, (66, 105), '+5V')
FLAG(S, (72, 105), 'GND')

# ================================================================ Drive sheet (A3): motor, servos, receiver, lights
S = 'drive'
P(S, 'U', 'rcboard', 'DRV8870', 'DRV8870', 'Package_SO:Texas_HSOP-8-1EP_3.9x4.9mm_P1.27mm_ThermalVias', 'C86590',
  'DRV8870DDAR', (45, 30), 0, {'5': 'VBAT', '3': 'MOTOR_IN1', '2': 'MOTOR_IN2', '4': '+3V3', '6': 'MOTOR_A',
                               '8': 'MOTOR_B', '7': 'MOTOR_ISEN', '1': 'GND', '9': 'GND'})
CP(S, (15, 24), 'VBAT')
C(S, *C22U25L, (21, 24), 'VBAT', fp=FP_C1206)
C(S, *C100N, (26, 24), 'VBAT')
# I_TRIP = VREF / (10 * R_ISEN) = 3.3 V / (10 * 0.1 R) = 3.3 A
R(S, '0.1R 2W', 'C160587', 'RLP25FEER100', (62, 42), 'MOTOR_ISEN', 'GND', fp='Resistor_SMD:R_2512_6332Metric')
P(S, 'J', 'Connector_Generic', 'Conn_01x02', 'MOTOR', 'TerminalBlock_Phoenix:TerminalBlock_Phoenix_PT-1,5-2-3.5-H_1x02_P3.50mm_Horizontal',
  'C474892', 'KF350-3.5-2P', (75, 28), 0, {'1': 'MOTOR_A', '2': 'MOTOR_B'})
for i in range(4):   # servo / ESC outputs: S, +, -
    HDR(S, 3, 'SERVO%d' % (i + 1), (100 + 12 * i, 25), ['SERVO%d' % (i + 1), 'V5_SERVO', 'GND'], *HDR3)
CP(S, (150, 45), 'V5_SERVO')
for i in range(3):   # receiver inputs, receiver powered from the servo rail; 1k series protection
    HDR(S, 3, 'RC%d' % (i + 1), (100 + 12 * i, 65), ['RC%d_S' % (i + 1), 'V5_SERVO', 'GND'], *HDR3)
    R(S, *R1K, (100 + 12 * i, 52), 'RC%d_S' % (i + 1), 'RC_IN%d' % (i + 1))
for i in range(2):   # light outputs, low-side switched (LED+ = 5 V servo rail)
    x = 20 + 30 * i
    P(S, 'Q', 'Transistor_FET', 'AO3400A', 'AO3400A', 'Package_TO_SOT_SMD:SOT-23', 'C20917', 'AO3400A',
      (x + 10, 80), 0, {'1': 'LIGHT%d_G' % (i + 1), '2': 'GND', '3': 'LIGHT%d_D' % (i + 1)})
    R(S, *R100, (x, 76), 'LIGHT%d' % (i + 1), 'LIGHT%d_G' % (i + 1), rot=90)
    R(S, *R100K, (x + 2, 90), 'LIGHT%d_G' % (i + 1), 'GND')
    HDR(S, 2, 'LIGHT%d' % (i + 1), (x + 18, 70), ['V5_SERVO', 'LIGHT%d_D' % (i + 1)], *HDR2)

# ================================================================ IO sheet (A4): debug, IMU, Qwiic, UART, expansion
S = 'io'
P(S, 'J', 'Connector', 'Conn_ARM_JTAG_SWD_10', 'Cortex-Debug', 'Connector_PinHeader_1.27mm:PinHeader_2x05_P1.27mm_Vertical_SMD',
  'C2935458', 'PZ127VS-12-10-H10-A38', (20, 25), 0,
  {'1': '+3V3', '2': 'SWDIO', '3': 'GND', '4': 'SWCLK', '5': 'GND', '6': 'SWO', '8': 'NC', '9': 'GND', '10': 'NRST'})
P(S, 'U', 'Sensor_Motion', 'LSM6DS3', 'LSM6DS3TR-C', 'Package_LGA:LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y', 'C967633',
  'LSM6DS3TR-C', (60, 28), 0, {'1': 'IMU_SA0', '2': 'IMU_SDX', '3': 'GND', '4': 'IMU_INT1', '5': '+3V3', '6': 'GND',
                               '7': 'GND', '8': '+3V3', '9': 'IMU_INT2', '12': '+3V3', '13': 'I2C_SCL', '14': 'I2C_SDA'})
R(S, *R10K, (45, 40), 'IMU_SA0', 'GND')    # I2C address 0x6A
R(S, *R10K, (50, 40), 'IMU_SDX', 'GND')    # unused aux I2C data pulled low (datasheet: VDDIO or GND)
C(S, *C100N, (75, 20), '+3V3')
C(S, *C100N, (80, 20), '+3V3')
P(S, 'J', 'Connector_Generic', 'Conn_01x04', 'Qwiic', 'Connector_JST:JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal',
  'C160404', 'SM04B-SRSS-TB(LF)(SN)', (95, 25), 0, {'1': 'GND', '2': '+3V3', '3': 'I2C_SDA', '4': 'I2C_SCL'})
P(S, 'JP', 'Jumper', 'SolderJumper_2_Bridged', 'I2C_PU', 'Jumper:SolderJumper-2_P1.3mm_Bridged_RoundedPad1.0x1.5mm',
  '', '', (95, 45), 0, {'1': '+3V3', '2': 'I2C_PU'})
R(S, *R4K7, (103, 52), 'I2C_PU', 'I2C_SDA')
R(S, *R4K7, (109, 52), 'I2C_PU', 'I2C_SCL')
HDR(S, 4, 'UART', (20, 60), ['GND', '+5V', 'UART_TX', 'UART_RX'], 'C2691448', 'PZ254V-11-04P')
P(S, 'J', 'Connector_Generic', 'Conn_02x05_Odd_Even', 'EXPANSION', 'Connector_PinHeader_2.54mm:PinHeader_2x05_P2.54mm_Vertical',
  'C492422', 'PZ254V-12-10P', (60, 62), 0,
  {'1': '+3V3', '2': 'GND', '3': 'PA5', '4': 'PA8', '5': 'PA15', '6': 'PB4', '7': 'PB5', '8': 'PB9', '9': 'PB14',
   '10': 'PB15'}, dnp=True)
for i in range(4):
    P(S, 'H', 'Mechanical', 'MountingHole', 'M3', 'MountingHole:MountingHole_3.2mm_M3', '', '', (85 + 6 * i, 70), 0, {})

NOTES = {
 'mcu': [((10, 108), 'Pin map: PA0-PA3 SERVO1-4 (TIM2 CH1-4) | PA4 VBAT_SENSE (ADC) | PA6/PA7 MOTOR_IN1/2 (TIM3 CH1/2)\n'
                     'PB0/PB1 LIGHT1/2 (TIM3 CH3/4) | PB6-PB8 RC_IN1-3 (TIM4 CH1-3, 5 V tolerant) | PA9/PA10 USART1\n'
                     'PB10/PB11 I2C2 (IMU + Qwiic) | PB12/PB13 IMU INT1/INT2 | PC13 user LED (low-active)\n'
                     'HSE 8 MHz, C_L = 12 pF: C = 2*(12 pF - 4 pF) = 16 pF -> 15 pF C0G. LSE optional (DNP).')],
 'power': [((10, 112), 'Battery 2S-3S LiPo (6-12.6 V) on XT30. AO4407A: reverse polarity protection (gate to GND).\n'
                       'SMAJ15A clamps transients. VBAT_SENSE = VBAT * 10k/43k (12.6 V -> 2.93 V).\n'
                       'TPS563201 buck -> V5_SERVO (5.07 V, 3 A) for servos and receiver.\n'
                       '+5V (logic) = V5_SERVO or USB VBUS, each via B5819W; AP2112K-3.3 for the MCU.')],
 'drive': [((10, 100), 'DRV8870: brushed motor 6.5-45 V, I_trip = VREF/(10*R_ISEN) = 3.3 V/(10*0.1) = 3.3 A.\n'
                       'IN1/IN2 PWM from TIM3: forward/reverse/brake. Below 6.5 V (empty 2S) the driver locks out.\n'
                       'SERVO1-4: S / 5V / GND (use SERVO2 for an ESC; cut the ESC BEC red wire).\n'
                       'RC1-3 inputs: receiver PWM/PPM, powered from the servo rail, 1k series protection.')],
 'io': [((10, 75), 'IMU LSM6DS3TR-C on I2C2 at 0x6A (SA0 = GND), INT1 -> PB12, INT2 -> PB13.\n'
                   'Qwiic shares I2C2; 4.7k pull-ups, cut JP to remove. UART: GND 5V TX RX (Bluetooth/telemetry).\n'
                   'Expansion 2x5 (loose header): 3V3 GND PA5 PA8 PA15 PB4 PB5 PB9 PB14 PB15.')],
}
SHEETS = [('mcu', 'MCU', 'A3', 2), ('power', 'Power', 'A3', 3), ('drive', 'Drive', 'A3', 4), ('io', 'IO', 'A4', 5)]
SHEETS_TITLES = [('mcu', 'STM32F103C8T6 core'), ('power', 'Battery, 5 V buck, USB-C, 3.3 V'),
                 ('drive', 'Motor driver, servos, receiver, lights'), ('io', 'Debug, IMU, Qwiic, UART, expansion')]
SHEET_UUID = {s: U() for s, *_ in SHEETS}
SHEET_FILE_UUID = {s: U() for s, *_ in SHEETS}
REV, TITLE = 'C', 'STM32 RC-car controller Rev C'

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
           ['title_block', ['title', Q(title)], ['date', Q('2026-10-10')], ['rev', Q(REV)], ['company', Q('Cagri Catik')]],
           lib_symbols(libs)] + items + [['embedded_fonts', 'no']]
    return doc


def build_root():
    items = []
    for i, (s, name, paper, page) in enumerate(SHEETS):
        x, y, w, h = 30 + i * 60, 50, 40, 25
        items.append(['sheet', ['at', f(x), f(y)], ['size', f(w), f(h)], ['exclude_from_sim', 'no'], ['in_bom', 'yes'],
                      ['on_board', 'yes'], ['dnp', 'no'], ['fields_autoplaced', 'yes'],
                      ['stroke', ['width', '0.1524'], ['type', 'solid']], ['fill', ['color', '0', '0', '0', '0.0000']],
                      ['uuid', Q(SHEET_UUID[s])],
                      ['property', Q('Sheetname'), Q(name), ['at', f(x), f(y - 0.7), '0'], eff(justify=['left', 'bottom'])],
                      ['property', Q('Sheetfile'), Q(s + '.kicad_sch'), ['at', f(x), f(y + h + 0.6), '0'],
                       eff(justify=['left', 'top'])],
                      ['instances', ['project', Q(PROJECT), ['path', Q('/' + ROOT_UUID), ['page', Q(str(page))]]]]])
    note = ('STM32 RC-car controller Rev C\\n'
            'Battery 2S-3S XT30 -> reverse protection -> 5 V/3 A buck (servos, receiver) + DRV8870 brushed motor driver\\n'
            '4 servo/ESC outputs, 3 receiver inputs, 2 light outputs, LSM6DS3TR-C IMU, USB-C, Cortex-Debug, Qwiic, UART\\n'
            'STM32F103C8T6, 8 MHz HSE, 4 layers, JLCPCB assembly (LCSC field on every part)')
    items.append(['text', Q(note), ['exclude_from_sim', 'no'], ['at', '40', '100', '0'], eff(justify=['left', 'top']),
                  ['uuid', Q(U())]])
    return ['kicad_sch', ['version', '20250114'], ['generator', Q('eeschema')], ['generator_version', Q('9.0')],
            ['uuid', Q(ROOT_UUID)], ['paper', Q('A4')],
            ['title_block', ['title', Q(TITLE)], ['date', Q('2026-10-10')], ['rev', Q(REV)],
             ['company', Q('Cagri Catik')]],
            ['lib_symbols']] + items + [['sheet_instances', ['path', Q('/'), ['page', Q('1')]]], ['embedded_fonts', 'no']]

for s, name, paper, page in SHEETS:
    open(os.path.join(OUT, s + '.kicad_sch'), 'w').write(sexp.dump(build_sheet(s, paper)) + '\n')
open(os.path.join(OUT, PROJECT + '.kicad_sch'), 'w').write(sexp.dump(build_root()) + '\n')

# expected netlist for verification
exp = {}
for p in PARTS:
    if p.ref.startswith('#'): continue
    for pin, net in p.conns.items():
        if net != 'NC': exp.setdefault(net, set()).add((p.ref, pin))
json.dump({k: sorted(v) for k, v in exp.items()}, open(os.path.join(OUT, 'expected_nets.json'), 'w'), indent=0)
print('\n'.join('%-5s %-12s %-10s %s%s' % (p.ref, p.value, p.lcsc, p.fp.split(':')[-1], ' DNP' if p.dnp else '')
                for p in PARTS if not p.ref.startswith('#')))

