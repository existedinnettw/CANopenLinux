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
target_include_directories(canopenlinux PUBLIC . CANopenNode CANopenNode/example)
add_executable(canopend CANopenNode/example/OD.c CO_main_basic.c)
target_link_libraries(canopend PRIVATE canopenlinux)
