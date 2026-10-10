/* RC-car controller Rev C – bring-up application.
 *
 * - user LED (PC13) blinks at 1 Hz
 * - USB CDC: every received line is echoed; a status line is sent every second:
 *     VBAT=7.84V IMU=0x6A RC=1502/1498/0us
 * - commands over USB CDC (115200 8N1 or any rate, it is a virtual COM port):
 *     s<1-4> <us>     servo pulse 500..2500 us (default 1500 = centre)     e.g. "s1 1200"
 *     m <-100..100>   motor duty in %, sign = direction, 0 = coast          e.g. "m 30"
 *     l<1-2> <0..100> light brightness in %                                e.g. "l1 100"
 *     c <0-6> <r> <g> <b>  WS2812 colour 0..255, LED 1..6 or 0 = all      e.g. "c 0 255 0 0"
 *     ind <l|r|h|off> indicators left / right / hazard (amber, 1.5 Hz)     e.g. "ind h"
 * - WS2812 chain on PA8 (TIM1 CH1 + DMA): 1 front left, 2 front right, 3 sill left, 4 sill right,
 *   5 rear left, 6 rear right; default: white headlights, blue sills, red tail lights
 * - receiver inputs RC1..RC3 (TIM4 CH1..3) are measured by input capture; 0 = no signal
 */
#include "app.h"
#include "main.h"
#include "usbd_cdc_if.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern ADC_HandleTypeDef hadc1;
extern I2C_HandleTypeDef hi2c2;
extern TIM_HandleTypeDef htim1, htim2, htim3, htim4;

#define IMU_ADDR        (0x6A << 1)   /* LSM6DS3TR-C, SA0 = GND */
#define IMU_WHO_AM_I    0x0F
#define VBAT_DIVIDER    4.3f          /* 33k / 10k */
#define MOTOR_TOP       3599u         /* TIM3 period, 20 kHz */

static uint8_t imu_id;
static volatile uint16_t rc_us[3];
static volatile uint16_t rc_rise[3];
static volatile uint32_t rc_seen_ms[3];
static char line[64];

/* ---------------------------------------------------------------- WS2812 */
#define WS_LEDS     6
#define WS_T0H      29              /* 0.40 us of the 1.25 us bit (90 ticks at 72 MHz) */
#define WS_T1H      58              /* 0.80 us */
#define WS_RESET    50              /* 50 low bit times = 62 us latch */
enum { FRONT_L, FRONT_R, SILL_L, SILL_R, REAR_L, REAR_R };
static uint8_t ws_rgb[WS_LEDS][3] = {
    {80, 80, 80}, {80, 80, 80},     /* headlights */
    {0, 0, 60},   {0, 0, 60},       /* sills */
    {60, 0, 0},   {60, 0, 0},       /* tail lights */
};
static uint16_t ws_buf[WS_LEDS * 24 + WS_RESET];
static volatile uint8_t ws_busy;
static char indicator;              /* 0, 'l', 'r', 'h' */

static void ws_show(void)
{
    if (ws_busy) return;
    uint8_t blink_on = (HAL_GetTick() / 333) & 1;
    uint16_t *p = ws_buf;
    for (int i = 0; i < WS_LEDS; i++) {
        const uint8_t *c = ws_rgb[i];
        uint8_t amber[3] = {255, 120, 0};
        int left = (i == FRONT_L || i == REAR_L || i == SILL_L), right = (i == FRONT_R || i == REAR_R || i == SILL_R);
        if (indicator && blink_on && ((indicator == 'h') || (indicator == 'l' && left) || (indicator == 'r' && right)))
            c = amber;
        uint8_t grb[3] = {c[1], c[0], c[2]};                    /* WS2812 expects green, red, blue */
        for (int b = 0; b < 3; b++)
            for (int bit = 7; bit >= 0; bit--)
                *p++ = (grb[b] >> bit) & 1 ? WS_T1H : WS_T0H;
    }
    for (int i = 0; i < WS_RESET; i++) *p++ = 0;
    ws_busy = 1;
    HAL_TIM_PWM_Start_DMA(&htim1, TIM_CHANNEL_1, (uint32_t *)ws_buf, sizeof ws_buf / sizeof ws_buf[0]);
}

void HAL_TIM_PWM_PulseFinishedCallback(TIM_HandleTypeDef *htim)
{
    if (htim->Instance == TIM1) {
        HAL_TIM_PWM_Stop_DMA(&htim1, TIM_CHANNEL_1);
        ws_busy = 0;
    }
}
static uint32_t line_len;

static void cdc_print(const char *s)
{
    uint32_t t0 = HAL_GetTick();
    while (CDC_Transmit_FS((uint8_t *)s, (uint16_t)strlen(s)) == USBD_BUSY && HAL_GetTick() - t0 < 20) { }
}

static float vbat_volts(void)
{
    HAL_ADC_Start(&hadc1);
    if (HAL_ADC_PollForConversion(&hadc1, 10) != HAL_OK) return 0.0f;
    uint32_t raw = HAL_ADC_GetValue(&hadc1);
    return raw * 3.3f / 4095.0f * VBAT_DIVIDER;
}

static void servo_set(int ch, int us)
{
    static const uint32_t chan[4] = {TIM_CHANNEL_1, TIM_CHANNEL_2, TIM_CHANNEL_3, TIM_CHANNEL_4};
    if (ch < 1 || ch > 4) return;
    if (us < 500) us = 500;
    if (us > 2500) us = 2500;
    __HAL_TIM_SET_COMPARE(&htim2, chan[ch - 1], (uint32_t)us);
}

