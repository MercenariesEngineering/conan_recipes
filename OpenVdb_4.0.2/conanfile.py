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

    _source_subfolder = "source_subfolder"
    recipe_version="v2"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("blosc/1.11.2@mercseng/v0")
        self.requires("boost/1.73.0@mercseng/v1")
        self.requires("OpenEXR/2.5.1@mercseng/v0")
        self.requires("tbb/2020.02@mercseng/v2")
        self.requires("zlib/1.2.11@mercseng/v0")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        tools.get("https://github.com/dreamworksanimation/openvdb/archive/v%s.tar.gz" % self.version)
        os.rename("openvdb-{}".format(self.version), self._source_subfolder)

        tools.replace_in_file("%s/CMakeLists.txt" % self._source_subfolder, 
            "PROJECT ( OpenVDB )",
            """PROJECT ( OpenVDB )
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
set(BOOST_ROOT ${CONAN_BOOST_ROOT})
set(BOOST_LIBRARYDIR ${CONAN_BOOST_ROOT}/lib)
set(TBB_LOCATION ${CONAN_TBB_ROOT})
set(ILMBASE_LOCATION ${CONAN_OPENEXR_ROOT})
set(OPENEXR_LOCATION ${CONAN_OPENEXR_ROOT})
""")

        tools.replace_in_file("%s/openvdb/CMakeLists.txt" % self._source_subfolder,
            "COMPILE_FLAGS \"-DOPENVDB_PRIVATE -DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG}\"",
            "COMPILE_FLAGS \"-DOPENVDB_PRIVATE -DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG} $<$<CXX_COMPILER_ID:MSVC>:/bigobj>\"")
        tools.replace_in_file("%s/openvdb/CMakeLists.txt" % self._source_subfolder,
            "COMPILE_FLAGS \"-DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG}\"",
            "COMPILE_FLAGS \"-DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG} $<$<CXX_COMPILER_ID:MSVC>:/bigobj>\"")
        tools.replace_in_file("%s/openvdb/CMakeLists.txt" % self._source_subfolder,
            "COMPILE_FLAGS \"-DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG} -DGL_GLEXT_PROTOTYPES=1\"",
            "COMPILE_FLAGS \"-DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG} -DGL_GLEXT_PROTOTYPES=1 $<$<CXX_COMPILER_ID:MSVC>:/bigobj>\"")

        # Disable VdbViewer
        tools.replace_in_file("%s/openvdb/CMakeLists.txt" % self._source_subfolder,
            """IF ( USE_GLFW3 )""",
            """IF (OPENVDB_BUILD_VDB_VIEW AND NOT WIN32)
IF ( USE_GLFW3 )""")
        tools.replace_in_file("%s/openvdb/CMakeLists.txt" % self._source_subfolder,
            """SET ( GLFW_INCLUDE_DIRECTORY  ${GLFW_INCLUDE_DIR} CACHE STRING "GLFW include directory")
ENDIF ()""",
            """SET ( GLFW_INCLUDE_DIRECTORY  ${GLFW_INCLUDE_DIR} CACHE STRING "GLFW include directory")
ENDIF ()
ENDIF ()""")
        tools.replace_in_file("%s/openvdb/CMakeLists.txt" % self._source_subfolder,
            """FIND_PACKAGE ( GLEW REQUIRED )""",
            """IF (OPENVDB_BUILD_VDB_VIEW)
FIND_PACKAGE ( GLEW REQUIRED )
ENDIF()""")
        tools.replace_in_file("%s/openvdb/CMakeLists.txt" % self._source_subfolder,
            "IF (NOT WIN32)",
            "IF (OPENVDB_BUILD_VDB_VIEW AND NOT WIN32)")
        tools.replace_in_file("%s/openvdb/CMakeLists.txt" % self._source_subfolder,
            "IF ( NOT WIN32 )",
            "IF (OPENVDB_BUILD_VDB_VIEW AND NOT WIN32)")

        # Find Half library
        tools.replace_in_file("%s/cmake/FindILMBase.cmake" % self._source_subfolder,
            """SET ( IEX_LIBRARY_NAME       Iex-${ILMBASE_VERSION_MAJOR}_${ILMBASE_VERSION_MINOR}       )""",
            """SET ( IEX_LIBRARY_NAME       Iex-${ILMBASE_VERSION_MAJOR}_${ILMBASE_VERSION_MINOR}       )
SET ( HALF_LIBRARY_NAME       Half-${ILMBASE_VERSION_MAJOR}_${ILMBASE_VERSION_MINOR}       )""")
        tools.replace_in_file("%s/cmake/FindILMBase.cmake" % self._source_subfolder,
            """SET ( IEX_LIBRARY_NAME       Iex       )""",
            """SET ( IEX_LIBRARY_NAME       Iex       )
SET ( HALF_LIBRARY_NAME       Half)""")
        tools.replace_in_file("%s/cmake/FindILMBase.cmake" % self._source_subfolder,
            """FIND_LIBRARY ( Ilmbase_HALF_LIBRARY Half PATHS ${ILMBASE_LIBRARYDIR} )""",
            """FIND_LIBRARY ( Ilmbase_HALF_LIBRARY ${HALF_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR} )""")
        tools.replace_in_file("%s/cmake/FindILMBase.cmake" % self._source_subfolder,
            """FIND_LIBRARY ( Ilmbase_HALF_LIBRARY Half PATHS ${ILMBASE_LIBRARYDIR}""",
            """FIND_LIBRARY ( Ilmbase_HALF_LIBRARY ${HALF_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR}""")

    def _configure_cmake(self):
        """Configure CMake."""
        cmake = CMake(self)

        definition_dict = {
            "OPENVDB_BUILD_UNITTESTS": False,
            "OPENVDB_BUILD_DOCS": False,
            "OPENVDB_BUILD_PYTHON_MODULE": False,
            "OPENVDB_BUILD_CORE": True,
            "OPENVDB_DISABLE_BOOST_IMPLICIT_LINKING": False,
            "OPENVDB_BUILD_VDB_VIEW": False,
        }

        if not self.options["OpenEXR"].shared:
            definition_dict["OPENVDB_OPENEXR_STATICLIB"] = True
        if not self.options["blosc"].shared:
            definition_dict["Blosc_USE_STATIC_LIBS"] = True

        # Boost default find package is not great... give it a hand.
        #boost_libs = ['atomic', 'chrono', 'container', 'context', 'contract', 'coroutine', 'date_time', 'exception', 'fiber', 'filesystem', 'graph', 'graph_parallel', 'iostreams', 'locale', 'log', 'math', 'mpi', 'program_options', 'python', 'random', 'regex', 'serialization', 'stacktrace', 'system', 'test', 'thread', 'timer', 'type_erasure', 'wave']
        boost_libs = ['iostreams', 'python', 'system', 'thread']
        for searched_lib in boost_libs:
            for built_lib in self.deps_cpp_info["boost"].libs:
                if built_lib.find(searched_lib) != -1:
                    definition_dict["Boost_%s_FOUND" % searched_lib.upper()] = True
                    definition_dict["Boost_%s_LIBRARY" % searched_lib.upper()] = built_lib

        cmake.configure(defs = definition_dict, source_folder = self._source_subfolder)
        return cmake

    def build(self):
        """Build the elements to package."""
        cmake = self._configure_cmake()
        if self.options.shared:
            cmake.build(target="openvdb_shared")
        else:
            cmake.build(target="openvdb_static")

    def package(self):
        """Assemble the package."""
        self.copy("*.h", dst="include/openvdb", src="%s/openvdb"%self._source_subfolder)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.dll", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.defines = ["OPENVDB_USE_BLOSC","OPENVDB_3_ABI_COMPATIBLE"]
        if not self.options.shared:
            self.cpp_info.defines.append("OPENVDB_STATICLIB")
        if not self.options["OpenEXR"].shared:
            self.cpp_info.defines.append("OPENVDB_OPENEXR_STATICLIB")
