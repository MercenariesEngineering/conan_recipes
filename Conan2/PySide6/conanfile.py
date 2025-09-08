from conan import ConanFile
from conan.tools.build import build_jobs
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.env import Environment
from conan.tools.files import get, download, copy, replace_in_file, export_conandata_patches, apply_conandata_patches
from conan.tools.microsoft import VCVars
from conan.tools.scm import Version
import os

class PySide6(ConanFile):
    name = "pyside6"
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

    def validate(self):
        if self.settings.compiler == "msvc" and Version(self.settings.compiler.version) < "192":
            raise ConanInvalidConfiguration("This recipe does not support MSVC < 2019")

    def requirements(self):
        self.requires("cpython/3.9.19")
        self.requires("libxml2/2.13.8")
        self.requires("libxslt/1.1.42")
        self.requires("opengl/system")
        self.requires("openssl/1.1.1w")
        self.requires("python-maquina/1.0.0@mercs")
        self.requires("qt/"+self.version)
        self.requires("md4c/0.4.8")

    def build_requirements(self):
        self.tool_requires("cpython/<host_version>", options={"shared": True})
        self.tool_requires("python-maquina/<host_version>@mercs")
        self.tool_requires("python-maquina-dev/1.0.0@mercs")
        self.tool_requires("ninja/[>=1.10.2 <2]")
        #if self.settings.os == "Windows" and self.settings.compiler == "msvc":
        #    self.build_requires("jom/1.1.4")

    def export_sources(self):
        export_conandata_patches(self)

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
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        #get(self, "file:///C:/Users/pierre/Downloads/pyside-setup-everywhere-src-%s.zip" % self.version, strip_root=True)

    def _patch_sources(self):
        apply_conandata_patches(self)

        build_folder = self.build_folder.replace("\\", "/")

        # Help Shiboken find dependencies from Conan's CMakeDeps.
        replace_in_file(self, 
            os.path.join(self.source_folder, "sources", "pyside6", "cmake", "PySideSetup.cmake"),
            """list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}")""",
            """
list(APPEND CMAKE_MODULE_PATH \""""+build_folder+"""\")
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}")
"""
        )

        # Help Pyside find dependencies from Conan's CMakeDeps.
        replace_in_file(self, 
            os.path.join(self.source_folder, "sources", "shiboken6", "cmake", "ShibokenSetup.cmake"),
            """list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}")""",
            """
list(APPEND CMAKE_MODULE_PATH \""""+build_folder+"""\")
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}")
"""
        )
        
    def generate(self):
        deps = CMakeDeps(self)
        deps.set_property("libxml2", "cmake_file_name", "LibXml2")
        deps.set_property("libxslt", "cmake_file_name", "LibXslt")
        deps.set_property("libxslt", "cmake_additional_variables_prefixes", ["LIBXSLT"])
        deps.set_property("qt", "cmake_find_mode", "none")
        deps.generate()

        ms = VCVars(self)
        ms.generate()

        env = Environment()
        clang_path = os.path.join(self.build_folder, "libclang")
        env.define_path("CLANG_INSTALL_DIR", clang_path)
        # There may be a DLL conflict. Put libClang DLLs in front of the PATH.
        if self.settings.os == "Windows":
            env.prepend_path("PATH", os.path.join(clang_path, "bin"))
        else:
            env.prepend_path("LD_LIBRARY_PATH", os.path.join(clang_path, "lib"))
        env.vars(self).save_script("conan_find_libclang")

    @property
    def clang_source_file(self): 
        # Version 14 is minimum, 18 is recommended
        if self.settings.os == "Windows":
            return "libclang-release_20.1.3-based-windows-vs2019_64.7z"
        else:
            return "libclang-release_20.1.3-based-linux-Rhel8.8-gcc10.3-x86_64.7z"
    
    def _get_clang(self):        
        clang_file = self.clang_source_file
        download(self, "http://download.qt.io/development_releases/prebuilt/libclang/%s" % clang_file, clang_file)
        #copy(self, pattern=clang_file, src="C:/Users/pierre/Downloads", dst=self.build_folder)
        
        # Conan won't natively handle 7z files. Cmake is actually the easiest unzipping tool at hand.
        self.run("cmake -E tar xf "+clang_file)
        os.unlink(clang_file)

    def build(self):
        self._patch_sources()
        self._get_clang()

        qt_package = self.dependencies["qt"].package_folder
        ssl_package = self.dependencies["openssl"].package_folder
        binary_suffix = ".exe" if self.settings.os == "Windows" else ""
        arguments = [
            "--qtpaths=\"%s\"" % os.path.join(qt_package, "bin", "qtpaths6"+binary_suffix),
            "--openssl=\"%s\"" % os.path.join(ssl_package, "bin"),
            "--ignore-git",
            "--skip-docs",
            "--limited-api=no",
            "--verbose-build",
            "--parallel=%s" % build_jobs(self),
            #"--skip-modules=QtNetwork,QtOpenGLFunctions,QtQuick,QtQuickWidgets,QtQml",
        ]
        
        if self.settings.build_type == "Debug":
            arguments.append("--debug")
        #if self.settings.os == "Windows":
        #    arguments.append("--jom")
        
        if self.settings.os == "Windows":
            python_exe = "python_d.exe" if self.settings.build_type == "Debug" else "python.exe"
        else:
            python_exe = "python"
        setup = os.path.join(self.source_folder, "setup.py")
        self.run(python_exe + " %s install %s" % (setup, " ".join(arguments)))

    @property
    def _install_dir(self):
        pythonVersion = Version(self.dependencies["cpython"].ref.version)
        pythonVersionMajorMinor = f"{pythonVersion.major}.{pythonVersion.minor}"
        qtVersion = self.dependencies["qt"].ref.version

        # pyside is using the venv name to contain the install dir.
        # see https://a_gitlab_url/libraries/conan/thirdparty/pyside/pyside/-/commit/0a40ebb1
        # venv_name = os.path.basename(sys.prefix)
        # Not sure what's the best way to do this, but this is unlikely to be it
        venv_name = f"qfp-py{pythonVersionMajorMinor}-qt{qtVersion}-64bit-"
        venv_name += "debug" if self.settings.build_type == "Debug" else "release"

        install_dir = os.path.join(self.build_folder, "build", venv_name, "install")
        if not os.path.isdir(install_dir):
            raise ConanException(f"Could not find the install directory {install_dir}")
        return install_dir

    def package(self):
        copy(self, pattern="*", src=self._install_dir, dst=self.package_folder)
        copy(self, pattern="LICENSE.LGPLv3", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))

        if self.settings.os == "Linux":
            # package minimal libclang
            copy(self, pattern="*", src=os.path.join(self.source_folder, "libclang", "include"), dst=os.path.join(self.package_folder, "libclang", "include"))
            copy(self, pattern="*", src=os.path.join(self.source_folder, "libclang", "lib", "clang"), dst=os.path.join(self.package_folder, "libclang", "lib", "clang"))
            copy(self, pattern="libclang.so.18", src=os.path.join(self.source_folder, "libclang", "lib"), dst=os.path.join(self.package_folder, "libclang", "lib"))

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

        elif self.settings.os == "Windows":
            # package minimal libclang
            copy(self, pattern="*", src=os.path.join(self.source_folder, "libclang", "include"), dst=os.path.join(self.package_folder, "libclang", "include"))
            copy(self, pattern="*", src=os.path.join(self.source_folder, "libclang", "lib", "clang"), dst=os.path.join(self.package_folder, "libclang", "lib", "clang"))
            copy(self, pattern="*", src=os.path.join(self.source_folder, "libclang", "bin"), dst=os.path.join(self.package_folder, "libclang", "bin"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "PySide6")
        self.cpp_info.set_property("cmake_target_name", "PySide::PySide6")

        v = Version(self.dependencies["cpython"].ref.version)
        if self.settings.os == "Windows":
            self.user_info.site_package = os.path.join(self.package_folder, "lib/site-packages")
        else:
            self.user_info.site_package = os.path.join(self.package_folder, f"lib/python{v.major}.{v.minor}/site-packages")

        self.runenv_info.append_path("PYTHONPATH", self.user_info.site_package)
        if self.settings.os == "Windows":
            self.cpp_info.bindirs = ['bin']
            self.runenv_info.prepend_path("PATH", os.path.join(self.package_folder, "bin"))
            self.runenv_info.prepend_path("PATH", os.path.join(self.package_folder, "libclang", "bin"))
            self.buildenv_info.prepend_path("PATH", os.path.join(self.package_folder, "libclang", "bin"))
        else:
            self.cpp_info.bindirs = ['bin']
            self.runenv_info.append_path("PATH", os.path.join(self.package_folder, "bin"))
            self.runenv_info.append_path("LD_LIBRARY_PATH", os.path.join(self.package_folder, "libclang", "lib"))
            self.runenv_info.append_path("CLANG_INSTALL_DIR", os.path.join(self.package_folder, "libclang"))
