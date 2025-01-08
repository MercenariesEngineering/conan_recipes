from conans import ConanFile, CMake, tools
import os, shutil

class MaterialXConan(ConanFile):
    name = "materialx"
    version = "1.38.10"
    license = ""
    url = "https://www.materialx.org"
    description = "MaterialX is an open standard for transfer of rich material and look-development content between applications and renderers"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=True", "fPIC=True"
    generators = "cmake"
    exports_sources = "CMakeLists.txt"

    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("glu/9.0.1@mercseng/v0")

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        # https://github.com/materialx/MaterialX/archive/v1.36.3.tar.gz
        filename = "v%s.tar.gz" % self.version
        tools.download("https://github.com/AcademySoftwareFoundation/MaterialX/archive/%s" % filename, filename)
        tools.untargz(filename)
        os.unlink(filename)

        # Add a wrapper CMakeLists.txt file which initializes conan before executing the real CMakeLists.txt
        os.rename(os.path.join("MaterialX-%s" % self.version, "CMakeLists.txt"), os.path.join("MaterialX-%s" % self.version, "CMakeLists_original.txt"))
        shutil.copy("CMakeLists.txt", "MaterialX-%s" % self.version)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["MATERIALX_BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["MATERIALX_BUILD_PYTHON"] = False
        cmake.definitions["MATERIALX_BUILD_VIEWER"] = False
        cmake.definitions["MATERIALX_BUILD_DOCS"] = False
        cmake.definitions["MATERIALX_BUILD_TESTS"] = False
        cmake.definitions["MATERIALX_PYTHON_LTO"] = False
        cmake.definitions["MATERIALX_INSTALL_PYTHON"] = False
        
        # GLU is considered as a system requirement, so we must help cmake to find its include directories
        if self.settings.os == "Linux":
            var = cmake.definitions.get("CMAKE_CXX_FLAGS", "")
            for path in self.deps_cpp_info["glu"].include_paths:
                var += " -I {}".format(path)
            cmake.definitions["CMAKE_CXX_FLAGS"] = var

        cmake.configure(source_dir="MaterialX-%s" % self.version)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy( "*", src = "package/bin"    , dst = "bin")
        self.copy( "*", src = "package/lib"    , dst = "lib", symlinks = True)
        self.copy( "*", src = "package/include", dst = "include", symlinks = True)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
