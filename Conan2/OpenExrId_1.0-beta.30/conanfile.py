from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy, get, download, collect_libs
import os

required_conan_version = ">=2.0"

class OpenEXRIdConan(ConanFile):
    name = "openexrid"
    version = "1.0-beta.30"
    user="mercs"
    license = "MIT"
    url = "https://github.com/MercenariesEngineering/openexrid"
    description = "OpenEXR files able to isolate any object of a CG image with a perfect antialiazing "
    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        self.requires("openexr/3.2.3")
        self.requires("imath/3.1.9", transitive_headers=True)
        self.requires("openimageio/2.5.18.0")
        self.requires("re2/20240702")
        self.requires("zlib/1.3.1")

    def layout(self):
        cmake_layout(self, src_folder="src")
        
    def source(self):
        ## Download lib source for build
        #copy(self, "*", src="x:/Dev/openexrid/", dst=self.source_folder)
        #get(self, "https://github.com/MercenariesEngineering/openexrid/archive/refs/tags/v%s.tar.gz" % self.version, strip_root=True)
        get(self, "https://github.com/MercenariesEngineering/openexrid/archive/d4357b2b397bdce5c6fe554e72e6c6d6bedec932.zip", strip_root=True)
        #
        # Download pre-built plugins to package
        linux_filename = "openexrid-%s-linux.tar.gz" % self.version
        win_filename = "openexrid-%s-win64.zip" % self.version
        download(self, "https://github.com/MercenariesEngineering/openexrid/releases/download/v%s/%s" % (self.version, linux_filename), "plugins/%s" % linux_filename)
        download(self, "https://github.com/MercenariesEngineering/openexrid/releases/download/v%s/%s" % (self.version, win_filename), "plugins/%s" % win_filename)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["USE_CONAN"] = True
        tc.variables["BUILD_LIB"] = True
        tc.variables["BUILD_PLUGINS"] = False
        tc.variables["ILMBASE_LOCATION"] = self.dependencies["openexr"].cpp_info.libdirs
        tc.variables["OPENEXR_ROOT"] = self.dependencies["openexr"].cpp_info.libdirs
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        
    def package(self):
        # Package lib
        copy(self, "*.h", src=os.path.join(self.source_folder, "openexrid"), dst=os.path.join(self.package_folder, "include", "openexrid"))
        copy(self, "*.lib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        # Package pre-built plugins
        copy(self, "*", src="plugins/", dst="bin/")

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OpenExrId")
        self.cpp_info.set_property("cmake_target_name", "Mercs::OpenExrId")
        self.cpp_info.libs = collect_libs(self)
