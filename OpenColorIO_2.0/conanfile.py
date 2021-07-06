import os
import shutil
from conans import ConanFile, CMake, tools

class OpenColorIOConan(ConanFile):
    name = "OpenColorIO"
    version = "2.0"
    license = ""
    url = "https://opencolorio.org/"
    description = "Open Source Color Management"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"
    recipe_version= "v1"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("expat/2.2.9@mercseng/v0")
        self.requires("OpenEXR/2.5.1@mercseng/v0")
        self.requires("OpenImageIO/2.1.15.0@mercseng/v3")
        self.requires("yaml-cpp/0.6.3@mercseng/v0")
        self.requires("pystring/1.1.3@mercseng/v0")

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/refs/tags/v2.0.1.tar.gz")
        os.rename("OpenColorIO-2.0.1", self._source_subfolder)
        
        # Write static lib to /lib folder, not/lib/static

        os.rename(os.path.join(self._source_subfolder, "CMakeLists.txt"), os.path.join(self._source_subfolder, "CMakeLists_original.txt"))
        shutil.copy("CMakeLists.txt", os.path.join(self._source_subfolder, "CMakeLists.txt"))

    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "OCIO_BUILD_APPS": False,
            "OCIO_BUILD_NUKE": False,
            "OCIO_BUILD_TESTS": False,   
            "OCIO_BUILD_GPU_TESTS" : False,
            "OCIO_USE_HEADLESS" : False,

            "OCIO_BUILD_FROZEN_DOCS": False,
            "OCIO_BUILD_DOCS": False,
  
            "OCIO_BUILD_PYTHON": False,
            "OCIO_BUILD_JAVA": False,

            "OCIO_USE_SSE" : True,
            "OCIO_INLINES_HIDDEN": False,
            
            "OCIO_INSTALL_EXT_PACKAGES": "MISSING",         
            "OCIO_BUILD_SHARED": self.options.shared,
            "OCIO_BUILD_STATIC": not self.options.shared,
            "OCIO_WARNING_AS_ERROR" : False,

            "OCIO_LIBNAME_SUFFIX" : "",
            "OCIO_NAMESPACE" : "OpenColorIO",
        }

        if self.settings.os == "Linux":
            definition_dict["CMAKE_CXX_FLAGS"] = "-Wno-deprecated-declarations"

        return definition_dict

    def build(self):
        """Build the elements to package."""
        ext_dir = os.path.join(self.build_folder, 'ext')
        os.mkdir(ext_dir)

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
        if (not self.options.shared):
            self.cpp_info.defines = ["OpenColorIO_STATIC"]
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
