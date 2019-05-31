from conans import ConanFile, CMake, tools
import os

class OpenimageioConan(ConanFile):
    name = "openimageio"
    version = "1.6.18"
    license = "Modified BSD License"
    url = "http://www.openimageio.org"
    requires = "boost/1.64.0@conan/stable", "IlmBase/2.2.0@Mikayex/stable", "libjpeg-turbo/1.5.2@pierousseau/stable", "libpng/1.6.37@bincrafters/stable", "libtiff/4.0.9@bincrafters/stable", "OpenEXR/2.2.0@pierousseau/stable", "zlib/1.2.11@conan/stable"
    description = "OpenImageIO http://www.openimageio.org"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False","IlmBase:shared=False", "zlib:shared=False", "OpenEXR:shared=False", "libpng:shared=False", "libjpeg-turbo:shared=False", "libtiff:shared=False", "boost:shared=False", "boost:without_filesystem=False", "boost:without_regex=False", "boost:without_system=False", "boost:without_thread=False"
    generators = "cmake"

    def source(self):
        filename = "Release-%s.tar.gz" % self.version
        tools.download("https://github.com/OpenImageIO/oiio/archive/Release-%s.tar.gz" % self.version, filename)
        #from shutil import copyfile
        #copyfile("c:/tmp/"+filename, filename)
        tools.untargz(filename)
        os.unlink(filename)

        if self.settings.os == "Windows" :
            libjpeg = "turbojpeg-static.lib"
        else :
            libjpeg = "libturbojpeg.a"
        
        tools.replace_in_file("oiio-Release-%s/CMakeLists.txt" % self.version, "project (OpenImageIO)",
                              """project (OpenImageIO)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
set(ILMBASE_HOME ${CONAN_ILMBASE_ROOT})
set(BOOST_ROOT ${CONAN_BOOST_ROOT})
set(BOOST_LIBRARYDIR ${CONAN_BOOST_ROOT}/lib)
set(OPENEXR_HOME ${CONAN_OPENEXR_ROOT})
find_package("ZLIB")
set(PNG_PNG_INCLUDE_DIR ${CONAN_INCLUDE_DIRS_LIBPNG})
set(JPEG_LIBRARY ${CONAN_LIB_DIRS_LIBJPEG-TURBO}/%s)
""" % libjpeg)
        # Remove -DOPENEXR_DLL
        tools.replace_in_file("oiio-Release-%s/CMakeLists.txt" % self.version, "add_definitions (-DOPENEXR_DLL)", "")

    def build(self):
        cmake = CMake(self)
        # cmake.configure(source_dir="%s/oiio-Release-%s" % (self.source_folder, self.version))
        # cmake.build()

        # Explicit way:
        self.run('cmake %s/oiio-Release-%s %s -DBUILDSTATIC:BOOLEAN=ON -DLINKSTATIC:BOOLEAN=ON -DCMAKE_INSTALL_PREFIX="%s"' % (self.source_folder, self.version, cmake.command_line, self.package_folder))
        self.run("cmake --build . --target install %s" % cmake.build_config)
        
    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = ["openimageio"]
        self.cpp_info.defines = ["OIIO_STATIC_BUILD"]
