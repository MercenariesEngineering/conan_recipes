#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class FreetypeConan(ConanFile):
    _ft_nam = "freetype"
    _ft_ver = "2.9.1"
    _ft_src = "ft_src"
    _ft_bld = "ft_bld"
    _hb_nam = "harfbuzz"
    _hb_ver = "2.4.0"
    _hb_src = "hb_src"
    _hb_bld = "hb_bld"
    name = _ft_nam
    version = ""+_ft_ver+"_with_Harfbuzz"
    description = "FreeType is a freely available software library to render fonts."
    url = "http://github.com/bincrafters/conan-freetype"
    homepage = "https://www.freetype.org"
    license = "FTL", "GPL-2.0-only"
    topics = ("conan", "freetype", "fonts")
    author = "Bincrafters <bincrafters@gmail.com>"
    exports = ["FindHarfBuzz.cmake"]
    exports_sources = ["CMakeLists_ft.txt", "CMakeLists_hb.txt", "freetype.pc.in"]
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
        'shared': False,
        'fPIC': True,
        'with_png': True,
        'with_zlib': True,
        'with_bzip2': True,
        "with_icu": False
    }

    def requirements(self):
        if self.options.with_png:
            self.requires.add("libpng/1.6.37@bincrafters/stable")
        if self.options.with_zlib:
            self.requires.add("zlib/1.2.11@conan/stable")
        if self.options.with_bzip2:
            self.requires.add("bzip2/1.0.6@conan/stable")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def _source_freetype(self):
        source_url = "https://download.savannah.gnu.org/releases/"
        version = self._ft_ver[:-2]
        archive_file = '{0}-{1}.tar.gz'.format(self._ft_nam, version)
        source_file = '{0}/{1}/{2}'.format(source_url, self._ft_nam, archive_file)
        sha256 = "bf380e4d7c4f3b5b1c1a7b2bf3abb967bda5e9ab480d0df656e0e08c5019c5e6"
        tools.get(source_file, sha256=sha256)
        os.rename('{0}-{1}'.format(self._ft_nam, version), self._ft_src)
        if self.settings.os == "Windows":
            pattern = 'if (WIN32 AND NOT MINGW AND BUILD_SHARED_LIBS)\n' + \
                      '  message(FATAL_ERROR "Building shared libraries on Windows needs MinGW")\n' + \
                      'endif ()\n'
            cmake_file = os.path.join(self._ft_src, 'CMakeLists.txt')
            tools.replace_in_file(cmake_file, pattern, '')

        tools.replace_in_file("ft_src/CMakeLists.txt",
            "project(freetype)",
            """project(freetype)
include(../conanbuildinfo.cmake)
conan_basic_setup()""")

    def _source_harfbuzz(self):
        source_url = "https://github.com/harfbuzz/harfbuzz"
        sha256 = "dc3132a479c8c4fa1c9dd09d433a3ab9b0d2f302f844a764d57faf1629bfb9c5"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self._hb_ver), sha256=sha256)
        extracted_dir = self._hb_nam + "-" + self._hb_ver
        os.rename(extracted_dir, self._hb_src)
        if self._hb_ver == "2.4.0":
            tools.replace_in_file("hb_src/src/hb-coretext.cc",
                "bool backward = HB_DIRECTION_IS_BACKWARD (buffer->props.direction);",
                "HB_UNUSED bool backward = HB_DIRECTION_IS_BACKWARD (buffer->props.direction);")

        tools.replace_in_file("hb_src/CMakeLists.txt",
            "project(harfbuzz)",
            """project(harfbuzz)
include(../conanbuildinfo.cmake)
conan_basic_setup()""")

    def source(self):
        self._source_freetype()
        self._source_harfbuzz()



    def _patch_msvc_mt(self):
        if self.settings.os == "Windows" and \
           self.settings.compiler == "Visual Studio" and \
           "MT" in self.settings.compiler.runtime:
            header_file = os.path.join(self._ft_src, "include", "freetype", "config", "ftconfig.h")
            tools.replace_in_file(header_file, "#ifdef _MSC_VER", "#if 0")

    def _configure_cmake_ft_1(self):
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
        cmake.definitions["PROJECT_VERSION"] = self._ft_ver
        cmake.definitions["WITH_ZLIB"] = self.options.with_zlib
        cmake.definitions["WITH_PNG"] = self.options.with_png
        cmake.definitions["WITH_BZip2"] = self.options.with_bzip2
        cmake.definitions["WITH_HARFBUZZ"] = False
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_HarfBuzz"] = True
        cmake.configure(source_dir="../"+self._ft_src, build_dir=self._ft_bld)
        return cmake

    def _configure_cmake_ft_2(self, cmake):
        cmake.definitions["WITH_HARFBUZZ"] = True
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_HarfBuzz"] = False
        cmake.definitions["HARFBUZZ_ROOT"] = self.package_folder
        cmake.definitions["CONAN_LIBS_HARFBUZZ"] = "harfbuzz"
        cmake.definitions["CONAN_LIB_DIRS_HARFBUZZ"] = self.package_folder+"/lib"
        cmake.definitions["CONAN_INCLUDE_DIRS_HARFBUZZ"] = self.package_folder+"/include"
        cmake.definitions["CMAKE_MODULE_PATH"] = ".."
        cmake.configure(source_dir="../"+self._ft_src, build_dir=self._ft_bld)
        return cmake

    def _configure_cmake_hb(self):
        cmake = CMake(self)
        cmake.definitions["HB_HAVE_FREETYPE"] = True
        cmake.definitions["HB_BUILD_TESTS"] = False
        cmake.definitions["HB_BUILD_UTILS"] = False
        cmake.definitions["HB_BUILD_SUBSET"] = False
        cmake.definitions["HB_HAVE_ICU"] = self.options.with_icu
        cmake.definitions["CMAKE_PREFIX_PATH"] = self.package_folder+"/lib"
        cmake.definitions["CMAKE_INCLUDE_PATH"] = self.package_folder+"/include"

        if self.options.with_icu:
            cmake.definitions["CMAKE_CXX_STANDARD"] = "17"

        cmake.configure(source_dir="../"+self._hb_src, build_dir=self._hb_bld)
        return cmake

    def build(self):
        self._patch_msvc_mt()
        cmake_ft = self._configure_cmake_ft_1()
        cmake_ft.build()
        cmake_ft.install()
        self._make_freetype_config()

        cmake_hb = self._configure_cmake_hb()
        cmake_hb.build()
        cmake_hb.install()

        self._configure_cmake_ft_2(cmake_ft)
        cmake_ft.build()

    def _make_freetype_config(self):
        freetype_config_in = os.path.join(self._ft_src, "builds", "unix", "freetype-config.in")
        if not os.path.isdir(os.path.join(self.package_folder, "bin")):
            os.makedirs(os.path.join(self.package_folder, "bin"))
        freetype_config = os.path.join(self.package_folder, "bin", "freetype-config")
        shutil.copy(freetype_config_in, freetype_config)
        libs = "-lfreetyped" if self.settings.build_type == "Debug" else "-lfreetype"
        staticlibs = "-lm %s" % libs if self.settings.os == "Linux" else libs
        libtool_version = "22.0.16"  # check docs/version.txt, this is a different version mumber!
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
""".format(version=libtool_version, staticlibs=staticlibs))

    def _package_ft(self):
        cmake = self._configure_cmake_ft_1()
        self._configure_cmake_ft_2(cmake)
        cmake.install()
        self._make_freetype_config()
        #self.copy("FTL.TXT", dst="licenses", src=os.path.join(self._ft_src, "docs"))
        #self.copy("GPLv2.TXT", dst="licenses", src=os.path.join(self._ft_src, "docs"))
        #self.copy("LICENSE.TXT", dst="licenses", src=os.path.join(self._ft_src, "docs"))

    def _package_hb(self):
        self.copy("FindHarfBuzz.cmake")
        #self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake_hb()
        cmake.install()

    def package(self):
        self._package_ft()
        self._package_hb()

    @staticmethod
    def _chmod_plus_x(filename):
        if os.name == 'posix':
            os.chmod(filename, os.stat(filename).st_mode | 0o111)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("m")
        if self.settings.compiler == 'Visual Studio' and not self.options.shared:
            self.cpp_info.libs.extend(["dwrite", "rpcrt4", "usp10"])
        self.cpp_info.includedirs.append(os.path.join("include", "freetype2"))
        self.cpp_info.includedirs.append(os.path.join("include", "harfbuzz"))
        freetype_config = os.path.join(self.package_folder, "bin", "freetype-config")
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.env_info.FT2_CONFIG = freetype_config
        self._chmod_plus_x(freetype_config)
