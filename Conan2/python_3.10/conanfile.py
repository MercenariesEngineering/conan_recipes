from conan import ConanFile
from conan.tools.files import copy, collect_libs
import os

class pythonConan(ConanFile):
    name = "python3.10-headers"
    version = "3.10"
    user="mercs"
    settings = "os"
    description = "Python is a programming language that lets you work quickly and integrate systems more effectively"
    url = "https://www.python.org/"
    exports_sources = "dist/*"

    def package(self):
        if self.settings.os == "Windows" :
            copy(self, "*.h", src=os.path.join(self.source_folder, "dist", "windows", "include"), dst=os.path.join(self.package_folder, "include"))
            copy(self, "*.lib", src=os.path.join(self.source_folder, "dist", "windows", "lib"), dst=os.path.join(self.package_folder, "lib"))
            copy(self, "*.dll", src=os.path.join(self.source_folder, "dist", "windows", "bin"), dst=os.path.join(self.package_folder, "bin"))
        elif self.settings.os == "Linux" :
            copy(self, "*.h", src=os.path.join(self.source_folder, "dist", "linux", "include"), dst=os.path.join(self.package_folder, "include"))
            copy(self, "libpython3.10.so.1.0", src=os.path.join(self.source_folder, "dist", "linux", "lib"), dst=os.path.join(self.package_folder, "lib"))
            self.run("ln -s libpython3.10.so.1.0 "+str(os.path.join(self.package_folder, "lib", "libpython3.10.so")))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "python3.10-headers")
        self.cpp_info.set_property("cmake_target_name", "Mercs::python3.10-headers")
