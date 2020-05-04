from conans import ConanFile, CMake, tools
import os

# Recipe based on "PortAudio/2018-12-24@tdelame/stable"
class PortAudio(ConanFile):
    description = "Free, cross-platform, open-source, audio I/O library"
    url = "www.portaudio.com"
    license = " "
    name = "PortAudio"
    version = "2018-12-24"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def requirements(self):
        """Define runtime requirements."""
        if self.settings.os == "Linux":
            self.requires("libalsa/1.1.9" )
            #self.requires("libalsa/1.2.1.2@tdelame/stable" )

    def configure(self):
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("https://app.assembla.com/spaces/portaudio/git/source/b7870b08f770c1e84b754e662c08b6942ff7d021?_format=zip",
            filename="root.zip",
            destination=self._source_subfolder)

    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "CMAKE_BUILD_TYPE": self.settings.build_type,
            "PA_BUILD_SHARED": self.options.shared,
            "PA_BUILD_STATIC": not self.options.shared,
            "PA_ENABLE_DEBUG_OUTPUT": self.settings.build_type != "Release",
            "PA_LIBNAME_ADD_SUFFIX": self.settings.os == "Windows",
            "PA_BUILD_EXAMPLES": False,
            "PA_BUILD_TESTS": False,
            "PA_DLL_LINK_WITH_STATIC_RUNTIME": False
        }

        if self.settings.os == "Linux":
            alsa_info = self.deps_cpp_info["libalsa"]
            definition_dict["ALSA_INCLUDE_DIR"] = alsa_info.include_paths[0]
            definition_dict["ALSA_LIBRARY"] = os.path.join(alsa_info.lib_paths[0], "libasound.so")
            definition_dict["PA_USE_ALSA"] = True
            definition_dict["PA_USE_JACK"] = False

            if self.settings.build_type == "Release":
                definition_dict["CMAKE_C_FLAGS"] = "-fPIC -m64 -O3"
            else:
                definition_dict["CMAKE_C_FLAGS"] = "-fPIC -m64 -Og -g"

        elif self.settings.os == "Windows":
            definition_dict["PA_USE_MME"] = True
            definition_dict["PA_USE_WDMKS_DEVICE_INFO"] = False
            definition_dict["PA_UNICODE_BUILD"] = False
            definition_dict["PA_USE_WASAPI"] = False
            definition_dict["PA_USE_WDMKS"] = False
            definition_dict["PA_USE_ASIO"] = False
            definition_dict["PA_USE_DS"] = False

        return definition_dict

    def build(self):
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.install()

        """Assemble the package."""
        #self.copy("portaudio.h", src="%s/include"%self._source_subfolder, dst="include" )
        #if self.settings.os == "Linux":
        #    libpattern = "*.so*" if self.options.shared else "*.a"
        #    self.copy("pa_linux_alsa.h", src="%s/include"%self._source_subfolder, dst="include" )
        #    self.copy(libpattern, dst ="lib", keep_path=False)
        #elif self.settings.os == "Windows":
        #    self.copy("pa_win_mme.h", src="%s/include"%self._source_subfolder, dst="include" )
        #    if self.options.shared:
        #        self.copy("*.dll", dst="lib", keep_path=False)
        #    self.copy("*.lib", dst="lib", keep_path=False)
        #self.copy(pattern="LICENSE.txt", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        """Edit package info."""
        #self.cpp_info.libs = ["portaudio"]
        self.cpp_info.libs = tools.collect_libs(self)
