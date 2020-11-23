from conans import ConanFile, CMake, tools

class OpenEXRIdConan(ConanFile):
    name = "OpenExrId"
    version = "1.0-beta.22"
    license = "MIT"
    url = "https://github.com/MercenariesEngineering/openexrid"
    description = "OpenEXR files able to isolate any object of a CG image with a perfect antialiazing "
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False] }
    default_options = "shared=False","*:shared=False","fPIC=True"
    generators = "cmake"

    def requirements(self):
        # From our recipes :
        self.requires("OpenEXR/2.5.1@mercseng/v0")
        self.requires("OpenImageIO/2.1.15.0@mercseng/v2")
        self.requires("re2/2019-06-01@mercseng/v0")
        self.requires("zlib/1.2.11@mercseng/v0")

    def configure(self):
        if self.settings.os == "Linux":
            # fPIC option exists only on linux
            self.options["OpenEXR"].fPIC=True
            self.options["OpenImageIO"].fPIC=True
            self.options["re2"].fPIC=True
            self.options["zlib"].fPIC=True

    def source(self):
        # Build lib from source
        commit_sha = "0d72ba102c77e9f5f58d2e83f50fce503de1dda3"
        self.run("git clone https://github.com/MercenariesEngineering/openexrid.git && cd openexrid && git checkout %s" % commit_sha)

        # Package pre-built plugins
        version = self.version
        version = "1.0-beta.21"
        if self.settings.os == "Linux":
            filename = "openexrid-%s-linux.tar.gz" % version
        else:
            filename = "openexrid-%s-win64.zip" % version
        tools.download("https://github.com/MercenariesEngineering/openexrid/releases/download/v%s/%s" % (version, filename), "plugins/%s"%filename)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["USE_CONAN"] = True
        cmake.definitions["BUILD_LIB"] = True
        cmake.definitions["BUILD_PLUGINS"] = False
        cmake.definitions["ILMBASE_LOCATION"] = self.deps_cpp_info["OpenEXR"].rootpath
        cmake.definitions["OPENEXR_ROOT"] = self.deps_cpp_info["OpenEXR"].rootpath

        cmake.configure(source_dir="%s/openexrid" % self.source_folder)
        cmake.build()
        
    def package(self):
        self.copy("*.h", dst="include/openexrid", src="openexrid/openexrid")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

        self.copy("*", dst="bin/", src="plugins/")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
