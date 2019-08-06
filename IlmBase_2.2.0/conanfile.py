from conans import ConanFile, CMake, tools
import os


class IlmBaseConan(ConanFile):
    name = "IlmBase"
    description = "IlmBase is a component of OpenEXR. OpenEXR is a high dynamic-range (HDR) image file format developed by Industrial Light & Magic for use in computer imaging applications."
    version = "2.2.0"
    license = "BSD"
    url = "https://github.com/Mikayex/conan-ilmbase.git"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "namespace_versioning": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "namespace_versioning=True", "fPIC=True"
    generators = "cmake"
    exports = "FindIlmBase.cmake"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        if "fPIC" in self.options.fields and self.options.shared:
            self.options.fPIC = True

    def source(self):
        tools.download("http://download.savannah.nongnu.org/releases/openexr/ilmbase-%s.tar.gz" % self.version,
                       "ilmbase.tar.gz")
        tools.untargz("ilmbase.tar.gz")
        os.unlink("ilmbase.tar.gz")
        tools.replace_in_file("ilmbase-%s/CMakeLists.txt" % self.version, "PROJECT ( ilmbase )",
                              """PROJECT ( ilmbase )
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

        # Remove tests compilation
        tools.replace_in_file("ilmbase-%s/CMakeLists.txt" % self.version, "ADD_SUBDIRECTORY ( HalfTest )", "")
        tools.replace_in_file("ilmbase-%s/CMakeLists.txt" % self.version, "ADD_SUBDIRECTORY ( IexTest )", "")
        tools.replace_in_file("ilmbase-%s/CMakeLists.txt" % self.version, "ADD_SUBDIRECTORY ( ImathTest )", "")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["NAMESPACE_VERSIONING"] = self.options.namespace_versioning
        if "fPIC" in self.options.fields:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC

        src_dir = "ilmbase-%s" % self.version
        cmake.configure(source_dir=src_dir)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include/OpenEXR", src="ilmbase-%s/Half" % self.version, keep_path=False)
        self.copy("*.h", dst="include/OpenEXR", src="ilmbase-%s/Iex" % self.version, keep_path=False)
        self.copy("*.h", dst="include/OpenEXR", src="ilmbase-%s/IexMath" % self.version, keep_path=False)
        self.copy("*.h", dst="include/OpenEXR", src="ilmbase-%s/IlmThread" % self.version, keep_path=False)
        self.copy("*.h", dst="include/OpenEXR", src="ilmbase-%s/Imath" % self.version, keep_path=False)
        self.copy("IlmBaseConfig.h", dst="include/OpenEXR", src="config", keep_path=False)

        self.copy("*.lib", dst="lib", src=".", keep_path=False)
        self.copy("*.a", dst="lib", src=".", keep_path=False)
        self.copy("*.so", dst="lib", src=".", keep_path=False)
        self.copy("*.so.*", dst="lib", src=".", keep_path=False)
        self.copy("*.dylib*", dst="lib", src=".", keep_path=False)

        self.copy("*.dll", dst="bin", src="bin", keep_path=False)

        self.copy("FindIlmBase.cmake", src=".", dst=".")
        self.copy("license*", dst="licenses", src="ilmbase-%s" % self.version, ignore_case=True, keep_path=False)

    def package_info(self):
        parsed_version = self.version.split('.')
        version_suffix = "-%s_%s" % (parsed_version[0], parsed_version[1]) if self.options.namespace_versioning else ""

        if self.options.shared and self.settings.os == "Windows":
            self.cpp_info.defines.append("OPENEXR_DLL")
        self.cpp_info.includedirs = ['include', 'include/OpenEXR']
        self.cpp_info.libs = ["Imath" + version_suffix, "IexMath" + version_suffix, "Half", "Iex" + version_suffix,
                              "IlmThread" + version_suffix]

        if not self.settings.os == "Windows":
            self.cpp_info.cppflags = ["-pthread"]
