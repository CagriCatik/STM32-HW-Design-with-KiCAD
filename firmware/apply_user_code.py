#!/usr/bin/env python3
"""Hook the bring-up application (firmware/app) into the CubeMX-generated project.

Only edits inside CubeMX "USER CODE" blocks, so regenerating from the .ioc keeps the changes.
  python3 apply_user_code.py rc_controller
"""
import os, re, shutil, sys

proj = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
shutil.copy(os.path.join(here, 'app', 'app.c'), os.path.join(proj, 'Src', 'app.c'))
shutil.copy(os.path.join(here, 'app', 'app.h'), os.path.join(proj, 'Inc', 'app.h'))

def user_block(path, name, code):
    t = open(path).read()
    pat = re.compile(r'(/\* USER CODE BEGIN %s \*/\n)(.*?)(\s*/\* USER CODE END %s \*/)' % (re.escape(name), re.escape(name)), re.S)
    m = pat.search(t)
    assert m, (path, name)
    t = t[:m.start(2)] + code + t[m.end(2):]
    open(path, 'w').write(t)

main = os.path.join(proj, 'Src', 'main.c')
user_block(main, 'Includes', '#include "app.h"')
user_block(main, '2', '  app_init();')
user_block(main, '3', '    app_loop();\n  }')   # block 3 also holds the closing brace of while (1)

cdc = os.path.join(proj, 'Src', 'usbd_cdc_if.c')
user_block(cdc, 'INCLUDE', '#include "app.h"')
t = open(cdc).read()
# CDC_Receive_FS: hand the data to the app before the next packet is armed
if 'app_cdc_rx' not in t:
    t = t.replace('  USBD_CDC_SetRxBuffer(&hUsbDeviceFS, &Buf[0]);\n  USBD_CDC_ReceivePacket(&hUsbDeviceFS);',
                  '  app_cdc_rx(Buf, *Len);\n  USBD_CDC_SetRxBuffer(&hUsbDeviceFS, &Buf[0]);\n  USBD_CDC_ReceivePacket(&hUsbDeviceFS);', 1)
assert 'app_cdc_rx' in t
open(cdc, 'w').write(t)

cm = os.path.join(proj, 'CMakeLists.txt')
t = open(cm).read()
if 'Src/app.c' not in t:
    t = t.replace('# Add user sources here', '# Add user sources here\n    Src/app.c', 1)
    assert 'Src/app.c' in t
    open(cm, 'w').write(t)
print('user code applied to', proj)
