import os
import shutil
from conans import ConanFile, tools

class IspcInstaller(ConanFile):
    name = "ispc_installer"
    version = "1.9.2"
    description = "Intel® Implicit SPMD Program Compiler"
    url = "https://ispc.github.io/"
    license = "BSD"
    settings = "os", "arch"

    def source(self):
        """Retrieve source code."""
        #https://github.com/ispc/ispc/releases/download/v1.9.2/ispc-v1.9.2b-linux.tar.gz
        #https://github.com/ispc/ispc/releases/download/v1.9.2/ispc-v1.9.2-windows.zip
        if self.settings.os == "Linux":
            file="ispc-v1.9.2b-linux.tar.gz"
            folder="ispc-v1.9.2-linux"
        else:
            file="ispc-v1.9.2-windows.zip"
            folder="ispc-v1.9.2-windows"
        tools.get("https://github.com/ispc/ispc/releases/download/v%s/%s" % (self.version, file))
        shutil.move(folder, "ispc")

    def build(self):
        pass

    def package(self):
        """Assemble the package."""
        if self.settings.os == "Linux":
            self.copy("ispc/ispc", dst="bin", keep_path=False)
        else:
            self.copy("ispc/ispc.exe", dst="bin", keep_path=False)

    def package_info(self):
        """Edit package info."""
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
