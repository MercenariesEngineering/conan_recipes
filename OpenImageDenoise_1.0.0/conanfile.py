from conans import ConanFile, CMake, tools
import os
import shutil

class OpenImageDenoiseConan(ConanFile):
    name = "OpenImageDenoise"
    version = "1.0.0"
    description = "High-Performance Denoising Library for Ray Tracing."
    license = "Apache 2.0"
    url = "https://openimagedenoise.github.io"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=True", "fPIC=True"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("tbb/2020.02@mercseng/v0")

    def configure(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/OpenImageDenoise/oidn/releases/download/v%s/oidn-%s.src.tar.gz" % (self.version, self.version))
        os.rename("oidn-%s" % self.version, self._source_subfolder)

        tools.replace_in_file("%s/mkl-dnn/cmake/OpenMP.cmake" % self._source_subfolder,
            """else()
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fopenmp-simd")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp-simd")""",
            """""")

        if self.settings.os == "Linux":
            # force static linking of libstdc++/libgcc
            tools.replace_in_file("%s/CMakeLists.txt" % self._source_subfolder,
                """target_link_libraries(${PROJECT_NAME}
  PRIVATE
    common mkldnn
)""",
                """target_link_libraries(${PROJECT_NAME}
  PRIVATE
    "-static-libstdc++ -static-libgcc"
    common mkldnn
)""")

        # Add a wrapper CMakeLists.txt file which initializes conan before executing the real CMakeLists.txt
        os.rename(os.path.join(self._source_subfolder, "CMakeLists.txt"), os.path.join(self._source_subfolder, "CMakeLists_original.txt"))
        shutil.copy("CMakeLists.txt", self._source_subfolder)

    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "OIDN_STATIC_LIB": not self.options.shared,
            "TBB_ROOT": self.deps_cpp_info["tbb"].rootpath,
        }

        return definition_dict 

    def build(self):
        """Build the elements to package."""
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
        self.cpp_info.includedirs.append(os.path.join("include", "OpenImageDenoise"))
        if self.options.shared :
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
        else:
            self.cpp_info.defines.append("OIDN_STATIC_LIB")
