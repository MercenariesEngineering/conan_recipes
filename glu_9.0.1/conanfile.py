from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class glu(ConanFile):
    name = "glu"
    version = "9.0.1"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://cgit.freedesktop.org/mesa/glu/"
    license = "SGI-B-2.0"
    settings = "os", "compiler"

    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _autotools = None


    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        if self.settings.os == "Linux":
            tools.get("https://archive.mesa3d.org/glu/{}-{}.tar.gz".format(self.name, self.version))
            os.rename("{}-{}".format(self.name, self.version), self._source_subfolder)

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools

        arguments = [
            "--prefix={}".format(self.package_folder),
            "--{}-static".format("disable" if self.options.shared else "enable"),
            "--{}-shared".format("enable" if self.options.shared else "disable")
        ]
        self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        self._autotools.configure(args=arguments, configure_dir=self._source_subfolder)
        return self._autotools

    def build(self):
        if self.settings.os == "Linux":
            builder = self._configure_autotools()
            builder.make()

    def package(self):
        if self.settings.os == "Linux":
            builder = self._configure_autotools()
            builder.install()

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.system_libs = ["Glu32"]
            self.cpp_info.include_dirs = []
            self.cpp_info.libdirs = []
        elif self.settings.os == "Linux":
            self.cpp_info.libs = ["GLU"]

    def package_id(self):
        if self.settings.os == "Windows":
            self.info.header_only()
