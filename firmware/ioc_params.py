#!/usr/bin/env python3
"""Apply the Rev C peripheral parameters to the CubeMX .ioc written by cubemx_pinout.txt.
CubeMX's script mode can set pins and modes but not parameters, so they are patched here; CubeMX then
re-loads the file (config load) and recomputes all derived clock values before generating code."""
import re, sys

P = {
    # 8 MHz HSE x9 = 72 MHz SYSCLK, APB1 36 MHz, USB 72 / 1.5 = 48 MHz, ADC 12 MHz
    'RCC': {'PLLSourceVirtual': 'RCC_PLLSOURCE_HSE', 'PLLSourceVirtualString': 'RCC_PLLSOURCE_HSE',
            'PLLMUL': 'RCC_PLL_MUL9', 'SYSCLKSource': 'RCC_SYSCLKSOURCE_PLLCLK', 'APB1CLKDivider': 'RCC_HCLK_DIV2',
            'USBPrescaler': 'RCC_USBCLKSOURCE_PLL_DIV1_5', 'ADCPresc': 'RCC_ADCPCLK2_DIV6'},
    # servos: 1 us tick, 20 ms period, 1.5 ms centre
    'TIM2': {'Prescaler': '71', 'Period': '19999', 'Pulse-PWM\\ Generation1\\ CH1': '1500',
             'Pulse-PWM\\ Generation2\\ CH2': '1500', 'Pulse-PWM\\ Generation3\\ CH3': '1500',
             'Pulse-PWM\\ Generation4\\ CH4': '1500'},
    # motor (CH1/CH2) and lights (CH3/CH4): 20 kHz, 0..3599
    'TIM3': {'Prescaler': '0', 'Period': '3599'},
    # receiver pulse capture: 1 us tick, free running
    # (the F1 cannot capture both edges; the firmware flips the polarity after each edge)
    'TIM4': {'Prescaler': '71', 'Period': '65535'},
    # WS2812 on PA8: 800 kHz bit clock (90 ticks at 72 MHz), duty written by DMA per bit
    'TIM1': {'Prescaler': '0', 'Period': '89'},
    'I2C2': {'ClockSpeed': '400000'},   # > 100 kHz selects fast mode
    'USART1': {'BaudRate': '115200'},
}
PINS = {   # labels and initial states
    'PA0-WKUP': {'GPIO_Label': 'SERVO1'}, 'PA1': {'GPIO_Label': 'SERVO2'}, 'PA2': {'GPIO_Label': 'SERVO3'},
    'PA3': {'GPIO_Label': 'SERVO4'}, 'PA4': {'GPIO_Label': 'VBAT_SENSE'}, 'PA6': {'GPIO_Label': 'MOTOR_IN1'},
    'PA7': {'GPIO_Label': 'MOTOR_IN2'}, 'PB0': {'GPIO_Label': 'LIGHT1'}, 'PB1': {'GPIO_Label': 'LIGHT2'},
    'PB6': {'GPIO_Label': 'RC_IN1'}, 'PB7': {'GPIO_Label': 'RC_IN2'}, 'PB8': {'GPIO_Label': 'RC_IN3'},
    'PA8': {'GPIO_Label': 'LED_DATA'},
    'PB12': {'GPIO_Label': 'IMU_INT1', 'GPIO_ModeDefaultEXTI': 'GPIO_MODE_IT_RISING'},
    'PB13': {'GPIO_Label': 'IMU_INT2', 'GPIO_ModeDefaultEXTI': 'GPIO_MODE_IT_RISING'},
    'PC13-TAMPER-RTC': {'GPIO_Label': 'LED_USER', 'PinState': 'GPIO_PIN_SET'},
}
NVIC = {'DMA1_Channel2_IRQn': 'true\\:0\\:0\\:false\\:false\\:true\\:false\\:true\\:true',
        'TIM4_IRQn': 'true\\:0\\:0\\:false\\:false\\:true\\:true\\:true\\:true',
        'EXTI15_10_IRQn': 'true\\:0\\:0\\:false\\:false\\:true\\:true\\:true\\:true'}

path = sys.argv[1]
lines = open(path).read().splitlines()
kv = {}
order = []
for l in lines:
    if '=' in l and not l.startswith('#'):
        k, v = l.split('=', 1); kv[k] = v; order.append(k)
def put(k, v):
    if k not in kv: order.append(k)
    kv[k] = v
for ip, params in P.items():
    names = [n for n in kv.get(ip + '.IPParameters', '').split(',') if n]
    for k, v in params.items():
        put('%s.%s' % (ip, k), v)
        n = k.replace('\\ ', ' ')
        if n not in names: names.append(n)
    put(ip + '.IPParameters', ','.join(names))
for pin, params in PINS.items():
    names = [n for n in kv.get(pin + '.GPIOParameters', '').split(',') if n]
    for k, v in params.items():
        put('%s.%s' % (pin, k), v)
        if k not in names: names.append(k)
    put(pin + '.GPIOParameters', ','.join(names))
    put(pin + '.Locked', 'true')
for k, v in NVIC.items():
    put('NVIC.' + k, v)
put('ProjectManager.LibraryCopy', '1')   # copy only the HAL/CMSIS files the project uses
# DMA for TIM1_CH1 (WS2812): memory -> CCR1, half-words, normal mode
DMA = {'Request0': 'TIM1_CH1', 'RequestsNb': '1', 'TIM1_CH1.0.Direction': 'DMA_MEMORY_TO_PERIPH',
       'TIM1_CH1.0.Instance': 'DMA1_Channel2', 'TIM1_CH1.0.MemDataAlignment': 'DMA_MDATAALIGN_HALFWORD',
       'TIM1_CH1.0.MemInc': 'DMA_MINC_ENABLE', 'TIM1_CH1.0.Mode': 'DMA_NORMAL',
       'TIM1_CH1.0.PeriphDataAlignment': 'DMA_PDATAALIGN_HALFWORD', 'TIM1_CH1.0.PeriphInc': 'DMA_PINC_DISABLE',
       'TIM1_CH1.0.Priority': 'DMA_PRIORITY_HIGH',
       'TIM1_CH1.0.RequestParameters': 'Instance,Direction,PeriphInc,MemInc,PeriphDataAlignment,MemDataAlignment,Mode,Priority'}
for k, v in DMA.items():
    put('Dma.' + k, v)
ips = sorted(v for k, v in kv.items() if re.match(r'Mcu\.IP\d+$', k))
if 'DMA' not in ips:
    ips.append('DMA')
    for k in [k for k in kv if re.match(r'Mcu\.IP\d+$', k)]:
        del kv[k]; order.remove(k)
    for i, ip in enumerate(sorted(ips)):
        put('Mcu.IP%d' % i, ip)
    put('Mcu.IPNb', str(len(ips)))
head = [l for l in lines if l.startswith('#')]
open(path, 'w').write('\n'.join(head + ['%s=%s' % (k, kv[k]) for k in sorted(set(order))]) + '\n')
