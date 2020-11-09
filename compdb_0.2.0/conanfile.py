import os
from conans import ConanFile, tools

class PythonPackages(ConanFile):
    description = "The compilation database Swiss army knife"
    name = "compdb"
    version = "0.2.0"
    settings = "os", "arch"
    default_options = "*:shared=False"

    packages = [
        ("compdb", "0.2.0")
    ]
    
    def configure(self):
        self.options["cpython"].shared = True

    def build_requirements(self):
        self.build_requires("cpython/3.7.7@mercseng/v0")

    def build(self):
        """Build the elements to package."""
        for package_name, package_version in self.packages:
            command = "python -m pip install {name}=={version} --target={package_folder} --upgrade".format(
                name=package_name,
                version=package_version,
                package_folder=self.package_folder)
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

