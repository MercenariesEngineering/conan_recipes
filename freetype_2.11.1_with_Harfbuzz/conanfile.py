from conans import ConanFile, CMake, tools
import os
import shutil

# NOTE: on linux, with static libs, if you use harfbuzz, make sure to add freetype at the end of the
# link options, otherwise you will have some symbol missing.

class FreetypeConan(ConanFile):
    _ft_nam = "freetype"
    _ft_ver = "2.11.1"
    _ft_src = "ft_src"
    _ft_bld = "ft_bld"
    _hb_nam = "harfbuzz"
    _hb_ver = "3.3.1"
    _hb_src = "hb_src"
    _hb_bld = "hb_bld"
    _libtool_version = "23.0.17"  # check docs/version.txt, this is a different version mumber!
    name = _ft_nam
    version = ""+_ft_ver+"_with_Harfbuzz"
    description = "FreeType is a freely available software library to render fonts."
    url = "http://github.com/bincrafters/conan-freetype"
    homepage = "https://www.freetype.org"
    license = "FTL", "GPL-2.0-only"
    topics = ("conan", "freetype", "fonts")
    author = "Bincrafters <bincrafters@gmail.com>"
    exports_sources = ["CMakeLists_ft.txt", "freetype.pc.in"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_png": [True, False],
        "with_zlib": [True, False],
        "with_bzip2": [True, False],
        "with_icu": [True, False]
    }
    default_options = {
        'shared': True,
        'fPIC': True,
        'with_png': True,
        'with_zlib': True,
        'with_bzip2': True,
        "with_icu": False
    }
    short_paths = True

    def requirements(self):
        if self.options.with_png:
            self.requires.add("libpng/1.6.37@mercseng/v0")
        if self.options.with_zlib:
            self.requires("zlib/1.2.11@mercseng/v0")
        if self.options.with_bzip2:
            self.requires("bzip2/1.0.8@mercseng/v0")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    #def configure(self):
    #    del self.settings.compiler.libcxx

    def source(self):
        tools.get('https://download.savannah.gnu.org/releases/{0}/{0}-{1}.tar.gz'.format(self._ft_nam, self._ft_ver))
        os.rename(self._ft_nam + "-" + self._ft_ver, self._ft_src)

        tools.get("https://github.com/harfbuzz/harfbuzz/archive/{0}.tar.gz".format(self._hb_ver))
        os.rename(self._hb_nam + "-" + self._hb_ver, self._hb_src)

        tools.replace_in_file("ft_src/CMakeLists.txt",
            "project(freetype C)",
            """project(freetype)
include(../conanbuildinfo.cmake)
conan_basic_setup()""")

        tools.replace_in_file("ft_src/CMakeLists.txt",
            "set(BASE_SRCS",
            """set(BASE_SRCS
../hb_src/src/harfbuzz.cc"""
            )


        tools.replace_in_file("ft_src/CMakeLists.txt",
            """if (HARFBUZZ_FOUND)
  string(REGEX REPLACE
    "/\\\\* +(#define +FT_CONFIG_OPTION_USE_HARFBUZZ) +\\\\*/" "\\\\1"
    FTOPTION_H "${FTOPTION_H}")
endif ()""",
            """if (1) # HARFBUZZ_FOUND


  string(REGEX REPLACE
    "/\\\\* +(#define +FT_CONFIG_OPTION_USE_HARFBUZZ) +\\\\*/" "\\\\1"
    FTOPTION_H "${FTOPTION_H}")





## EXTRACTED FROM HARFBUZZ CMAKE

set(project_headers  hb-aat-layout.h hb-aat.h hb-blob.h hb-buffer.h hb-common.h hb-deprecated.h hb-draw.h hb-face.h hb-font.h hb-map.h hb-ot-color.h hb-ot-deprecated.h hb-ot-font.h hb-ot-layout.h hb-ot-math.h hb-ot-meta.h hb-ot-metrics.h hb-ot-name.h hb-ot-shape.h hb-ot-var.h hb-ot.h hb-set.h hb-shape-plan.h hb-shape.h hb-unicode.h hb-version.h hb.h)
include_directories(${PROJECT_SOURCE_DIR}/../hb_src/src)

## Functions and headers
include (CheckFunctionExists)
include (CheckIncludeFile)
macro (check_funcs) # Similar to AC_CHECK_FUNCS of autotools
  foreach (func_name ${ARGN})
    string(TOUPPER ${func_name} definition_to_add)
    check_function_exists(${func_name} HAVE_${definition_to_add})
    if (${HAVE_${definition_to_add}})
      add_definitions(-DHAVE_${definition_to_add})
    endif ()
  endforeach ()
endmacro ()
if (UNIX)
  list(APPEND CMAKE_REQUIRED_LIBRARIES m)
endif ()
check_funcs(atexit mprotect sysconf getpagesize mmap isatty roundf)
check_include_file(unistd.h HAVE_UNISTD_H)
if (${HAVE_UNISTD_H})
  add_definitions(-DHAVE_UNISTD_H)
endif ()
check_include_file(sys/mman.h HAVE_SYS_MMAN_H)
if (${HAVE_SYS_MMAN_H})
  add_definitions(-DHAVE_SYS_MMAN_H)
endif ()
check_include_file(stdbool.h HAVE_STDBOOL_H)
if (${HAVE_STDBOOL_H})
  add_definitions(-DHAVE_STDBOOL_H)
endif ()

add_definitions(-DHAVE_FREETYPE=1)

if (MSVC)
  add_definitions(-wd4244 -wd4267 -D_CRT_SECURE_NO_WARNINGS -D_CRT_NONSTDC_NO_WARNINGS)
endif ()


if (HB_HAVE_ICU)
  add_definitions(-DHAVE_ICU)

  # https://github.com/WebKit/webkit/blob/master/Source/cmake/FindICU.cmake
  find_package(PkgConfig)
  pkg_check_modules(PC_ICU QUIET icu-uc)

  find_path(ICU_INCLUDE_DIR NAMES unicode/utypes.h HINTS ${PC_ICU_INCLUDE_DIRS} ${PC_ICU_INCLUDEDIR})
  find_library(ICU_LIBRARY NAMES libicuuc cygicuuc cygicuuc32 icuuc HINTS ${PC_ICU_LIBRARY_DIRS} ${PC_ICU_LIBDIR})

  include_directories(${ICU_INCLUDE_DIR})

  list(APPEND project_headers hb-icu.h)

  list(APPEND THIRD_PARTY_LIBS ${ICU_LIBRARY})

  mark_as_advanced(ICU_INCLUDE_DIR ICU_LIBRARY)
endif ()



## Atomic ops availability detection
file(WRITE "${PROJECT_BINARY_DIR}/try_compile_intel_atomic_primitives.c"
"       void memory_barrier (void) { __sync_synchronize (); }
        int atomic_add (int *i) { return __sync_fetch_and_add (i, 1); }
        int mutex_trylock (int *m) { return __sync_lock_test_and_set (m, 1); }
        void mutex_unlock (int *m) { __sync_lock_release (m); }
        int main () { return 0; }
")
try_compile(HB_HAVE_INTEL_ATOMIC_PRIMITIVES
  ${PROJECT_BINARY_DIR}/try_compile_intel_atomic_primitives
  ${PROJECT_BINARY_DIR}/try_compile_intel_atomic_primitives.c)
if (HB_HAVE_INTEL_ATOMIC_PRIMITIVES)
  add_definitions(-DHAVE_INTEL_ATOMIC_PRIMITIVES)
endif ()


if (CMAKE_CXX_COMPILER_ID STREQUAL "Clang" OR CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    # Make sure we don't link to libstdc++
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-rtti -fno-exceptions")
    set (CMAKE_CXX_IMPLICIT_LINK_LIBRARIES "m") # libm
    set (CMAKE_CXX_IMPLICIT_LINK_DIRECTORIES "")
    #set_target_properties(harfbuzz PROPERTIES LINKER_LANGUAGE C)

    # No threadsafe statics as we do it ourselves
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-threadsafe-statics")
endif ()

if (BUILD_SHARED_LIBS AND WIN32 AND NOT MINGW)
  add_definitions("-DHB_DLL_EXPORT")
endif ()

foreach(ITEM ${project_headers})
  install(FILES "../hb_src/src/${ITEM}" DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/freetype2/")
endforeach()

### END HARFBUZZ INSERTION

endif ()""")



    def _patch_msvc_mt(self):
        if self.settings.os == "Windows" and \
           self.settings.compiler == "Visual Studio" and \
           "MT" in self.settings.compiler.runtime:
            header_file = os.path.join(self._ft_src, "include", "freetype", "config", "ftconfig.h")
            tools.replace_in_file(header_file, "#ifdef _MSC_VER", "#if 0")

    def _configure_cmake(self):
        cmake = CMake(self)
        system_libraries = ''
        if self.settings.os == 'Linux':
            system_libraries = '-lm'
        cmake.definitions["PC_SYSTEM_LIBRARIES"] = system_libraries
        cmake.definitions["PC_FREETYPE_LIBRARY"] = '-lfreetyped' if self.settings.build_type == 'Debug' else '-lfreetype'

        if self.options.with_png:
            cmake.definitions["PC_PNG_LIBRARY"] = '-l%s' % self.deps_cpp_info['libpng'].libs[0]
        else:
            cmake.definitions["PC_PNG_LIBRARY"] = ''

        if self.options.with_zlib:
            cmake.definitions["PC_ZLIB_LIBRARY"] = '-l%s' % self.deps_cpp_info['zlib'].libs[0]
        else:
            cmake.definitions["PC_ZLIB_LIBRARY"] = ''

        if self.options.with_bzip2:
            cmake.definitions["PC_BZIP2_LIBRARY"] = '-l%s' % self.deps_cpp_info['bzip2'].libs[0]
        else:
            cmake.definitions["PC_BZIP2_LIBRARY"] = ''

        cmake.definitions["PROJECT_VERSION"] = self._libtool_version
        cmake.definitions["FT_WITH_ZLIB"] = self.options.with_zlib
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_ZLIB"] = not self.options.with_zlib
        cmake.definitions["FT_WITH_PNG"] = self.options.with_png
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_PNG"] = not self.options.with_png
        cmake.definitions["FT_WITH_BZIP2"] = self.options.with_bzip2
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_BZip2"] = not self.options.with_bzip2

        cmake.definitions["FT_DISABLE_HARFBUZZ"] = True
        cmake.definitions["FT_WITH_HARFBUZZ"] = False

        cmake.definitions["HB_HAVE_FREETYPE"] = True
        cmake.definitions["HB_BUILD_UTILS"] = False
        cmake.definitions["HB_BUILD_SUBSET"] = False
        cmake.definitions["HB_HAVE_ICU"] = self.options.with_icu
        cmake.definitions["CMAKE_PREFIX_PATH"] = self.package_folder+"/lib"
        cmake.definitions["CMAKE_INCLUDE_PATH"] = self.package_folder+"/include"

        if self.options.with_icu:
            cmake.definitions["CMAKE_CXX_STANDARD"] = "17"

        cmake.configure(source_dir="../"+self._ft_src, build_dir=self._ft_bld)
        return cmake

    #def _configure_cmake_ft_2(self, cmake):
    #    cmake.definitions["FT_WITH_HARFBUZZ"] = True
    #    cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_HarfBuzz"] = False
    #    cmake.definitions["HARFBUZZ_ROOT"] = self.package_folder
    #    cmake.definitions["INCLUDE_DIRS_HARFBUZZ"] = self.package_folder+"/include"
    #    cmake.definitions["LIB_DIRS_HARFBUZZ"] = self.package_folder+"/lib"
    #    cmake.definitions["CMAKE_MODULE_PATH"] = ".."
    #    cmake.configure(source_dir="../"+self._ft_src, build_dir=self._ft_bld)
    #    return cmake
    #
    #def _configure_cmake_hb(self):
    #    cmake = CMake(self)
    #    cmake.definitions["HB_HAVE_FREETYPE"] = True
    #    cmake.definitions["HB_BUILD_UTILS"] = False
    #    cmake.definitions["HB_BUILD_SUBSET"] = False
    #    cmake.definitions["HB_HAVE_ICU"] = self.options.with_icu
    #    cmake.definitions["CMAKE_PREFIX_PATH"] = self.package_folder+"/lib"
    #    cmake.definitions["CMAKE_INCLUDE_PATH"] = self.package_folder+"/include"
    #
    #    if self.options.with_icu:
    #        cmake.definitions["CMAKE_CXX_STANDARD"] = "17"
    #
    #    cmake.configure(source_dir="../"+self._hb_src, build_dir=self._hb_bld)
    #    return cmake

    def build(self):
        self._patch_msvc_mt()
        cmake = self._configure_cmake()
        cmake.build()
        cmake.install()
        self._make_freetype_config()

        #cmake_hb = self._configure_cmake_hb()
        #cmake_hb.build()
        #cmake_hb.install()
        #
        #self._configure_cmake_ft_2(cmake_ft)
        #cmake_ft.build()

    def _make_freetype_config(self):
        freetype_config_in = os.path.join(self._ft_src, "builds", "unix", "freetype-config.in")
        if not os.path.isdir(os.path.join(self.package_folder, "bin")):
            os.makedirs(os.path.join(self.package_folder, "bin"))
        freetype_config = os.path.join(self.package_folder, "bin", "freetype-config")
        shutil.copy(freetype_config_in, freetype_config)
        libs = "-lfreetyped" if self.settings.build_type == "Debug" else "-lfreetype"
        staticlibs = "-lm %s" % libs if self.settings.os == "Linux" else libs
        tools.replace_in_file(freetype_config, r"%PKG_CONFIG%", r"/bin/false")  # never use pkg-config
        tools.replace_in_file(freetype_config, r"%prefix%", r"$conan_prefix")
        tools.replace_in_file(freetype_config, r"%exec_prefix%", r"$conan_exec_prefix")
        tools.replace_in_file(freetype_config, r"%includedir%", r"$conan_includedir")
        tools.replace_in_file(freetype_config, r"%libdir%", r"$conan_libdir")
        tools.replace_in_file(freetype_config, r"%ft_version%", r"$conan_ftversion")
        tools.replace_in_file(freetype_config, r"%LIBSSTATIC_CONFIG%", r"$conan_staticlibs")
        tools.replace_in_file(freetype_config, r"-lfreetype", libs)
        tools.replace_in_file(freetype_config, r"export LC_ALL", """export LC_ALL
BINDIR=$(dirname $0)
conan_prefix=$(dirname $BINDIR)
conan_exec_prefix=${{conan_prefix}}/bin
conan_includedir=${{conan_prefix}}/include
conan_libdir=${{conan_prefix}}/lib
conan_ftversion={version}
conan_staticlibs="{staticlibs}"
""".format(version=self._libtool_version, staticlibs=staticlibs))

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self._make_freetype_config()

    @staticmethod
    def _chmod_plus_x(filename):
        if os.name == 'posix':
            os.chmod(filename, os.stat(filename).st_mode | 0o111)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            if self.options.shared:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
            else:
                self.cpp_info.libs = ["freetype"]
            self.cpp_info.system_libs.append("m")
        if self.settings.compiler == 'Visual Studio' and not self.options.shared:
            self.cpp_info.system_libs.extend(["dwrite", "rpcrt4", "usp10"])
        self.cpp_info.includedirs.append(os.path.join("include", "freetype2"))
        self.cpp_info.includedirs.append(os.path.join("include", "harfbuzz"))
        freetype_config = os.path.join(self.package_folder, "bin", "freetype-config")
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.env_info.FT2_CONFIG = freetype_config
        self.user_info.LIBTOOL_VERSION = self._libtool_version
        self._chmod_plus_x(freetype_config)
        self.cpp_info.names['cmake_find_package'] = 'Freetype'
        self.cpp_info.names['cmake_find_package_multi'] = 'Freetype'
        self.cpp_info.names['pkg_config'] = 'freetype2'
