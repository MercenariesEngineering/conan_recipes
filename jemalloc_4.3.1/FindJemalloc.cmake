# - Try to find jemalloc headers and libraries.
#
# Usage of this module as follows:
#
#     find_package(JeMalloc)
#
# Variables used by this module, they can change the default behaviour and need
# to be set before calling find_package:
#
#  JEMALLOC_ROOT_DIR Set this variable to the root installation of
#                    jemalloc if the module has problems finding
#                    the proper installation path.
#
# Variables defined by this module:
#
#  JEMALLOC_FOUND             System has jemalloc libs/headers
#  JEMALLOC_LIBRARIES         The jemalloc library/libraries
#  JEMALLOC_INCLUDE_DIR       The location of jemalloc headers

find_path(JEMALLOC_ROOT_DIR
    NAMES include/jemalloc/jemalloc.h
)

find_library(JEMALLOC_LIBRARIES
    NAMES jemalloc_pic jemalloc
    HINTS ${JEMALLOC_ROOT_DIR}/lib
)

find_path(JEMALLOC_INCLUDE_DIR
    NAMES jemalloc/jemalloc.h
    HINTS ${JEMALLOC_ROOT_DIR}/include
)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(jemalloc DEFAULT_MSG
    JEMALLOC_LIBRARIES
    JEMALLOC_INCLUDE_DIR
)
find_package (Threads)

if(jemalloc_FOUND)
    add_library(jemalloc STATIC IMPORTED)
	set_property(TARGET jemalloc PROPERTY IMPORTED_LOCATION "${JEMALLOC_LIBRARIES}")
	if(WIN32)
        set_property(TARGET jemalloc PROPERTY INTERFACE_INCLUDE_DIRECTORIES "${JEMALLOC_INCLUDE_DIR};${JEMALLOC_INCLUDE_DIR}/msvc_compat")
    endif()
    set_property(TARGET jemalloc PROPERTY INTERFACE_LINK_LIBRARIES "Threads::Threads")
endif()

mark_as_advanced(
    JEMALLOC_ROOT_DIR
    JEMALLOC_LIBRARIES
    JEMALLOC_INCLUDE_DIR
)
