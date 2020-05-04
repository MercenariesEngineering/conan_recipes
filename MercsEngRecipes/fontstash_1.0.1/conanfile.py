import os
from conans import ConanFile

# Recipe based on "fontstash/1.0.1@tdelame/stable"
class fontstash(ConanFile):
    description = "light-weight online font texture atlas builder written in C"
    url = "https://github.com/memononen/fontstash"
    license = "zlib"
    version = "1.0.1"
    name = "fontstash"
    exports_sources = ["fontstash.h", "gl3fontstash.h", "glfontstash.h", "stb_truetype.h", "LICENSE.txt"]
    
    def package(self):
        """Assemble the package."""
        self.copy("*.h", dst="include/fontstash")
        self.copy("*.txt", dst="licenses")
        
    def package_info(self):
        self.cpp_info.includedirs = ["include"]

    def package_id(self):
        self.info.header_only()
