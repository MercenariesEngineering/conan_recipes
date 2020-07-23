from conans import ConanFile, CMake, tools
import os

class USDConan(ConanFile):
    name = "USD"
    version = "20.02"
    license = ""
    url = "https://graphics.pixar.com/usd/docs/index.html"
    description = "Universal scene description"
    license = "Modified Apache 2.0 License"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    requires = "Alembic/1.7.3@pierousseau/stable", "boost/1.64.0@conan/stable", "hdf5/1.10.1@pierousseau/stable", "IlmBase/2.2.0@pierousseau/stable", "materialx/1.36.3@pierousseau/stable", "OpenImageIO/1.6.18@pierousseau/stable", "OpenColorIO/1.1.1@pierousseau/stable", "ptex/2.3.2@pierousseau/stable", "TBB/2019_U6@pierousseau/stable", "zlib/1.2.11@conan/stable"
    default_options = "shared=True", "fPIC=True", "*:shared=False", "TBB:shared=True", "*:fPIC=True"
    generators = "cmake"
    short_paths = True

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        # https://github.com/PixarAnimationStudios/USD/archive/v20.02.tar.gz
        filename = "v20.02.tar.gz"
        tools.download("https://github.com/PixarAnimationStudios/USD/archive/%s" % filename, filename)
        tools.unzip(filename)
        os.unlink(filename)
        os.rename("USD-20.02", "USD-%s" % self.version)

        # setup conan for cmake
        tools.replace_in_file("USD-%s/CMakeLists.txt" % self.version, "project(usd)",
                              """project(usd)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

IF (DEFINED HDF5_ROOT)
    MESSAGE(STATUS "Using HDF5_ROOT: ${HDF5_ROOT}")
    # set HDF5_ROOT in the env so FindHDF5.cmake can find it
    SET(ENV{HDF5_ROOT} ${HDF5_ROOT})
ENDIF()
SET(HDF5_USE_STATIC_LIBRARIES ${USE_STATIC_HDF5})
""")

        tools.replace_in_file("USD-%s/pxr/usd/plugin/usdAbc/CMakeLists.txt" % self.version, """${OPENEXR_Iex_LIBRARY}""", """${ILMBASE_Iex_LIBRARY}""")
        tools.replace_in_file("USD-%s/pxr/usd/plugin/usdAbc/CMakeLists.txt" % self.version, """${OPENEXR_Half_LIBRARY}""", """${ILMBASE_Half_LIBRARY}""")

        # keeping this would mess up dllimport directives in MSVC
        tools.replace_in_file("USD-%s/cmake/defaults/msvcdefaults.cmake" % self.version, """_add_define("BOOST_ALL_DYN_LINK")""", "")
        # nope, openEXR is not built as a dll.
        tools.replace_in_file("USD-%s/cmake/defaults/msvcdefaults.cmake" % self.version, """_add_define("OPENEXR_DLL")""", "")

        if self.settings.os == "Linux":
            tools.replace_in_file("USD-%s/CMakeLists.txt" % self.version,
            """set(CMAKE_CXX_FLAGS "${_PXR_CXX_FLAGS} ${CMAKE_CXX_FLAGS}")""", 
"""set(CMAKE_CXX_FLAGS "${_PXR_CXX_FLAGS} ${CMAKE_CXX_FLAGS}")
set(CMAKE_CXX_STANDARD_LIBRARIES "-static-libgcc -static-libstdc++ ${CMAKE_CXX_STANDARD_LIBRARIES}")
""")

        tools.replace_in_file("USD-%s/cmake/modules/FindMaterialX.cmake" % self.version, """documents/Libraries""", """libraries/stdlib""")

    def _configure_cmake(self):
        cmake = CMake(self)

        if ("fPIC" in self.options.fields and self.options.fPIC == True):
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = True

        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            cmake.definitions["TBB_USE_DEBUG_BUILD"] = True # link against tbb_debug.lib/a

        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared

        cmake.definitions["PXR_BUILD_ALEMBIC_PLUGIN"] = True
        cmake.definitions["PXR_ENABLE_HDF5_SUPPORT"] = True
        cmake.definitions["USE_STATIC_HDF5"] = True

        cmake.definitions["PXR_BUILD_MATERIALX_PLUGIN"] = True
        cmake.definitions["PXR_ENABLE_OSL_SUPPORT"] = False

        cmake.definitions["PXR_BUILD_IMAGING"] = False
        #cmake.definitions["PXR_ENABLE_PTEX_SUPPORT"] = True
        #cmake.definitions["DPXR_ENABLE_OPENVDB_SUPPORT"] = True
        #cmake.definitions["DPXR_BUILD_EMBREE_PLUGIN"] = True
        #cmake.definitions["DPXR_BUILD_PRMAN_PLUGIN"] = True
        #cmake.definitions["PXR_BUILD_OPENIMAGEIO_PLUGIN"] = True
        #cmake.definitions["PXR_BUILD_OPENCOLORIO_PLUGIN"] = True

        cmake.definitions["DPXR_BUILD_USD_IMAGING"] = False
        cmake.definitions["PXR_BUILD_USDVIEW"] = False

        cmake.definitions["PXR_BUILD_DOCUMENTATION"] = False
        cmake.definitions["PXR_BUILD_TESTS"] = False

        cmake.definitions["PXR_BUILD_KATANA_PLUGIN"] = False
        cmake.definitions["PXR_BUILD_DRACO_PLUGIN"] = False
        cmake.definitions["PXR_BUILD_HOUDINI_PLUGIN"] = False

        cmake.definitions["PXR_ENABLE_GL_SUPPORT"] = False
        cmake.definitions["PXR_ENABLE_PYTHON_SUPPORT"] = False

        cmake.configure(source_dir="USD-%s" % self.version)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install() # install will package some files better than explicit copy

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.bindirs = ["lib", "bin"] # This will put "lib" folder in the path, which we need to find the plugins.
        self.cpp_info.defines = ["NOMINMAX", "YY_NO_UNISTD_H"]
        
        if self.settings.build_type == "Debug":
            self.cpp_info.defines.append("BUILD_OPTLEVEL_DEV")
        
        if self.options.shared == "False":
            self.cpp_info.defines.append("PXR_STATIC=1")
