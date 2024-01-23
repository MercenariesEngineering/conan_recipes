import os
from conans import ConanFile, tools

class PythonPackages(ConanFile):
    description = "List of python packages used by Maquina."
    name = "python-maquina-dev"
    version = "1.0.0"
    settings = "os", "compiler", "build_type", "arch"
    packages = [
        ("conan", "1.62"),
        ("docutils", "0.17.1"),
        ("pip", "23.0.1"),
        ("pytest", "5.3.4"),
        ("pylint", "2.4.4"),
        ("stdlib-list", "0.8.0"),
        ("sphinx", "5.3.0"),
        ("sphinx-code-tabs", "0.5.3"),
        ("sphinx-rtd-theme", "1.2.0")
    ]
    exports_sources = "bootloader_Windows-64bit.zip"
    recipe_version = "2"
    
    def config_options(self):
        if self.settings.os == "Windows":
            self.settings.remove("build_type")
            self.settings.remove("compiler")

    def requirements(self):
        self.requires("cpython/3.7.7@mercseng/v1")
        self.requires("python-maquina/1.0.0@mercseng/v2")

    def build(self):
        """Build the elements to package."""
        with tools.environment_append({"PYTHONPATH": [self.package_folder]}):
            packages_list = ""
            for package_name, package_version in self.packages:
                packages_list = packages_list + " " + (package_name+"=="+package_version if package_version else package_name) 

            command = "python -m pip install {packages_list} --target={package_folder} --upgrade --cache-dir={cache_folder}".format(
                packages_list=packages_list,
                package_folder=self.package_folder,
                cache_folder=os.path.join(self.build_folder, "cache"))
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
                        try:
                            with open(filename, "r") as infile:
                                lines = infile.readlines()

                            if len(lines[0]) > 2 and lines[0].startswith("#!"):
                                lines[0] = python_shebang
                                with open(filename, "w") as outfile:
                                    outfile.writelines(lines)
                        except UnicodeDecodeError:
                            pass
    
    def package_info(self):
        """Edit package info."""
        self.env_info.PYTHONPATH.append(self.package_folder)
        bin_directory = os.path.join(self.package_folder, "bin")
        if os.path.exists(bin_directory):
            self.env_info.PATH.append(bin_directory)

