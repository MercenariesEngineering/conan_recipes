from conans import ConanFile, CMake, tools
import os

class OpenColorIOConan(ConanFile):
    name = "OpenColorIO"
    version = "1.1.1"
    license = ""
    url = "https://opencolorio.org/"
    description = "Open Source Color Management"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    generators = "cmake"

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        # https://github.com/imageworks/OpenColorIO/archive/v1.1.1.tar.gz
        filename = "v%s.tar.gz" % self.version
        tools.download("https://github.com/imageworks/OpenColorIO/archive/%s" % filename, filename)
        tools.untargz(filename)
        os.unlink(filename)

    def build(self):
        cmake = CMake(self)
        if ("fPIC" in self.options.fields and self.options.fPIC == True):
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = True

        cmake.definitions["OCIO_BUILD_APPS"] = False
        cmake.definitions["OCIO_BUILD_DOCS"] = False
        cmake.definitions["OCIO_BUILD_JNIGLUE"] = False
        cmake.definitions["OCIO_BUILD_NUKE"] = False
        cmake.definitions["OCIO_BUILD_PYGLUE"] = False
        cmake.definitions["OCIO_BUILD_SHARED"] = self.options.shared
        cmake.definitions["OCIO_BUILD_STATIC"] = not self.options.shared
        cmake.definitions["OCIO_BUILD_TESTS"] = False
        cmake.definitions["OCIO_BUILD_TRUELIGHT"] = False
        if self.settings.os == "Linux":
            cmake.definitions["CMAKE_CXX_FLAGS"] = "-Wno-deprecated-declarations"

        cmake.configure(source_dir="OpenColorIO-%s" % self.version)
        cmake.build()

    def package(self):
        self.copy("*.h", src="OpenColorIO-%s/export/OpenColorIO/" % self.version, dst="include/OpenColorIO/")
        self.copy("*.h", src="export/", dst="include/OpenColorIO/")
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if (not self.options.shared):
            self.cpp_info.defines = ["OpenColorIO_STATIC"]
