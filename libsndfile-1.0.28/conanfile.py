from conans import ConanFile, AutoToolsBuildEnvironment, tools, RunEnvironment
import os
import glob

class LibSndFile(ConanFile):
    name = "libsndfile"
    version = "1.0.28"
    license = "LGPL"
    url = "http://www.mega-nerd.com/libsndfile/"
    description = "C library for reading and writing files containing samples audio data"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    _source_subfolder = "source_subfolder"
    _autotools = None

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        tools.get("http://www.mega-nerd.com/libsndfile/files/libsndfile-{}.tar.gz".format(self.version))
        os.rename("libsndfile-%s" % self.version, self._source_subfolder)

        if self.settings.os == "Windows":
            with tools.chdir(os.path.join(self._source_subfolder, "src")):
                tools.replace_in_file("common.c", 
                    "#if HAVE_UNISTD_H", 
                    '''#undef HAVE_UNISTD_H
#if HAVE_UNISTD_H''')

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self)
            args = [
                "--without-caps", "--disable-alsa", "--disable-sqlite", "--disable-external-libs", "--disable-bow-docs",
                "--enable-shared={}".format("yes" if self.options.shared else "no"),
                "--enable-static={}".format("no" if self.options.shared else "yes"),
            ]
            self._autotools.configure(args=args, configure_dir=self._source_subfolder)
        return self._autotools

    def build(self):
        with tools.environment_append(RunEnvironment(self).vars):
            autotools = self._configure_autotools()
            autotools.make()
    def package(self):
        """Assemble the package."""
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        autotools = self._configure_autotools()
        autotools.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        for f in glob.glob(os.path.join(self.package_folder, "lib", "*.la")):
            os.remove(f)

        if self.settings.os == "Linux" and self.options.shared:
            # libsndfile.so.1.0 might be requested by libalsa on host systems.
            with tools.chdir(os.path.join(self.package_folder, "lib")):
                os.symlink("libsndfile.so.1.0.28", "libsndfile.so.1.0")

    def package_info(self):
        """Edit package info."""
        self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
        self.cpp_info.names['pkg_config'] = 'sndfile'
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["m", "dl", "pthread", "rt"]
