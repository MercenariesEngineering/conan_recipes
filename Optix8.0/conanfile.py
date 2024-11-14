import json, os
from conans import ConanFile, tools

class Optix8(ConanFile):
    name = "Optix"
    description = "Headers for NVidia Optix8"
    topics = "conan", "optix", "headers"
    homepage = "https://developer.nvidia.com/rtx/ray-tracing/optix"
    license = "cuda"
    url = "https://developer.nvidia.com/rtx/ray-tracing/optix"
    _source_subfolder = "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"]["8.0.0"], destination=f"./{self._source_subfolder}/include")

    def package(self):
        self.copy("*", src=os.path.join(self.build_folder, self._source_subfolder, "include"), dst="include", keep_path=True)

    def package_id(self):
        self.info.header_only()
