from conans import ConanFile, tools
import os

class UnistdConan(ConanFile):
    name = "unistd"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    description = "Blank unistd.h file for Visual"
    url = "None"
    license = "None"
    author = "None"
    topics = None

    def package(self):
        if self.settings.os == "Windows":
            with open('unistd.h', 'w') as fp:
                pass
            self.copy(pattern="unistd.h", dst="include")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
