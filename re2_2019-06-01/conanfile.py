import os
from conans import ConanFile, CMake, tools

class Re2Conan(ConanFile):
    name = "re2"
    version = "2019-06-01"
    license = "BSD-3-Clause"
    url = "https://github.com/google/re2"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    build_policy = "missing"
    description = "RE2 is a fast, safe, thread-friendly alternative to backtracking regular expression engines like those used in PCRE, Perl, and Python. It is a C++ library."
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    recipe_version = "1"
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        tools.get("https://github.com/google/re2/archive/2019-06-01.tar.gz")
        os.rename("re2-%s" % self.version, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.configure(defs={
                "CMAKE_INSTALL_PREFIX": self.package_folder,
                "BUILD_TESTING": "OFF"
            })
        cmake.build(target="install")

    def package_info(self):
        self.cpp_info.libs = ["re2"]
