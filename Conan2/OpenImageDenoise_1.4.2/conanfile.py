from conan import ConanFile, conan_version
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import get, replace_in_file, collect_libs
import os
import posixpath

class openimagedenoiseConan(ConanFile):
    name = "openimagedenoise"
    version = "1.4.2"
    user="mercs"
    description = "High-Performance Denoising Library for Ray Tracing."
    license = "Apache 2.0"
    url = "https://openimagedenoise.github.io"
    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        self.requires("onetbb/2021.10.0")

    def build_requirements(self):
        self.tool_requires("ispc/1.14.1@mercs")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, "https://github.com/OpenImageDenoise/oidn/releases/download/v%s/oidn-%s.src.tar.gz" % (self.version, self.version), strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["OIDN_STATIC_LIB"] = not self.options.shared
        tc.variables["OIDN_APPS"] = False
        tc.variables["OIDN_INSTALL_DEPENDENCIES"] = False
        tc.variables["TBB_ROOT"] = self.dependencies["onetbb"].package_folder.replace('\\', '\\\\')
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
        self.cpp_info.set_property("cmake_file_name", "OpenImageDenoise")
        self.cpp_info.set_property("cmake_target_name", "Mercs::OpenImageDenoise")
        self.cpp_info.libs = collect_libs(self)
        self.cpp_info.includedirs.append(os.path.join("include", "OpenImageDenoise"))
        if self.options.shared :
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
        else:
            self.cpp_info.defines.append("OIDN_STATIC_LIB")
