from distutils.spawn import find_executable
from conans import ConanFile, CMake, tools
import os, shutil


class Ptex(ConanFile):
    name = "ptex"
    version = "2.3.1"
    license = "Apache 2.0"
    description = "Per-Face Texture Mapping for Production Rendering"
    url = "https://github.com/wdas/ptex"
    settings = "os"
    requires = ( ( "zlib/1.2.11@tdelame/stable" ) )
    build_requires = ( ( "cmake/3.11.2@tdelame/stable" ) )
    generators = "virtualrunenv"

    def source(self):
        zip_name = "{}-{}.zip".format( self.name, self.version )
        tools.download( "https://github.com/wdas/ptex/archive/v{}.zip".format( self.version ), zip_name )
        tools.unzip(zip_name)
        shutil.move( "{}-{}".format( self.name, self.version), self.name )
        os.remove(zip_name)

    def build(self):

        zlib_root_dir = os.path.join( self.deps_cpp_info[ "zlib" ].libdirs[ 0 ], "../" )

        definition_dict = {
            "CMAKE_BUILD_TYPE": "Release",
            "PTEX_VER": "v2.3.1",
            "PTEX_BUILD_STATIC_LIBS": False,
            "PTEX_BUILD_SHARED_LIBS": True,
            "PRMAN_15_COMPATIBLE_PTEX": False,
            "ZLIB_ROOT": zlib_root_dir,
        }

        if self.settings.os == "Linux" and find_executable( "lld" ) is not None:
            definition_dict[ "CMAKE_SHARED_LINKER_FLAGS" ] = "-fuse-ld=lld"
            definition_dict[ "CMAKE_EXE_LINKER_FLAGS"    ] = "-fuse-ld=lld"

        os.environ[ "CXXFLAGS_STD" ] = "c++14"

        cmake = CMake(self)
        cmake.configure( defs = definition_dict, source_folder = self.name )
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
  
