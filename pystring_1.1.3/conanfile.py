import os
import shutil
from conans import ConanFile, CMake, tools

class PystringConan(ConanFile):
    name = "pystring"
    version = "1.1.3"
    description = "Pystring is a collection of C++ functions which match the " \
                  "interface and behavior of python's string class methods using std::string."
    license = "BSD-3-Clause"
    topics = ("conan", "pystring", "string")
    homepage = "https://github.com/imageworks/pystring"
    url = "https://github.com/conan-io/conan-center-index"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    recipe_version= "v1"

    _source_subfolder = "source_subfolder"
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    
    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/imageworks/pystring/archive/refs/tags/v1.1.3.tar.gz")
        os.rename("pystring-1.1.3", self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
        if (not self.options.shared):
            self.cpp_info.defines = ["pystring_STATIC"]
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
