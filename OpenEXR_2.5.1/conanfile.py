from conans import ConanFile, CMake, tools
import os


# Recipe based on "openexr/2.4.0", redefined for upper/lowercase compatibility
class OpenEXRConan(ConanFile):
    name = "OpenEXR"
    version = "2.5.1"
    description = "OpenEXR is a high dynamic-range (HDR) image file format developed by Industrial Light & " \
                  "Magic for use in computer imaging applications."
    topics = ("conan", "openexr", "hdr", "image", "picture")
    license = "BSD-3-Clause"
    homepage = "https://github.com/openexr/openexr"
    url = "https://github.com/conan-io/conan-center-index"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake", "cmake_find_package"
    exports_sources = "CMakeLists.txt"
    _source_subfolder = "source_subfolder"

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def requirements(self):
        """Define runtime requirements."""
        self.requires("zlib/1.2.11@mercseng/v0")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/openexr/openexr/archive/v%s.tar.gz" % self.version)
        os.rename("openexr-{}".format(self.version), self._source_subfolder)
        
    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "PYILMBASE_ENABLE": False,
            "OPENEXR_VIEWERS_ENABLE": False,
            "OPENEXR_BUILD_BOTH_STATIC_SHARED": False,
            "OPENEXR_BUILD_UTILS": False,
            "CMAKE_DEBUG_POSTFIX": "",
            "BUILD_TESTING": False,
        }

        return definition_dict

    def build(self):
        """Build the elements to package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions())
        cmake.build()

    def package(self):
        """Assemble the package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions())
        cmake.install()
        self.copy("LICENSE.md", src=self._source_subfolder, dst="licenses")

    def package_info(self):
        """Edit package info."""
        if self.settings.os == "Windows":
            self.cpp_info.libs = tools.collect_libs(self)
        else:
            # Lib order matters on linux.
            parsed_version = self.version.split('.')
            version_suffix = "-%s_%s" % (parsed_version[0], parsed_version[1])
            self.cpp_info.libs = [
                    "IlmImf" + version_suffix,
                    "Imath" + version_suffix,
                    "Iex" + version_suffix,
                    "IexMath" + version_suffix,
                    "Half" + version_suffix,
                    "IlmThread" + version_suffix,
                    "IlmImfUtil" + version_suffix
                ]
        
        self.cpp_info.includedirs = [os.path.join("include", "OpenEXR"), "include"]
        if self.options.shared and self.settings.os == "Windows":
            self.cpp_info.defines.append("OPENEXR_DLL")

        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("pthread")
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))            
