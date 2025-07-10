from conan import ConanFile
from conan.tools.build import build_jobs
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.env import Environment
from conan.tools.files import get, download, copy, replace_in_file
from conan.tools.microsoft import VCVars
import os

class PySide2(ConanFile):
    name = "pyside2"
    version = "5.15.16"
    user="mercs"
    description = "Qt for Python"
    license = "LGPL-3.0"
    url = "https://doc.qt.io/qtforpython"
    settings = "os", "compiler", "build_type", "arch"
    package_type = "library"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True
    }
    short_paths = True

    def requirements(self):
        self.requires("cpython/3.10.14")
        self.requires("libxml2/2.13.8")
        self.requires("libxslt/1.1.42")
        self.requires("opengl/system")
        self.requires("openssl/1.1.1w")
        self.requires("python-maquina/1.0.0@mercs")
        self.requires("qt/5.15.16")

    def build_requirements(self):
        self.tool_requires("cpython/<host_version>", options={"shared": True})
        self.tool_requires("python-maquina/<host_version>@mercs")
        self.tool_requires("python-maquina-dev/1.0.0@mercs")
        if self.settings.os == "Windows" and self.settings.compiler == "msvc":
            self.build_requires("jom/1.1.4")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        # The default options of Qt's recipe matches our expectations. We could still check it is
        # the case here:
        #if self.settings.os == "Windows":
        #    self.options["qt"].opengl = "dynamic"
    
    def source(self):
        get(self, "https://download.qt.io/official_releases/QtForPython/pyside2/PySide2-%s-src/pyside-setup-opensource-src-%s.zip" % (self.version, self.version), strip_root=True)
        #get(self, "file:///C:/Users/pierre/Downloads/pyside-setup-opensource-src-%s.zip" % self.version, strip_root=True)

    def _patch_sources(self):
        qt_components_found = ""
        for comp in self.dependencies["qt"].cpp_info.components:
            qt_components_found = qt_components_found + """set(Qt5""" + comp[2:] + """_FOUND TRUE)
"""

        # Help Shiboken find Qt from Conan's CMakeDeps.
        replace_in_file(self, 
            os.path.join(self.source_folder, "sources", "shiboken2", "CMakeLists.txt"),
            """list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/data/")""",
            """
list(APPEND CMAKE_PREFIX_PATH \""""+self.build_folder.replace("\\", "/")+"""\")
list(APPEND CMAKE_MODULE_PATH \""""+self.build_folder.replace("\\", "/")+"""\")
"""+qt_components_found+"""

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/data/")
"""
        )

        # Help Pyside find Qt from Conan's CMakeDeps.
        replace_in_file(self, 
            os.path.join(self.source_folder, "sources", "pyside2", "CMakeLists.txt"),
            """include(shiboken_helpers)""",
            """
list(APPEND CMAKE_PREFIX_PATH \""""+self.build_folder.replace("\\", "/")+"""\")
list(APPEND CMAKE_MODULE_PATH \""""+self.build_folder.replace("\\", "/")+"""\")
set(Qt5Core_VERSION \""""+str(self.dependencies["qt"].ref.version)+"""\")

include(shiboken_helpers)
"""
        )

        replace_in_file(self, 
            os.path.join(self.source_folder, "sources", "pyside2", "CMakeLists.txt"),
            """remove_skipped_modules()""",
            """
"""+qt_components_found+"""

remove_skipped_modules()
"""
        )

        
    def generate(self):
        deps = CMakeDeps(self)
        deps.set_property("libxml2", "cmake_file_name", "LIBXML2")
        deps.set_property("libxslt", "cmake_file_name", "LIBXSLT")
        deps.generate()

        ms = VCVars(self)
        ms.generate()

        env = Environment()
        if self.settings.os == "Windows":
            if self.settings.compiler.version == 190:
                env.define("CMAKE_GENERATOR", "Visual Studio 14 2015 Win64")
            elif self.settings.compiler.version == 191:
                env.define("CMAKE_GENERATOR", "Visual Studio 15 2017 Win64")
            else:
                env.define("CMAKE_GENERATOR", "Visual Studio 16 2019 Win64")

        #env.append("Qt5_DIR", self.build_folder)
        env.define("PYSIDE_DISABLE_INTERNAL_QT_CONF", "1")
        env.define("BUILD_TYPE", "")

        # There may be a DLL conflict. Put Qt and libClang DLLs in front of the PATH.
        clang_path = os.path.join(self.build_folder, "libclang")
        if self.settings.os == "Windows":
            env.prepend_path("PATH", self.dependencies["qt"].cpp_info.bindirs[0])
            env.prepend_path("PATH", os.path.join(clang_path, "bin"))
        else:
            env.prepend_path("LD_LIBRARY_PATH", os.path.join(clang_path, "lib"))
        env.define_path("CLANG_INSTALL_DIR", clang_path)
        envvars = env.vars(self, scope="build")
        env.vars(self).save_script("conan_find_libclang")

    def _get_clang(self):        
        if self.settings.os == "Windows":
            if self.settings.compiler.version == 190:
                clang_file = "libclang-release_70-based-windows-vs2015_64.7z"
            elif self.settings.compiler.version == 191:
                clang_file = "libclang-release_80-based-windows-vs2017_64.7z"
            else:
                clang_file = "libclang-release_130-based-windows-vs2019_64.7z"
        else:
            clang_file = "libclang-release_100-based-linux-Rhel7.6-gcc5.3-x86_64.7z"

        download(self, "http://download.qt.io/development_releases/prebuilt/libclang/%s" % clang_file, "clang.7z")
        #copy(self, pattern=clang_file, src="C:/Users/pierre/Downloads", dst=self.build_folder)
        
        # Conan won't natively handle 7z files. Cmake is actually the easiest unzipping tool at hand.
        self.run("cmake -E tar xf "+clang_file)
        os.unlink(clang_file)

    def build(self):
        self._patch_sources()
        self._get_clang()

        arguments = [
            "--qmake=\"%s\"" % os.path.join(self.dependencies["qt"].package_folder, "bin", "qmake.exe" if self.settings.os == "Windows" else "qmake"),
            #"--skip-modules=QtNetwork,QtOpenGLFunctions,QtQuick,QtQuickWidgets,QtQml",
            "--skip-docs",
            "--prefix=%s" % self.package_folder,
            "--parallel=%s" % build_jobs(self),
            "--openssl=\"%s\"" % os.path.join(self.dependencies["openssl"].package_folder, "bin"),
            "--qt-src-dir=\"%s\"" % os.path.join(self.dependencies["qt"].package_folder),
            #"--qt-src-dir=\"%s\"" % self.build_folder,
            "--ignore-git",
        ]
        
        if self.settings.build_type == "Debug":
            arguments.append("--debug")
        if self.settings.os == "Windows":
            arguments.append("--jom")
        
        if self.settings.os == "Windows":
            python_exe = "python_d.exe" if self.settings.build_type == "Debug" else "python.exe"
        else:
            python_exe = "python"
        setup = os.path.join(self.source_folder, "setup.py")
        self.run(python_exe + " %s install %s" % (setup, " ".join(arguments)))

    def package(self):
        copy(self, pattern="LICENSE.LGPLv3", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        if self.settings.os == "Linux":
            # package minimal libclang
            copy(self, pattern="*", src=os.path.join(self.source_folder, "libclang", "include"), dst=os.path.join(self.package_folder, "libclang", "include"))
            copy(self, pattern="*", src=os.path.join(self.source_folder, "libclang", "lib", "clang"), dst=os.path.join(self.package_folder, "libclang", "lib", "clang"))
            copy(self, pattern="libclang.so.10", src=os.path.join(self.source_folder, "libclang", "lib"), dst=os.path.join(self.package_folder, "libclang", "lib"))

            # fix shebangs
            python_shebang = "#!/usr/bin/env python\n"
            bin_directory = os.path.join(self.package_folder, "bin")
            if os.path.exists(bin_directory):
                with chdir(bin_directory):
                    for filename in [entry for entry in os.listdir(".") if os.path.isfile(entry)]:
                        try:
                            with open(filename, "r", encoding="utf-8") as infile:
                                lines = infile.readlines()
                            
                            if len(lines[0]) > 2 and lines[0].startswith("#!"):
                                lines[0] = python_shebang
                                with open(filename, "w", encoding="utf-8") as outfile:
                                    outfile.writelines(lines)
                        except UnicodeDecodeError:
                            pass

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "PySide2")
        self.cpp_info.set_property("cmake_target_name", "PySide::PySide2")

        if self.settings.os == "Windows":
            self.cpp_info.bindirs = ['Scripts']
            self.runenv_info.append_path("PATH", os.path.join(self.package_folder, "Scripts"))
            self.runenv_info.append_path("PYTHONPATH", os.path.join(self.package_folder, "Lib", "site-packages"))
        else:
            self.cpp_info.bindirs = ['bin']
            self.runenv_info.append_path("PATH", os.path.join(self.package_folder, "bin"))
            self.runenv_info.append_path("PYTHONPATH", os.path.join(self.package_folder, "lib", "python", "site-packages"))
            self.runenv_info.append_path("LD_LIBRARY_PATH", os.path.join(self.package_folder, "libclang", "lib"))
            self.runenv_info.append_path("CLANG_INSTALL_DIR", os.path.join(self.package_folder, "libclang"))
        