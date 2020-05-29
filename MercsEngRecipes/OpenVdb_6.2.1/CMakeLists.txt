cmake_minimum_required(VERSION 2.8.12)

project(cmake_wrapper)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

FIND_PACKAGE ( Blosc REQUIRED )
if (NOT BLOSC_blosc_LIBRARY)
    set (BLOSC_blosc_LIBRARY ${BLOSC_LIBRARY})
endif()

function(add_cloned_imported_target dst src)
    add_library(${dst} INTERFACE IMPORTED)
    foreach(name INTERFACE_LINK_LIBRARIES INTERFACE_INCLUDE_DIRECTORIES INTERFACE_COMPILE_DEFINITIONS INTERFACE_COMPILE_OPTIONS)
        get_property(value TARGET ${src} PROPERTY ${name} )
        set_property(TARGET ${dst} PROPERTY ${name} ${value})
    endforeach()
endfunction()

if (NOT TARGET Blosc::blosc)
    add_cloned_imported_target(Blosc::blosc CONAN_PKG::blosc)
endif ()

# We don't want to use the FindPackage file provided by Jemalloc, because it dosen't define a Jemalloc::jemalloc target.
list (REMOVE_ITEM CMAKE_MODULE_PATH "${CONAN_JEMALLOC_ROOT}")
list (REMOVE_ITEM CMAKE_MODULE_PATH "${CONAN_JEMALLOC_ROOT}/")

include(CMakeLists_original.txt)
