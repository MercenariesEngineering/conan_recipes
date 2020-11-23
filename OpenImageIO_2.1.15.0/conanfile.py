import os
import shutil
from conans import ConanFile, CMake, tools

class OpenimageioConan(ConanFile):
    name = "OpenImageIO"
    version = "2.1.15.0"
    license = "Modified BSD License"
    url = "http://www.openimageio.org"
    description = "OpenImageIO is a library for reading and writing images, and a bunch of related classes, utilities, and applications"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "zlib:shared=False", "OpenEXR:shared=False", "libpng:shared=False", "libjpeg-turbo:shared=False", "libtiff:shared=False", "boost:shared=False", "boost:i18n_backend=icu", "boost:zstd=True", "boost:lzma=True", "fPIC=True"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"
    recipe_version = "2"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("boost/1.73.0@mercseng/v1")
        self.requires("bzip2/1.0.8@mercseng/v0")
        self.requires("freetype/2.10.2_with_Harfbuzz@mercseng/v0")
        self.requires("jbig/20160605@mercseng/v0")
        self.requires("libjpeg-turbo/1.5.2@mercseng/v0")
        self.requires("libpng/1.6.37@mercseng/v0")
        self.requires("libtiff/4.0.9@mercseng/v0")
        self.requires("lzma/5.2.4@mercseng/v0")
        self.requires("OpenEXR/2.5.1@mercseng/v0")
        self.requires("tbb/2020.02@mercseng/v2")
        self.requires("zlib/1.2.11@mercseng/v0")

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/OpenImageIO/oiio/archive/Release-%s.tar.gz" % self.version)
        os.rename("oiio-Release-%s" %self.version, self._source_subfolder)

        # Add a wrapper CMakeLists.txt file which initializes conan before executing the real CMakeLists.txt
        os.rename(os.path.join(self._source_subfolder, "CMakeLists.txt"), os.path.join(self._source_subfolder, "CMakeLists_original.txt"))
        shutil.copy("CMakeLists.txt", os.path.join(self._source_subfolder, "CMakeLists.txt"))

    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "BUILD_SHARED_LIBS": self.options.shared,
            "LINKSTATIC": True,
            "OIIO_BUILD_TESTS": False,
            "OIIO_BUILD_TOOLS": False,
            "OIIO_THREAD_ALLOW_DCLP": True,
            "STOP_ON_WARNING": False,
            
            "EMBEDPLUGINS": True,
            "INSTALL_DOCS": False,
            "BUILD_DOCS": False,
            "USE_STD_REGEX": True,

            "USE_PYTHON": False,
            "USE_HDF5": False,
            "USE_OpenColorIO": False,
            "USE_OpenCV": False,
            "USE_DCMTK": False,
            "USE_Field3D": False,
            "USE_Libheif": False,
            "USE_LibRaw": False,
            "USE_Webp": False,
            "USE_Nuke": False,
            "USE_R3DSDK": False,
            "USE_OpenGL": False,
            "USE_OpenVDB": False,
            "USE_PTex": False,
            "USE_Qt5": False,
            "USE_Libsquish": False,
            "USE_OpenJpeg": False,
            "USE_FFmpeg": False,
            "USE_GIF": False,
            "USE_JPEGTurbo": True,

            "JPEGTurbo_ROOT": self.deps_cpp_info["libjpeg-turbo"].rootpath,
            "JPEG_NAMES": "turbojpeg-static.lib" if self.settings.os == "Windows" else "libturbojpeg.a",
            "BOOST_ROOT": self.deps_cpp_info["boost"].rootpath,
            "BOOST_LIBRARYDIR": "%s/lib" % self.deps_cpp_info["boost"].rootpath,
            "Boost_FILESYSTEM_LIBRARY": "boost_filesystem" if self.settings.os == "Windows" else "libboost_filesystem",
            "Boost_REGEX_LIBRARY": "boost_regex" if self.settings.os == "Windows" else "libboost_regex",
            "Boost_SYSTEM_LIBRARY": "boost_system" if self.settings.os == "Windows" else "libboost_system",
            "Boost_THREAD_LIBRARY": "boost_thread" if self.settings.os == "Windows" else "libboost_thread",
        }

        if (self.settings.compiler == "gcc" and self.settings.compiler.version == 4.1):
            definition_dict["USE_SIMD"] = "0"

        return definition_dict

    def build(self):
        """Build the elements to package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.build()

    def package(self):
        """Assemble the package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.install()

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
        if not self.options.shared:
            self.cpp_info.defines = ["OIIO_STATIC_DEFINE"]

        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
