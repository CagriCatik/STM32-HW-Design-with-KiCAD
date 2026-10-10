/* RC-car controller Rev C – bring-up application (called from the CubeMX-generated main.c). */
#ifndef APP_H
#define APP_H

#include <stdint.h>

void app_init(void);
void app_loop(void);
void app_cdc_rx(const uint8_t *buf, uint32_t len);   /* called from CDC_Receive_FS */

#endif
