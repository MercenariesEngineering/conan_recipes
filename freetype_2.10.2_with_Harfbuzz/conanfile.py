from conans import ConanFile, CMake, tools
import os
import shutil

# NOTE: on linux, with static libs, if you use harfbuzz, make sure to add freetype at the end of the
# link options, otherwise you will have some symbol missing.

class FreetypeConan(ConanFile):
    _ft_nam = "freetype"
    _ft_ver = "2.10.2"
    _ft_src = "ft_src"
    _ft_bld = "ft_bld"
    _hb_nam = "harfbuzz"
    _hb_ver = "2.6.7"
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
    short_paths = True

    def requirements(self):
        if self.options.with_png:
            self.requires.add("libpng/1.6.37@mercseng/version-0")
        if self.options.with_zlib:
            self.requires("zlib/1.2.11@mercseng/version-0")
        if self.options.with_bzip2:
            self.requires("bzip2/1.0.8@mercseng/version-0")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    #def configure(self):
    #    del self.settings.compiler.libcxx

    def _source_freetype(self):
        source_url = "https://download.savannah.gnu.org/releases/"
        #version = self._ft_ver[:-2]
        archive_file = '{0}-{1}.tar.gz'.format(self._ft_nam, self._ft_ver)
        source_file = '{0}/{1}/{2}'.format(source_url, self._ft_nam, archive_file)
        tools.get(source_file)
        os.rename('{0}-{1}'.format(self._ft_nam, self._ft_ver), self._ft_src)

        tools.replace_in_file("ft_src/CMakeLists.txt",
            "project(freetype C)",
            """project(freetype C)
include(../conanbuildinfo.cmake)
conan_basic_setup()""")

    def _source_harfbuzz(self):
        source_url = "https://github.com/harfbuzz/harfbuzz"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self._hb_ver))
        extracted_dir = self._hb_nam + "-" + self._hb_ver
        os.rename(extracted_dir, self._hb_src)

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

        cmake.definitions["PROJECT_VERSION"] = self._libtool_version
        cmake.definitions["FT_WITH_ZLIB"] = self.options.with_zlib
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_ZLIB"] = not self.options.with_zlib
        cmake.definitions["FT_WITH_PNG"] = self.options.with_png
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_PNG"] = not self.options.with_png
        cmake.definitions["FT_WITH_BZIP2"] = self.options.with_bzip2
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_BZip2"] = not self.options.with_bzip2
        cmake.definitions["FT_WITH_HARFBUZZ"] = False
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_HarfBuzz"] = True
        cmake.configure(source_dir="../"+self._ft_src, build_dir=self._ft_bld)
        return cmake

    def _configure_cmake_ft_2(self, cmake):
        cmake.definitions["FT_WITH_HARFBUZZ"] = True
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_HarfBuzz"] = False
        cmake.definitions["HARFBUZZ_ROOT"] = self.package_folder
        cmake.definitions["INCLUDE_DIRS_HARFBUZZ"] = self.package_folder+"/include"
        cmake.definitions["LIB_DIRS_HARFBUZZ"] = self.package_folder+"/lib"
        cmake.definitions["CMAKE_MODULE_PATH"] = ".."
        cmake.configure(source_dir="../"+self._ft_src, build_dir=self._ft_bld)
        return cmake

    def _configure_cmake_hb(self):
        cmake = CMake(self)
        cmake.definitions["HB_HAVE_FREETYPE"] = True
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
            
            if self.options.shared == False:
                self.cpp_info.libs = ["freetype", "harfbuzz"]
            self.cpp_info.system_libs.append("m")
            self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
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
