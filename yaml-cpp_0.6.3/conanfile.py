import os
import shutil
from conans import ConanFile, CMake, tools

class YamlCppConan(ConanFile):
    name = "yaml-cpp"
    version = "0.6.3"
    license = ""
    url = "https://yaml.org/"
    description = "YAML is a human friendly data serialization standard for all programming languages."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"
    recipe_version= "v1"

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/jbeder/yaml-cpp/archive/refs/tags/yaml-cpp-0.6.3.tar.gz")
        os.rename("yaml-cpp-yaml-cpp-0.6.3", self._source_subfolder)
        
        # Write static lib to /lib folder, not/lib/static

        os.rename(os.path.join(self._source_subfolder, "CMakeLists.txt"), os.path.join(self._source_subfolder, "CMakeLists_original.txt"))
        shutil.copy("CMakeLists.txt", os.path.join(self._source_subfolder, "CMakeLists.txt"))

    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "YAML_BUILD_SHARED_LIBS" : self.options.shared,
            "YAML_CPP_BUILD_CONTRIB": True,
            "YAML_CPP_BUILD_TESTS": False,
            "YAML_CPP_BUILD_TOOLS": True,
            "YAML_CPP_INSTALL": True,
        }

        if self.settings.os == "Linux":
            definition_dict["CMAKE_CXX_FLAGS"] = "-Wno-deprecated-declarations"

        return definition_dict

    def build(self):
        """Build the elements to package."""
        ext_dir = os.path.join(self.build_folder, 'ext')
        os.mkdir(ext_dir)

        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.build()

    def package(self):
        """Assemble the package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.install()

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
        if (not self.options.shared):
            self.cpp_info.defines = ["YamlCpp_STATIC"]
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
