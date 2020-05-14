import os
import shutil
from conans import ConanFile, CMake, tools

class USDConan(ConanFile):
    name = "USD"
    version = "20.02"
    license = ""
    url = "https://graphics.pixar.com/usd/docs/index.html"
    description = "Universal scene description"
    license = "Modified Apache 2.0 License"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "debug_symbols": [True, False]}
    default_options = "shared=True", "fPIC=True", "debug_symbols=False", "*:shared=False", "TBB:shared=True", "*:fPIC=True"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    short_paths = True
    _source_subfolder = "source_subfolder"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("Alembic/1.7.12@mercseng/stable")
        self.requires("boost/1.64.0@conan/stable")
        self.requires("hdf5/1.10.1@pierousseau/stable")
        self.requires("materialx/1.36.3@pierousseau/stable")
        self.requires("OpenImageIO/1.6.18@mercseng/stable")
        self.requires("OpenColorIO/1.1.1@mercseng/stable")
        self.requires("ptex/2.3.2@pierousseau/stable")
        self.requires("TBB/2019_U6@pierousseau/stable")
        self.requires("zlib/1.2.11")

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/PixarAnimationStudios/USD/archive/v%s.tar.gz" % self.version)
        os.rename("USD-%s" % self.version, self._source_subfolder)
 
        # point to HDF5
        tools.replace_in_file("%s/CMakeLists.txt" % self._source_subfolder, "project(usd)",
                              """project(usd)

IF (DEFINED HDF5_ROOT)
    MESSAGE(STATUS "Using HDF5_ROOT: ${HDF5_ROOT}")
    # set HDF5_ROOT in the env so FindHDF5.cmake can find it
    SET(ENV{HDF5_ROOT} ${HDF5_ROOT})
ENDIF()
""")

        # Keeping this would mess up dllimport directives in MSVC
        tools.replace_in_file("%s/cmake/defaults/msvcdefaults.cmake" % self._source_subfolder, """_add_define("BOOST_ALL_DYN_LINK")""", "")
        # Nope, openEXR is not necessarily built as a dll. If it actually is, it will be added back by OpenEXR recipe anyway.
        tools.replace_in_file("%s/cmake/defaults/msvcdefaults.cmake" % self._source_subfolder, """_add_define("OPENEXR_DLL")""", "")
        # Alembic plugin needs to link against OpenExr Math library.
        tools.replace_in_file("%s/pxr/usd/plugin/usdAbc/CMakeLists.txt" % self._source_subfolder, """${OPENEXR_Half_LIBRARY}""", "${OPENEXR_Half_LIBRARY} ${OPENEXR_Imath_LIBRARY}")

        # Linux: Add flags -static-libgcc -static-libstdc++
        if self.settings.os == "Linux":
            tools.replace_in_file("%s/CMakeLists.txt" % self._source_subfolder,
            """set(CMAKE_CXX_FLAGS "${_PXR_CXX_FLAGS} ${CMAKE_CXX_FLAGS}")""", 
"""set(CMAKE_CXX_FLAGS "${_PXR_CXX_FLAGS} ${CMAKE_CXX_FLAGS}")
set(CMAKE_CXX_STANDARD_LIBRARIES "-static-libgcc -static-libstdc++ ${CMAKE_CXX_STANDARD_LIBRARIES}")
""")
        # Fix FindMaterialX
        tools.replace_in_file("%s/cmake/modules/FindMaterialX.cmake" % self._source_subfolder, """documents/Libraries""", """libraries/stdlib""")

        # Add a wrapper CMakeLists.txt file which initializes conan before executing the real CMakeLists.txt
        os.rename(os.path.join(self._source_subfolder, "CMakeLists.txt"), os.path.join(self._source_subfolder, "CMakeLists_original.txt"))
        shutil.copy("CMakeLists.txt", os.path.join(self._source_subfolder, "CMakeLists.txt"))

    def _configure_cmake(self):
        """Configure CMake."""
        cmake = CMake(self)

        if self.options.debug_symbols and self.settings.build_type=="Release":
            cmake.build_type = 'RelWithDebInfo'

        definition_dict = {
            "BUILD_SHARED_LIBS":self.options.shared,
            "PXR_BUILD_ALEMBIC_PLUGIN":True,
            "PXR_BUILD_DOCUMENTATION": False,
            "PXR_BUILD_DRACO_PLUGIN": False,
            "PXR_BUILD_EMBREE_PLUGIN": False,
            "PXR_BUILD_HOUDINI_PLUGIN": False,
            "PXR_BUILD_IMAGING":False,
            "PXR_BUILD_KATANA_PLUGIN": False,
            "PXR_BUILD_MATERIALX_PLUGIN":True,
            "PXR_BUILD_OPENCOLORIO_PLUGIN": True,
            "PXR_BUILD_OPENIMAGEIO_PLUGIN": True,
            "PXR_BUILD_PRMAN_PLUGIN": False,
            "PXR_BUILD_TESTS": False,
            "PXR_BUILD_USD_IMAGING": False,
            "PXR_BUILD_USDVIEW": False,
            "PXR_ENABLE_GL_SUPPORT": False,
            "PXR_ENABLE_HDF5_SUPPORT":True,
            "PXR_ENABLE_OPENVDB_SUPPORT": True,
            "PXR_ENABLE_OSL_SUPPORT":False,
            "PXR_ENABLE_PTEX_SUPPORT": True,
            "PXR_ENABLE_PYTHON_SUPPORT": False,
            "TBB_USE_DEBUG_BUILD": self.settings.build_type == "Debug",
            "HDF5_USE_STATIC_LIBRARIES": not self.options["hdf5"].shared
        }

        cmake.configure(defs = definition_dict, source_folder = self._source_subfolder)
        return cmake

    def build(self):
        """Build the elements to package."""
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        """Assemble the package."""
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.bindirs = ["lib", "bin"] # This will put "lib" folder in the path, which we need to find the plugins.
        self.cpp_info.defines = ["NOMINMAX", "YY_NO_UNISTD_H"]
        
        if self.settings.build_type == "Debug":
            self.cpp_info.defines.append("BUILD_OPTLEVEL_DEV")
        
        if self.options.shared == "False":
            self.cpp_info.defines.append("PXR_STATIC=1")
