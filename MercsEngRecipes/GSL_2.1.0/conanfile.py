import os
from conans import ConanFile, tools

# Recipe based on "GSL/2.1.0@tdelame/stable"
class GSL(ConanFile):
    description = "Guidelines Support Library"
    url = "https://github.com/microsoft/GSL"
    license = "MIT"
    version = "2.1.0"
    name = "GSL"

    _source_subfolder = "source_subfolder"
    
    def source(self):
        """Retrieve source code."""
        url = "{}/archive/v{}.tar.gz".format(self.url, self.version)
        tools.get(url)
        os.rename("{}-{}".format(self.name, self.version), self._source_subfolder)

    def package(self):
        """Assemble the package."""
        self.copy("*", src=os.path.join(self._source_subfolder, "include") ,dst="include")
        self.copy("LICENSE", src=self._source_subfolder, dst="licenses")
        
    def package_id(self):
        self.info.header_only()
