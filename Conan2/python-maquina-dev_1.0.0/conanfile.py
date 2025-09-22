from conan import ConanFile
from conan.tools.env import Environment
from conan.tools.files import chdir
import os

class PythonPackages(ConanFile):
    name = "python-maquina-dev"
    version = "1.0.0"
    user="mercs"
    description = "List of python packages used by Maquina."
    settings = "os", "compiler", "build_type", "arch"
    user = "mercs"
    channel = "v0"

    package_type = "shared-library"
    packages = [
        # Python 3.9
        ("docutils", "0.21.2"),
        ("html5lib", "1.1"),
        ("pip", "25.1.1"),
        ("pytest", "8.4.1"),
        ("pylint", "3.3.7"),
        ("setuptools", "80.9.0"),
        ("stdlib-list", "0.11.1"),
        ("sphinx", "7.4.7"),
        ("sphinx-code-tabs", "0.5.5"),
        ("sphinx-rtd-theme", "3.0.2")

        # Python 3.10
        #("docutils", "0.21.2"),
        #("pip", "25.1.1"),
        #("pytest", "8.4.1"),
        #("pylint", "3.3.7"),
        #("stdlib-list", "0.11.1"),
        #("sphinx", "8.1.3"),
        #("sphinx-code-tabs", "0.5.5"),
        #("sphinx-rtd-theme", "3.0.2")
    ]
    exports_sources = "bootloader_Windows-64bit.zip"
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.settings.build_type
            del self.settings.compiler

    def requirements(self):
        self.requires("cpython/3.9.19", package_id_mode="minor_mode")
        self.requires("python-maquina/1.0.0@mercs")
        
    def build_requirements(self):
        self.tool_requires("cpython/3.9.19", options={"shared": True})
        self.tool_requires("python-maquina/1.0.0@mercs")

    def build(self):
        env = Environment()
        env.prepend_path("PYTHONPATH", os.path.join(self.dependencies["python-maquina"].package_folder))
        env.prepend_path("PYTHONPATH", self.package_folder)
        envvars = env.vars(self)

        packages_list = ""
        for package_name, package_version in self.packages:
            packages_list = packages_list + " " + (package_name+"=="+package_version if package_version else package_name) 

        command = "python -m pip install {packages_list} --target={package_folder} --upgrade --cache-dir={cache_folder}".format(
            packages_list=packages_list,
            package_folder=self.package_folder,
            cache_folder=os.path.join(self.build_folder, "cache"))
        
        with envvars.apply():
            self.run(command)

    def package(self):
        if self.settings.os == "Linux":
            # fix shebangs
            python_shebang = "#!/usr/bin/env python\n"
            bin_directory = os.path.join(self.package_folder, "bin")
            if os.path.exists(bin_directory):
                with chdir(self, bin_directory):
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
        self.buildenv_info.prepend_path("PYTHONPATH", self.package_folder)
        self.runenv_info.prepend_path("PYTHONPATH", self.package_folder)
        self.user_info.site_package = self.package_folder
