#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import platform
from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools


class LibjpegTurboConan(ConanFile):
    name = "libjpeg-turbo"
    version = "1.5.2"
    description = "SIMD-accelerated libjpeg-compatible JPEG codec library"
    url = "http://github.com/bincrafters/conan-libjpeg-turbo"
    author = "Bincrafters <bincrafters@gmail.com>"
    homepage = "https://libjpeg-turbo.org"
    license = "BSD 3-Clause, ZLIB"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "SIMD": [True, False],
               "arithmetic_encoder": [True, False],
               "arithmetic_decoder": [True, False],
               "libjpeg7_compatibility": [True, False],
               "libjpeg8_compatibility": [True, False],
               "mem_src_dst": [True, False],
               "turbojpeg": [True, False],
               "java": [True, False],
               "enable12bit": [True, False]}
    default_options = {'shared': False, 'fPIC': True, 'SIMD': True, 'arithmetic_encoder': True, 'arithmetic_decoder': True, 'libjpeg7_compatibility': True, 'libjpeg8_compatibility': True, 'mem_src_dst': True, 'turbojpeg': True, 'java': False, 'enable12bit': False}
    _source_subfolder = "source_subfolder"

    def configure(self):
        del self.settings.compiler.libcxx

        if self.settings.os == "Windows":
            self.requires.add("nasm/2.13.01@pierousseau/stable", private=True)
        if self.settings.compiler == "Visual Studio":
            self.options.remove("fPIC")
        if self.settings.os == "Emscripten":
            del self.options.SIMD

    def source(self):
        tools.get("http://downloads.sourceforge.net/project/libjpeg-turbo/%s/libjpeg-turbo-%s.tar.gz" % (self.version, self.version))
        os.rename("libjpeg-turbo-%s" % self.version, self._source_subfolder)
        os.rename(os.path.join(self._source_subfolder, "CMakeLists.txt"),
                  os.path.join(self._source_subfolder, "CMakeLists_original.txt"))
        shutil.copy("CMakeLists.txt",
                    os.path.join(self._source_subfolder, "CMakeLists.txt"))


    @property
    def _simd(self):
        if self.settings.os == "Emscripten":
            return False
        return self.options.SIMD

    def build_configure(self):
        prefix = os.path.abspath(self.package_folder)
        with tools.chdir(self._source_subfolder):
            # works for unix and mingw environments
            env_build = AutoToolsBuildEnvironment(self, win_bash=self.settings.os == 'Windows' and
                                                  platform.system() == 'Windows')
            env_build.fpic = self.options.fPIC
            if self.settings.os == 'Windows':
                prefix = tools.unix_path(prefix)
            args = ['--prefix=%s' % prefix]
            if self.options.shared:
                args.extend(['--disable-static', '--enable-shared'])
            else:
                args.extend(['--disable-shared', '--enable-static'])
            args.append('--with-jpeg7' if self.options.libjpeg7_compatibility else '--without-jpeg7')
            args.append('--with-jpeg8' if self.options.libjpeg8_compatibility else '--without-jpeg8')
            args.append('--with-arith-enc' if self.options.arithmetic_encoder else '--without-arith-enc')
            args.append('--with-arith-dec' if self.options.arithmetic_decoder else '--without-arith-dec')
            args.append('--with-turbojpeg' if self.options.turbojpeg else '--without-turbojpeg')
            args.append('--with-mem-srcdst' if self.options.mem_src_dst else '--without-mem-srcdst')
            args.append('--with-12bit' if self.options.enable12bit else '--without-12bit')
            args.append('--with-java' if self.options.java else '--without-java')
            args.append('--with-simd' if self.options.SIMD else '--without-simd')
            if self.options.fPIC:
                args.append('--with-pic')

            if self.settings.os == "Macos":
                tools.replace_in_file("configure",
                                      r'-install_name \$rpath/\$soname',
                                      r'-install_name \$soname')

            env_build.configure(args=args)
            env_build.make()
            env_build.make(args=['install'])

    def build_cmake(self):
        # fix cmake that gather install targets from the wrong dir
        for bin_program in ['tjbench', 'cjpeg', 'djpeg', 'jpegtran']:
            tools.replace_in_file("%s/CMakeLists_original.txt" % self._source_subfolder,
                                  '${CMAKE_CURRENT_BINARY_DIR}/' + bin_program + '-static.exe',
                                  '${CMAKE_CURRENT_BINARY_DIR}/bin/' + bin_program + '-static.exe')
        cmake = CMake(self)
        cmake.definitions['ENABLE_STATIC'] = not self.options.shared
        cmake.definitions['ENABLE_SHARED'] = self.options.shared
        cmake.definitions['WITH_SIMD'] = self._simd
        cmake.definitions['WITH_ARITH_ENC'] = self.options.arithmetic_encoder
        cmake.definitions['WITH_ARITH_DEC'] = self.options.arithmetic_decoder
        cmake.definitions['WITH_JPEG7'] = self.options.libjpeg7_compatibility
        cmake.definitions['WITH_JPEG8'] = self.options.libjpeg8_compatibility
        cmake.definitions['WITH_MEM_SRCDST'] = self.options.mem_src_dst
        cmake.definitions['WITH_TURBOJPEG'] = self.options.turbojpeg
        cmake.definitions['WITH_JAVA'] = self.options.java
        cmake.definitions['WITH_12BIT'] = self.options.enable12bit
        cmake.configure(source_dir=self._source_subfolder)
        cmake.build()
        cmake.install()

    def build(self):
        if self.settings.compiler == "Visual Studio":
            self.build_cmake()
        else:
            self.build_configure()

    def package(self):
        # remove unneeded directories
        shutil.rmtree(os.path.join(self.package_folder, 'share', 'man'), ignore_errors=True)
        shutil.rmtree(os.path.join(self.package_folder, 'share', 'doc'), ignore_errors=True)
        shutil.rmtree(os.path.join(self.package_folder, 'doc'), ignore_errors=True)

        # remove binaries
        for bin_program in ['cjpeg', 'djpeg', 'jpegtran', 'tjbench', 'wrjpgcom', 'rdjpgcom']:
            for ext in ['', '.exe']:
                try:
                    os.remove(os.path.join(self.package_folder, 'bin', bin_program+ext))
                except:
                    pass

        self.copy("license*", src=self._source_subfolder, dst="licenses", ignore_case=True, keep_path=False)
        # Copying generated header
        if self.settings.compiler == "Visual Studio":
            self.copy("jconfig.h", dst="include", src=".")

    def package_info(self):
        if self.settings.compiler == "Visual Studio":
            if self.options.shared:
                self.cpp_info.libs = ['jpeg', 'turbojpeg']
            else:
                self.cpp_info.libs = ['jpeg-static', 'turbojpeg-static']
        else:
            self.cpp_info.libs = ['jpeg', 'turbojpeg']
