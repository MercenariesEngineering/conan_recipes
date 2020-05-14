from conans import ConanFile, CMake, tools
import os

class EmbreeConan(ConanFile):
    name = "embree"
    version = "3.9.0"
    license = "Apache 2.0 license"
    url = "embree.org"
    description = "High Performance Ray Tracing Kernels"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    requires = "TBB/2019_U6@pierousseau/stable"
    default_options = "shared=False", "fPIC=True", "TBB:shared=True"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/embree/embree/archive/v%s.tar.gz" % self.version)
        os.rename("embree-%s" % self.version, self._source_subfolder)

    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "CMAKE_BUILD_TYPE": self.settings.build_type,
            "BUILD_TESTING": False,
            "EMBREE_TUTORIALS": False, # Don't pull in GLFW and IMGUI
            "EMBREE_STATIC_LIB": not self.options.shared,
            "EMBREE_IGNORE_CMAKE_CXX_FLAGS": False,
            "EMBREE_TASKING_SYSTEM": "TBB",
            "EMBREE_MAX_ISA": "AVX2", # avx512KNL does not compile on windows
            "EMBREE_ISPC_SUPPORT": True,
            #"EMBREE_RAY_MASK": True,
            #"EMBREE_BACKFACE_CULLING": True,
            #"EMBREE_FILTER_FUNCTION": True,
            #"EMBREE_IGNORE_INVALID_RAYS": False,
            #"EMBREE_GEOMETRY_TRIANGLE": True,
            #"EMBREE_GEOMETRY_QUAD": True,
            #"EMBREE_GEOMETRY_CURVE": True,
            #"EMBREE_GEOMETRY_SUBDIVISION": True,
            #"EMBREE_GEOMETRY_USER": True,
            #"EMBREE_GEOMETRY_INSTANCE": True,
            #"EMBREE_GEOMETRY_GRID": True,
            #"EMBREE_GEOMETRY_POINT": True,
            #"EMBREE_RAY_PACKETS": True,
            #"EMBREE_MAX_INSTANCE_LEVEL_COUNT": "1",
            "EMBREE_CURVE_SELF_INTERSECTION_AVOIDANCE_FACTOR": "0",
            "EMBREE_TBB_DEBUG_POSTFIX" : ""
        }

        if self.settings.os == "Linux" and self.options.shared:
            definition_dict["CMAKE_CXX_FLAGS"] = "-static-libstdc++ -static-libgcc"

        # Prevent compiler stack overflow: https://github.com/embree/embree/issues/157
        if self.settings.compiler == 'Visual Studio' and self.settings.compiler.version == 14 and self.settings.build_type == "Release":
            definition_dict["CMAKE_CXX_FLAGS"] = "-d2SSAOptimizer-"

        return definition_dict 

    def build(self):
        """Build the elements to package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions())
        cmake.build()

    def package(self):
        """Assemble the package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions())
        cmake.install()
        # extra includes !
        self.copy("*.h", src="%s/common" %self._source_subfolder, dst="common")
        self.copy("*.h", src="%s/kernels"%self._source_subfolder, dst="kernels")

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.defines.append("TASKING_TBB")
