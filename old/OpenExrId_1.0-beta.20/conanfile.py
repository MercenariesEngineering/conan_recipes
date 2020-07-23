from conans import ConanFile, CMake, tools

class OpenEXRIdConan(ConanFile):
    name = "OpenExrId"
    version = "1.0-beta.20"
    license = "MIT"
    url = "https://github.com/MercenariesEngineering/openexrid"
    description = "OpenEXR files able to isolate any object of a CG image with a perfect antialiazing "
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False] }
    default_options = "shared=False","*:shared=False","fPIC=True"
    generators = "cmake"

    def requirements(self):
        # From our recipes :
        self.requires("zlib/1.2.11@pierousseau/stable")
        self.requires("IlmBase/2.2.0@pierousseau/stable")
        self.requires("OpenEXR/2.2.0@pierousseau/stable")
        self.requires("re2/2019-06-01@pierousseau/stable")
        self.requires("OpenImageIO/1.6.18@pierousseau/stable")

    def configure(self):
        if self.settings.os == "Linux":
            # fPIC option exists only on linux
            self.options["boost"].fPIC=True
            self.options["IlmBase"].fPIC=True
            self.options["OpenEXR"].fPIC=True
            self.options["OpenImageIO"].fPIC=True
            self.options["re2"].fPIC=True
            self.options["zlib"].fPIC=True

    def source(self):
        # Build lib from source
        self.run("git clone http://github.com/MercenariesEngineering/openexrid.git --branch v%s" % self.version)

        # Package pre-built plugins
        if self.settings.os == "Linux":
            filename = "openexrid-%s-linux.tar.gz" % self.version
        else:
            filename = "openexrid-%s-win64.zip" % self.version
        tools.download("https://github.com/MercenariesEngineering/openexrid/releases/download/v%s/%s" % (self.version, filename), "plugins/%s"%filename)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["USE_CONAN"] = True
        cmake.definitions["BUILD_LIB"] = True
        cmake.definitions["BUILD_PLUGINS"] = False

        cmake.configure(source_dir="%s/openexrid" % self.source_folder)
        cmake.build()
        
    def package(self):
        self.copy("*.h", dst="include/openexrid", src="openexrid/openexrid")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

        self.copy("*", dst="bin/", src="plugins/")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
