import os
from conans import ConanFile, tools

class ISPC(ConanFile):
    description = "Intel® Implicit SPMD Program Compiler"
    url = "https://ispc.github.io/"
    license = "BSD-3"
    version = "1.13.0"
    settings = "os"
    name = "ispc"

    def source(self):
        """Retrieve source code."""
        directory = "ispc-v{}-windows".format(self.version) if self.settings.os == "Windows" \
            else "ispc-v{}-linux".format(self.version)
        archive_name = "{}.{}".format(directory, "zip" if self.settings.os == "Windows" else "tar.gz")
        
        tools.get("https://github.com/ispc/ispc/releases/download/v{}/{}".format(self.version, archive_name))
        os.rename(directory, self.name)

    def package(self):
        """Assemble the package."""
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self.name)
        self.copy("ispc{}".format(".exe" if self.settings.os == "Windows" else ""), src=os.path.join(self.name, "bin"), dst="bin")

    def package_info(self):
        """Edit package info."""
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))