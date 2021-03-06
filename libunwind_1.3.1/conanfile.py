from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration
import os


class LiunwindConan(ConanFile):
    name = "libunwind"
    version = "1.3.1"
    description = "Manipulate the preserved state of each call-frame and resume the execution at any point."
    topics = ("conan", "libunwind", "unwind", "debuggers", "exception-handling", "introspection", "setjmp")
    url = "https://github.com/bincrafters/conan-libunwind"
    homepage = "https://github.com/libunwind/libunwind"
    license = "MIT"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "coredump": [True, False], "ptrace": [True, False], "setjmp": [True, False]}
    default_options = {"shared": True, "fPIC": True, "coredump": True, "ptrace": True, "setjmp": True}
    requires = "lzma/5.2.4@mercseng/v0"
    _autotools = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def configure(self):
        if self.settings.os not in ["Linux", "FreeBSD"]:
            raise ConanInvalidConfiguration("libunwind is not supported by your platform")
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        sha256 = "43997a3939b6ccdf2f669b50fdb8a4d3205374728c2923ddc2354c65260214f8"
        tools.get("{0}/releases/download/v{1}/libunwind-{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            args = [
                "--enable-shared={}".format("yes" if self.options.shared else "no"),
                "--enable-static={}".format("no" if self.options.shared else "yes"),
                "--enable-coredump={}".format("yes" if self.options.coredump else "no"),
                "--enable-ptrace={}".format("yes" if self.options.ptrace else "no"),
                "--enable-setjmp={}".format("yes" if self.options.setjmp else "no"),
                "--disable-tests",
                "--disable-documentation"
            ]
            self._autotools.configure(configure_dir=self._source_subfolder, args=args)
        return self._autotools

    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        autotools = self._configure_autotools()
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))