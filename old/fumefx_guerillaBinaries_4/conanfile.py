from conans import ConanFile
from conans import tools

class fumefxConan(ConanFile):
    name = "fumefx"
    version = "guerillaBinaries_4"
    settings = "os", "compiler", "build_type", "arch"
    description = "FumeFX is a powerful fluid dynamics plugin for Autodesk Maya and 3ds Max, designed for simulation and rendering of realistic explosions, fire, smoke and other gaseous phenomena"
    url = "http://www.afterworks.com/FumeFXMaya.asp"
    license = "None"

    def package(self):
        self.run("rm -Rf include lib")
        self.run("mkdir \"include\" \"include/fumefx\" \"lib\" \"bin\"")

        if self.settings.os == "Windows" :
            src_path = "X:\\Dev\\GuerillaLibs2015\\"
            includes = [
                "contrib\\FumeFXIO\\include\\FXShadeData.h",
                "contrib\\FumeFXIO\\include\\LinuxPorting.h",
                "contrib\\FumeFXIO\\include\\SDColor.h",
                "contrib\\FumeFXIO\\include\\SDMath.h",
                "contrib\\FumeFXIO\\include\\SDPoint3.h",
                "contrib\\FumeFXIO\\include\\stdafx.h",
                "contrib\\FumeFXIO\\include\\stddefs.h",
                "contrib\\FumeFXIO\\include\\vfTypes.h",
                "contrib\\FumeFXIO\\include\\VoxelFlowBase.h"]
            libs = [
                "\\contrib\\FumeFXIO\\VS_2008SP1\\x64\\FumeFXIO.lib"]
            bins = [
                "\\contrib\\FumeFXIO\\VS_2008SP1\\x64\\FumeFXIO.dll"]
        elif self.settings.os == "Linux" :
            src_path = "/usr/local/toolchain/extra/"
            includes = [
                "include/fumefx/FXShadeData.h",
                "include/fumefx/LinuxPorting.h",
                "include/fumefx/SDColor.h",
                "include/fumefx/SDMath.h",
                "include/fumefx/SDPoint3.h",
                "include/fumefx/stdafx.h",
                "include/fumefx/stddefs.h",
                "include/fumefx/vfTypes.h",
                "include/fumefx/VoxelFlowBase.h"]
            libs = [
                "lib/libfumefx.a"]
            bins = []

        for path in includes:
            self.run("cp -R %s%s include/fumefx/" % (src_path, path))

        for path in libs:
            self.run("cp -R %s%s lib/" % (src_path, path))

        for path in bins:
            self.run("cp -R %s%s bin/" % (src_path, path))

        self.copy("*.h")
        self.copy("*.lib")
        self.copy("*.dll")
        self.copy("*.a")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
