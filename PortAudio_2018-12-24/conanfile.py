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
    default_options = {"shared": True, "fPIC": True}
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def build_requirements(self):
        """Define runtime requirements."""
        if self.settings.os == "Linux":
            # Build requirements because we need it to build but we do not want to use it on dev 
            # machines or include it in packages.
            self.build_requires("libalsa/1.2.2@mercseng/v0")

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")
        else:
            self.options.shared = True
            self.options["libalsa"].shared = True

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
            definition_dict["ALSA_LIBRARY"] = os.path.join(alsa_info.lib_paths[0], "libasound.{}".format("so" if self.options.shared else "a"))
            definition_dict["PA_USE_ALSA"] = True
            definition_dict["PA_USE_JACK"] = False
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
        """Build the elements to package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions())
        cmake.build()

    def package(self):
        """Assemble the package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions())
        cmake.install()

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))