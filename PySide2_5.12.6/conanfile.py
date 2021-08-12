import os, sys, glob
from distutils.dir_util import copy_tree
from conans import ConanFile, tools

class PySide2(ConanFile):
    name = "PySide2"
    version = "5.12.6"
    description = "Qt for Python"
    license = "LGPL-3.0"
    url = "https://doc.qt.io/qtforpython"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=True", "fPIC=True"
    _source_subfolder = "source_subfolder"
    short_paths = True
    recipe_version = "3"

    def build_requirements(self):
        """Define buid toolset."""
        if tools.os_info.is_windows and self.settings.compiler == "Visual Studio":
            self.build_requires("jom_installer/1.1.2@mercseng/v0")
        self.build_requires("cpython/3.7.7@mercseng/v0")

    def requirements(self):
        """Define runtime requirements."""
        self.requires("qt/5.12.6@mercseng/v1")
        self.requires("OpenSSL/1.1.1g@mercseng/v0")
        self.requires("libxml2/2.9.9@mercseng/v0")

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def configure(self):
        # The default options of Qt's recipe matches our expectations. We could still check it is
        # the case here:
        if self.settings.os == "Windows":
            self.options["qt"].opengl = "dynamic"
    
    def source(self):
        """Retrieve source code."""        
        tools.get("https://download.qt.io/official_releases/QtForPython/pyside2/PySide2-%s-src/pyside-setup-everywhere-src-%s.zip" % (self.version, self.version))
        os.rename("pyside-setup-everywhere-src-%s" % self.version, self._source_subfolder)

        # https://bugreports.qt.io/browse/PYSIDE-1259
        if self.settings.os == "Linux":
            tools.replace_in_file(
                os.path.join(self._source_subfolder, "sources", "shiboken2", "ApiExtractor", "clangparser", "compilersupport.cpp"),
                "QVersionNumber lastVersionNumber(1, 0, 0);",
                "QVersionNumber lastVersionNumber(0, 0, 0);"
            )

        tools.replace_in_file(
            os.path.join(self._source_subfolder, "build_scripts", "main.py"),
            """"include/python{}".format(py_version))""",
            """"include/python{}".format(py_version))
                if not os.path.exists(py_include_dir):
                    py_include_dir = py_include_dir + get_config_var("ABIFLAGS")"""
        )

        if self.settings.os == "Windows" and not "LLVM_INSTALL_DIR" in os.environ:
            if self.settings.compiler.version == 14:
                clang_file = "libclang-release_70-based-windows-vs2015_64.7z"
            elif self.settings.compiler.version == 15:
                clang_file = "libclang-release_80-based-windows-vs2017_64.7z"
            else:
                clang_file = "libclang-release_100-based-windows-vs2019_64.7z"
            tools.download("http://download.qt.io/development_releases/prebuilt/libclang/%s" % clang_file, "clang.7z")
            # Conan won't natively handle 7z files. Cmake is actually the easiest unzipping tool at hand.
            self.run("cmake -E tar xf clang.7z")
            os.unlink("clang.7z")

    def build(self):
        """Build the elements to package."""        
        qmake = "qmake"

        environment = {}
        if self.settings.os == "Windows":
            environment = tools.vcvars_dict(self)
            environment["CMAKE_GENERATOR"] = "Visual Studio 14 2015 Win64"
            qmake += ".exe"

        environment["PYSIDE_DISABLE_INTERNAL_QT_CONF"] = "1"

        # There may be a DLL conflict. Put Qt and libClang DLLs in front of the PATH.
        if self.settings.os == "Windows":
            if not "PATH" in environment:
                environment["PATH"] = []
            environment["PATH"].insert(0, self.deps_cpp_info["qt"].bin_paths[0])
            if not "LLVM_INSTALL_DIR" in os.environ:
                clang_path = os.path.join(self.source_folder, "libclang")
                environment["PATH"].insert(0, (os.path.join(clang_path, "bin")))
                environment["LLVM_INSTALL_DIR"] = clang_path

        arguments = [
            "--qmake=\"%s\"" % os.path.join(self.deps_cpp_info["qt"].rootpath, "bin", qmake),
            #"--skip-modules=QtNetwork,QtOpenGLFunctions,QtQuick,QtQuickWidgets,QtQml",
            "--skip-docs",
            "--prefix=%s" % self.package_folder,
            "--parallel=%s" % tools.cpu_count(),
            "--openssl=\"%s\"" % os.path.join(self.deps_cpp_info["OpenSSL"].rootpath, "bin"),
            "--ignore-git",
        ]
        
        if self.settings.build_type == "Debug":
            arguments.append("--debug")

        if self.settings.os == "Windows":
            arguments.append("--jom")
        
        setup = os.path.join(self.source_folder, self._source_subfolder, "setup.py")
        with tools.environment_append(environment):
            with tools.chdir(self._source_subfolder): 
                if self.settings.os == "Windows":
                    python_exe = "python_d.exe" if self.settings.build_type == "Debug" else "python.exe"
                else:
                    python_exe = "python"
                self.run(python_exe + " %s install %s" % (setup, " ".join(arguments)))

    def package(self):
        """Assemble the package."""
        self.copy(pattern="LICENSE.LGPLv3", dst="licenses", src=os.path.join(self.source_folder, self._source_subfolder))
        if self.settings.os == "Linux":
            # fix shebangs
            python_shebang = "#!/usr/bin/env python3.7\n"
            bin_directory = os.path.join(self.package_folder, "bin")
            if os.path.exists(bin_directory):
                with tools.chdir(bin_directory):
                    for filename in [entry for entry in os.listdir(".") if os.path.isfile(entry)]:
                        with open(filename, "r") as infile:
                            lines = infile.readlines()
                        
                        if len(lines[0]) > 2 and lines[0].startswith("#!"):
                            lines[0] = python_shebang
                            with open(filename, "w") as outfile:
                                outfile.writelines(lines)

    def package_info(self):
        """Edit package info."""
        if self.settings.os == "Windows":
            self.env_info.PATH.append(os.path.join(self.package_folder, "Scripts"))
            self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "Lib", "site-packages"))
        else:
            self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
            self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "lib", "python3.7", "site-packages"))
        