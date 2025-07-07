from conan import ConanFile
from conan.tools.env import Environment
from conan.tools.files import chdir
import os


class PythonPackages(ConanFile):
    name = "python-maquina"
    version = "1.0.0"
    user="mercs"
    description = "List of python packages used by Maquina."
    settings = "os", "compiler", "build_type", "arch"
    package_type = "shared-library"
    packages = [
        ("wheel", "0.45.1"),
        ("numpy", "2.2.6"),
        ("psutil", "7.0.0"),
        ("pylint", "3.3.7"),
        ("docutils", "0.21.2"),
        ("Sphinx", "8.1.3"),
        ("recommonmark", "0.7.1"),
        ("sphinx-rtd-theme", "3.0.2"),
        ("sphinx-markdown-tables", "0.0.17"),
        ("pytest", "8.4.1"),
        ("PyOpenGL", "3.1.9")
    ]
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.settings.build_type
            del self.settings.compiler

    def build_requirements(self):
        self.tool_requires("cpython/3.10.14", options={"shared": True})

    def build(self):
        env = Environment()
        env.append_path("PYTHONPATH", self.package_folder)
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
        self.runenv_info.append_path("PYTHONPATH", self.package_folder)
