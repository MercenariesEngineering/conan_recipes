import os
from conans import ConanFile, MSBuild, tools, AutoToolsBuildEnvironment


# No tkinker and no dbm
class CpythonConan(ConanFile):
    name = "cpython"
    version = "3.9.21"
    license = "PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2"
    url = "https://github.com/lasote/conan-cpython"
    description = "CPython"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "optimizations": [True, False]}
    default_options = "shared=True", "fPIC=True", "optimizations=True"
    recipe_version = "0"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("OpenSSL/1.1.1g@mercseng/v0")
        # Because cpython is both a 'requires' dependency and a 'build_requires' dependency,
        # We must override OpenSSL's zlib dependency to something compatible with our other dependencies:
        self.requires("zlib/1.2.11@mercseng/v0") 

        if self.settings.os == "Linux":
            self.requires("expat/2.2.9@mercseng/v0")
            self.requires("lzma/5.2.4@mercseng/v0")
            self.requires("libuuid/1.0.3@mercseng/v0")
            self.requires("bzip2/1.0.8@mercseng/v0")
            self.requires("libffi/3.3@mercseng/v0")
            self.requires("gdbm/1.18.1@mercseng/v0")
            self.requires("sqlite3/3.32.3@mercseng/v0")
            self.requires("ncurses/6.2@mercseng/v0")
            self.requires("readline/8.0@mercseng/v0")  
    
    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/python/cpython/archive/v%s.tar.gz" % self.version)

        # This test often blocks the build on the virtual machine
        os.remove(os.path.join(self.src_subfolder, "Lib", "test", "test_socket.py"))

    def build(self):
        """Build the elements to package."""
        with tools.chdir(self.src_subfolder):
            if self.settings.os == "Windows":
                with tools.chdir("PCBuild"):
                    with tools.vcvars(self):
                        build_type = self.settings.build_type
                        arch = "x64" if self.settings.arch == "x86_64" else "Win32"
                        self.run("build.bat -c {build_type} -p {arch}".format(build_type=build_type, arch=arch))
                        out_folder = {"x86_64": "amd64", "x86": "win32"}.get(str(self.settings.arch))
                        with tools.chdir(out_folder):
                            python_exe = "python_d.exe" if self.settings.build_type == "Debug" else "python.exe"
                            with tools.environment_append({"PYTHONHOME": None}):
                                self.run(python_exe + " -m ensurepip")
                                self.run(python_exe + " -m pip install wheel")
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
                        "--with-pydebug" if self.settings.build_type == "Debug" else "--without-pydebug",
                        "--without-assertions"
                    ]

                # setup.py does not try very hard to find libbuid headers, so we have to hack the include
                # flags to make sure setup.py will find this header.
                libuuid = self.deps_cpp_info["libuuid"]
                atools.include_paths.append(os.path.join(libuuid.rootpath, "include", "uuid"))

                atools.configure(args=args)
                atools.make()
                with tools.environment_append({"LD_LIBRARY_PATH": ["."]}):
                    self.run("./python -m ensurepip")
                    self.run("./python -m pip install wheel")

    def package(self):
        """Assemble the package."""
        if self.settings.os != "Windows":
            with tools.chdir("cpython-%s" % self.version):
                atools = AutoToolsBuildEnvironment(self)
                atools.install()

            with tools.chdir(os.path.join(self.package_folder, "bin")):
                # patch binaries shebangs
                python_shebang = "#!/usr/bin/env python3.9\n"
                for name in ["2to3-3.9", "idle3.9", "pydoc3.9", "pyvenv-3.9", "pip3", "pip3.9"]:
                    with open(name, "r") as infile:
                        lines = infile.readlines()
                    lines[0] = python_shebang
                    with open(name, "w") as outfile:
                        outfile.writelines(lines)
                # create an alias for 'python'
                os.symlink("python3.9", "python")
        else:
            out_folder = {"x86_64": "amd64", "x86": "win32"}.get(str(self.settings.arch))
            self.copy(pattern="*",                    src=os.path.join("cpython-%s" % self.version, "PCBuild", out_folder), keep_path=False)
            self.copy(pattern="*.lib", dst="libs",    src=os.path.join("cpython-%s" % self.version, "PCBuild", out_folder), keep_path=False)
            self.copy(pattern="*.h",   dst="include", src=os.path.join("cpython-%s" % self.version, "Include"), keep_path=True)
            self.copy(pattern="*.h",   dst="include", src=os.path.join("cpython-%s" % self.version, "PC"), keep_path=True)
            self.copy(pattern="*",     dst="Lib",     src=os.path.join("cpython-%s" % self.version, "Lib"), keep_path=True)
            self.copy(pattern="*.pyd", dst="DLLs",    src=os.path.join("cpython-%s" % self.version, "PCBuild", out_folder), keep_path=False)
            self.copy(pattern="*",     dst="Scripts", src=os.path.join("cpython-%s" % self.version, "Scripts"), keep_path=True)

    def package_info(self):
        """Edit package info."""
        if self.settings.os != "Windows":
            version_suffix = ".".join(self.version.split(".")[0:2])
            debug_suffix = "d" if self.settings.build_type == "Debug" else ""
            name = "python%s%sm" % (version_suffix, debug_suffix)
            self.cpp_info.includedirs.append("include/%s" % name)
            self.cpp_info.libs.append(name)
            self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
            if self.settings.os == "Macos":
                self.cpp_info.libs.append("dl")
                self.cpp_info.exelinkflags.append("-framework CoreFoundation")
                self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
            elif self.settings.os == "Linux":
                self.cpp_info.libs.extend(["pthread", "dl", "util"])
            self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
            self.env_info.PYTHON_ROOT = self.package_folder
        else:
            self.cpp_info.libdirs=[os.path.join(self.package_folder, "libs")]
            debug_suffix = "_d" if self.settings.build_type == "Debug" else ""
            self.cpp_info.libs = ["python%s%s%s" % (self.version[0], self.version[2], debug_suffix)]
            self.cpp_info.defines.append("HAVE_SNPRINTF")
            self.env_info.PATH.append(self.package_folder)
            self.env_info.PATH.append(os.path.join(self.package_folder, "Scripts"))
            self.env_info.PYTHONHOME = self.package_folder

    @property
    def src_subfolder(self):
        return os.path.join(self.source_folder, "cpython-%s" % self.version)

    def configure(self):
        if self.settings.os == "Windows" and self.options.shared == "False":
            raise Exception("Win static python lib is not supported")