/* DRV8870: IN1/IN2 PWM, slow decay (one input high, the other PWM'd low) */
static void motor_set(int pct)
{
    if (pct > 100) pct = 100;
    if (pct < -100) pct = -100;
    uint32_t duty = (uint32_t)(abs(pct) * (MOTOR_TOP + 1) / 100);
    if (pct == 0) {                       /* coast */
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, 0);
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_2, 0);
    } else if (pct > 0) {
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, MOTOR_TOP + 1);
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_2, MOTOR_TOP + 1 - duty);
    } else {
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, MOTOR_TOP + 1 - duty);
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_2, MOTOR_TOP + 1);
    }
}

static void light_set(int ch, int pct)
{
    if (pct < 0) pct = 0;
    if (pct > 100) pct = 100;
    __HAL_TIM_SET_COMPARE(&htim3, ch == 1 ? TIM_CHANNEL_3 : TIM_CHANNEL_4, (uint32_t)pct * (MOTOR_TOP + 1) / 100);
}

void app_init(void)
{
    HAL_ADCEx_Calibration_Start(&hadc1);
    for (uint32_t c = TIM_CHANNEL_1; c <= TIM_CHANNEL_4; c += 4) {
        HAL_TIM_PWM_Start(&htim2, c);                 /* servos at 1500 us from CubeMX */
        __HAL_TIM_SET_COMPARE(&htim3, c, 0);
        HAL_TIM_PWM_Start(&htim3, c);                 /* motor coast, lights off */
    }
    HAL_TIM_IC_Start_IT(&htim4, TIM_CHANNEL_1);
    HAL_TIM_IC_Start_IT(&htim4, TIM_CHANNEL_2);
    HAL_TIM_IC_Start_IT(&htim4, TIM_CHANNEL_3);
    if (HAL_I2C_Mem_Read(&hi2c2, IMU_ADDR, IMU_WHO_AM_I, I2C_MEMADD_SIZE_8BIT, &imu_id, 1, 10) != HAL_OK) imu_id = 0;
}

void app_loop(void)
{
    static uint32_t last, last_ws;
    uint32_t now = HAL_GetTick();
    if (now - last_ws >= 20) { last_ws = now; ws_show(); }   /* 50 Hz refresh, animates the indicators */
    if (now - last < 500) return;
    last = now;
    HAL_GPIO_TogglePin(LED_USER_GPIO_Port, LED_USER_Pin);
    if (HAL_GPIO_ReadPin(LED_USER_GPIO_Port, LED_USER_Pin) == GPIO_PIN_SET) return;   /* status once per second */
    uint16_t rc[3];
    for (int i = 0; i < 3; i++) rc[i] = (now - rc_seen_ms[i] < 100) ? rc_us[i] : 0;
    char s[96];
    int mv = (int)(vbat_volts() * 1000.0f);
    snprintf(s, sizeof s, "VBAT=%d.%02dV IMU=0x%02X RC=%u/%u/%uus\r\n", mv / 1000, (mv % 1000) / 10, imu_id,
             rc[0], rc[1], rc[2]);
    cdc_print(s);
}

static void handle_line(char *l)
{
    int a = 0, b = 0, c = 0, d = 0;
    if (sscanf(l, "s%d %d", &a, &b) == 2) servo_set(a, b);
    else if (sscanf(l, "m %d", &a) == 1) motor_set(a);
    else if (sscanf(l, "l%d %d", &a, &b) == 2) light_set(a, b);
    else if (sscanf(l, "c %d %d %d %d", &a, &b, &c, &d) == 4) {
        for (int i = 0; i < WS_LEDS; i++)
            if (a == 0 || a == i + 1) { ws_rgb[i][0] = (uint8_t)b; ws_rgb[i][1] = (uint8_t)c; ws_rgb[i][2] = (uint8_t)d; }
    } else if (strncmp(l, "ind ", 4) == 0) {
        indicator = (l[4] == 'l' || l[4] == 'r' || l[4] == 'h') ? l[4] : 0;
    }
}

void app_cdc_rx(const uint8_t *buf, uint32_t len)
{
    CDC_Transmit_FS((uint8_t *)buf, (uint16_t)len);   /* echo (best effort, from the USB interrupt) */
    for (uint32_t i = 0; i < len; i++) {
        char c = (char)buf[i];
        if (c == '\r' || c == '\n') {
            line[line_len] = 0;
            if (line_len) handle_line(line);
            line_len = 0;
        } else if (line_len < sizeof line - 1) {
            line[line_len++] = c;
        }
    }
}

/* Receiver pulses: capture rising edge, flip to falling, width = difference (1 us ticks) */
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)
{
    if (htim->Instance != TIM4) return;
    int i;
    uint32_t ch;
    switch (htim->Channel) {
    case HAL_TIM_ACTIVE_CHANNEL_1: i = 0; ch = TIM_CHANNEL_1; break;
    case HAL_TIM_ACTIVE_CHANNEL_2: i = 1; ch = TIM_CHANNEL_2; break;
    case HAL_TIM_ACTIVE_CHANNEL_3: i = 2; ch = TIM_CHANNEL_3; break;
    default: return;
    }
    uint16_t t = (uint16_t)HAL_TIM_ReadCapturedValue(htim, ch);
    uint32_t pol = (TIM4->CCER >> (4 * i + 1)) & 1u;   /* CCxP: 0 = rising, 1 = falling */
    if (!pol) {
        rc_rise[i] = t;
        __HAL_TIM_SET_CAPTUREPOLARITY(htim, ch, TIM_INPUTCHANNELPOLARITY_FALLING);
    } else {
        uint16_t w = (uint16_t)(t - rc_rise[i]);
        if (w > 500 && w < 2600) { rc_us[i] = w; rc_seen_ms[i] = HAL_GetTick(); }
        __HAL_TIM_SET_CAPTUREPOLARITY(htim, ch, TIM_INPUTCHANNELPOLARITY_RISING);
    }
}
