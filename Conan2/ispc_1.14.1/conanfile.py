from conan import ConanFile
from conan.tools.files import get, copy
import os

class ispcConan(ConanFile):
    name = "ispc"
    version = "1.14.1"
    user="mercs"
    settings = "os", "arch"
    description = "Python is a programming language that lets you work quickly and integrate systems more effectively"
    license = "BSD-3"
    url = "https://ispc.github.io/"

    def build(self):
        if self.settings.os == "Linux":
            get(self, "https://github.com/ispc/ispc/releases/download/v%s/ispc-v%s-linux.tar.gz" % (self.version, self.version))
        else:
            get(self, "https://github.com/ispc/ispc/releases/download/v%s/ispc-v%s-windows.zip" % (self.version, self.version))

    def package(self):
        if self.settings.os == "Windows" :
            copy(self, "ispc.exe", src=os.path.join(self.source_folder, "bin"), dst=os.path.join(self.package_folder, "bin"))
        elif self.settings.os == "Linux" :
            copy(self, "ispc", src=os.path.join(self.source_folder, "bin"), dst=os.path.join(self.package_folder, "bin"))

    def package_info(self):
        self.cpp_info.set_property("cmake_target_name", "Mercs::ispc")
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
