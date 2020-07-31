from conans import ConanFile, tools
import os

class fumefxConan(ConanFile):
    name = "fumefx"
    version = "4.0"
    settings = "os"
    description = "FumeFX is a powerful fluid dynamics plugin for Autodesk Maya and 3ds Max, designed for simulation and rendering of realistic explosions, fire, smoke and other gaseous phenomena"
    url = "http://www.afterworks.com/FumeFXMaya.asp"
    license = "None"
    exports_sources = "dist/*"

    def package(self):
        self.copy("*.h", src="dist/include", dst="include")
        if self.settings.os == "Windows" :
            self.copy("FumeFXIO.lib", src="dist/lib", dst="lib")
            self.copy("FumeFXIO.dll", src="dist/bin", dst="bin")
        elif self.settings.os == "Linux" :
            self.copy("libfumefx.a", src="dist/lib", dst="lib")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
