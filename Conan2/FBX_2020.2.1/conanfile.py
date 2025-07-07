from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get, download, copy, collect_libs
from conan.tools.scm import Version
import os

class FBX(ConanFile):
    name = "fbx"
    version = "2020.2.1"
    user="mercs"
    description = "free, easy-to-use, C++ software development platform and API toolkit that allows application and content vendors to transfer existing content into the FBX format with minimal effort"
    url = "https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-2"
    license = "autodesk"
    settings = "os", "compiler", "build_type"
    package_type = "library"
    options = {
        "shared": [True, False]
    }
    default_options = {
        "shared": False
    }

    def config_options(self):
        if self.settings.os != "Windows":
            self.settings.remove("compiler")

    def requirements(self):
        self.requires("libxml2/2.13.8")

    def validate(self):
        if self.settings.os == "Windows" and self.settings.compiler != 'msvc':
            raise ConanInvalidConfiguration("FBX: Only Visual Studio is supported on Windows.")

    @property
    def _filename(self):
        if self.settings.os == "Linux":
            return "fbx202021_fbxsdk_linux.tar.gz"
        elif self.settings.os == "Windows":
            if self.settings.compiler.version == 190:
                return "fbx202021_fbxsdk_vs2015_win.exe"
            elif self.settings.compiler.version == 191:
                return "fbx202021_fbxsdk_vs2017_win.exe"
            elif Version(self.settings.compiler.version) >= Version("192"):
                return "fbx202021_fbxsdk_vs2019_win.exe"

    def build(self):

        if self.settings.os == "Linux":
            get(self, "https://www.autodesk.com/content/dam/autodesk/www/adn/fbx/2020-2-1/%s" % self._filename,)
            self.run('echo -e "yes\nyes\nn\n" | ./fbx202021_fbxsdk_linux {}'.format(self.build_folder))
        else:
            download(self, "https://www.autodesk.com/content/dam/autodesk/www/adn/fbx/2020-2-1/%s" % self._filename, self._filename)
            # This will trigger a privilege elevation request
            self.run('%s /S /D=%s' % (self._filename, self.build_folder))

    def package(self):
        copy(self, "License.txt", src=self.build_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "*.h", src=os.path.join(self.build_folder, "include"), dst=os.path.join(self.package_folder, "include"))

        config = "debug" if self.settings.build_type == "Debug" else "release"
        if self.settings.os == "Linux":
            copy(self, "lib/gcc/x64/%s/libfbxsdk.%s" % (config, "so" if self.options.shared else "a"), src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        else:
            if self.settings.compiler.version == 190:
                vs_folder="vs2015"
            elif self.settings.compiler.version == 191:
                vs_folder="vs2017"
            elif Version(self.settings.compiler.version) >= Version("192"):
                vs_folder="vs2019"
            if self.options.shared:
                copy(self, "lib/%s/x64/%s/libfbxsdk.lib" % (vs_folder, config), src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
                copy(self, "lib/%s/x64/%s/libfbxsdk.dll" % (vs_folder, config), src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
            else:
                runtime = "mt" if self.settings.compiler.runtime == "static" else "md"
                copy(self, "lib/%s/x64/%s/libfbxsdk-%s.lib" % (vs_folder, config, runtime), src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "FBX")
        self.cpp_info.set_property("cmake_target_name", "Mercs::FBX")
        self.cpp_info.libs = collect_libs(self)
