#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import glob
from conans import ConanFile, CMake, tools


class GlfwConan(ConanFile):
    name = "glfw"
    version = "3.3"
    description = "The GLFW library - Builds on Windows, Linux and Macos/OSX"
    settings = "os", "arch", "build_type", "compiler"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, "fPIC": True}
    license = "Zlib"
    url = "https://github.com/bincrafters/conan-glfw"
    homepage = "https://github.com/glfw/glfw"
    author = "Bincrafters <bincrafters@gmail.com>"
    topics = ("conan", "gflw", "opengl", "vulcan", "opengl-es")
    exports = "LICENSE"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        sha256 = "1092f6815d1f6d1f67479d2dad6057172b471122d911e7a7ea2be120956ffaa4"
        tools.get("{}/archive/{}.zip".format(self.homepage, self.version), sha256=sha256)
        extracted_folder = self.name + '-' + self.version
        os.rename(extracted_folder, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["GLFW_BUILD_EXAMPLES"] = False
        cmake.definitions["GLFW_BUILD_TESTS"] = False
        cmake.definitions["GLFW_BUILD_DOCS"] = False
        cmake.configure(build_dir=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

        if self.settings.os == "Macos" and self.options.shared:
            with tools.chdir(os.path.join(self._source_subfolder, 'src')):
                for filename in glob.glob('*.dylib'):
                    self.run('install_name_tool -id {filename} {filename}'.format(filename=filename))

    def package(self):
        self.copy("LICENSE.md", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(['Xrandr', 'Xrender', 'Xi', 'Xinerama', 'Xcursor', 'GL', 'm', 'dl', 'drm', 'Xdamage', 'X11-xcb', 'xcb-glx', 'xcb-dri2', 'xcb-dri3', 'xcb-present', 'xcb-sync', 'Xxf86vm', 'Xfixes', 'Xext', 'X11', 'pthread', 'xcb', 'Xau'])
            if self.options.shared:
                self.cpp_info.exelinkflags.append("-lrt -lm -ldl")
        elif self.settings.os == "Macos":
            self.cpp_info.exelinkflags.append("-framework OpenGL -framework Cocoa -framework IOKit -framework CoreVideo")
