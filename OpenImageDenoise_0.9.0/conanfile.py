from conans import ConanFile, CMake, tools
import os

# mkdir OpenImageDenoise_0.9.0
# cd OpenImageDenoise_0.9.0/
# conan new OpenImageDenoise/0.9.0 --bare
#   write this content to conanfile.py
# conan create OpenImageDenoise/0.9.0@pierousseau/stable

class OpenImageDenoiseConan(ConanFile):
    name = "OpenImageDenoise"
    version_base = "0.9"
    version_patch = "0"
    version = version_base + "." + version_patch
    license = ""
    url = "OpenImageDenoise/%s@pierousseau/stable" % version
    description = "High-Performance Denoising Library for Ray Tracing. https://openimagedenoise.github.io"
    requires = "tbb/20160916@lasote/vcpkg"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"


    def source(self):
        filename = "oidn-%s.src.tar.gz" % self.version
        tools.download("https://github.com/OpenImageDenoise/oidn/releases/download/v%s/%s" % (self.version, filename), filename)
        tools.untargz(filename)
        os.unlink(filename)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir="%s/oidn-%s" % (self.source_folder, self.version))
        cmake.build()

        # Explicit way:
        #self.run('cmake %s/hdf5-%s %s -DHDF5_ENABLE_THREADSAFE="ON" -DHDF5_BUILD_HL_LIB="OFF" -DHDF5_BUILD_CPP_LIB="OFF" -DHDF5_BUILD_EXAMPLES="OFF" -DHDF5_BUILD_TOOLS="OFF" -DBUILD_TESTING="OFF" -DCMAKE_INSTALL_PREFIX="%s"' % (self.source_folder, self.version, cmake.command_line, self.package_folder))
        #self.run("cmake --build . --target install %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", src="oidn-0.9.0/include", dst="include")
        self.copy("*.hpp", src="oidn-0.9.0/include", dst="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["OpenImageDenoise"]

