// ref to CO_main_basic.c

#include "stdlib.h"
#include "CO_epoll_interface.h"
#include "CANopen.h"
#include <cstdio>

#include <syslog.h> //vsyslog
#include <stdarg.h> //va_start, vat_end

// for CO_driver.c
void log_printf(int priority, const char *format, ...)
{
    va_list ap;

    va_start(ap, format);
    vsyslog(priority, format, ap);
    va_end(ap);
}

using namespace std;

int main()
{
    CO_t *CO = NULL;
    CO_config_t *config_ptr = NULL;
    uint32_t heapMemoryUsed = 0;

    CO = CO_new(config_ptr, &heapMemoryUsed);
    if (CO == NULL)
    {
        log_printf(LOG_CRIT, DBG_GENERAL,
                   "CO_new(), heapMemoryUsed=", heapMemoryUsed);
        exit(EXIT_FAILURE);
    }

    CO_epoll_t epMain;
    CO_ReturnError_t err;
#define MAIN_THREAD_INTERVAL_US 100000
    err = CO_epoll_create(&epMain, MAIN_THREAD_INTERVAL_US);
    if (err != CO_ERROR_NO)
    {
        log_printf(LOG_CRIT, DBG_GENERAL,
                   "CO_epoll_create(main), err=", err);
        exit(EXIT_FAILURE);
    }
    printf("CANopen object create success.\n");
}