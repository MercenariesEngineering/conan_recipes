cmake_minimum_required(VERSION 2.8.12)

project(cmake_wrapper)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package ( Blosc REQUIRED )
if (NOT BLOSC_blosc_LIBRARY)
	set (BLOSC_blosc_LIBRARY ${BLOSC_LIBRARY})
endif ()

include(CMakeLists_original.txt)
