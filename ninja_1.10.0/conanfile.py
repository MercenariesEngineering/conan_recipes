"""Conan recipe to build a ninja package."""
import os
from conans import ConanFile, tools

class Ninja(ConanFile):
    description = "small build system with a focus on speed"
    url = "https://ninja-build.org/"
    license = "Apache 2"
    version = "1.10.0"
    settings = "os", "build_type"
    name = "ninja"

    def config_options(self):
        """Executed before the actual assignment of options. Use it to configure or constrain
        the available options in a package. You can read values of self.settings but you cannot
        read values of self.options."""
        if self.settings.os != "Linux" and self.settings.os != "Windows":
            raise RuntimeError("This recipe is only available for Linux and Windows")

    def configure(self):
        self.settings.build_type = "Release"


    def source(self):
        """Retrieve source code."""
        zip_name = "{}-win.zip".format(self.name) if self.settings.os == "Windows" \
            else "{}-linux.zip".format(self.name)
        url = "https://github.com/ninja-build/ninja/releases/download/v{}/{}".format(self.version, zip_name)
        tools.download(url, zip_name)
        tools.unzip(zip_name)
        os.remove(zip_name)
        os.chmod("ninja", 0o555)

    def package(self):
        """Assemble the package."""
        self.copy("ninja", src="", dst="bin")

    def package_info(self):
        """Edit package info."""
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
