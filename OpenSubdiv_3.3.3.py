from distutils.spawn import find_executable
from conans import ConanFile, CMake, tools
import os, shutil

class OpenSubdiv(ConanFile):
    name = "OpenSubdiv"
    license = "Apache 2.0"
    description = "High performance subdivision surface evaluation"
    url = "https://github.com/PixarAnimationStudios/OpenSubdiv"
    generators = "virtualrunenv"

    version = "3.3.3"
    settings = "os", "build_type"
    options = { "shared": [ True, False ] }
    default_options = { "shared": True }
    requires = ( ( "TBB/2019_U2@tdelame/stable" ) )
    
    build_requires = ( ( "cmake/3.11.2@tdelame/stable" ), ( "ninja/1.8.2@tdelame/stable" ) )

    def requirements( self ):
        if self.settings.os == "Linux":
            self.requires( "GLEW/2.1.0@tdelame/stable" )

    def source(self):
        download_url = "https://github.com/PixarAnimationStudios/OpenSubdiv/archive/v3_3_3.zip"
        folder_name = "OpenSubdiv-3_3_3"
        zip_name = "{}.zip".format( folder_name )

        tools.download( download_url, zip_name )
        tools.unzip( zip_name )
        shutil.move( folder_name, self.name )
        os.remove( zip_name )

        # https://github.com/PixarAnimationStudios/OpenSubdiv/issues/1064
        tools.replace_in_file(
            "OpenSubdiv/cmake/FindTBB.cmake",
            "tbbmalloc_proxy_debug", "")
        tools.replace_in_file(
            "OpenSubdiv/cmake/FindTBB.cmake",
            "tbbmalloc_proxy", "")

        # do not want to compile stuff for regressions while I said to not compile regressions...
        tools.replace_in_file( 
            "OpenSubdiv/CMakeLists.txt", 
            "if (NOT ANDROID", "if (FALSE")
        
    def build(self):
        definition_dict = {
            "BUILD_SHARED_LIBS": self.options.shared,
            "CMAKE_BUILD_TYPE": self.settings.build_type,

            "NO_REGRESSION": True,
            "NO_TUTORIALS": True,
            "NO_EXAMPLES": True,
            "NO_GLFW_X11": True,
            "NO_GLTESTS": True,
            "NO_OPENCL": True,
            "NO_TESTS": True,
            "NO_METAL": True,
            "NO_PTEX": True,            
            "NO_CLEW": True,
            "NO_GLFW": True,
            "NO_CUDA": True,
            "NO_OMP": True,
            "NO_DOC": True,
            "NO_DX": True,
            
            "TBB_LOCATION": os.path.join( self.deps_cpp_info[ "TBB" ].include_paths[ 0 ], "../" )
        }

        if self.settings.os == "Linux":
            glew_root_dir = os.path.join( self.deps_cpp_info[ "GLEW" ].lib_paths[ 0 ], "../" )
            definition_dict[ "GLEW_LOCATION" ] = glew_root_dir
            definition_dict[ "CMAKE_CXX_FLAGS" ] = "-fPIC -m64 -I{}".format( self.deps_cpp_info[ "GLU" ].include_paths[ 0 ] )

            if self.settings.build_type == "Release":
                definition_dict[ "CMAKE_CXX_FLAGS" ] = "{} -O3".format( definition_dict[ "CMAKE_CXX_FLAGS" ] )

            if find_executable( "lld" ) is not None:
                definition_dict[ "CMAKE_SHARED_LINKER_FLAGS" ] = "-fuse-ld=lld"
                definition_dict[ "CMAKE_EXE_LINKER_FLAGS"    ] = "-fuse-ld=lld"

        cmake = CMake( self, generator = "Ninja" )
        cmake.configure(
            defs = definition_dict,
            source_folder = self.name
        )
        cmake.build()

    def package(self):
        self.copy( "*.h", src="OpenSubdiv/opensubdiv", dst="include/opensubdiv", keep_path = True )
        if self.settings.os == "Linux":
            pattern = "*.so*" if self.options.shared else "*.a"
            self.copy( pattern, src="lib", dst="lib", symlinks = True  )

    def package_info(self):
        self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
        self.cpp_info.libs = tools.collect_libs(self)
