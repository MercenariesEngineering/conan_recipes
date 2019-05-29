from conans import ConanFile
from conans import tools

class opencolorioConan(ConanFile):
    name = "opencolorio"
    version = "guerillaBinaries_1.0.8"
    settings = "os", "compiler", "build_type", "arch"
    description = "Open Source Color Management"
    url = "http://opencolorio.org"
    license = "None"

    def package(self):
        self.run("rm -Rf include lib")
        self.run("mkdir include include\\OpenColorIO lib")

        if self.settings.os == "Windows" :
            src_path = "X:\\Dev\\GuerillaLibs2015\\"
            includes = [
                "contrib\\opencolorio-1.0.8\\build\\export\\OpenColorABI.h",
                "contrib\\opencolorio-1.0.8\\export\\OpenColorIO\\OpenColorIO.h",
                "contrib\\opencolorio-1.0.8\\export\\OpenColorIO\\OpenColorTransforms.h",
                "contrib\\opencolorio-1.0.8\\export\\OpenColorIO\\OpenColorTypes.h"]
            libs = [
                "lib\\x64\\%s\\OpenColorIO.lib" % self.settings.build_type,
                "lib\\x64\\%s\\libyaml-cpp.lib" % self.settings.build_type,
                "lib\\x64\\%s\\tinyxml.lib"     % self.settings.build_type]
        elif self.settings.os == "Linux" :
            src_path = "/usr/local/toolchain/gcc-4.9.2/"
            includes = [
                "include/OpenColorIO/OpenColorABI.h",
                "include/OpenColorIO/OpenColorIO.h",
                "include/OpenColorIO/OpenColorTransforms.h",
                "include/OpenColorIO/OpenColorTypes.h"]
            libs = [
                "lib/libOpenColorIO.a",
                "lib/libyaml-cpp.a",
                "lib/libtinyxml.a"]

        for path in includes:
            self.run("cp -R %s%s include\\OpenColorIO" % (src_path, path))

        for path in libs:
            self.run("cp -R %s%s lib\\" % (src_path, path))

        self.copy("*.h")
        self.copy("*.lib")
        self.copy("*.a")
        self.copy("*.pdb") # seems ignored on current conan version

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
