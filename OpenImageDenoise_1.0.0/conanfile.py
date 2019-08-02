from conans import ConanFile, CMake, tools
import os

# mkdir OpenImageDenoise_0.9.0
# cd OpenImageDenoise_0.9.0/
# conan new OpenImageDenoise/0.9.0 --bare
#   write this content to conanfile.py
# conan create OpenImageDenoise/0.9.0@pierousseau/stable

class OpenImageDenoiseConan(ConanFile):
    name = "OpenImageDenoise"
    version_base = "1.0"
    version_patch = "0"
    version = version_base + "." + version_patch
    license = ""
    url = "OpenImageDenoise/%s@pierousseau/stable" % version
    description = "High-Performance Denoising Library for Ray Tracing. https://openimagedenoise.github.io"
    requires = "TBB/2019_U6@pierousseau/stable"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    generators = "cmake"

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        filename = "oidn-%s.src.tar.gz" % self.version
        tools.download("https://github.com/OpenImageDenoise/oidn/releases/download/v%s/%s" % (self.version, filename), filename)
        tools.untargz(filename)
        os.unlink(filename)

        tools.replace_in_file("oidn-%s/mkl-dnn/cmake/OpenMP.cmake" % self.version,
            """else()
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fopenmp-simd")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp-simd")""",
            """""")

    def build(self):
        cmake = CMake(self)

        cmake.definitions["OIDN_STATIC_LIB"] = not self.options.shared

        if ("fPIC" in self.options.fields and self.options.fPIC == True):
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = True

        cmake.definitions["TBB_ROOT"] = self.deps_cpp_info["TBB"].rootpath

        cmake.configure(source_dir="%s/oidn-%s" % (self.source_folder, self.version))
        cmake.build()

    def package(self):
        self.copy("*.h", src="oidn-%s/include" % self.version, dst="include")
        self.copy("*.hpp", src="oidn-%s/include" % self.version, dst="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.exe", dst="bin", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("libOpenImageDenoise.so*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if (not self.options.shared) :
            self.cpp_info.defines.append("OIDN_STATIC_LIB")
