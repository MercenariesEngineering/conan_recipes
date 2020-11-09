import os, sys
from distutils.dir_util import copy_tree
from conans import ConanFile, python_requires, tools

class pyside2(ConanFile):
    description = "Qt for Python"
    license = "LGPL-3.0"
    url = "https://doc.qt.io/qtforpython"
    version = "5.12.6"
    name = "pyside2"

    settings = "os"
    short_paths = True

    def configure(self):
        # Dynamically Loading Graphics Drivers for windows
        """
         As of Qt 5.5 this is the configuration used by the official, pre-built binary packages of Qt. 
         It is strongly recommended to use it also in custom builds, especially for Qt binaries that are deployed alongside applications.
        """
        if self.settings.os == "Windows":
            self.options["qt"].opengl = "dynamic"

        # QtSVG
        self.options["qt"].qtsvg = True

        self.options["qt"].openssl = False
        self.options["qt"].with_openal = False
        self.options["qt"].with_harfbuzz = False
        self.options["qt"].with_mysql = False
        self.options["qt"].with_pq = False
        self.options["qt"].with_odbc = False

    # Note: make sure you have libclang available in your LD_LIBRARY_PATH. I could make a recipe
    # for this dependence but since I compile everything with clang, I already have this build
    # dependence on all my machines.

    def requirements(self):
        """Define runtime requirements."""
        self.requires("qt/5.12.6@bincrafters/stable")
        
    
    def source(self):
        """Retrieve source code."""
        tools.get("https://download.qt.io/official_releases/QtForPython/pyside2/PySide2-5.12.6-src/pyside-setup-everywhere-src-5.12.6.zip")

    def build(self):
        """Build the elements to package."""
        qmake = "qmake"

        environment = {"PYSIDE_DISABLE_INTERNAL_QT_CONF": "1"}
        if self.settings.os == "Windows":
            environment = {"CMAKE_GENERATOR": "Visual Studio 14 2015 Win64"}
            qmake += ".exe"

        setup = os.path.join(self.source_folder, "pyside-setup-everywhere-src-5.12.6","setup.py")
        arguments = [
            "--qmake=\"{}\"".format(os.path.join(self.deps_cpp_info["qt"].rootpath, "bin", qmake)),
            "--skip-modules=QtNetwork,QtOpenGLFunctions", "--skip-docs",
            "--prefix={}".format(self.package_folder),
            "--parallel={}".format(tools.cpu_count())
        ]

        if self.settings.os == "Windows":
            arguments.append("--jom")
        
        with tools.environment_append(environment):
            with tools.chdir("pyside-setup-everywhere-src-5.12.6"):
                self.run("python {} install {}".format(setup, " ".join(arguments)))

    def package(self):
        """Assemble the package."""
        self.copy(pattern="LICENSE.LGPLv3", dst="licenses", src=os.path.join(self.source_folder, "pyside-setup-everywhere-src-5.12.6"))

    def package_info(self):
        """Edit package info."""
        if self.settings.os == "Windows":
            python_scripts_dir = os.path.join(sys.exec_prefix, "Scripts")
            pyside_scripts_dir = os.path.join(self.package_folder, "Scripts")

            copy_tree(pyside_scripts_dir, python_scripts_dir)
            
            
            python_site_packages_dir = os.path.join(sys.exec_prefix, "Lib", "site-packages")
            pyside_site_packages_dir = os.path.join(os.path.join(self.package_folder, "Lib", "site-packages"))

            copy_tree(pyside_site_packages_dir, python_site_packages_dir)
        else:
            self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
            self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "lib", "python3.7", "site-packages"))
        