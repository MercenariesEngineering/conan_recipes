import os
from conans import ConanFile, tools

class PythonPackages(ConanFile):
    description = "List of python packages used by Maquina."
    name = "python-maquina"
    version = "1.0.0"
    settings = "os", "compiler", "build_type", "arch"
    packages = [
        ("pip", None),
        ("setuptools", None),
        ("wheel", None),
        ("numpy", "1.17.5"),
        ("psutil", "5.6.7"),
        ("pylint", "2.4.4"),
        ("Sphinx", "2.3.1"),
        ("recommonmark", "0.6.0"),
        ("sphinx-rtd-theme", "0.4.3"),
        ("sphinx-markdown-tables", "0.0.10"),
        ("pytest", "5.3.4"),
        ("PyOpenGL", "3.1.5")
    ]
    recipe_version = "2"

    def config_options(self):
        if self.settings.os == "Windows":
            self.settings.remove("build_type")
            self.settings.remove("compiler")

    def requirements(self):
        self.requires("cpython/3.7.7@mercseng/v1")

    def build(self):
        """Build the elements to package."""
        with tools.environment_append({"PYTHONPATH": self.package_folder}):
            for package_name, package_version in self.packages:
                command = "python -m pip install {package} --target={package_folder} --upgrade --cache-dir={cache_folder}".format(
                    package=package_name+"=="+package_version if package_version else package_name,
                    package_folder=self.package_folder,
                    cache_folder=os.path.join(self.build_folder))
                self.run(command)

    def package(self):
        """Assemble the package."""
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
        self.env_info.PYTHONPATH.append(self.package_folder)
        bin_directory = os.path.join(self.package_folder, "bin")
        if os.path.exists(bin_directory):
            self.env_info.PATH.append(bin_directory)
