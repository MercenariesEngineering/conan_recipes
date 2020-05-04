from conans import ConanFile, CMake, tools
import os

class EmbreeConan(ConanFile):
    name = "embree"
    version = "3.9.0"
    license = ""
    url = "embree.org"
    description = "High Performance Ray Tracing Kernels"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    requires = "TBB/2019_U6@pierousseau/stable"
    default_options = "shared=False", "fPIC=True", "TBB:shared=True"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def configure(self):
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        # https://github.com/embree/embree/archive/v3.9.0.tar.gz
        filename = "v%s.tar.gz" % self.version
        tools.download("https://github.com/embree/embree/archive/%s" % filename, filename)
        tools.untargz(filename)
        os.unlink(filename)
        os.rename("embree-%s" % self.version, self._source_subfolder)

    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "EMBREE_TUTORIALS": False, # Don't pull in GLFW and IMGUI
            #"BUILD_TESTING": False,
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
        }

        if self.settings.os == "Linux":
            definition_dict["CMAKE_POSITION_INDEPENDENT_CODE"] = ("fPIC" in self.options.fields and self.options.fPIC == True)

        if self.settings.build_type == "Debug":
            definition_dict["EMBREE_TBB_ROOT"] = ""
            definition_dict["EMBREE_TBB_DEBUG_ROOT"] = self.deps_cpp_info["TBB"].rootpath
            definition_dict["EMBREE_TBB_DEBUG_POSTFIX"] = ""
        else:
            definition_dict["EMBREE_TBB_ROOT"] = self.deps_cpp_info["TBB"].rootpath
            definition_dict["EMBREE_TBB_DEBUG_ROOT"] = ""

        if not self.options.shared:
            definition_dict["EMBREE_STATIC_LIB"] = True
        elif self.settings.os == "Linux":
            definition_dict["EMBREE_IGNORE_CMAKE_CXX_FLAGS"] = False
            definition_dict["CMAKE_CXX_FLAGS"] = "-static-libstdc++ -static-libgcc"

        # Prevent compiler stack overflow: https://github.com/embree/embree/issues/157
        if self.settings.compiler == 'Visual Studio' and self.settings.compiler.version == 14 and self.settings.build_type == "Release":
            definition_dict["CMAKE_CXX_FLAGS"] = "-d2SSAOptimizer-"

        return definition_dict 

    def build(self):
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.install()
        # extra includes !
        self.copy("*.h", src="%s/common" %self._source_subfolder, dst="common")
        self.copy("*.h", src="%s/kernels"%self._source_subfolder, dst="kernels")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.defines.append("TASKING_TBB")
