from conans import ConanFile, CMake, tools
import os
import shutil

class OpenVdbConan(ConanFile):
    name = "OpenVdb"
    version = "4.0.2"
    license = ""
    url = "https://github.com/AcademySoftwareFoundation/openvdb"
    description = "OpenVDB is an Academy Award-winning C++ library comprising a hierarchical data structure and a suite of tools for the efficient manipulation of sparse, time-varying, volumetric data discretized on three-dimensional grids."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("blosc/1.11.2@pierousseau/stable")
        self.requires("boost/1.70.0")
        self.requires("glew/2.1.0@mercseng/stable")
        self.requires("glfw/3.3@pierousseau/stable")
        self.requires("OpenEXR/2.4.0@mercseng/stable")
        self.requires("TBB/2019_U6@pierousseau/stable")
        self.requires("zlib/1.2.11")

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/AcademySoftwareFoundation/openvdb/archive/v%s.tar.gz" % self.version)
        os.rename("openvdb-%s" % self.version, self._source_subfolder)

        tools.replace_in_file("%s/openvdb/CMakeLists.txt" % self._source_subfolder,
            "COMPILE_FLAGS \"-DOPENVDB_PRIVATE -DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG}\"",
            "COMPILE_FLAGS \"-DOPENVDB_PRIVATE -DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG} $<$<CXX_COMPILER_ID:MSVC>:/bigobj>\"")
        tools.replace_in_file("%s/openvdb/CMakeLists.txt" % self._source_subfolder,
            "COMPILE_FLAGS \"-DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG}\"",
            "COMPILE_FLAGS \"-DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG} $<$<CXX_COMPILER_ID:MSVC>:/bigobj>\"")
        tools.replace_in_file("%s/openvdb/CMakeLists.txt" % self._source_subfolder,
            "COMPILE_FLAGS \"-DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG} -DGL_GLEXT_PROTOTYPES=1\"",
            "COMPILE_FLAGS \"-DOPENVDB_USE_BLOSC ${OPENVDB_USE_GLFW_FLAG} -DGL_GLEXT_PROTOTYPES=1 $<$<CXX_COMPILER_ID:MSVC>:/bigobj>\"")

        tools.replace_in_file("%s/cmake/FindGLEW.cmake" % self._source_subfolder,
              "FIND_LIBRARY ( GLEW_LIBRARY_PATH GLEW32 PATHS ${GLEW_LOCATION}/lib )",
            """FIND_LIBRARY ( GLEW_LIBRARY_PATH GLEW32D PATHS ${GLEW_LOCATION}/lib )
FIND_LIBRARY ( GLEW_LIBRARY_PATH GLEW32 PATHS ${GLEW_LOCATION}/lib )""")

        tools.replace_in_file("%s/cmake/FindGLFW.cmake" % self._source_subfolder,
              "SET( GLFW_glfw_LIBRARY ${GLFW_LIBRARY_PATH} CACHE STRING \"GLFW library\")",
            """SET( GLFW_glfw_LIBRARY ${GLFW_LIBRARY_PATH})""")

        tools.replace_in_file("%s/cmake/FindGLFW.cmake" % self._source_subfolder,
              "FIND_LIBRARY ( GLFW_LIBRARY_PATH glfw PATHS ${GLFW_LOCATION}/lib ${GLFW_LOCATION}/lib64",
            """FIND_LIBRARY ( GLFW_LIBRARY_PATH glfw3 PATHS ${GLFW_LOCATION}/lib ${GLFW_LOCATION}/lib64""")

        # Add a wrapper CMakeLists.txt file which initializes conan before executing the real CMakeLists.txt
        os.rename(os.path.join(self._source_subfolder, "CMakeLists.txt"), os.path.join(self._source_subfolder, "CMakeLists_original.txt"))
        shutil.copy("CMakeLists.txt", self._source_subfolder)

    def find_library(self, definition_dict, searched_lib, dependency, prefix):
        if self.settings.os == "Windows":
            ext = "lib"
        else:
            ext = "so" if self.options[dependency].shared else "a"

        for built_lib in self.deps_cpp_info[dependency].libs:
            if built_lib.lower().find(searched_lib) != -1:
                definition_dict["%s_%s_LIBRARY" % (prefix, searched_lib.upper())] = "%s/%s.%s" % (self.deps_cpp_info[dependency].lib_paths[0], built_lib, ext)
                break

    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            #"BUILD_SHARED": self.options.shared,
            #"BUILD_TOOLS": False,
            "OPENVDB_BUILD_CORE": True,
            "OPENVDB_BUILD_DOCS": False,
            "OPENVDB_BUILD_UNITTESTS": False,
            "OPENVDB_BUILD_PYTHON_MODULE": False,
            "OPENVDB_BUILD_HOUDINI_SOPS": False,
            "OPENVDB_ENABLE_3_ABI_COMPATIBLE": True,
            "OPENVDB_DISABLE_BOOST_IMPLICIT_LINKING": False,
            "CMAKE_INSTALL_PREFIX": self.package_folder,

            "TBB_LOCATION": self.deps_cpp_info["TBB"].rootpath,
            "ILMBASE_LOCATION": self.deps_cpp_info["OpenEXR"].rootpath,
            "OPENEXR_LOCATION": self.deps_cpp_info["OpenEXR"].rootpath,
            "BOOST_ROOT": self.deps_cpp_info["boost"].rootpath,
            "BOOST_LIBRARYDIR": self.deps_cpp_info["boost"].lib_paths[0],
        }

        boost_libs = ['iostreams', 'system', 'thread']
        for searched_lib in boost_libs:
            self.find_library(definition_dict, searched_lib, "boost", "Boost")

        ilmbase_libs = ['half', 'imath', 'ilmthread', 'iex']
        for searched_lib in ilmbase_libs:
            self.find_library(definition_dict, searched_lib, "OpenEXR", "Ilmbase")

        exr_libs = ['ilmimf']
        for searched_lib in exr_libs:
            self.find_library(definition_dict, searched_lib, "OpenEXR", "Openexr")

        return definition_dict

    def build(self):
        """Build the elements to package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.build(target = "openvdb_shared" if self.options.shared else "openvdb_static")

    def package(self):
        """Assemble the package."""
        self.copy("*.h", dst="include/openvdb", src="%s/openvdb" % self._source_subfolder)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.defines = [
            "OPENVDB_USE_BLOSC",
            "OPENVDB_3_ABI_COMPATIBLE"
            ]

        if not self.options.shared:
            self.cpp_info.defines.append ("OPENVDB_STATICLIB")
        if not self.options["OpenEXR"].shared:
            self.cpp_info.defines.append ("OPENVDB_OPENEXR_STATICLIB")
