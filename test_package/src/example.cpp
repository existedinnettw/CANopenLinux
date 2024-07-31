// ref to CO_main_basic.c
#include <cstdlib>
#include <cstdio>
#include <syslog.h> //vsyslog
#include <stdarg.h> //va_start, vat_end

#include "CO_error.h" //log_printf interface
#include "CO_epoll_interface.h"
#include "CANopen.h"
#include "OD.h" //OD_INIT_CONFIG

// for CO_driver.c
void
log_printf(int priority, const char* format, ...) {
    va_list ap;

    va_start(ap, format);
    vsyslog(priority, format, ap);
    va_end(ap);
}

using namespace std;

int
main() {
    CO_t* CO = NULL;
    CO_config_t* config_ptr = NULL;
    uint32_t heapMemoryUsed = 0;

    // already define CO_MULTIPLE_OD
    /* example usage of CO_MULTIPLE_OD (but still single OD here) */
    CO_config_t co_config = {0};
    OD_INIT_CONFIG(co_config); /* helper macro from OD.h */
#if (CO_CONFIG_LEDS) & CO_CONFIG_LEDS_ENABLE
    co_config.CNT_LEDS = 1;
#endif
#if (CO_CONFIG_LSS) & CO_CONFIG_LSS_SLAVE
    co_config.CNT_LSS_SLV = 1;
#endif
#if (CO_CONFIG_LSS) & CO_CONFIG_LSS_MASTER
    co_config.CNT_LSS_MST = 1;
#endif
#if (CO_CONFIG_GTW) & CO_CONFIG_GTW_ASCII
    co_config.CNT_GTWA = 1;
#endif
#if (CO_CONFIG_TRACE) & CO_CONFIG_TRACE_ENABLE
    co_config.CNT_TRACE = 1;
#endif
    config_ptr = &co_config;

    CO = CO_new(config_ptr, &heapMemoryUsed);
    if (CO == NULL) {
        printf("co_new fail\n");
        log_printf(LOG_CRIT, DBG_GENERAL, "CO_new(), heapMemoryUsed=", heapMemoryUsed);
        exit(EXIT_FAILURE);
    }

    CO_epoll_t epMain;
    CO_ReturnError_t err;
#define MAIN_THREAD_INTERVAL_US 100000
    err = CO_epoll_create(&epMain, MAIN_THREAD_INTERVAL_US);
    if (err != CO_ERROR_NO) {
        printf("co_epoll_create fail\n");
        log_printf(LOG_CRIT, DBG_GENERAL, "CO_epoll_create(main), err=", err);
        exit(EXIT_FAILURE);
    }
    printf("CANopen object create success.\n");
}