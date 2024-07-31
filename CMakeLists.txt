cmake_minimum_required(VERSION 3.15)
project(CANopenLinux C)

add_library(
  canopenlinux
  CO_driver.c
  CO_error.c
  CO_epoll_interface.c
  CO_storageLinux.c
  CANopenNode/301/CO_ODinterface.c
  CANopenNode/301/CO_NMT_Heartbeat.c
  CANopenNode/301/CO_HBconsumer.c
  CANopenNode/301/CO_Emergency.c
  CANopenNode/301/CO_SDOserver.c
  CANopenNode/301/CO_SDOclient.c
  CANopenNode/301/CO_TIME.c
  CANopenNode/301/CO_SYNC.c
  CANopenNode/301/CO_PDO.c
  CANopenNode/301/crc16-ccitt.c
  CANopenNode/301/CO_fifo.c
  CANopenNode/303/CO_LEDs.c
  CANopenNode/304/CO_GFC.c
  CANopenNode/304/CO_SRDO.c
  CANopenNode/305/CO_LSSslave.c
  CANopenNode/305/CO_LSSmaster.c
  CANopenNode/309/CO_gateway_ascii.c
  CANopenNode/storage/CO_storage.c
  CANopenNode/extra/CO_trace.c
  CANopenNode/CANopen.c)
# Static link to specific OD.h may not suit for a library, so `CO_MULTIPLE_OD`
# is raise at default.
target_compile_definitions(canopenlinux PUBLIC CO_MULTIPLE_OD)
target_include_directories(
  canopenlinux PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
                      CANopenNode $<INSTALL_INTERFACE:.>)

# APP
add_executable(canopend objdict/OD.c CO_main_basic.c)
# include OD.h, aware override co_driver_target.h
target_include_directories(
  canopend PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/objdict>)
target_link_libraries(canopend PUBLIC canopenlinux)

add_subdirectory(cocomm)

if(NOT BUILD_TESTING STREQUAL OFF)
  enable_testing()
endif()

# install library
target_sources(
  canopenlinux
  PUBLIC FILE_SET
         co_headers
         TYPE
         HEADERS
         BASE_DIRS
         "${CMAKE_CURRENT_SOURCE_DIR}/CANopenNode"
         FILES
         "CANopenNode/301/CO_Emergency.h"
         "CANopenNode/301/CO_SYNC.h"
         "CANopenNode/301/crc16-ccitt.h"
         "CANopenNode/301/CO_SDOclient.h"
         "CANopenNode/301/CO_HBconsumer.h"
         "CANopenNode/301/CO_config.h"
         "CANopenNode/301/CO_NMT_Heartbeat.h"
         "CANopenNode/301/CO_Node_Guarding.h"
         "CANopenNode/301/CO_driver.h"
         "CANopenNode/301/CO_PDO.h"
         "CANopenNode/301/CO_ODinterface.h"
         "CANopenNode/301/CO_fifo.h"
         "CANopenNode/301/CO_TIME.h"
         "CANopenNode/301/CO_SDOserver.h"
         "CANopenNode/303/CO_LEDs.h"
         "CANopenNode/304/CO_SRDO.h"
         "CANopenNode/304/CO_GFC.h"
         "CANopenNode/305/CO_LSSslave.h"
         "CANopenNode/305/CO_LSS.h"
         "CANopenNode/305/CO_LSSmaster.h"
         "CANopenNode/309/CO_gateway_ascii.h"
         "CANopenNode/extra/CO_trace.h"
         "CANopenNode/CANopen.h"
         "CANopenNode/storage/CO_storage.h"
         "CANopenNode/storage/CO_storageEeprom.h"
         "CANopenNode/storage/CO_eeprom.h"
         FILE_SET
         co_lnx_headers
         TYPE
         HEADERS
         FILES
         "CO_application.h"
         "CO_driver_target.h"
         "CO_epoll_interface.h"
         "CO_error_msgs.h"
         "CO_error.h"
         "CO_storageLinux.h")

install(
  TARGETS canopenlinux FILE_SET co_headers
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
  FILE_SET co_lnx_headers)
