from distutils.spawn import find_executable
from conans import ConanFile, CMake, tools
import os, re, shutil, subprocess

class TBB(ConanFile):
    name = "TBB"
    license = "Apache 2.0"
    description = "Threading Building Blocks"
    url = "https://github.com/01org/tbb"
    version = "2019_U6"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        # Use the repository of Wenzel Jakob that adds a CMake layer over TBB code.
        url = "https://github.com/wjakob/tbb/archive/344fa84f34089681732a54f5def93a30a3056ab9.zip"
        unzipped_folder = "tbb-344fa84f34089681732a54f5def93a30a3056ab9"
        zip_name = "tbb.zip"

        tools.download( url, zip_name )
        tools.unzip( zip_name )
        shutil.move( unzipped_folder, self.name )
        os.remove( zip_name )

    def build(self):
        # TBBMALLOC PROXY is not included into this package because:
        # - it prevent crashes when it is linked to, since it should be
        # preloaded only to replace allocators.
        # - it serves a different purpose and could be then included into
        # another package if needed.
        cmake = CMake(self)

        if ("fPIC" in self.options.fields and self.options.fPIC == True):
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = True

        cmake.definitions["CMAKE_BUILD_TYPE"] = self.settings.build_type
        cmake.definitions["TBB_BUILD_SHARED"] = self.options.shared
        cmake.definitions["TBB_BUILD_STATIC"] = not self.options.shared
        cmake.definitions["TBB_BUILD_TBBMALLOC"] = True
        cmake.definitions["TBB_BUILD_TBBMALLOC_PROXY"] = False
        cmake.definitions["TBB_BUILD_TESTS"] = False
        cmake.definitions["TBB_CI_BUILD"] = False

        if self.settings.os == "Linux" and find_executable( "gcc" ) is not None:
            gcc_version = subprocess.check_output( [ "gcc", "-dumpversion" ] ).decode( "utf-8" )

            # Keep it simple to work on python 2.7 as well as on python 3+
            major, minor, build = 0, 0, 0
            version_numbers = re.findall( r"\d+", gcc_version )
            version_numbers_count = len( version_numbers )

            if version_numbers_count > 0:
                major = int( version_numbers[ 0 ] )

            if version_numbers_count > 1:
                minor = int( version_numbers[ 1 ] )

            if version_numbers_count > 2:
                build = int( version_numbers[ 2 ] )

            tbb_glibcxx_version = major * 10000 + minor * 100 + build
            cmake.definitions["TBB_USE_GLIBCXX_VERSION"] = tbb_glibcxx_version

            # Normally not necessary, but it does not cost anything to enforce it.
            if self.settings.build_type == "Debug":
                cmake.definitions["CMAKE_CXX_FLAGS"] = "-DTBB_USE_DEBUG=2"

        cmake.configure(source_folder = self.name)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy( "*", src = "package/bin"    , dst = "bin" )
        self.copy( "*", src = "package/lib"    , dst = "lib", symlinks = True )
        self.copy( "*", src = "package/include", dst = "include", symlinks = True )

    def package_info(self):
        self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
        self.env_info.PATH.append( os.path.join( self.package_folder, "bin" ) )
        self.cpp_info.libs = tools.collect_libs(self)

        if self.settings.build_type == "Debug":
            self.cpp_info.defines.append( "TBB_USE_DEBUG=1" )
        self.cpp_info.defines.append( "__TBB_NO_IMPLICIT_LINKAGE" )
