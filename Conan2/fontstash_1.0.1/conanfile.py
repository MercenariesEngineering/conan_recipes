from conan import ConanFile
from conan.tools.files import copy
import os

# Recipe based on "fontstash/1.0.1@tdelame/stable"
class fontstash(ConanFile):
    user="mercs"
    name = "fontstash"
    version = "1.0.1"
    description = "light-weight online font texture atlas builder written in C"
    url = "https://github.com/memononen/fontstash"
    license = "zlib"
    package_type = "header-library"
    exports_sources = "dist/*"
    
    def package(self):
        """Assemble the package."""
        copy(self, "*.h", src=os.path.join(self.source_folder, "dist"), dst=os.path.join(self.package_folder, "include/fontstash"))
        copy(self, "*.txt", src=os.path.join(self.source_folder, "dist"), dst=os.path.join(self.package_folder, "licenses"))
        
    def package_info(self):
        """Edit package info."""
        self.cpp_info.includedirs = ["include"]
