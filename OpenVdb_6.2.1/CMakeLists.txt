cmake_minimum_required(VERSION 2.8.12)

project(cmake_wrapper)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

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

# Forward this definition to code, otherwise OPENEXR_DLL will get defined
if (OPENVDB_OPENEXR_STATICLIB)
  add_definitions(-DOPENVDB_OPENEXR_STATICLIB)
endif ()

# We also want the dependencies defines:
conan_global_flags()

# We don't want to use the FindPackage file provided by Jemalloc, because it doesn't define a Jemalloc::jemalloc target.
list (REMOVE_ITEM CMAKE_MODULE_PATH "${CONAN_JEMALLOC_ROOT}")
list (REMOVE_ITEM CMAKE_MODULE_PATH "${CONAN_JEMALLOC_ROOT}/")

include(CMakeLists_original.txt)
