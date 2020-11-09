from conans import ConanFile, tools


class FbxConan(ConanFile):
    name = "FBX"
    version = "2020.0.1"
    settings = "os", "compiler", "build_type", "arch"
    description = "FBX SDK 2020.0.1"
    url = "None"
    license = "None"
    author = "None"
    topics = None

    def package(self):
        self.copy("*.h", "include")
        if self.settings.os == "Windows":
            self.copy("lib/vs2015/x64/%s/libfbxsdk.lib" % self.settings.build_type, "lib")
            self.copy("lib/vs2015/x64/%s/libfbxsdk.dll" % self.settings.build_type, "bin")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
