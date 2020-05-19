import os
from conans import ConanFile, MSBuild, tools, AutoToolsBuildEnvironment


# Based on recipe from https://github.com/lasote/conan-cpython
class CpythonConan(ConanFile):
    name = "cpython"
    version = "3.7.7"
    license = "PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2"
    url = "https://github.com/lasote/conan-cpython"
    description = "CPython"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "optimizations": [True, False]}
    default_options = "shared=True", "fPIC=True"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("OpenSSL/1.1.1c@conan/stable")
        # Because cpython is both a 'requires' dependency and a 'build_requires' dependency,
        # We must override OpenSSL's zlib dependency to something compatible with our other dependencies:
        self.requires("zlib/1.2.11") 

        if self.settings.os == "Linux":
            self.requires("expat/2.2.9")
            self.requires("lzma/5.2.4@bincrafters/stable")
            self.requires("libuuid/1.0.3")
            self.requires("bzip2/1.0.8")
            self.requires("libffi/3.2.1")
            self.requires("gdbm/1.18.1@bincrafters/stable")
            self.requires("sqlite3/3.30.1")
            self.requires("ncurses/6.1@conan/stable")
            self.requires("readline/7.0@bincrafters/stable")

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/python/cpython/archive/v%s.tar.gz" % self.version)

        # This automatic linking to python_x_.lib is not helping ; get rid of it
        tools.replace_in_file( os.path.join(self.src_subfolder, "PC", "pyconfig.h"),
"""/* For an MSVC DLL, we can nominate the .lib files used by extensions */
#ifdef MS_COREDLL
#       if !defined(Py_BUILD_CORE) && !defined(Py_BUILD_CORE_BUILTIN)
                /* not building the core - must be an ext */
#               if defined(_MSC_VER)
                        /* So MSVC users need not specify the .lib
                        file in their Makefile (other compilers are
                        generally taken care of by distutils.) */
#                       if defined(_DEBUG)
#                               pragma comment(lib,"python37_d.lib")
#                       elif defined(Py_LIMITED_API)
#                               pragma comment(lib,"python3.lib")
#                       else
#                               pragma comment(lib,"python37.lib")
#                       endif /* _DEBUG */
#               endif /* _MSC_VER */
#       endif /* Py_BUILD_CORE */
#endif /* MS_COREDLL */""", "")

    def build(self):
        """Build the elements to package."""
        with tools.chdir(self.src_subfolder):
            if self.settings.os == "Windows":
                with tools.chdir("PCBuild"):
                    self.run("get_externals.bat")
                    # Don't build UWP targets, they are useless and require a specific SDK.
                    build_targets=["pyexpat", "pylauncher", "pyshellext", "python", "python3dll", "pythoncore", "pythonw", "pywlauncher", "select", "sqlite3", "unicodedata", "venvlauncher", "venvwlauncher", "winsound"]
                    msbuild = MSBuild(self)
                    msbuild.build("pcbuild.sln", targets=build_targets)
            else:
                atools = AutoToolsBuildEnvironment(self)
                args = [
                        # optimizations: costly to build, but ~10/20% perf gain at runtime
                        "--with-lto",
                        "--enable-optimizations" if self.options.optimizations else "--disable-optimizations",
                        # manage dependences
                        "--with-system-expat",
                        "--with-openssl={}".format(self.deps_cpp_info["OpenSSL"].rootpath),
                        # manage features
                        "--enable-ipv6",
                        "--with-ensurepip",
                        "--enable-big-digits=30", # by default on 64bits platform, but I want to be sure
                        # manage build
                        "--enable-shared" if self.options.shared else "--disable-shared",
                        "--without-pydebug",
                        "--without-assertions"
                    ]

                # setup.py does not try very hard to find libbuid headers, so we have to hack the include
                # flags to make sure setup.py will find this header.
                libuuid = self.deps_cpp_info["libuuid"]
                atools.include_paths.append(os.path.join(libuuid.rootpath, "include", "uuid"))

                atools.configure(args=args)
                atools.make()

    def package(self):
        """Assemble the package."""
        if self.settings.os != "Windows":
            with tools.chdir("cpython-%s" % self.version):
                atools = AutoToolsBuildEnvironment(self)
                atools.install()

            with tools.chdir(os.path.join(self.package_folder, "bin")):
                # patch binaries shebangs
                python_shebang = "#!/usr/bin/env python3.7\n"
                for name in ["2to3-3.7", "idle3.7", "pydoc3.7", "pyvenv-3.7", "pip3", "pip3.7"]:
                    with open(name, "r") as infile:
                        lines = infile.readlines()
                    lines[0] = python_shebang
                    with open(name, "w") as outfile:
                        outfile.writelines(lines)
                # create an alias for 'python'
                os.symlink("python3.7", "python")
        else:
            out_folder = {"x86_64": "amd64", "x86": "win32"}.get(str(self.settings.arch))
            src = os.path.join("cpython-%s" % self.version, "PCBuild", out_folder)
            self.copy(pattern="*.dll", dst="bin", src=src, keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src=src, keep_path=False)
            self.copy(pattern="*.h", dst="include", src=os.path.join(self.src_subfolder, "Include"), keep_path=True)
            self.copy(pattern="*.h", dst="include", src=os.path.join("cpython-%s" % self.version, "PC"), keep_path=True)
            self.copy(pattern="*.exe", dst="bin", src=src, keep_path=False)

    def package_info(self):
        """Edit package info."""
        if self.settings.os != "Windows":
            name = "python%sm" % ".".join(self.version.split(".")[0:2])
            self.cpp_info.includedirs.append("include/%s" % name)
            self.cpp_info.libs.append(name)
            self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
            if self.settings.os == "Macos":
                self.cpp_info.libs.append("dl")
                self.cpp_info.exelinkflags.append("-framework CoreFoundation")
                self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
            elif self.settings.os == "Linux":
                self.cpp_info.libs.extend(["pthread", "dl", "util"])
        else:
            debug_suffix = "_d" if self.settings.build_type == "Debug" else ""
            self.cpp_info.libs = ["python%s%s%s" % (self.version[0], self.version[2], debug_suffix)]
            self.cpp_info.defines.append("HAVE_SNPRINTF")

        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.env_info.PYTHON_ROOT = self.package_folder

    @property
    def src_subfolder(self):
        return os.path.join(self.source_folder, "cpython-%s" % self.version)

    def configure(self):
        if self.settings.os == "Windows" and self.options.shared == "False":
            raise Exception("Win static python lib is not supported")
