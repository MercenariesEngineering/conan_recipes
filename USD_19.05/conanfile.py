from conans import ConanFile, CMake, tools
import os

class USDConan(ConanFile):
    name = "USD"
    version = "19.05"
    license = ""
    url = "https://graphics.pixar.com/usd/docs/index.html"
    description = "Universal scene description"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    requires = "boost/1.64.0@conan/stable", "hdf5/1.10.1@pierousseau/stable", "OpenEXR/2.2.0@pierousseau/stable", "OpenImageIO/1.6.18@pierousseau/stable", "OpenColorIO/1.1.1@pierousseau/stable", "ptex/2.3.2@pierousseau/stable", "TBB/2019_U6@pierousseau/stable"
    default_options = "shared=True", "fPIC=True", "*:shared=False", "*:fPIC=True"
    generators = "cmake"
    short_paths = True

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        # should be https://github.com/PixarAnimationStudios/USD/archive/v19.05.tar.gz, but in debug mode it tries to link with python debug libs.
        # We will use Autodesk's fork instead, which fixes this issue, until this pull request is merged: https://github.com/PixarAnimationStudios/USD/pull/785
        #filename = "v%s.tar.gz" % self.version
        #tools.download("https://github.com/PixarAnimationStudios/USD/archive/%s" % filename, filename)
        #tools.untargz(filename)
        #os.unlink(filename)

        # https://github.com/autodesk-forks/USD/archive/fix_debug_build.zip
        filename = "fix_debug_build.zip"
        tools.download("https://github.com/autodesk-forks/USD/archive/%s" % filename, filename)
        tools.unzip(filename)
        os.unlink(filename)
        os.rename("USD-fix_debug_build", "USD-%s" % self.version)

        # setup conan for cmake
        tools.replace_in_file("USD-%s/CMakeLists.txt" % self.version, "project(usd)",
                              """project(usd)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
""")
        # keeping this would mess up dllimport directives in MSVC
        tools.replace_in_file("USD-%s/cmake/defaults/msvcdefaults.cmake" % self.version, """_add_define("BOOST_ALL_DYN_LINK")""", "")

    def _configure_cmake(self):
        cmake = CMake(self)

        if self.settings.build_type=="Release":
            cmake.build_type = 'RelWithDebInfo'

        if ("fPIC" in self.options.fields and self.options.fPIC == True):
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = True

        cmake.definitions["TBB_ROOT"] = self.deps_cpp_info["TBB"].rootpath
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            cmake.definitions["TBB_LIBRARY"] = self.deps_cpp_info["TBB"].rootpath
            cmake.definitions["TBB_USE_DEBUG_BUILD"] = True # link against tbb_debug.lib/a

        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared        
        cmake.definitions["PXR_BUILD_TESTS"] = False
        cmake.definitions["PXR_BUILD_USDVIEW"] = False
        cmake.definitions["PXR_BUILD_IMAGING"] = False
        cmake.definitions["PXR_ENABLE_GL_SUPPORT"] = False
        cmake.definitions["PXR_ENABLE_PYTHON_SUPPORT"] = False

        cmake.configure(source_dir="USD-%s" % self.version)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install() # install will package some files better than explicit copy

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.bindirs = ["lib", "bin"] # This will put "lib" folder in the path, which we need to find the plugins.
        self.cpp_info.defines = ["NOMINMAX", "YY_NO_UNISTD_H"]
        
        if self.settings.build_type == "Debug":
            self.cpp_info.defines.append("BUILD_OPTLEVEL_DEV")
        
        if self.options.shared == "False":
            self.cpp_info.defines.append("PXR_STATIC=1")