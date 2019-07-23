from conans import CMake, ConanFile
from conans.tools import replace_in_file

def cmake_flag(name, flag_type, value_str):
    return str.format("-D{}:{}={}", name, flag_type, value_str)

def cmake_bool_flag(name, bool_value):
    cmake_bool_string = "ON" if bool_value else "OFF"
    return cmake_flag(name, "BOOL", cmake_bool_string)

def cmake_path_flag(name, path_str):
    path_with_quotes = '"' + path_str + '"'
    return cmake_flag(name, "PATH", path_with_quotes)

class BloscConan(ConanFile):
    description = "A blocking, shuffling and lossless compression library"
    name = "blosc"
    version = "1.11.2"
    license = "BSD"
    url = "https://github.com/zogi/conan-blosc.git"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = { "shared": [True, False], "fPIC": [True, False] }
    default_options = "shared=False", "fPIC=True"
    exports = ["FindBlosc.cmake", "fix-shared-lib-install.patch"]
    
    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def config(self):
        if self.options.shared and ("fPIC" in self.options.fields):
            self.options.fPIC = True

    def source(self):
        self.run("git clone https://github.com/Blosc/c-blosc -c advice.detachedHead=false -b v%s src" % self.version)
        self.run("cd src && git apply ../fix-shared-lib-install.patch")
        replace_in_file("src/CMakeLists.txt", "project(blosc)",
                        "project(blosc)\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\nconan_basic_setup()")

    def build(self):
        cmake = CMake(self)
        cmake_arg_list = [ cmake.command_line
                         , cmake_bool_flag("BUILD_SHARED", self.options.shared)
                         , cmake_bool_flag("BUILD_STATIC", not self.options.shared)
                         , cmake_bool_flag("BUILD_TESTS", False)
                         , cmake_bool_flag("BUILD_BENCHMARKS", False)
                         , cmake_bool_flag("PREFER_EXTERNAL_LZ4", False)
                         , cmake_bool_flag("PREFER_EXTERNAL_SNAPPY", False)
                         , cmake_bool_flag("PREFER_EXTERNAL_ZLIB", False)
                         , cmake_bool_flag("PREFER_EXTERNAL_ZSTD", False)
                         , cmake_path_flag("CMAKE_INSTALL_PREFIX", self.package_folder)
                         ]
        if "fPIC" in self.options.fields:
            cmake_arg_list.append(cmake_bool_flag("CMAKE_POSITION_INDEPENDENT_CODE", self.options.fPIC))

        cmake_args = " ".join(cmake_arg_list)
        self.run("cmake ./src %s" % cmake_args)
        self.run("cmake --build . --target install --config %s" % self.settings.build_type)

    def package(self):
        self.copy("FindBlosc.cmake", ".", ".")

    def package_info(self):
        prefix = "lib" if self.settings.os == "Windows" and not self.options.shared else ""
        self.cpp_info.libs.append(prefix + "blosc")
        if self.settings.os == "Windows" and self.options.shared:
            self.cpp_info.defines.append("BLOSC_SHARED_LIBRARY")
