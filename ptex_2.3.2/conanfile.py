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
    requires = "zlib/1.2.11@mercseng/v0"
    default_options = "shared=False", "fPIC=True"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("zlib/1.2.11@mercseng/v0")

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/wdas/ptex/archive/v%s.tar.gz" % self.version)
        os.rename("ptex-%s" % self.version, self._source_subfolder)

        # Disable Pkgconfig, use conan for zlib dependency
        tools.replace_in_file("%s/CMakeLists.txt" % self._source_subfolder,
            """# Use pkg-config to create a PkgConfig::Ptex_ZLIB imported target
find_package(PkgConfig REQUIRED)
pkg_checK_modules(Ptex_ZLIB REQUIRED zlib IMPORTED_TARGET)""",
            """include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
find_package(ZLIB)""")
        tools.replace_in_file("%s/src/build/ptex-config.cmake" % self._source_subfolder,
            """# Provide PkgConfig::ZLIB to downstream dependents
find_package(PkgConfig REQUIRED)
pkg_checK_modules(Ptex_ZLIB REQUIRED zlib IMPORTED_TARGET)""",
            "")
        tools.replace_in_file("%s/src/ptex/CMakeLists.txt" % self._source_subfolder,
            """PkgConfig::Ptex_ZLIB""",
            """${ZLIB_LIBRARIES}""")    
        tools.replace_in_file("%s/src/utils/CMakeLists.txt" % self._source_subfolder,
            """PkgConfig::Ptex_ZLIB""",
            """${ZLIB_LIBRARIES}""")

        # Disable tests
        tools.replace_in_file("%s/CMakeLists.txt" % self._source_subfolder,
            """add_subdirectory(src/tests)""", "")

    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "PTEX_SHA": "1b8bc985a71143317ae9e4969fa08e164da7c2e5",
            "PTEX_VER": self.version,
            "PTEX_BUILD_SHARED_LIBS": self.options.shared,
            "PTEX_BUILD_STATIC_LIBS": not self.options.shared,
            "ZLIB_ROOT": os.path.join( self.deps_cpp_info[ "zlib" ].libdirs[ 0 ], "../" ),
        }
        if not self.options.shared:
            definition_dict["PTEX_STATIC"] = True
        #if ("fPIC" in self.options.fields and self.options.fPIC == True):
        #    definition_dict["CMAKE_POSITION_INDEPENDENT_CODE"] = True

        return definition_dict

    def build(self):
        """Build the elements to package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.build()
   
    def package(self):
        """Assemble the package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.install()

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
        if not self.options.shared:
            self.cpp_info.defines.append("PTEX_STATIC")
        
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "lib"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))