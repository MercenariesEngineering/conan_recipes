from distutils.spawn import find_executable
from conans import ConanFile, CMake, tools
import os, stat, shutil

def on_shutil_rmtree_error( func, path, exc_info ):
    os.chmod( path, stat.S_IWRITE )
    os.remove( path )

def remove_directory( directory_path ):
    shutil.rmtree( directory_path, onerror = on_shutil_rmtree_error )

def remove( path ):
    if os.path.exists( path ):
        if os.path.isdir( path ):
            remove_directory( path )
        else:
            os.remove( path )


class LibSndFile( ConanFile ):
    name = "libsndfile"
    license = " "
    description = "C library for reading and writing files containing samples audio data"
    url = "http://www.mega-nerd.com/libsndfile/"
    generators = "virtualrunenv"

    version = "1.0.29"
    settings = "os", "build_type"
    options = { "shared": [ True, False ] }
    default_options = { "shared": True }

    def build_requirements( self ):
        if self.settings.os == "Linux":
            self.build_requires( "cmake/3.11.2@tdelame/stable" )
            self.build_requires( "ninja/1.8.2@tdelame/stable" )

    def source( self ):
        sha = "1a87c443fe37bd67c8d1e2d2b4c8b0291806eb90"
        download_url = "https://github.com/erikd/libsndfile/archive/{}.zip".format( sha )
        folder_name = "libsndfile-{}".format( sha )
        zipped_folder_name = "{}.zip".format( folder_name )

        tools.download( download_url, zipped_folder_name )
        tools.unzip( zipped_folder_name )
        shutil.move( folder_name, self.name )
        os.remove( zipped_folder_name )

        if self.settings.os == "Windows":
            tools.replace_in_file("libsndfile/src/common.c", "#if HAVE_UNISTD_H", '''#undef HAVE_UNISTD_H
#if HAVE_UNISTD_H''')

    def configure_cmake( self ):
        #Note: I do not add ogg, flac, and vorbis dependences here since we do
        # not have requests nor requirements for these formats.
        definition_dict = {
            "CMAKE_BUILD_TYPE": "RELEASE" if self.settings.build_type == "Release" else "DEBUG",
            
            "ENABLE_COMPATIBLE_LIBSNDFILE_NAME": True,
            "BUILD_SHARED_LIBS": self.options.shared,
            "ENABLE_PACKAGE_CONFIG": False,
            "ENABLE_BOW_DOCS": False,
            "BUILD_PROGRAMS": False,
            "BUILD_EXAMPLES": False,
            "BUILD_TESTING": False,
            "BUILD_REGTEST": False,
        }

        if self.settings.os == "Linux":

            if self.settings.build_type == "Release":
                definition_dict[ "CMAKE_C_FLAGS" ] = "-fPIC -m64 -O3"
            else:
                definition_dict[ "CMAKE_C_FLAGS" ] = "-fPIC -m64 -Og -g"

            if find_executable( "ldd" ) is not None:
                definition_dict[ "CMAKE_SHARED_LINKER_FLAGS" ] = "-fuse-ld=lld"
                definition_dict[ "CMAKE_EXE_LINKER_FLAGS"    ] = "-fuse-ld=lld"

        cmake = CMake( self )
        cmake.configure( defs = definition_dict, source_folder = self.name )
        return cmake

    def build( self ):
        cmake = self.configure_cmake()
        cmake.build()


    def package( self ):
        cmake = self.configure_cmake()
        cmake.install()
        remove( "{}/share".format( self.package_folder ) )
        remove( "{}/lib/pkgconfig".format( self.package_folder ) )

    def package_info( self ):
        self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
        self.cpp_info.libs = tools.collect_libs(self)

