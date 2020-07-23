from conans import ConanFile, tools
import os

class Spdlog(ConanFile):
    
    description = "Very fast, header only, C++ logging library. Customized for Rumba"
    url = "https://github.com/gabime/spdlog"
    license = "MIT"
    name = "spdlog-rumba"
    version = "1.5.0"   

    exports_sources = ["tweakme.h"]
    _source_subfolder = "source_subfolder"

    def source(self):
        """Retrieve source code."""
        url = "https://github.com/gabime/spdlog/archive/v{}.tar.gz".format(self.version)
        tools.get(url)
        os.rename("spdlog-{}".format(self.version), self._source_subfolder)

    def package(self):
        """Assemble the package."""
        self.copy("*",
            src=os.path.join(self.source_folder, self._source_subfolder, "include", "spdlog"),
            dst=os.path.join(self.package_folder, "include", "spdlog"),
            keep_path=True)
        self.copy("tweakme.h", dst="include/spdlog")

    def package_id(self):
        self.info.header_only()

