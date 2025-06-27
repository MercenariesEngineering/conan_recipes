from conan import ConanFile
from conan.tools.files import copy, collect_libs
import os

class pythonConan(ConanFile):
    name = "python2-headers"
    version = "2.6"
    user="mercs"
    settings = "os"
    description = "Python is a programming language that lets you work quickly and integrate systems more effectively"
    url = "https://www.python.org/"
    exports_sources = "dist/*"

    def package(self):
        if self.settings.os == "Windows" :
            copy(self, "*.h", src=os.path.join(self.source_folder, "dist", "windows"), dst=os.path.join(self.package_folder, "include"))
        elif self.settings.os == "Linux" :
            copy(self, "*.h", src=os.path.join(self.source_folder, "dist", "linux"), dst=os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "python2-headers")
        self.cpp_info.set_property("cmake_target_name", "Mercs::python2-headers")
