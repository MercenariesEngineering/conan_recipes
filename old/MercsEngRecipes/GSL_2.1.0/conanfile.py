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
        tools.get("https://github.com/microsoft/GSL/archive/v%s.tar.gz" % self.version)
        os.rename("GSL-%s" % self.version, self._source_subfolder)

    def package(self):
        """Assemble the package."""
        self.copy("*", src=os.path.join(self._source_subfolder, "include") ,dst="include")
        self.copy("LICENSE", src=self._source_subfolder, dst="licenses")
        
    def package_id(self):
        """Header only package hash."""
        self.info.header_only()
