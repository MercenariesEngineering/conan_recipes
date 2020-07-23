from conans import ConanFile, CMake, tools
import os


class OpenEXRConan(ConanFile):
    name = "OpenEXR"
    version = "2.2.0"
    license = "BSD"
    url = "https://github.com/Mikayex/conan-openexr.git"
    requires = "IlmBase/2.2.0@pierousseau/stable", "zlib/1.2.11@conan/stable"
    exports = "mingw-fix.patch", "FindOpenEXR.cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "namespace_versioning": [True, False], "fPIC": [True, False]}
    default_options = "shared=True", "namespace_versioning=True", "fPIC=True"
    generators = "cmake"
    build_policy = "missing"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        self.options["IlmBase"].namespace_versioning = self.options.namespace_versioning
        self.options["IlmBase"].shared = self.options.shared

    def source(self):
        tools.download("http://download.savannah.nongnu.org/releases/openexr/openexr-%s.tar.gz" % self.version,
                       "openexr.tar.gz")
        tools.untargz("openexr.tar.gz")
        os.unlink("openexr.tar.gz")
        tools.replace_in_file("openexr-%s/CMakeLists.txt" % self.version, "PROJECT (openexr)",
                              """PROJECT (openexr)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
set(ILMBASE_PACKAGE_PREFIX ${CONAN_ILMBASE_ROOT})
file(GLOB RUNTIME_FILES ${CONAN_ILMBASE_ROOT}/bin/*.dll ${CONAN_ILMBASE_ROOT}/lib/*.dylib)
file(COPY ${RUNTIME_FILES} DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})""")

        # Fixes for conan putting binaries in bin folder
        tools.replace_in_file("openexr-%s/IlmImf/CMakeLists.txt" % self.version,
                              "${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_CFG_INTDIR}/b44ExpLogTable", "b44ExpLogTable")
        tools.replace_in_file("openexr-%s/IlmImf/CMakeLists.txt" % self.version,
                              "${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_CFG_INTDIR}/dwaLookups", "dwaLookups")
        tools.replace_in_file("openexr-%s/IlmImf/CMakeLists.txt" % self.version, "ADD_EXECUTABLE ( dwaLookups",
                              """file(COPY ${RUNTIME_FILES} DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
ADD_EXECUTABLE ( dwaLookups""")
        tools.replace_in_file("openexr-%s/IlmImf/CMakeLists.txt" % self.version,
                              """  Iex${ILMBASE_LIBSUFFIX}
  IlmThread${ILMBASE_LIBSUFFIX}""", """  IlmThread${ILMBASE_LIBSUFFIX}
  Iex${ILMBASE_LIBSUFFIX}""")  # Fix wrong link order when using static IlmBase on gcc

        # Remove tests compilation
        tools.replace_in_file("openexr-%s/CMakeLists.txt" % self.version, "ADD_SUBDIRECTORY ( IlmImfExamples )", "")
        tools.replace_in_file("openexr-%s/CMakeLists.txt" % self.version, "ADD_SUBDIRECTORY ( IlmImfTest )", "")
        tools.replace_in_file("openexr-%s/CMakeLists.txt" % self.version, "ADD_SUBDIRECTORY ( IlmImfUtilTest )", "")
        tools.replace_in_file("openexr-%s/CMakeLists.txt" % self.version, "ADD_SUBDIRECTORY ( IlmImfFuzzTest )", "")

        if self.settings.os == "Windows" and self.settings.compiler == "gcc":  # MinGW compiler
            tools.patch(patch_file="mingw-fix.patch", base_path="openexr-%s" % self.version)

    def build(self):
        cmake = CMake(self)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else "-DBUILD_SHARED_LIBS=OFF"
        namespace_versioning = "-DNAMESPACE_VERSIONING=ON" if self.options.namespace_versioning else "-DNAMESPACE_VERSIONING=OFF"
        cmake_flags = [shared, namespace_versioning, "-DUSE_ZLIB_WINAPI=OFF"]

        self.run('cmake openexr-%s %s %s' % (self.version, ' '.join(cmake_flags), cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("Imf*.h", dst="include/OpenEXR", src="openexr-%s/IlmImf" % self.version, keep_path=False)
        self.copy("Imf*.h", dst="include/OpenEXR", src="openexr-%s/IlmImfUtil" % self.version, keep_path=False)
        self.copy("OpenEXRConfig.h", dst="include/OpenEXR", src="config", keep_path=False)

        self.copy("*IlmImf*.lib", dst="lib", src=".", keep_path=False)
        self.copy("*IlmImf*.a", dst="lib", src=".", keep_path=False)
        self.copy("*IlmImf*.so", dst="lib", src=".", keep_path=False)
        self.copy("*IlmImf*.so.*", dst="lib", src=".", keep_path=False)
        self.copy("*IlmImf*.dylib*", dst="lib", src=".", keep_path=False)

        self.copy("*IlmImf*.dll", dst="bin", src="bin", keep_path=False)
        self.copy("exr*", dst="bin", src="bin", keep_path=False)

        self.copy("FindOpenEXR.cmake", src=".", dst=".")

    def package_info(self):
        parsed_version = self.version.split('.')
        version_suffix = "-%s_%s" % (parsed_version[0], parsed_version[1]) if self.options.namespace_versioning else ""

        if self.options.shared and self.settings.os == "Windows":
            self.cpp_info.defines.append("OPENEXR_DLL")
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.includedirs = ['include', 'include/OpenEXR']
        self.cpp_info.libs = ["IlmImf" + version_suffix, "IlmImfUtil" + version_suffix]
