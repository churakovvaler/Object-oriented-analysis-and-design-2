cmake_minimum_required(VERSION 3.29)
project(CompanyStructure)

set(CMAKE_CXX_STANDARD 20)

add_definitions(-D_WIN32_WINNT=0x0A00)
add_definitions(-DWINVER=0x0A00)

add_executable(CompanyStructure main.cpp)

target_link_libraries(CompanyStructure ws2_32)