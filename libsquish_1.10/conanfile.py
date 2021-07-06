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


class LibSquish( ConanFile ):
    name = "libsquish"
    license = " "
    description = "C library for reading and writing files containing samples audio data"
    url = "https://github.com/svn2github/libsquish"
    generators = "virtualrunenv"

    version = "1.10"
    settings = "os", "arch", "compiler", "build_type"
    options = { "shared": [ True, False ], "fPIC": [True, False] }
    default_options = "shared=False", "fPIC=True"
    _source_subfolder = "source_subfolder"
    recipe_version="v1"

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source( self ):
        sha = "c763145a30512c10450954b7a2b5b3a2f9a94e00"
        download_url = "https://github.com/svn2github/libsquish/archive/{}.zip".format( sha )
        folder_name = "libsquish-{}".format( sha )
        zipped_folder_name = "{}.zip".format( folder_name )

        tools.download( download_url, zipped_folder_name )
        tools.unzip( zipped_folder_name )
        shutil.move( folder_name, self._source_subfolder )
        os.remove( zipped_folder_name )

    def build( self ):
        cmake = CMake(self)
        #cmake.definitions['CMAKE_BUILD_TYPE'] = "Release"

        definition_dict = {
            "CMAKE_BUILD_TYPE": "Release"
        }
        if ("fPIC" in self.options.fields and self.options.fPIC == True):
            definition_dict["CMAKE_POSITION_INDEPENDENT_CODE"] = True

        cmake.configure(defs = definition_dict, source_dir=self._source_subfolder)
        cmake.build()
        cmake.install()

    def package( self ):
        #remove( "{}/share".format( self.package_folder ) )
        #remove( "{}/lib/pkgconfig".format( self.package_folder ) )
        pass

    def package_info( self ):
        self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
        self.cpp_info.libs = tools.collect_libs(self)

