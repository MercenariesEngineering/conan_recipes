from conans import ConanFile, CMake, tools
import os

# Recipe based on "OpenSubdiv/3.4.0@tdelame/stable"
class opensubdiv(ConanFile):
    description = "High performance subdivision surface evaluation"
    url = "https://github.com/PixarAnimationStudios/OpenSubdiv"
    license = "Apache 2.0"
    name = "OpenSubdiv"
    version = "3.4.3"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True", "TBB:shared=True"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"
    
    def requirements(self):
        """Define runtime requirements."""
        self.requires("TBB/2019_U6@pierousseau/stable")
        self.requires("zlib/1.2.11@pierousseau/stable")

    def configure(self):
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/PixarAnimationStudios/OpenSubdiv/archive/v3_4_3.tar.gz")
        os.rename("OpenSubdiv-3_4_3", self._source_subfolder)

        with tools.chdir(self._source_subfolder):
            # don't replace conan's CMAKE_MODULE_PATH, extend it
            tools.replace_in_file( "CMakeLists.txt", """${CMAKE_CURRENT_SOURCE_DIR}/cmake""", """${CMAKE_MODULE_PATH}" "${CMAKE_CURRENT_SOURCE_DIR}/cmake""")
            # do not want to compile stuff for regressions while I said to not compile regressions...
            tools.replace_in_file( "CMakeLists.txt", "if (NOT ANDROID", "if (FALSE")
        
    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "BUILD_SHARED_LIBS": self.options.shared,
            "NO_EXAMPLES": True,
            "NO_TUTORIALS": True,
            "NO_REGRESSION": True,
            "NO_PTEX": True,
            "NO_DOC": True,
            "NO_OMP": True,
            "NO_TBB": False,
            "NO_CUDA": True,
            "NO_OPENCL": True,
            "NO_CLEW": True,
            "NO_OPENGL": False,
            "NO_METAL": True,
            "NO_DX": True,
            "NO_TESTS": True,
            "NO_GLTESTS": True,
            "NO_GLEW": True,
            "NO_GLFW": True,
            "NO_GLFW_X11": True,
        }

        if self.settings.os == "Linux":
            definition_dict["CMAKE_POSITION_INDEPENDENT_CODE"] = ("fPIC" in self.options.fields and self.options.fPIC == True)
            #definition_dict["CMAKE_CXX_FLAGS"] = "-I{}".format(self.deps_cpp_info["GLU" ].include_paths[0])

        return definition_dict 

    def build(self):
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions())
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions())
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
