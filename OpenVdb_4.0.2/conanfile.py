from conans import ConanFile, CMake, tools
import os

class OpenVdbConan(ConanFile):
    name = "OpenVdb"
    version = "4.0.2"
    license = ""
    url = "https://github.com/dreamworksanimation/openvdb"
    description = "OpenVDB - Sparse volume data structure and tools http://www.openvdb.org/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    generators = "cmake"

    recipe_version="v0"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("blosc/1.11.2@mercseng/v0")
        self.requires("boost/1.73.0@mercseng/v0")
        self.requires("OpenEXR/2.5.1@mercseng/v0")
        self.requires("tbb/2020.02@mercseng/v1")
        self.requires("zlib/1.2.11@mercseng/v0")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        filename = "Release-%s.tar.gz" % self.version
        tools.download("https://github.com/dreamworksanimation/openvdb/archive/v%s.tar.gz" % self.version, filename)
        tools.untargz(filename)
        os.unlink(filename)

        if self.settings.os == "Windows" :
            boost_libs = """
set(Boost_IOSTREAMS_LIBRARY boost_iostreams)
set(Boost_SYSTEM_LIBRARY boost_system)
set(Boost_THREAD_LIBRARY boost_thread)
set(Boost_PYTHON_LIBRARY boost_python)"""
        else :
            boost_libs = """
set(Boost_IOSTREAMS_LIBRARY libboost_iostreams)
set(Boost_SYSTEM_LIBRARY libboost_system)
set(Boost_THREAD_LIBRARY libboost_thread)
set(Boost_PYTHON_LIBRARY libboost_python)"""

        tools.replace_in_file("openvdb-%s/CMakeLists.txt" % self.version, 
            "PROJECT ( OpenVDB )",
            """PROJECT ( OpenVDB )
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
set(BOOST_ROOT ${CONAN_BOOST_ROOT})
set(BOOST_LIBRARYDIR ${CONAN_BOOST_ROOT}/lib)
set(TBB_LOCATION ${CONAN_TBB_ROOT})
set(ILMBASE_LOCATION ${CONAN_OPENEXR_ROOT})
set(OPENEXR_LOCATION ${CONAN_OPENEXR_ROOT})
set(OPENVDB_BUILD_UNITTESTS OFF CACHE BOOL "unit tests")
set(OPENVDB_DISABLE_BOOST_IMPLICIT_LINKING OFF CACHE BOOL "")
set(OPENVDB_BUILD_VDB_VIEW OFF)
%s
""" % boost_libs)

        tools.replace_in_file("openvdb-%s/openvdb/CMakeLists.txt" % self.version,
            "COMPILE_FLAGS \"-DOPENVDB_PRIVATE -DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG}\"",
            "COMPILE_FLAGS \"-DOPENVDB_PRIVATE -DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG} $<$<CXX_COMPILER_ID:MSVC>:/bigobj>\"")
        tools.replace_in_file("openvdb-%s/openvdb/CMakeLists.txt" % self.version,
            "COMPILE_FLAGS \"-DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG}\"",
            "COMPILE_FLAGS \"-DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG} $<$<CXX_COMPILER_ID:MSVC>:/bigobj>\"")
        tools.replace_in_file("openvdb-%s/openvdb/CMakeLists.txt" % self.version,
            "COMPILE_FLAGS \"-DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG} -DGL_GLEXT_PROTOTYPES=1\"",
            "COMPILE_FLAGS \"-DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG} -DGL_GLEXT_PROTOTYPES=1 $<$<CXX_COMPILER_ID:MSVC>:/bigobj>\"")

        # Disable VdbViewer
        tools.replace_in_file("openvdb-%s/openvdb/CMakeLists.txt" % self.version,
            """IF ( USE_GLFW3 )""",
            """IF (OPENVDB_BUILD_VDB_VIEW AND NOT WIN32)
IF ( USE_GLFW3 )""")
        tools.replace_in_file("openvdb-%s/openvdb/CMakeLists.txt" % self.version,
            """SET ( GLFW_INCLUDE_DIRECTORY  ${GLFW_INCLUDE_DIR} CACHE STRING "GLFW include directory")
ENDIF ()""",
            """SET ( GLFW_INCLUDE_DIRECTORY  ${GLFW_INCLUDE_DIR} CACHE STRING "GLFW include directory")
ENDIF ()
ENDIF ()""")
        tools.replace_in_file("openvdb-%s/openvdb/CMakeLists.txt" % self.version,
            """FIND_PACKAGE ( GLEW REQUIRED )""",
            """IF (OPENVDB_BUILD_VDB_VIEW)
FIND_PACKAGE ( GLEW REQUIRED )
ENDIF()""")
        tools.replace_in_file("openvdb-%s/openvdb/CMakeLists.txt" % self.version,
            "IF (NOT WIN32)",
            "IF (OPENVDB_BUILD_VDB_VIEW AND NOT WIN32)")
        tools.replace_in_file("openvdb-%s/openvdb/CMakeLists.txt" % self.version,
            "IF ( NOT WIN32 )",
            "IF (OPENVDB_BUILD_VDB_VIEW AND NOT WIN32)")

        # Find Half library
        tools.replace_in_file("openvdb-%s/cmake/FindILMBase.cmake" % self.version,
            """SET ( IEX_LIBRARY_NAME       Iex-${ILMBASE_VERSION_MAJOR}_${ILMBASE_VERSION_MINOR}       )""",
            """SET ( IEX_LIBRARY_NAME       Iex-${ILMBASE_VERSION_MAJOR}_${ILMBASE_VERSION_MINOR}       )
SET ( HALF_LIBRARY_NAME       Half-${ILMBASE_VERSION_MAJOR}_${ILMBASE_VERSION_MINOR}       )""")
        tools.replace_in_file("openvdb-%s/cmake/FindILMBase.cmake" % self.version,
            """SET ( IEX_LIBRARY_NAME       Iex       )""",
            """SET ( IEX_LIBRARY_NAME       Iex       )
SET ( HALF_LIBRARY_NAME       Half)""")
        tools.replace_in_file("openvdb-%s/cmake/FindILMBase.cmake" % self.version,
            """FIND_LIBRARY ( Ilmbase_HALF_LIBRARY Half PATHS ${ILMBASE_LIBRARYDIR} )""",
            """FIND_LIBRARY ( Ilmbase_HALF_LIBRARY ${HALF_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR} )""")
        tools.replace_in_file("openvdb-%s/cmake/FindILMBase.cmake" % self.version,
            """FIND_LIBRARY ( Ilmbase_HALF_LIBRARY Half PATHS ${ILMBASE_LIBRARYDIR}""",
            """FIND_LIBRARY ( Ilmbase_HALF_LIBRARY ${HALF_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR}""")

    def configure(self):
        pass

    def build(self):
        cmake = CMake(self)

        # Explicit way:
        self.run('cmake %s/openvdb-%s %s -DCMAKE_INSTALL_PREFIX="%s"' % (self.source_folder, self.version, cmake.command_line, self.package_folder))
        self.run("cmake --build . --target openvdb_static %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include/openvdb", src="openvdb-%s/openvdb"%self.version)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.defines = ["OPENVDB_STATICLIB","OPENVDB_OPENEXR_STATICLIB","OPENVDB_USE_BLOSC","OPENVDB_3_ABI_COMPATIBLE"]
