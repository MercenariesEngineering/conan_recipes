from conans import ConanFile, CMake, tools
import os


# Recipe based on "openexr/2.4.0", redefined for upper/lowercase compatibility
class OpenEXRConan(ConanFile):
    name = "OpenEXR"
    version = "2.4.0"
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
        self.requires("zlib/1.2.11")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/openexr/openexr/archive/v%s.tar.gz" % self.version)
        os.rename("openexr-{}".format(self.version), self._source_subfolder)
        
        for lib in ("OpenEXR", "IlmBase"):
            if self.settings.os == "Windows":
                tools.replace_in_file(os.path.join(self._source_subfolder,  lib, "config", "LibraryDefine.cmake"),
                                      "${CMAKE_COMMAND} -E chdir ${CMAKE_INSTALL_FULL_LIBDIR}",
                                      "${CMAKE_COMMAND} -E chdir ${CMAKE_INSTALL_FULL_BINDIR}")
            if self.settings.build_type == "Debug":
                tools.replace_in_file(os.path.join(self._source_subfolder,  lib, "config", "LibraryDefine.cmake"),
                                      "set(verlibname ${CMAKE_SHARED_LIBRARY_PREFIX}${libname}${@LIB@_LIB_SUFFIX}${CMAKE_SHARED_LIBRARY_SUFFIX})".replace("@LIB@", lib.upper()),
                                      "set(verlibname ${CMAKE_SHARED_LIBRARY_PREFIX}${libname}${@LIB@_LIB_SUFFIX}_d${CMAKE_SHARED_LIBRARY_SUFFIX})".replace("@LIB@", lib.upper()))
                tools.replace_in_file(os.path.join(self._source_subfolder,  lib, "config", "LibraryDefine.cmake"),
                                      "set(baselibname ${CMAKE_SHARED_LIBRARY_PREFIX}${libname}${CMAKE_SHARED_LIBRARY_SUFFIX})",
                                      "set(baselibname ${CMAKE_SHARED_LIBRARY_PREFIX}${libname}_d${CMAKE_SHARED_LIBRARY_SUFFIX})")

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
        self.cpp_info.libs = tools.collect_libs(self)
        
        self.cpp_info.includedirs = [os.path.join("include", "OpenEXR"), "include"]
        if self.options.shared and self.settings.os == "Windows":
            self.cpp_info.defines.append("OPENEXR_DLL")

        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("pthread")
