from conan import ConanFile, conan_version
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import get, replace_in_file, collect_libs
import os

class partioConan(ConanFile):
    name = "partio"
    version = "1.7.4"
    user="mercs"
    description = "C++ (with python bindings) library for easily reading/writing/manipulating common animation particle formats such as PDB, BGEO, PTC."
    url = "https://github.com/wdas/partio"
    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        self.requires("zlib/1.3.1")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, "https://github.com/wdas/partio/archive/v%s.tar.gz" % self.version, strip_root=True)

        replace_in_file(self, "CMakeLists.txt", "find_package(GLUT REQUIRED)", "find_package(GLUT QUIET)")
        replace_in_file(self, "CMakeLists.txt", "ADD_SUBDIRECTORY (src/py)", "")
        replace_in_file(self, "CMakeLists.txt", "ADD_SUBDIRECTORY (src/tools)", "")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "partio")
        self.cpp_info.set_property("cmake_target_name", "Mercs::partio")
        self.cpp_info.libs = collect_libs(self)
