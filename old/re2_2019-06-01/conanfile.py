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

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        tools.get("https://github.com/google/re2/archive/2019-06-01.tar.gz")

    def build(self):
        cmake = CMake(self)
        cmake.configure(defs={
                "CMAKE_INSTALL_PREFIX": self.package_folder,
                "BUILD_SHARED_LIBS": "ON" if self.options.shared else "OFF",
                "BUILD_TESTING": "OFF",
                "CMAKE_CXX_FLAGS": "-fPIC" if ("fPIC" in self.options.fields and self.options.fPIC == True) else "",
            }, source_dir="re2-%s" % self.version)
        cmake.build(target="install")

    def package_info(self):
        self.cpp_info.libs = ["re2"]
