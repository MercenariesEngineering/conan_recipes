from conans import ConanFile, CMake, tools
import os

# mkdir partio_1.7.4
# cd partio_1.7.4/
# conan new partio/1.7.4 --bare
#   write this content to conanfile.py
# conan create partio/1.7.4@pierousseau/stable

class partioConan(ConanFile):
    name = "partio"
    version_base = "1.7"
    version_patch = "4"
    version = version_base + "." + version_patch
    license = ""
    url = "https://github.com/wdas/partio"
    description = "partio - A library for particle IO and manipulation"
    #requires = "SeExpr/2.11@pierousseau/stable"
    requires = "zlib/1.2.11@conan/stable"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        # https://github.com/wdas/partio/archive/v1.7.4.tar.gz
        filename = "v%s.tar.gz" % self.version
        tools.download("https://github.com/wdas/partio/archive/%s" % filename, filename)
        tools.untargz(filename)
        os.unlink(filename)

        tools.replace_in_file("partio-%s/CMakeLists.txt" % self.version,
            "PROJECT(partio LANGUAGES CXX VERSION 1.5.2)",
            """PROJECT(partio LANGUAGES CXX VERSION 1.5.2)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")
        tools.replace_in_file("partio-%s/CMakeLists.txt" % self.version,
            "find_package(GLUT REQUIRED)",
            """find_package(GLUT QUIET)""")
        tools.replace_in_file("partio-%s/CMakeLists.txt" % self.version,
            "ADD_SUBDIRECTORY (src/py)",
            """""")
        tools.replace_in_file("partio-%s/CMakeLists.txt" % self.version,
            "ADD_SUBDIRECTORY (src/tools)",
            """""")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir="%s/partio-%s" % (self.source_folder, self.version))
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
