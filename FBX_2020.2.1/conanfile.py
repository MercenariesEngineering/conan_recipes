import os
from conans import ConanFile, tools

class FBX(ConanFile):
    description = "free, easy-to-use, C++ software development platform and API toolkit that allows application and content vendors to transfer existing content into the FBX format with minimal effort"
    url = "https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-2"
    license = "autodesk"
    version = "2020.2.1"
    settings = "os", "compiler", "build_type", "arch"
    name = "FBX"
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    def config_options(self):
        if self.settings.os != "Windows":
            self.settings.remove("compiler")
        elif self.settings.compiler != 'Visual Studio':
            raise RuntimeError("Only Visual Studio is supported on Windows.")

    def requirements(self):
        self.requires("libxml2/2.9.9@mercseng/v0")

    @property
    def _filename(self):
        if self.settings.os == "Linux":
            return "fbx202021_fbxsdk_linux.tar.gz"
        elif self.settings.os == "Windows":
            if self.settings.compiler.version == 14:
                return "fbx202021_fbxsdk_vs2015_win.exe"
            elif self.settings.compiler.version == 15:
                return "fbx202021_fbxsdk_vs2017_win.exe"
            elif self.settings.compiler.version == 16:
                return "fbx202021_fbxsdk_vs2019_win.exe"

    def source(self):
        """Retrieve source code."""
        if self.settings.os == "Linux":
            tools.get("https://www.autodesk.com/content/dam/autodesk/www/adn/fbx/2020-2-1/%s" % self._filename)
        else:
            tools.download("https://www.autodesk.com/content/dam/autodesk/www/adn/fbx/2020-2-1/%s" % self._filename, self._filename)

    def build(self):
        """Build the elements to package"""
        if self.settings.os == "Linux":
            self.run('echo -e "yes\nyes\nn\n" | ./fbx202021_fbxsdk_linux {}'.format(self.build_folder))
        else:
            self.run('%s /S /D=%s' % (self._filename, self.build_folder))

    def package(self):
        """Assemble the package."""
        self.copy(pattern="License.txt", dst="licenses")
        self.copy(pattern="*.h", src="include", dst="include")

        config = "debug" if self.settings.build_type == "Debug" else "release"
        if self.settings.os == "Linux":
            self.copy("lib/gcc/x64/%s/libfbxsdk.%s" % (config, "so" if self.options.shared else "a"), src="", dst="lib", keep_path=False)
        else:
            if self.settings.compiler.version == 14:
                vs_folder="vs2015"
            elif self.settings.compiler.version == 15:
                vs_folder="vs2017"
            elif self.settings.compiler.version == 16:
                vs_folder="vs2019"
            if self.options.shared:
                self.copy("lib/%s/x64/%s/libfbxsdk.lib" % (vs_folder, config), src="", dst="lib", keep_path=False)
                self.copy("lib/%s/x64/%s/libfbxsdk.dll" % (vs_folder, config), src="", dst="lib", keep_path=False)
            else:
                runtime = "mt" if self.settings.compiler.runtime == "MT" else "md"
                self.copy("lib/%s/x64/%s/libfbxsdk-%s.lib" % (vs_folder, config, runtime), src="", dst="lib", keep_path=False)

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
