import os
from conans import ConanFile, CMake, tools

class GlewConan(ConanFile):
    name = "glew"
    version = "2.1.0"
    description = "The GLEW library"
    url = "http://github.com/bincrafters/conan-glew"
    homepage = "http://github.com/nigels-com/glew"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "FindGLEW.cmake"]
    generators = "cmake"
    settings = "os", "arch", "build_type", "compiler"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    _source_subfolder = "_source_subfolder"

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        release_name = "%s-%s" % (self.name, self.version)
        tools.get("{0}/releases/download/{1}/{1}.tgz".format(self.homepage, release_name), sha256="04de91e7e6763039bc11940095cd9c7f880baba82196a7765f727ac05a993c95")
        os.rename(release_name, self._source_subfolder)
        tools.replace_in_file("%s/build/cmake/CMakeLists.txt" % self._source_subfolder, "include(GNUInstallDirs)",
"""
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
include(GNUInstallDirs)
""")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_UTILS"] = "OFF"
        cmake.configure(source_folder="{}/build/cmake".format(self._source_subfolder))
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

        self.copy("FindGLEW.cmake", ".", ".", keep_path=False)
        self.copy("include/*", ".", "%s" % self._source_subfolder, keep_path=True)
        self.copy("%s/license*" % self._source_subfolder, dst="licenses",  ignore_case=True, keep_path=False)
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)

        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                self.copy(pattern="*.pdb", dst="bin", keep_path=False)
                if self.options.shared:
                    if self.settings.build_type == "Release":
                        self.copy("glew32.lib", "lib", "lib", keep_path=False)
                        self.copy("glew32.dll", "bin", "bin", keep_path=False)
                    else:
                        self.copy("glew32d.lib", "lib", "lib", keep_path=False)
                        self.copy("glew32d.dll", "bin", "bin", keep_path=False)
                else:
                    if self.settings.build_type == "Release":
                        self.copy("libglew32.lib", "lib", "lib", keep_path=False)
                    else:
                        self.copy("libglew32d.lib", "lib", "lib", keep_path=False)
            else:
                if self.options.shared:
                    self.copy(pattern="*32.dll.a", dst="lib", keep_path=False)
                    self.copy(pattern="*32d.dll.a", dst="lib", keep_path=False)
                    self.copy(pattern="*.dll", dst="bin", keep_path=False)
                else:
                    self.copy(pattern="*32.a", dst="lib", keep_path=False)
                    self.copy(pattern="*32d.a", dst="lib", keep_path=False)
        elif self.settings.os == "Macos":
            if self.options.shared:
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", keep_path=False)
        else:
            if self.options.shared:
                self.copy(pattern="*.so", dst="lib", keep_path=False)
                self.copy(pattern="*.so.*", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ['glew32']

            if not self.options.shared:
                self.cpp_info.defines.append("GLEW_STATIC")

            if self.settings.compiler == "Visual Studio":
                if not self.options.shared:
                    self.cpp_info.libs[0] = "lib" + self.cpp_info.libs[0]
                    self.cpp_info.libs.append("OpenGL32.lib")
            else:
                self.cpp_info.libs.append("opengl32")

        else:
            self.cpp_info.libs = ['GLEW']
            if self.settings.os == "Macos":
                self.cpp_info.exelinkflags.append("-framework OpenGL")
            elif not self.options.shared:
                self.cpp_info.libs.append("GL")

        if self.settings.build_type == "Debug":
            self.cpp_info.libs[0] += "d"
