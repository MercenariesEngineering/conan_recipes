import json, os
from conans import ConanFile, tools

class Cuda(ConanFile):
    url = "https://developer.nvidia.com/cuda-downloads"
    license = "NVidia"
    version = "12.0.0"
    settings = "os", "compiler", "build_type", "arch"
    name = "cuda_nvrtc"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    short_paths = True

    cuda_components = [ "cuda_nvrtc", "cuda_nvcc" ]

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

        for component in self.cuda_components:
            v = data[component]
            if isinstance (v, dict) and cuda_arch in v:
                relative_path = v[cuda_arch]['relative_path']
                # Unzip the library
                print(f"Get {self.url_base}/{relative_path}")
                tools.get(self.url_base+relative_path)

    def package(self):
        """Assemble the package."""
        for entry in os.listdir("."):
            if os.path.isdir(entry):
                self.copy(src=entry+"/include", dst="include", pattern="*")
                if self.settings.os != "Windows":
                    self.copy(src=entry+"/lib", dst="lib64", pattern="*.a")
                else:
                    self.copy(src=entry+"/lib/x64", dst="lib", pattern="*.lib")

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = [ "nvrtc_static", "nvrtc-builtins_static", "nvptxcompiler_static" ]
