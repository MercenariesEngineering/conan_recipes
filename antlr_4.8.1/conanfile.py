from conans import ConanFile, CMake
import os

class AntlrConan(ConanFile):
    name = "antlr"
    version = "4.8.1"
    license = "BSD"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    exports_sources = "src/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("libuuid/1.0.3@mercseng/v0")

    def build(self):
        cmake = CMake(self)
        definition_dict = {"WITH_STATIC_CRT":"Off"}
        cmake.configure(source_folder="src", defs=definition_dict)
        cmake.build(target = "antlr4_shared" if self.options.shared else "antlr4_static")

        # Explicit way:
        # self.run('cmake "%s/src" %s' % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="src/runtime/src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.jar", dst="class", src="src/class")

    def package_info(self):
        self.cpp_info.libs = ["antlr4-runtime-static" if self.settings.os == "Windows" else "antlr4-runtime"]
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
        else:
            if self.settings.os == "Windows":
                self.cpp_info.defines.append("ANTLR4CPP_STATIC")
        self.env_info.CLASSPATH.append(os.path.join(self.package_folder, "class/antlr-4.8-complete.jar"))
