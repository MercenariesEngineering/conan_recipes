import json, os
from conans import ConanFile, tools

class Cuda(ConanFile):
    url = "https://developer.nvidia.com/cuda-downloads"
    license = "NVidia"
    version = "12.5.0"
    settings = "os", "compiler", "build_type", "arch"
    name = "cuda"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    short_paths = True

    def config_options(self):
        if self.settings.os != "Windows":
            self.settings.remove("compiler")
        elif self.settings.compiler != 'Visual Studio':
            raise RuntimeError("Only Visual Studio is supported on Windows.")

    def source(self):
        """Retrieve source code."""
        self.json_file = f"redistrib_{self.version}.json"
        self.url_base = "https://developer.download.nvidia.com/compute/cuda/redist/"
        url = self.url_base+self.json_file
        tools.download(url, self.json_file)

    def build(self):
        """Build the elements to package"""
        if self.settings.os == "Windows":
            cuda_arch = "windows-x86_64"
        if self.settings.os == "Linux":
            cuda_arch = "linux-x86_64"

        f = open(self.json_file)

        # Parse the json file
        data = json.load(f)
        for k,v in data.items():
        #v = data["cuda_cudart"]
          if isinstance(v, dict):
            if cuda_arch in v:
                relative_path = v[cuda_arch]['relative_path']
                # Unzip the library
                tools.get(self.url_base+relative_path)

    def package(self):
        """Assemble the package."""
        if self.settings.os == "Windows":
            lib_folder = "x64"
        if self.settings.os == "Linux":
            lib_folder = ""
        for entry in os.listdir("."):
            if os.path.isdir(entry):
                print (entry)
                self.copy(pattern="*.*", src=entry, excludes=entry+"/lib/x64/*")
                self.copy(pattern="*.*", src=entry+"/lib/x64", dst="lib")

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
