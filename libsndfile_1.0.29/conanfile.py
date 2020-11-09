from conans import ConanFile, CMake, tools
import os

class LibSndFile(ConanFile):
    name = "libsndfile"
    version = "1.0.29"
    license = "LGPL"
    url = "http://www.mega-nerd.com/libsndfile/"
    description = "C library for reading and writing files containing samples audio data"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        commit_sha="1a87c443fe37bd67c8d1e2d2b4c8b0291806eb90"
        tools.get("https://github.com/erikd/libsndfile/archive/%s.zip" % commit_sha)
        os.rename("libsndfile-%s" % commit_sha, self._source_subfolder)

        if self.settings.os == "Windows":
            with tools.chdir(os.path.join(self._source_subfolder, "src")):
                tools.replace_in_file("common.c", 
                    "#if HAVE_UNISTD_H", 
                    '''#undef HAVE_UNISTD_H
#if HAVE_UNISTD_H''')

    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "ENABLE_COMPATIBLE_LIBSNDFILE_NAME": True,
            "BUILD_SHARED_LIBS": self.options.shared,
            "ENABLE_PACKAGE_CONFIG": False,
            "ENABLE_BOW_DOCS": False,
            "ENABLE_EXTERNAL_LIBS": False,
            "BUILD_PROGRAMS": False,
            "BUILD_EXAMPLES": False,
            "BUILD_TESTING": False,
            "BUILD_REGTEST": False,
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

        if self.settings.os == "Linux" and self.options.shared:
            # libsndfile.so.1.0 might be requested by libalsa on host systems.
            with tools.chdir(os.path.join(self.package_folder, "lib")):
                os.symlink("libsndfile.so.1.0.29", "libsndfile.so.1.0")

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))