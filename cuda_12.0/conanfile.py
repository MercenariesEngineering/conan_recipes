import json, os
from conans import ConanFile, tools

class Cuda(ConanFile):
    url = "https://developer.nvidia.com/cuda-downloads"
    license = "NVidia"
    version = "12.0.0"
    settings = "os", "compiler", "build_type", "arch"
    name = "cuda"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    short_paths = True

    cuda_components = [
        "cuda_cccl", "cuda_compat", "cuda_cudart", "cuda_cupti", "cuda_gdb",
        "cuda_nvcc", "cuda_nvml_dev", "cuda_nvprof", "cuda_nvprune", "cuda_nvrtc",
        "cuda_nvtx", "cuda_opencl", "cuda_profiler_api", "cuda_sanitizer_api",
        "libcublas", "libcudla", "libcufft", "libcufile", "libcurand",
        "libcusolver", "libcusparse", "libnpp", "libnvidia_nscq", "libnvjitlink",
        "libnvjpeg", "nvidia_fs", "visual_studio_integration" ]
    #cuda_components = []
    exclude_cuda_components = [ "nvidia_driver" ]

    def _package_component(self, component):
        return (component not in self.exclude_cuda_components) and (len (self.cuda_components) == 0 or component in self.cuda_components)

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
          if self._package_component (k) and isinstance(v, dict):
            if cuda_arch in v:
                relative_path = v[cuda_arch]['relative_path']
                # Unzip the library
                print(f"Get {self.url_base}/{relative_path}")
                tools.get(self.url_base+relative_path)

    def package(self):
        """Assemble the package."""
        if self.settings.os == "Windows":
            lib_folder = "x64"
        if self.settings.os == "Linux":
            lib_folder = ""
        print ("** List content of cwd: "+os.getcwd())
        for entry in os.listdir("."):
            print (entry)
        print ("**")
        for component in os.listdir("."):
            if os.path.isdir(component):
                print (component+":")
                try:
                    os.chmod(component+"/LICENSE", 0o644)
                except:
                    pass
                for entry in os.listdir ("./"+component):
                    print ("  "+entry)
                    srcentry = entry
                    dstentry = entry
                    if entry == "lib":
                        if self.settings.os == "Linux":
                            dstentry = "lib64"
                        elif self.settings.os == "Windows":
                            srcentry = entry+"/x64"
                    self.copy(pattern="*", src=component+"/"+srcentry, dst=dstentry)

                #self.copy(pattern="*", src=entry)
                #if self.settings.os == "Linux":
                #    os.rename ("./lib", "./lib64")
                #if self.settings.os == "Windows":
                #    os.rename ("./lib/x64", "./lib64")
                #    os.remove ("./lib")
                #self.copy(pattern="*", src=entry, excludes=entry+"/lib/x64/*")
                #self.copy(pattern="*", src=entry+"/lib/x64", dst="lib")

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
