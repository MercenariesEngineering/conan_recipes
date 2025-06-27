from conan import ConanFile
from conan.tools.apple import is_apple_os
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, replace_in_file, rmdir, unzip, collect_libs, apply_conandata_patches, export_conandata_patches
from conan.tools.gnu import Autotools
from conan.tools.microsoft import MSBuildDeps, MSBuildToolchain, MSBuild, is_msvc, is_msvc_static_runtime, msvc_runtime_flag, msvs_toolset
from conan.tools.scm import Version
from conan.tools.system import package_manager
from conan.errors import ConanInvalidConfiguration
import os

required_conan_version = ">=2.0.6"


class wxWidgetsConan(ConanFile):
    name = "wxwidgets"
    description = "wxWidgets is a C++ library that lets developers create applications for Windows, macOS, " \
                  "Linux and other platforms with a single code base."
    topics = ("wxwidgets", "gui", "ui")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.wxwidgets.org"
    license = "wxWidgets"
    settings = "os", "arch", "compiler", "build_type"

    package_type = "library"
    options = {
               "aui": [True, False],
               "cairo": [True, False],
               "custom_disables": ["ANY"],
               "custom_enables": ["ANY"], # comma splitted list
               "debugreport": [True, False],
               "fPIC": [True, False],
               "fs_inet": [True, False],
               "help": [True, False],
               "html": [True, False],
               "html_help": [True, False],
               "jpeg": [None, "system", "libjpeg", "libjpeg-turbo", "mozjpeg"],
               "mediactrl": [True, False],  # disabled by default as wxWidgets still uses deprecated GStreamer 0.10
               "opengl": [True, False],
               "propgrid": [True, False],
               "protocol": [True, False],
               "ribbon": [True, False],
               "richtext": [True, False],
               "secretstore": [True, False],
               "shared": [True, False],
               "sockets": [True, False],
               "stc": [True, False],
               "unicode": [True, False],
               "url": [True, False],
               "webview": [True, False],
               "xml": [True, False],
               "xrc": [True, False],
               #"compatibility": ["2.8", "3.0", "3.1"],
    }
    default_options = {
               "aui": True,
               "cairo": True,
               "custom_disables": "",
               "custom_enables": "",
               "debugreport": True,
               "fPIC": True,
               "fs_inet": True,
               "help": True,
               "html": True,
               "html_help": True,
               "jpeg": "libjpeg",
               "mediactrl": False,
               "opengl": True,
               "propgrid": True,
               "protocol": True,
               "ribbon": True,
               "richtext": True,
               "secretstore": True,
               "shared": False,
               "sockets": True,
               "stc": True,
               "unicode": True,
               "url": True,
               "webview": False,
               "xml": True,
               "xrc": True,
               #"compatibility": "2.8",
               # WebKitGTK for GTK2 is not available as a system dependency on modern distros.
               # When gtk/system defaults to GTK3, turn this back on.
    }


    def export_sources(self):
        export_conandata_patches(self)
        copy(self, "vc140.tar.gz", self.recipe_folder, self.export_sources_folder)

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")
        if self.settings.os != "Linux":
            self.options.rm_safe("secretstore")
            self.options.rm_safe("cairo")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    @property
    def _gtk_version(self):
        return f"gtk{self.dependencies['gtk'].options.version}"

    def system_requirements(self):
        apt = package_manager.Apt(self)
        packages = []
        if self.options.get_safe("secretstore"):
            packages.append("libsecret-1-dev")
        if self.options.webview:
            if self._gtk_version == "gtk2":
                packages.extend(["libsoup2.4-dev",
                                 "libwebkitgtk-dev"])
            else:
                packages.extend(["libsoup3.0-dev",
                                 "libwebkit2gtk-4.0-dev"])
        if self.options.get_safe("cairo"):
            packages.append("libcairo2-dev")
        apt.install(packages)

        yum = package_manager.Yum(self)
        packages = []
        if self.options.get_safe("secretstore"):
            packages.append("libsecret-devel")
        if self.options.webview:
                packages.extend(["libsoup3-devel",
                                 "webkit2gtk4.1-devel"])
        if self.options.get_safe("cairo"):
            packages.append("cairo-devel")
        yum.install(packages)

    def build_requirements(self):
        self.tool_requires("ninja/[>=1.10.2 <2]")
        self.tool_requires("cmake/[>=3.17 <4]")

    # TODO: add support for gtk non system version when it's ready for Conan 2
    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("xorg/system")
            self.requires("gtk/system")
            if self.options.get_safe("opengl", default=False):
                self.requires("opengl/system")
            self.requires("xkbcommon/1.6.0", options={"with_x11": True})
            # TODO: Does not work right now
            # if self.options.get_safe("cairo"):
            #    self.requires("cairo/1.18.0")
            if self.options.mediactrl:
                self.requires("gstreamer/1.22.3")
                self.requires("gst-plugins-base/1.19.2")
            self.requires("libcurl/[>=7.78.0 <9]")

        if self.options.jpeg == "libjpeg":
            self.requires("libjpeg/9e")
        elif self.options.jpeg == "libjpeg-turbo":
            self.requires("libjpeg-turbo/3.0.2")
        elif self.options.jpeg == "mozjpeg":
            self.requires("mozjpeg/4.1.5")

        self.requires("freetype/2.13.2")
        self.requires("libpng/[>=1.6 <2]")
        self.requires("libtiff/4.6.0")
        self.requires("zlib/[>=1.2.11 <2]")
        self.requires("expat/[>=2.6.2 <3]")
        self.requires("pcre2/10.42")
        self.requires("nanosvg/cci.20231025")

    def validate(self):
        if self.settings.os == "Linux":
            if not self.dependencies.direct_host["xkbcommon"].options.with_x11:
                raise ConanInvalidConfiguration("The 'with_x11' option for the 'xkbcommon' package must be enabled")

    #def layout(self):
    #    cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        unzip(self, os.path.join(self.export_sources_folder, "vc140.tar.gz"), self.source_folder)

    def _configure_autotools(self):
        autotools = Autotools(self)
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
        if self.options.xrc :
            configure_args.append("--enable-xrc")

        configure_args.append("--with-zlib=sys")

        autotools.cxx_flags.append("-Wno-narrowing")
        autotools.cxx_flags.append("-Wno-unused-local-typedefs")

        autotools.configure(configure_dir=self.source_folder, args=configure_args)
        return autotools

    def generate(self):
        if is_msvc(self):
            # The msbuild generator only works with Visual Studio
            deps = MSBuildDeps(self)
            deps.generate()
            # The toolchain.props is not injected yet, but it also generates VCVars
            toolchain = MSBuildToolchain(self)
            toolchain.properties["IncludeExternals"] = "true"
            toolchain.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)

    def build(self):
        self._patch_sources()
        if is_msvc(self):
            msbuild = MSBuild(self)
            msbuild.platform = "x64"
            msbuild.build(self.source_folder+"\\build\\msw\\wx.sln")            
        else:
            autotools = self._configure_autotools()
            autotools.make()
            if self.options.stc :
                with tools.environment_append(autotools.vars):
                    self.run("cd contrib/src/stc && make && cd ../../..")

    def package(self):
        copy(self, pattern="LICENSE",  dst=os.path.join(self.package_folder, "licenses"),      src=self.source_folder)
        copy(self, pattern='*.h',      dst=os.path.join(self.package_folder, "include", "wx"), src=os.path.join(self.source_folder, "include", "wx"), keep_path=True)
        copy(self, pattern='*.h',      dst=os.path.join(self.package_folder, "include", "wx"), src=os.path.join(self.source_folder, "contrib", "include", "wx"), keep_path=True)
        copy(self, pattern='*.a',      dst=os.path.join(self.package_folder, "lib"),           src=os.path.join(self.build_folder, "lib"), keep_path=True)
        copy(self, pattern='*.lib',    dst=os.path.join(self.package_folder, "lib"),           src=os.path.join(self.build_folder, "build", "msw", "lib", "x64", "Release"), keep_path=True)
        copy(self, pattern='*.lib',    dst=os.path.join(self.package_folder, "lib"),           src=os.path.join(self.build_folder, "build", "msw", "lib", "x64", "Debug"), keep_path=True)

        # copy setup.h
        copy(self, pattern='*setup.h', dst=os.path.join(self.package_folder, "include", "msvc"), src=os.path.join(self.build_folder, "include", "msvc"))
        copy(self, pattern='*setup.h', dst=os.path.join(self.package_folder, "lib"), src=os.path.join(self.build_folder, "lib"))

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "wxWidgets")
        self.cpp_info.set_property("cmake_target_name", "wxWidgets::wxWidgets")
        self.cpp_info.set_property("pkg_config_name", "wxwidgets")

        _version = Version(self.version)
        version_suffix_major_minor = f"-{_version.major}.{_version.minor}"

        if self.settings.os == 'Linux':
            unicode_ = 'u' if self.options.unicode else ''
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
                version = f"{_version.major}{_version.minor}"
                suffix = ''

            def base_library_pattern(library):
                return '{prefix}base{version}{unicode_}{debug}_%s{suffix}' % library

            def library_pattern(library):
                return '{prefix}{toolkit}{version}{unicode_}{debug}_%s{suffix}' % library

            libs = ['wxregex{version}{unicode_}{debug}{suffix}',
                    '{prefix}base{version}{unicode_}{debug}{suffix}',
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
                libs.append(library_pattern('stc'))
            if self.options.webview:
                libs.append(library_pattern('webview'))
            if self.options.xrc:
                libs.append(library_pattern('xrc'))
            for lib in reversed(libs):
                self.cpp_info.libs.append(lib.format(prefix=prefix, toolkit=toolkit, version=version, unicode=unicode_, debug=debug, suffix=suffix))
        elif self.settings.os == 'Windows':
            self.cpp_info.libs = collect_libs(self)

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

            arch_suffix = '_x64' if is_msvc(self) else ''
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
            self.cpp_info.system_libs.extend(['kernel32',
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
                self.cpp_info.system_libs.extend(['uxtheme',
                                                  'version',
                                                  'shlwapi',
                                                  'oleacc'])
        if is_msvc(self):
            self.cpp_info.includedirs.append(os.path.join('include', 'msvc'))
        elif self.settings.os != 'Windows':
            unix_include_path = os.path.join("include", "wx{}".format(version_suffix_major_minor))
            self.cpp_info.includedirs = [unix_include_path] + self.cpp_info.includedirs
