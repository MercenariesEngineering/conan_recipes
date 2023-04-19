#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import platform
from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools

class FFmpegConan(ConanFile):
    name = "FFmpeg"
    version = "4.3.1"
    description = "A complete, cross-platform solution to record, convert and stream audio and video."
    url = "http://github.com/bincrafters/conan-libjpeg-turbo"
    author = "Bincrafters <bincrafters@gmail.com>"
    homepage = "https://ffmpeg.org/"
    license = "LGPL v2.1+"
    _source_subfolder = "source_subfolder"
    configure_options = '--enable-yasm --enable-asm --enable-shared --disable-static --disable-programs --enable-avresample --enable-zlib'
    settings = "os", "arch", "compiler", "build_type"
    recipe_version = "2"

    def source(self):
        tools.get("https://github.com/FFmpeg/FFmpeg/archive/n%s.tar.gz" % (self.version))
        os.rename("FFmpeg-n%s" % self.version, self._source_subfolder)

    def build_requirements(self):
        self.build_requires("zlib/1.2.11@mercseng/v0")
        self.build_requires("nasm/2.13.02@mercseng/v0")

    def build(self):
        if self.settings.compiler == 'Visual Studio':
            self.build_msvc()
        else:
            env_build = AutoToolsBuildEnvironment(self)

            args = self.configure_options.split(" ")
            args.append('--prefix=%s' % self.package_folder)
            args.append('--enable-pic')

            with tools.chdir(self._source_subfolder):
                env_build.configure(args=args)
                env_build.make()
                env_build.make(args=['install'])

    def build_msvc(self):
        env_vars = tools.vcvars_dict(self)
        zlib = self.deps_cpp_info["zlib"]
        env_vars["INCLUDE"] += zlib.include_paths
        env_vars["LIB"] += zlib.lib_paths
        with tools.environment_append(env_vars):
            # FFmpeg only have configure/makefile option on Windows
            # We use msys2 and Visual to build it has required by the FFmpeg documentation
            f = open("build.sh", "w")
            f.write("""#/usr/bin/bash
export PATH=/usr/bin:$PATH
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig
cd {}
./configure --toolchain=msvc --arch=x86_64 {} --extra-cflags="-MD" --prefix={}
make -j8
make install
            """.format(tools.unix_path(self._source_subfolder), self.configure_options, tools.unix_path(self.package_folder)))
            f.close()
            if not "MSYS2" in os.environ:
                self.output.error("Please define MSYS2 with the path to the msys2 root directory. Don't forget to install make and diffutils in msys2:\n\tpacman -S make\n\tpacman -S diffutils")
            msys2 = os.environ["MSYS2"]
            self.output.info("Using MSYS2 in "+msys2)
            self.run(msys2+'/usr/bin/bash.exe build.sh')

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
        else:
            self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
