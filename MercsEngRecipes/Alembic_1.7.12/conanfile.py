from conans import ConanFile, CMake, tools
import os

class AlembicConan(ConanFile):
    name = "Alembic"
    version = "1.7.12"
    license = ""
    url = "http://www.alembic.io/"
    description = "Alembic is an open framework for storing and sharing scene data that includes a C++ library, a file format, and client plugins and applications. http://alembic.io/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True", "hdf5:shared=False", "OpenEXR:shared=False", "zlib:shared=False"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("hdf5/1.10.1@pierousseau/stable")
        self.requires("OpenEXR/2.4.0@mercseng/stable")
        self.requires("zlib/1.2.11")

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/alembic/alembic/archive/%s.tar.gz" % self.version)
        os.rename("alembic-%s" % self.version, self._source_subfolder)

    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "ALEMBIC_BUILD_LIBS": True,
            "ALEMBIC_ILMBASE_LINK_STATIC": not self.options["OpenEXR"].shared,
            "ALEMBIC_SHARED_LIBS": self.options.shared,
            "ALEMBIC_LIB_USES_BOOST": False,
            "ALEMBIC_LIB_USES_TR1": False,
            "USE_ARNOLD": False,
            "USE_BINARIES": False,
            "USE_EXAMPLES": False,
            "USE_HDF5": True,
            "USE_MAYA": False,
            "USE_PRMAN": False,
            "USE_PYALEMBIC": False,
            "USE_STATIC_BOOST": True,
            "USE_STATIC_HDF5": not self.options["hdf5"].shared,
            "USE_TESTS": False,
            "ILMBASE_ROOT": self.deps_cpp_info["OpenEXR"].rootpath,
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

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
