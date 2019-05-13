from distutils.spawn import find_executable
from conans import ConanFile, CMake, tools
import os, shutil

class EmbreeConan(ConanFile):
    name = "embree"
    license = "Apache 2.0"
    description = "The embree ray tracing library"
    url = "https://github.com/embree/embree"
    generators = "virtualrunenv"

    version = "3.3.0"
    settings = "os", "build_type"
    options = { "shared": [ True, False ] }
    default_options = { "shared": True }
    requires = ( ( "TBB/2019_U2@tdelame/stable" ) )
    build_requires = ( ( "cmake/3.11.2@tdelame/stable" ), ( "ninja/1.8.2@tdelame/stable" ) )

    def source(self):
        zip_name = "{}-{}.zip".format( self.name, self.version )
        tools.download( "https://github.com/embree/embree/archive/v{}.zip".format( self.version ), zip_name)
        tools.unzip(zip_name)
        shutil.move( "{}-{}".format( self.name, self.version), self.name )
        os.unlink(zip_name)

    def build(self):
        definition_dict = {
            "CMAKE_BUILD_TYPE": self.settings.build_type,
            "BUILD_SHARED_LIBS": self.options.shared,
            "EMBREE_STATIC_LIB": not self.options.shared,
            "EMBREE_TUTORIALS": False,
            "EMBREE_TASKING_SYSTEM": "TBB",
            "EMBREE_MAX_ISA": "AVX512SKX",
            "EMBREE_ISPC_SUPPORT": False,

            "TBB_INCLUDE_DIR"   : self.deps_cpp_info[ "TBB" ].include_paths[ 0 ],
            "TBB_LIBRARY"       : os.path.join( self.deps_cpp_info[ "TBB" ].lib_paths[ 0 ], "libtbb.so" ),
            "TBB_LIBRARY_MALLOC": os.path.join( self.deps_cpp_info[ "TBB" ].lib_paths[ 0 ], "libtbbmalloc.so" )
        }

        if self.settings.os == "Linux" and find_executable( "lld" ) is not None:
            definition_dict[ "CMAKE_SHARED_LINKER_FLAGS" ] = "-fuse-ld=lld"
            definition_dict[ "CMAKE_EXE_LINKER_FLAGS"    ] = "-fuse-ld=lld"

        cmake = CMake( self, generator = "Ninja" )
        cmake.configure(
            defs = definition_dict,
            source_folder = self.name
        )
        cmake.build()

    def package(self):
        self.copy( "*.h"   , src="embree/include", dst="include", keep_path = True )
        self.copy( "*.isph", src="embree/include", dst="include", keep_path = True )
        self.copy( "*.h"   , src="embree/kernels", dst="kernels", keep_path = True )
        self.copy( "*.h"   , src="embree/common",  dst="common" , keep_path = True )

        self.copy( "*.so*", dst="lib", symlinks = True )


    def package_info(self):
        self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = [ 'include', 'kernels' ]
        self.cpp_info.defines.append( "TASKING_TBB" )
