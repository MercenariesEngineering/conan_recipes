from conans.errors import ConanInvalidConfiguration
from conans import ConanFile, tools
import os


class Ninja(ConanFile):
    name = "ninja"
    version = "1.8.2"
    url = "https://ninja-build.org/"
    license = "Apache 2"
    description = "small build system with a focus on speed"
    settings = "os"
    generators = "virtualrunenv"

    def source( self ):
        if self.settings.os == "Windows":
            zip_name = "{}-win.zip".format( self.name )
        elif self.settings.os == "Linux":
            zip_name = "{}-linux.zip".format( self.name )
        else:
            raise ConanInvalidConfiguration( "no ninja package for your plateform" )
        tools.download( 
            "https://github.com/ninja-build/ninja/releases/download/v{}/{}".format( 
                self.version, zip_name ), zip_name )
        tools.unzip( zip_name )
        os.remove( zip_name )
        os.chmod( "ninja", 0o555 )

    def package(self):
        self.copy( "ninja", src = "", dst = "bin" )

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
