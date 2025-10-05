from conan import ConanFile
from conan.tools.build import build_jobs
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.env import Environment
from conan.tools.files import get, download, copy, chdir, replace_in_file, export_conandata_patches, apply_conandata_patches
from conan.tools.microsoft import VCVars
from conan.tools.scm import Version
import os

class PySide6(ConanFile):
    name = "libclang"
    description = "libclang"
    license = "Apache-2.0"
    url = "http://download.qt.io/development_releases/prebuilt/libclang"
    settings = "os", "compiler", "build_type", "arch"

    package_type = "library"
    options = {
        "shared": [True,False]
    }
    default_options = {
        "shared": True
    }
    short_paths = True

    @property
    def clang_source_file(self): 
        # Version 14 is minimum, 18 is recommended
        if self.settings.os == "Windows":
            return "libclang-release_20.1.3-based-windows-vs2019_64.7z"
        else:
            return "libclang-release_20.1.3-based-linux-Rhel8.8-gcc10.3-x86_64.7z"
    
    def build(self):
        clang_file = self.clang_source_file
        download(self, "http://download.qt.io/development_releases/prebuilt/libclang/%s" % clang_file, clang_file)
        #copy(self, pattern=clang_file, src="/mnt/work/code/3rdparty", dst=self.build_folder)
        
        # Conan won't natively handle 7z files. Cmake is actually the easiest unzipping tool at hand.
        self.run("cmake -E tar xf "+clang_file)
        os.unlink(clang_file)

    def package(self):
        # package minimal libclang
        copy(self, pattern="*", src=os.path.join(self.source_folder, "libclang", "include"), dst=os.path.join(self.package_folder, "include"))
        copy(self, pattern="*", src=os.path.join(self.source_folder, "libclang", "lib", "clang"), dst=os.path.join(self.package_folder, "lib", "clang"))
        copy(self, pattern="*", src=os.path.join(self.source_folder, "libclang", "bin"), dst=os.path.join(self.package_folder, "bin"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Clang")
        self.cpp_info.set_property("cmake_target_name", "Clang::Clang")
        if self.settings.os == "Windows":
            self.buildenv_info.define("CLANG_INSTALL_DIR", os.path.join(self.package_folder, "libclang"))
            self.buildenv_info.prepend_path("PATH", os.path.join(self.package_folder, "libclang", "bin"))
        else:
            self.buildenv_info.define("CLANG_INSTALL_DIR", os.path.join(self.package_folder, "libclang"))
            self.buildenv_info.append_path("LD_LIBRARY_PATH", os.path.join(self.package_folder, "libclang", "lib"))
