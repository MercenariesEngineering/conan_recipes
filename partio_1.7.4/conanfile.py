from conans import ConanFile, CMake, tools
import os

class partioConan(ConanFile):
    name = "partio"
    version = "1.7.4"
    description = "partio - A library for particle IO and manipulation"
    license = ""
    url = "https://github.com/wdas/partio"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "CMakeLists.txt"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("zlib/1.2.11@mercseng/v0")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/wdas/partio/archive/v%s.tar.gz" % self.version)
        os.rename("partio-%s" % self.version, self._source_subfolder)

        tools.replace_in_file("%s/CMakeLists.txt" % self._source_subfolder,
            "find_package(GLUT REQUIRED)", "find_package(GLUT QUIET)")
        tools.replace_in_file("%s/CMakeLists.txt" % self._source_subfolder,
            "ADD_SUBDIRECTORY (src/py)", "")
        tools.replace_in_file("%s/CMakeLists.txt" % self._source_subfolder,
            "ADD_SUBDIRECTORY (src/tools)", "")

    def build(self):
        """Build the elements to package."""
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        """Assemble the package."""
        cmake = CMake(self)
        cmake.configure()
        cmake.install()

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
