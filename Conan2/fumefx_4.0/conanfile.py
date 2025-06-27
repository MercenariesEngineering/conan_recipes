from conan import ConanFile
from conan.tools.files import copy, collect_libs
import os

class fumefxConan(ConanFile):
    name = "fumefx"
    version = "4.0"
    user="mercs"
    settings = "os"
    description = "FumeFX is a powerful fluid dynamics plugin for Autodesk Maya and 3ds Max, designed for simulation and rendering of realistic explosions, fire, smoke and other gaseous phenomena"
    url = "http://www.afterworks.com/FumeFXMaya.asp"
    package_type = "shared-library"
    exports_sources = "dist/*"

    def package(self):
        copy(self, "*.h", src=os.path.join(self.source_folder, "dist", "include"), dst=os.path.join(self.package_folder, "include"))
        if self.settings.os == "Windows" :
            copy(self, "FumeFXIO.lib", src=os.path.join(self.source_folder, "dist", "lib"), dst=os.path.join(self.package_folder, "lib"))
            copy(self, "FumeFXIO.dll", src=os.path.join(self.source_folder, "dist", "bin"), dst=os.path.join(self.package_folder, "bin"))
        elif self.settings.os == "Linux" :
            copy(self, "libfumefx.a", src=os.path.join(self.source_folder, "dist", "lib"), dst=os.path.join(self.package_folder, "lib"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "fumefx")
        self.cpp_info.set_property("cmake_target_name", "Mercs::fumefx")
        self.cpp_info.libs = collect_libs(self)
        if self.settings.os == "Windows":
            self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
