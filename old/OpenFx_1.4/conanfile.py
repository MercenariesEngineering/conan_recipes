from conans import ConanFile, tools
import os

class OpenFxConan(ConanFile):
    name = "OpenFx"
    version = "1.4"
    license = ""
    url = "OpenFx/%s@pierousseau/stable" % version
    description = "An Open Plug-in API for 2D Visual Effects. http://openfx.sourceforge.net/"
    src_folder = "openfx-OFX_Release_1_4_TAG"
    generators = "cmake"

    def source(self):
        # https://github.com/ofxa/openfx/archive/OFX_Release_1_4_TAG.tar.gz
        filename = "OFX_Release_1_4_TAG.tar.gz"
        tools.download("https://github.com/ofxa/openfx/archive/%s" % filename, filename)
        tools.untargz(filename)
        os.unlink(filename)

    def package(self):
        self.copy("*.h", src="%s/include" % self.src_folder, dst="include")

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        self.cpp_info.includedirs = ['include']
