cmake_minimum_required(VERSION 2.8.12)

project(pystring)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(MSVC OR MSVC90 OR MSVC10)
    set(MSVC ON)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

set(SOURCE_SUBFOLDER ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder)

if(CMAKE_COMPILER_IS_GNUCXX)
    message(STATUS "GCC detected, adding compile flags")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}  -g -O3 -Wall -Wshadow -Wconversion -Wcast-qual -Wformat=2")
endif(CMAKE_COMPILER_IS_GNUCXX)

add_library(pystring ${SOURCE_SUBFOLDER}/pystring.h ${SOURCE_SUBFOLDER}/pystring.cpp)
target_include_directories(pystring PUBLIC ${CMAKE_CURRENT_LIST_DIR})

install(TARGETS pystring
        ARCHIVE DESTINATION lib
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib)

install(FILES ${SOURCE_SUBFOLDER}/pystring.h DESTINATION include)