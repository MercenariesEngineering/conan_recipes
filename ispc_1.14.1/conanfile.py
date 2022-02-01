import os
import shutil
from conans import ConanFile, tools

class ISPC(ConanFile):
    description = "Intel Implicit SPMD Program Compiler"
    url = "https://ispc.github.io/"
    license = "BSD-3"
    version = "1.14.1"
    settings = "os", "arch"
    name = "ispc"

    def source(self):
        """Retrieve binaries."""
        if self.settings.os == "Linux":
            file="ispc-v%s-linux.tar.gz" % self.version
            folder="ispc-v%s-linux" % self.version
            tools.get("https://github.com/ispc/ispc/releases/download/v%s/%s" % (self.version, file))
            shutil.move(folder, "ispc")
        else:
            file="ispc-v%s-windows.zip" % self.version
            folder="ispc-v%s-windows" % self.version
            tools.get("https://github.com/ispc/ispc/releases/download/v%s/%s" % (self.version, file), destination="ispc")

    def build(self):
        pass

    def package(self):
        """Assemble the package."""
        if self.settings.os == "Linux":
            self.copy("ispc/bin/ispc", dst="bin", keep_path=False)
        else:
            self.copy("ispc/bin/ispc.exe", dst="bin", keep_path=False)

    def package_info(self):
        """Edit package info."""
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
