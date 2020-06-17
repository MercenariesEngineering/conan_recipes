import os
from conans import ConanFile, tools

# Recipe based on "GSL/2.1.0@tdelame/stable"
class libClangConan(ConanFile):
    name = "libclang"
    description = "LibClang is a stable high level C interface to clang. When in doubt LibClang is probably the interface you want to use"
    url = "https://clang.llvm.org/docs/Tooling.html#libclang"
    settings = "os", "compiler", "arch"
    version = "7.0"
    
    def configure(self):
        if self.settings.os != "Windows" or self.settings.compiler != "Visual Studio" or self.settings.compiler.version != "14" or self.settings.arch != "x86_64":
            raise ConanInvalidConfiguration("Libclang recipe is win64 VS2015 only right now. Use your package manager on linux !")

        if self.settings.compiler == "Visual Studio":
            del self.settings.compiler.runtime

    def source(self):
        """Retrieve source code."""
        tools.download("http://download.qt.io/development_releases/prebuilt/libclang/libclang-release_70-based-windows-vs2015_64.7z", "clang.7z")
        # Conan won't natively handle 7z files. Cmake is actually the easiest unzipping tool at hand.
        self.run("cmake -E tar xf clang.7z")
        os.unlink("clang.7z")

    def package(self):
        """Assemble the package."""
        self.copy("*", src=os.path.join(self.source_folder, "libclang"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.env_info.LLVM_INSTALL_DIR = self.package_folder
