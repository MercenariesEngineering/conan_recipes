from conans import ConanFile
from conans import tools

class embreeConan(ConanFile):
    name = "embree"
    version = "guerillaBinaries_3.2.0"
    settings = "os", "compiler", "build_type", "arch"
    description = "Intel Embree - High Performance Ray Tracing Kernels"
    url = "https://www.embree.org/"
    license = "None"

    def package(self):
        self.run("rm -Rf include lib")
        self.run("mkdir include include\\embree lib")

        if self.settings.os == "Windows" :
            src_path = "X:\\Dev\\GuerillaLibs2015\\"
            includes = [
                "contrib\\embree-3.2.0\\common",
                "contrib\\embree-3.2.0\\include",
                "contrib\\embree-3.2.0\\kernels"]
            libs = [
                "lib\\x64\\%s\\math.lib"     % self.settings.build_type,
                "lib\\x64\\%s\\simd.lib"     % self.settings.build_type]
        elif self.settings.os == "Linux" :
            src_path = "/usr/local/toolchain/extra-1.0/embree-3.2.0/"
            includes = [
                "common",
                "include",
                "kernels"]
            libs = [
                "lib/libmath.a",
                "lib/libsimd.a"]

        for path in includes:
            self.run("cp -R %s%s include\\embree\\" % (src_path, path))

        for path in libs:
            self.run("cp -R %s%s lib\\" % (src_path, path))

        self.copy("*.h")
        self.copy("*.lib")
        self.copy("*.a")
        self.copy("*.pdb") # seems ignored on current conan version

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
