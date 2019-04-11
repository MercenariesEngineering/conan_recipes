from distutils.spawn import find_executable
from conans import ConanFile, CMake, tools
import os


class PortAudio( ConanFile ):
    name = "PortAudio"
    license = " "
    description = "Free, cross-platform, open-source, audio I/O library"
    url = "www.portaudio.com"
    generators = "virtualrunenv"

    version = "2018-12-24"
    settings = "os", "build_type"
    options = { "shared": [ True, False ] }
    default_options = { "shared": True }

    def build_requirements( self ):
        if self.settings.os == "Linux":
            self.build_requires( "alsa-lib/1.0.29@tdelame/stable" )
            self.build_requires( "cmake/3.11.2@tdelame/stable" )
            self.build_requires( "ninja/1.8.2@tdelame/stable" )

    def source( self ):
        download_url = "https://app.assembla.com/spaces/portaudio/git/source/b7870b08f770c1e84b754e662c08b6942ff7d021?_format=zip"
        zipped_folder_name = "root.zip"

        tools.download( download_url, zipped_folder_name )
        tools.unzip( zipped_folder_name, self.name )
        os.remove( zipped_folder_name )

    def build( self ):
        definition_dict = {
            "CMAKE_BUILD_TYPE": self.settings.build_type,
            "PA_BUILD_SHARED": self.options.shared,
            "PA_BUILD_STATIC": not self.options.shared,
            "PA_ENABLE_DEBUG_OUTPUT": self.settings.build_type != "Release",
            "PA_LIBNAME_ADD_SUFFIX": self.settings.os == "Windows",
            "PA_BUILD_EXAMPLES": False,
            "PA_BUILD_TESTS": False,
            "PA_DLL_LINK_WITH_STATIC_RUNTIME": False
        }

        if self.settings.os == "Linux":
            alsa_info = self.deps_cpp_info[ "alsa-lib" ]
            definition_dict[ "ALSA_INCLUDE_DIR" ] = alsa_info.include_paths[ 0 ]
            definition_dict[ "ALSA_LIBRARY" ] = os.path.join( alsa_info.lib_paths[ 0 ], "libasound.so" )
            definition_dict[ "PA_USE_ALSA" ] = True
            definition_dict[ "PA_USE_JACK" ] = False

            if self.settings.build_type == "Release":
                definition_dict[ "CMAKE_C_FLAGS" ] = "-fPIC -m64 -O3"
            else:
                definition_dict[ "CMAKE_C_FLAGS" ] = "-fPIC -m64 -Og -g"

            if find_executable( "lld" ) is not None:
                definition_dict[ "CMAKE_SHARED_LINKER_FLAGS" ] = "-fuse-ld=lld"
                definition_dict[ "CMAKE_EXE_LINKER_FLAGS"    ] = "-fuse-ld=lld"

        elif self.settings.os == "Windows":
            definition_dict[ "PA_USE_MME" ] = True

            definition_dict[ "PA_USE_WDMKS_DEVICE_INFO" ] = False
            definition_dict[ "PA_UNICODE_BUILD" ] = False
            definition_dict[ "PA_USE_WASAPI" ] = False
            definition_dict[ "PA_USE_WDMKS" ] = False
            definition_dict[ "PA_USE_ASIO" ] = False
            definition_dict[ "PA_USE_DS" ] = False

        cmake = CMake( self )
        cmake.configure(
            defs = definition_dict,
            source_folder = self.name
        )
        cmake.build()


    def package( self ):
        if self.settings.os == "Linux":
            libpattern = "*.so*" if self.options.shared else "*.a"
            self.copy( "portaudio.h", src = "PortAudio/include", dst = "include" )
            self.copy( "pa_linux_alsa.h", src = "PortAudio/include", dst = "include" )
            self.copy( libpattern, dst ="lib" )
        elif self.settings.os == "Windows":
            self.copy( "portaudio.h", src = "PortAudio/include", dst = "include" )
            self.copy( "pa_win_mme.h", src = "PortAudio/include", dst = "include" )
            if self.options.shared:
                self.copy( "*.dll", dst ="lib", keep_path=False )
            self.copy( "*.lib", dst ="lib", keep_path=False )

    def package_info(self):
        self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux" and not self.options.shared:
            self.cpp_info.libs.append( "asound" )

