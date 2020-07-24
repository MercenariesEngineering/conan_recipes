from conans import ConanFile, CMake, tools
import os

class Ptex(ConanFile):
    name = "ptex"
    version = "2.3.2"
    license = "Apache 2.0"
    description = "Per-Face Texture Mapping for Production Rendering"
    url = "https://github.com/wdas/ptex"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    requires = "zlib/1.2.11@mercseng/version-0"
    default_options = "shared=False", "fPIC=True"
    generators = "cmake"

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        # https://github.com/wdas/ptex/archive/v2.3.2.tar.gz
        filename = "v%s.tar.gz" % self.version
        tools.download("https://github.com/wdas/ptex/archive/%s" % filename, filename)
        tools.untargz(filename)
        os.unlink(filename)

        tools.replace_in_file("ptex-%s/CMakeLists.txt" % self.version,
            """# Use pkg-config to create a PkgConfig::Ptex_ZLIB imported target
find_package(PkgConfig REQUIRED)
pkg_checK_modules(Ptex_ZLIB REQUIRED zlib IMPORTED_TARGET)""",
            """include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
find_package(ZLIB)""")
        tools.replace_in_file("ptex-%s/src/build/ptex-config.cmake" % self.version,
            """# Provide PkgConfig::ZLIB to downstream dependents
find_package(PkgConfig REQUIRED)
pkg_checK_modules(Ptex_ZLIB REQUIRED zlib IMPORTED_TARGET)""",
            "")
        tools.replace_in_file("ptex-%s/src/ptex/CMakeLists.txt" % self.version,
            """PkgConfig::Ptex_ZLIB""",
            """${ZLIB_LIBRARIES}""")    
        tools.replace_in_file("ptex-%s/src/utils/CMakeLists.txt" % self.version,
            """PkgConfig::Ptex_ZLIB""",
            """${ZLIB_LIBRARIES}""")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["PTEX_SHA"] = "1b8bc985a71143317ae9e4969fa08e164da7c2e5"
        cmake.definitions["PTEX_VER"] = self.version
        cmake.definitions["PTEX_BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["PTEX_BUILD_STATIC_LIBS"] = not self.options.shared
        cmake.definitions["ZLIB_ROOT"] = os.path.join( self.deps_cpp_info[ "zlib" ].libdirs[ 0 ], "../" )
        if ("fPIC" in self.options.fields and self.options.fPIC == True):
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = True
        #if self.settings.os == "Linux" and find_executable( "lld" ) is not None:
        #    cmake.definitions[ "CMAKE_SHARED_LINKER_FLAGS" ] = "-fuse-ld=lld"
        #    cmake.definitions[ "CMAKE_EXE_LINKER_FLAGS"    ] = "-fuse-ld=lld"
        cmake.configure(source_dir="ptex-%s" % self.version)
        cmake.build()
   
    def package(self):
        self.copy("*.h", dst="include/", keep_path=False)
        self.copy("lib/Ptex.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))