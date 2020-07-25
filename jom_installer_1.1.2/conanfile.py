from conans import ConanFile, tools
import os


class JomInstallerConan(ConanFile):
    name = "jom_installer"
    version = "1.1.2"
    description = "jom is a clone of nmake to support the execution of multiple independent commands in parallel"
    url = "https://github.com/bincrafters/conan-jom_installer"
    homepage = "http://wiki.qt.io/Jom"
    license = "GPL-3.0"

    exports = ["LICENSE.md"]

    settings = {"os" : ["Windows"]}

    def source(self):
        tools.get("http://download.qt.io/official_releases/jom/jom_%s.zip" % self.version.replace('.', '_'))

    def package(self):
        self.copy("*.exe", dst="bin", src="")
        
    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))