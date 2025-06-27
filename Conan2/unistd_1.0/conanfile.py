from conan import ConanFile
from conan.tools.files import copy, get
from conan.tools.layout import basic_layout
import os

required_conan_version = ">=1.50.0"


class UnistdConan(ConanFile):
    name = "unistd"
    version = "1.0"
    user="mercs"
    description = "Blank unistd.h file for Visual."
    license = "None"
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    def package(self):
        if self.settings.os == "Windows":
            with open('unistd.h', 'w') as fp:
                pass
            copy(self, "unistd.h", self.build_folder, dst=os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.set_property("cmake_target_name", "Mercs::unistd")
        if self.settings.os == "Windows":
            self.cpp_info.includedirs = [os.path.join(self.package_folder, "include")]
