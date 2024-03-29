#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
from conans.errors import ConanInvalidConfiguration
import os
import glob


class LibiconvConan(ConanFile):
    name = "libiconv"
    version = "1.15"
    description = "Convert text to and from Unicode"
    url = "https://github.com/bincrafters/conan-libiconv"
    homepage = "https://www.gnu.org/software/libiconv/"
    author = "Bincrafters <bincrafters@gmail.com>"
    topics = "libiconv", "iconv", "text", "encoding", "locale", "unicode", "conversion"
    license = "LGPL-2.1"
    exports = ["LICENSE.md"]
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, 'fPIC': True}
    short_paths = True
    _source_subfolder = "source_subfolder"
    recipe_version = "1"

    @property
    def _is_mingw_windows(self):
        return self.settings.os == 'Windows' and self.settings.compiler == 'gcc' and os.name == 'nt'

    @property
    def _is_msvc(self):
        return self.settings.compiler == 'Visual Studio'

    def build_requirements(self): 
        if self.settings.os == 'Windows' and "CONAN_BASH_PATH" not in os.environ:
            self.build_requires("msys2/20190524")

    def configure(self):
        del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        archive_name = "{0}-{1}".format(self.name, self.version)
        source_url = "https://ftp.gnu.org/gnu/libiconv"
        tools.get("{0}/{1}.tar.gz".format(source_url, archive_name),
                  sha256="ccf536620a45458d26ba83887a983b96827001e92a13847b45e4925cc8913178")
        os.rename(archive_name, self._source_subfolder)

    def _build_autotools(self):
        prefix = os.path.abspath(self.package_folder)
        rc = None
        host = None
        build = None
        if self._is_mingw_windows or self._is_msvc:
            prefix = prefix.replace('\\', '/')
            build = False
            if self.settings.arch == "x86":
                host = "i686-w64-mingw32"
                rc = "windres --target=pe-i386"
            elif self.settings.arch == "x86_64":
                host = "x86_64-w64-mingw32"
                rc = "windres --target=pe-x86-64"

        #
        # If you pass --build when building for iPhoneSimulator, the configure script halts.
        # So, disable passing --build by setting it to False.
        #
        if self.settings.os == "iOS" and self.settings.arch == "x86_64":
            build = False

        env_build = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)

        if self.settings.os != "Windows":
            env_build.fpic = self.options.fPIC

        configure_args = ['--prefix=%s' % prefix]
        if self.options.shared:
            configure_args.extend(['--disable-static', '--enable-shared'])
        else:
            configure_args.extend(['--enable-static', '--disable-shared'])

        env_vars = {}

        if self._is_mingw_windows:
            configure_args.extend(['CPPFLAGS=-I%s/include' % prefix,
                                   'LDFLAGS=-L%s/lib' % prefix,
                                   'RANLIB=:'])
        if self._is_msvc:
            runtime = str(self.settings.compiler.runtime)
            configure_args.extend(['CC=$PWD/build-aux/compile cl -nologo',
                                   'CFLAGS=-%s' % runtime,
                                   'CXX=$PWD/build-aux/compile cl -nologo',
                                   'CXXFLAGS=-%s' % runtime,
                                   'CPPFLAGS=-D_WIN32_WINNT=0x0600 -I%s/include' % prefix,
                                   'LDFLAGS=-L%s/lib' % prefix,
                                   'LD=link',
                                   'NM=dumpbin -symbols',
                                   'STRIP=:',
                                   'AR=$PWD/build-aux/ar-lib lib',
                                   'RANLIB=:'])
            env_vars['win32_target'] = '_WIN32_WINNT_VISTA'

            with tools.chdir(self._source_subfolder):
                tools.run_in_windows_bash(self, 'chmod +x build-aux/ar-lib build-aux/compile')

        if rc:
            configure_args.extend(['RC=%s' % rc, 'WINDRES=%s' % rc])

        with tools.chdir(self._source_subfolder):
            with tools.environment_append(env_vars):
                env_build.configure(args=configure_args, host=host, build=build)
                env_build.make()
                env_build.install()

    def build(self):
        with tools.vcvars(self.settings) if self._is_msvc else tools.no_op():
            self._build_autotools()

    def package(self):
        self.copy(os.path.join(self._source_subfolder, "COPYING.LIB"),
                  dst="licenses", ignore_case=True, keep_path=False)
        # remove libtool .la files - they have hard-coded paths
        with tools.chdir(os.path.join(self.package_folder, "lib")):
            for filename in glob.glob("*.la"):
                os.unlink(filename)

    def package_info(self):
        if self._is_msvc and self.options.shared:
            self.cpp_info.libs = ['iconv.dll.lib']
        else:
            self.cpp_info.libs = ['iconv']
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        if self.options.shared and self.settings.os == "Linux":
            self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))        
