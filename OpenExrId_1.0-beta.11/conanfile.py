from conans import ConanFile, CMake, tools


class OpenExrIdConan(ConanFile):
    name = "OpenExrId"
    version = "1.0-beta.11"
    license = "MIT"
    url = "https://github.com/MercenariesEngineering/openexrid"
    description = "OpenEXR files able to isolate any object of a CG image with a perfect antialiazing "
    requires = "OpenEXR/2.2.0@pierousseau/stable"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False] }
    default_options = "shared=False","OpenEXR:shared=False","fPIC=True"
    generators = "cmake"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        self.run("git clone http://github.com/MercenariesEngineering/openexrid.git")
        self.run("cd openexrid")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("openexrid/CMakeLists.txt", "project (openexrid)", '''project (OpenExrId)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
set(OPENEXR_LOCATION ${CONAN_OPENEXR_ROOT})''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir="%s/openexrid" % self.source_folder)
        cmake.build()
        
    def package(self):
        self.copy("*.h", dst="include/openexrid", src="openexrid/openexrid")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
