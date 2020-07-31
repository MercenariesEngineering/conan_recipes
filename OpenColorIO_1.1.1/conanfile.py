import os
import shutil
from conans import ConanFile, CMake, tools

class OpenColorIOConan(ConanFile):
    name = "OpenColorIO"
    version = "1.1.1"
    license = ""
    url = "https://opencolorio.org/"
    description = "Open Source Color Management"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("expat/2.2.9@mercseng/v0")
        self.requires("OpenEXR/2.5.1@mercseng/v0")

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        #Get a commit from the RB-1.1 branch, incorporating fixes for clang compilation
        commit_sha="6a7c18bec3a2ca8d43d710389ae9cdc2074bff04"
        tools.get("https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/%s.zip" % commit_sha)
        os.rename("OpenColorIO-%s" % commit_sha, self._source_subfolder)
        
        # Write static lib to /lib folder, not/lib/static
        tools.replace_in_file("%s/src/core/CMakeLists.txt" % self._source_subfolder, """${CMAKE_INSTALL_EXEC_PREFIX}/lib/static""", """${CMAKE_INSTALL_EXEC_PREFIX}/lib""")

        os.rename(os.path.join(self._source_subfolder, "CMakeLists.txt"), os.path.join(self._source_subfolder, "CMakeLists_original.txt"))
        shutil.copy("CMakeLists.txt", os.path.join(self._source_subfolder, "CMakeLists.txt"))

    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "OCIO_BUILD_APPS": False,
            "OCIO_BUILD_DOCS": False,
            "OCIO_BUILD_JNIGLUE": False,
            "OCIO_BUILD_NUKE": False,
            "OCIO_BUILD_PYGLUE": False,
            "OCIO_BUILD_SHARED": self.options.shared,
            "OCIO_BUILD_STATIC": not self.options.shared,
            "OCIO_BUILD_TESTS": False,
            "OCIO_BUILD_TRUELIGHT": False,
            "OCIO_INSTALL_EXT_PACKAGES": "MISSING",
        }

        if self.settings.os == "Linux":
            definition_dict["CMAKE_CXX_FLAGS"] = "-Wno-deprecated-declarations"

        return definition_dict

    def build(self):
        """Build the elements to package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.build()

    def package(self):
        """Assemble the package."""
        self.copy("*.h", src="%s/export/OpenColorIO/" % self._source_subfolder, dst="include/OpenColorIO/")
        self.copy("*.h", src="export/", dst="include/OpenColorIO/")
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)

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
