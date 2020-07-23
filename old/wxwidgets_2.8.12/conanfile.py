#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, MSBuild, tools
import os


class wxWidgetsConan(ConanFile):
    name = "wxwidgets"
    version = "2.8.12"
    description = "wxWidgets is a C++ library that lets developers create applications for Windows, Mac OS X, " \
                  "Linux and other platforms with a single code base."
    url = "https://github.com/bincrafters/conan-wxwidgets"
    homepage = "https://www.wxwidgets.org/"
    license = "wxWidgets"
    exports = ["LICENSE.md", "*.patch", "vc140.tar.gz"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "unicode": [True, False],
               #"compatibility": ["2.8", "3.0", "3.1"],
               "zlib": [None, "system", "zlib"],
               "png": [None, "system", "libpng"],
               "jpeg": [None, "system", "libjpeg", "libjpeg-turbo", "mozjpeg"],
               "tiff": [None, "system", "libtiff"],
               "expat": [None, "system", "expat"],
               "secretstore": [True, False],
               "aui": [True, False],
               "opengl": [True, False],
               "html": [True, False],
               "mediactrl": [True, False],  # disabled by default as wxWidgets still uses deprecated GStreamer 0.10
               "propgrid": [True, False],
               "debugreport": [True, False],
               "ribbon": [True, False],
               "richtext": [True, False],
               "sockets": [True, False],
               "stc": [True, False],
               "webview": [True, False],
               "xml": [True, False],
               "xrc": [True, False],
               "cairo": [True, False]}
    default_options = {
               "shared": False,
               "fPIC": True,
               "unicode": True,
               #"compatibility": "2.8",
               "zlib": "zlib",
               "png": "libpng",
               "jpeg": "libjpeg-turbo",
               "tiff": "libtiff",
               "expat": "expat",
               "secretstore": False,
               "aui": True,
               "opengl": True,
               "html": True,
               "mediactrl": False,
               "propgrid": False,
               "debugreport": True,
               "ribbon": False,
               "richtext": True,
               "sockets": True,
               "stc": True,
               "webview": False,
               "xml": True,
               "xrc": True,
               "cairo": False
    }
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
        if self.settings.os != 'Linux':
            self.options.remove('cairo')

    def system_requirements(self):
        if self.settings.os == 'Linux' and tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                if self.settings.arch == 'x86':
                    arch_suffix = ':i386'
                elif self.settings.arch == 'x86_64':
                    arch_suffix = ':amd64'
                packages = ['libx11-dev%s' % arch_suffix,
                            'libgtk2.0-dev%s' % arch_suffix]
                # TODO : GTK3
                # packages.append('libgtk-3-dev%s' % arch_suffix)
                if self.options.secretstore:
                    packages.append('libsecret-1-dev%s' % arch_suffix)
                if self.options.opengl:
                    packages.extend(['mesa-common-dev%s' % arch_suffix,
                                     'libgl1-mesa-dev%s' % arch_suffix])
                if self.options.webview:
                    packages.extend(['libsoup2.4-dev%s' % arch_suffix,
                                     'libwebkitgtk-dev%s' % arch_suffix])
                # TODO : GTK3
                #                    'libwebkitgtk-3.0-dev%s' % arch_suffix])
                #if self.options.mediactrl:
                #    packages.extend(['libgstreamer0.10-dev%s' % arch_suffix,
                #                     'libgstreamer-plugins-base0.10-dev%s' % arch_suffix])
                if self.options.cairo:
                    packages.append('libcairo2-dev%s' % arch_suffix)
                for package in packages:
                    installer.install(package)

    def requirements(self):
        if self.options.png == 'libpng':
            self.requires.add('libpng/1.6.37@bincrafters/stable')
        if self.options.jpeg == 'libjpeg':
            self.requires.add('libjpeg/9c@bincrafters/stable')
        elif self.options.jpeg == 'libjpeg-turbo':
            self.requires.add('libjpeg-turbo/1.5.2@pierousseau/stable')
        elif self.options.jpeg == 'mozjpeg':
            self.requires.add('mozjpeg/3.3.1@bincrafters/stable')
        if self.options.tiff == 'libtiff':
            self.requires.add('libtiff/4.0.9@bincrafters/stable')
        if self.options.zlib == 'zlib':
            self.requires.add('zlib/1.2.11@conan/stable')
        if self.options.expat == 'expat':
            self.requires.add('Expat/2.2.6@pix4d/stable')

    def source(self):
        # https://github.com/wxWidgets/wxWidgets/releases/download/v2.8.12/wxWidgets-2.8.12.tar.gz
        filename = "wxWidgets-%s.tar.gz" % self.version
        tools.download("https://github.com/wxWidgets/wxWidgets/releases/download/v%s/%s" % (self.version, filename), filename)
        tools.untargz(filename)
        os.unlink(filename)
        os.rename("wxWidgets-" + self.version, self._source_subfolder)

        #tools.patch(base_path=self._source_subfolder, patch_file="wx_2.8.12.patch")
        self.run("cd " + self._source_subfolder + " && patch -p0 < ../wx_2.8.12.patch && cd ..")
        
        if self.settings.compiler == 'Visual Studio':
            #tools.download("http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD", "config.guess")
            #tools.download("http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD", "config.sub")
            #os.remove(self._source_subfolder+"/config.guess")
            #os.remove(self._source_subfolder+"/config.sub")
            #os.rename("config.guess", self._source_subfolder+"/config.guess")
            #os.rename("config.sub"  , self._source_subfolder+"/config.sub")
            tools.untargz("vc140.tar.gz", self._source_subfolder)

    def add_libraries_from_pc(self, library):
        pkg_config = tools.PkgConfig(library)
        libs = [lib[2:] for lib in pkg_config.libs_only_l]  # cut -l prefix
        lib_paths = [lib[2:] for lib in pkg_config.libs_only_L]  # cut -L prefix
        self.cpp_info.libs.extend(libs)
        self.cpp_info.libdirs.extend(lib_paths)
        self.cpp_info.sharedlinkflags.extend(pkg_config.libs_only_other)
        self.cpp_info.exelinkflags.extend(pkg_config.libs_only_other)

    def _configure_autotools(self):
        autotools = AutoToolsBuildEnvironment(self)
        configure_args = []
        if ("fPIC" in self.options.fields and self.options.fPIC == True):
            autotools.fpic = True
            configure_args.append("--with-fpic")
        else:
            autotools.fpic = False
        if self.options.shared:
            configure_args.append("--enable-shared")
        else:
            configure_args.append("--disable-shared")
            configure_args.append("--enable-static")
        if self.settings.build_type == "Debug":
            configure_args.append("--enable-debug")
        if self.options.png == None:
            configure_args.append("--without-libpng")
        if self.options.jpeg == None:
            configure_args.append("--without-libjpeg")
        if self.options.tiff == None:
            configure_args.append("--without-libtiff")
        if self.options.expat == None:
            configure_args.append("--without-expat")
        if self.options.sockets == None:
            configure_args.append("--disable-sockets")
        if self.options.unicode :
            configure_args.append("--enable-unicode")
        if self.options.aui :
            configure_args.append("--enable-aui")
        if self.options.opengl :
            configure_args.append("--with-opengl")
        if self.options.html :
            configure_args.append("--enable-html")
        if self.options.mediactrl :
            configure_args.append("--enable-mediactrl")
        if self.options.debugreport :
            configure_args.append("--enable-debugreport")
        if self.options.richtext :
            configure_args.append("--enable-richtext")
        if self.options.sockets :
            configure_args.append("--enable-sockets")
        #if self.options.stc :
        #    configure_args.append("--enable-stc")
        #if self.options.webview :
        #    configure_args.append("--enable-webview")
        #if self.options.xml :
        #    configure_args.append("--enable-xml")
        if self.options.xrc :
            configure_args.append("--enable-xrc")

        configure_args.append("--with-zlib=sys")

        autotools.cxx_flags.append("-Wno-narrowing")
        autotools.cxx_flags.append("-Wno-unused-local-typedefs")

        autotools.configure(configure_dir=self._source_subfolder, args=configure_args)
        return autotools

    def build(self):
        if self.settings.compiler == "Visual Studio":
            msbuild = MSBuild(self)
            msbuild.build(self._source_subfolder+"\\build\\msw\\wx.sln")            
        else:
            autotools = self._configure_autotools()
            autotools.make()
            if self.options.stc :
                with tools.environment_append(autotools.vars):
                    self.run("cd contrib/src/stc && make && cd ../../..")

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        #autotools = self._configure_autotools()
        #autotools.install()
        self.copy(pattern='*.h', dst='include/wx', src=self._source_subfolder+'/include/wx', keep_path=True)
        self.copy(pattern='*.h', dst='include/wx', src=self._source_subfolder+'/contrib/include/wx', keep_path=True)
        self.copy(pattern='*.a', dst='lib', src='lib/', keep_path=True)
        self.copy(pattern='*.lib', dst='lib', src=self._source_subfolder+'/build/msw/lib/x64/Release', keep_path=True)
        self.copy(pattern='*.lib', dst='lib', src=self._source_subfolder+'/build/msw/lib/x64/Debug', keep_path=True)

        # copy setup.h
        self.copy(pattern='*setup.h', dst=os.path.join('include', 'wx'), src='lib', keep_path=False)
        self.copy(pattern='*setup.h', dst=os.path.join('include', 'wx'), src=self._source_subfolder+'/lib', keep_path=False)

        #if self.settings.os == 'Windows':
        #    # copy wxrc.exe
        #    self.copy(pattern='*', dst='bin', src='bin', keep_path=False)
        #else:
        #    # make relative symlink
        #    bin_dir = os.path.join(self.package_folder, 'bin')
        #    for x in os.listdir(bin_dir):
        #        filename = os.path.join(bin_dir, x)
        #        if os.path.islink(filename):
        #            target = os.readlink(filename)
        #            if os.path.isabs(target):
        #                rel = os.path.relpath(target, bin_dir)
        #                os.remove(filename)
        #                os.symlink(rel, filename)

    def package_info(self):

        if self.settings.os == 'Linux':
            version_tokens = self.version.split('.')
            version_major = version_tokens[0]
            version_minor = version_tokens[1]
            version_suffix_major_minor = '-%s.%s' % (version_major, version_minor)
            unicode = 'u' if self.options.unicode else ''
            debug = 'd' if self.settings.build_type == 'Debug' else ''
            if self.settings.os == 'Linux':
                prefix = 'wx_'
                toolkit = 'gtk2'
                version = ''
                suffix = version_suffix_major_minor
            elif self.settings.os == 'Macos':
                prefix = 'wx_'
                toolkit = 'osx_cocoa'
                version = ''
                suffix = version_suffix_major_minor
            elif self.settings.os == 'Windows':
                prefix = 'wx'
                toolkit = 'msw'
                version = '%s%s' % (version_major, version_minor)
                suffix = ''

            def base_library_pattern(library):
                return '{prefix}base{version}{unicode}{debug}_%s{suffix}' % library

            def library_pattern(library):
                return '{prefix}{toolkit}{version}{unicode}{debug}_%s{suffix}' % library

            libs = ['wxregex{version}{unicode}{debug}{suffix}',
                    '{prefix}base{version}{unicode}{debug}{suffix}',
                    library_pattern('core'),
                    library_pattern('adv')]
            if self.options.sockets:
                libs.append(base_library_pattern('net'))
            if self.options.xml:
                libs.append(base_library_pattern('xml'))
            if self.options.aui:
                libs.append(library_pattern('aui'))
            if self.options.opengl:
                libs.append(library_pattern('gl'))
            if self.options.html:
                libs.append(library_pattern('html'))
            if self.options.mediactrl:
                libs.append(library_pattern('media'))
            if self.options.propgrid:
                libs.append(library_pattern('propgrid'))
            if self.options.debugreport:
                libs.append(library_pattern('qa'))
            if self.options.ribbon:
                libs.append(library_pattern('ribbon'))
            if self.options.richtext:
                libs.append(library_pattern('richtext'))
            if self.options.stc:
                #if not self.options.shared:
                #    scintilla_suffix = '{debug}' if self.settings.os == "Windows" else '{suffix}'
                #    libs.append('wxscintilla' + scintilla_suffix)
                libs.append(library_pattern('stc'))
            if self.options.webview:
                libs.append(library_pattern('webview'))
            if self.options.xrc:
                libs.append(library_pattern('xrc'))
            for lib in reversed(libs):
                self.cpp_info.libs.append(lib.format(prefix=prefix,
                                                     toolkit=toolkit,
                                                     version=version,
                                                     unicode=unicode,
                                                     debug=debug,
                                                     suffix=suffix))
        elif self.settings.os == 'Windows':
            self.cpp_info.libs = tools.collect_libs(self)


        self.cpp_info.defines.append('wxUSE_GUI=1')
        if self.settings.build_type == 'Debug':
            self.cpp_info.defines.append('__WXDEBUG__')
        if self.options.shared:
            self.cpp_info.defines.append('WXUSINGDLL')
        if self.settings.os == 'Linux':
            self.cpp_info.defines.append('__WXGTK__')
            self.add_libraries_from_pc('gtk+-2.0')
            self.add_libraries_from_pc('x11')
            self.cpp_info.libs.extend(['dl', 'pthread', 'SM'])
        elif self.settings.os == 'Macos':
            self.cpp_info.defines.extend(['__WXMAC__', '__WXOSX__', '__WXOSX_COCOA__'])
            for framework in ['Carbon',
                              'Cocoa',
                              'AudioToolbox',
                              'OpenGL',
                              'AVKit',
                              'AVFoundation',
                              'Foundation',
                              'IOKit',
                              'ApplicationServices',
                              'CoreText',
                              'CoreGraphics',
                              'CoreServices',
                              'CoreMedia',
                              'Security',
                              'ImageIO',
                              'System',
                              'WebKit']:
                self.cpp_info.exelinkflags.append('-framework %s' % framework)
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        elif self.settings.os == 'Windows':
            # see cmake/init.cmake
            compiler_prefix = {'Visual Studio': 'vc',
                               'gcc': 'gcc',
                               'clang': 'clang'}.get(str(self.settings.compiler))

            arch_suffix = '_x64' if self.settings.compiler == 'Visual Studio' and self.settings.arch == 'x86_64' else ''
            # use the following code in next release:
            # arch_suffix = '_x64' if self.settings.arch == 'x86_64' else ''
            lib_suffix = '_dll' if self.options.shared else '_lib'
            libdir = '%s%s%s' % (compiler_prefix, arch_suffix, lib_suffix)
            libdir = os.path.join('lib', libdir)
            self.cpp_info.bindirs.append(libdir)
            self.cpp_info.libdirs.append(libdir)
            self.cpp_info.defines.append('__WXMSW__')
            # disable annoying auto-linking
            self.cpp_info.defines.extend(['wxNO_NET_LIB',
                                          'wxNO_XML_LIB',
                                          'wxNO_REGEX_LIB',
                                          'wxNO_ZLIB_LIB',
                                          'wxNO_JPEG_LIB',
                                          'wxNO_PNG_LIB',
                                          'wxNO_TIFF_LIB',
                                          'wxNO_ADV_LIB',
                                          'wxNO_HTML_LIB',
                                          'wxNO_GL_LIB',
                                          'wxNO_QA_LIB',
                                          'wxNO_XRC_LIB',
                                          'wxNO_AUI_LIB',
                                          'wxNO_PROPGRID_LIB',
                                          'wxNO_RIBBON_LIB',
                                          'wxNO_RICHTEXT_LIB',
                                          'wxNO_MEDIA_LIB',
                                          'wxNO_STC_LIB',
                                          'wxNO_WEBVIEW_LIB'])
            self.cpp_info.libs.extend(['kernel32',
                                       'user32',
                                       'gdi32',
                                       'comdlg32',
                                       'winspool',
                                       'shell32',
                                       'comctl32',
                                       'ole32',
                                       'oleaut32',
                                       'uuid',
                                       'wininet',
                                       'rpcrt4',
                                       'winmm',
                                       'advapi32',
                                       'wsock32'])
            # Link a few libraries that are needed when using gcc on windows
            if self.settings.compiler == 'gcc':
                self.cpp_info.libs.extend(['uxtheme',
                                           'version',
                                           'shlwapi',
                                           'oleacc'])
        if self.settings.compiler == 'Visual Studio':
            self.cpp_info.includedirs.append(os.path.join('include', 'msvc'))
        elif self.settings.os != 'Windows':
            unix_include_path = os.path.join("include", "wx{}".format(version_suffix_major_minor))
            self.cpp_info.includedirs = [unix_include_path] + self.cpp_info.includedirs
