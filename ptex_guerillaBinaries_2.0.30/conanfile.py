from conans import ConanFile
from conans import tools

class ptexConan(ConanFile):
    name = "ptex"
    version = "guerillaBinaries_2.0.30"
    settings = "os", "compiler", "build_type", "arch"
    description = "Per-Face Texture Mapping for Production Rendering http://ptex.us/"
    url = "https://github.com/wdas/ptex"
    license = "None"

    def package(self):
        self.run("rm -Rf include lib")
        self.run("mkdir include lib")

        if self.settings.os == "Windows" :
            src_path = "X:\\Dev\\GuerillaLibs2015\\"
            includes = [
                "contrib\\ptex-v2.0.30\\src\\ptex\\PtexHalf.h",
                "contrib\\ptex-v2.0.30\\src\\ptex\\PtexInt.h",
                "contrib\\ptex-v2.0.30\\src\\ptex\\Ptexture.h",
                "contrib\\ptex-v2.0.30\\src\\ptex\\PtexUtils.h"]
            libs = [
                "lib\\x64\\%s\\ptex.lib"     % self.settings.build_type]
        elif self.settings.os == "Linux" :
            src_path = "/usr/local/toolchain/gcc-4.9.2/"
            includes = [
                "include/PtexHalf.h",
                "include/PtexInt.h",
                "include/Ptexture.h",
                "include/PtexUtils.h"]
            libs = [
                "lib/libPTex.a"]

        for path in includes:
            self.run("cp -R %s%s include\\" % (src_path, path))

        for path in libs:
            self.run("cp -R %s%s lib\\" % (src_path, path))

        self.copy("*.h")
        self.copy("*.lib")
        self.copy("*.a")
        self.copy("*.pdb") # seems ignored on current conan version

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
