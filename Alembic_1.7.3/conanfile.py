from conans import ConanFile, CMake, tools
import os

class AlembicConan(ConanFile):
    name = "Alembic"
    version = "1.7.3"
    license = ""
    url = "Alembic/1.7.3@pierousseau/stable"
    requires = "hdf5/1.10.1@pierousseau/stable", "IlmBase/2.2.0@pierousseau/stable", "OpenEXR/2.2.0@pierousseau/stable", "zlib/1.2.11@conan/stable"
    description = "Alembic is an open framework for storing and sharing scene data that includes a C++ library, a file format, and client plugins and applications. http://alembic.io/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "hdf5:shared=False", "IlmBase:shared=False", "OpenEXR:shared=False", "zlib:shared=False", "fPIC=True"
    generators = "cmake"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        filename = "Release-%s.tar.gz" % self.version
        tools.download("https://github.com/alembic/alembic/archive/%s.tar.gz" % self.version, filename)
        tools.untargz(filename)
        os.unlink(filename)

        tools.replace_in_file("alembic-%s/CMakeLists.txt" % self.version, "PROJECT(Alembic)",
                              """PROJECT(Alembic)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
set(ILMBASE_HOME ${CONAN_ILMBASE_ROOT})
set(BOOST_HOME ${CONAN_BOOST_ROOT})
set(HDF5_ROOT ${CONAN_HDF5_ROOT})
""")

    def build(self):
        cmake = CMake(self)
        self.run('cmake %s/alembic-%s %s -DALEMBIC_ILMBASE_LINK_STATIC="ON" -DALEMBIC_SHARED_LIBS="OFF" -DUSE_BINARIES="OFF" -DUSE_TESTS="OFF" -DUSE_HDF5="ON" -DUSE_STATIC_BOOST="ON" -DUSE_STATIC_HDF5="ON" -DCMAKE_INSTALL_PREFIX="%s"' % (self.source_folder, self.version, cmake.command_line, self.package_folder))
        self.run("cmake --build . --target install %s" % cmake.build_config)

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = ["Alembic"]
