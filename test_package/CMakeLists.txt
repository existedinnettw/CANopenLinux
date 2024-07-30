cmake_minimum_required(VERSION 3.15)
project(PackageTest C CXX)

find_package(canopenlinux CONFIG REQUIRED)

add_executable(example src/example.cpp src/CO_driver.c src/OD.c)
target_link_libraries(example canopenlinux::canopenlinux)
target_include_directories(example PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
