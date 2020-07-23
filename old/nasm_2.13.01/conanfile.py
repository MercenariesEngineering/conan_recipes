import os
from conans import ConanFile
from conans.client import tools
from conans import __version__ as conan_version

class NasmConan(ConanFile):
    name = "nasm"
    version = "2.13.01"
    license = "BSD-2-Clause"
    url = "https://github.com/lasote/conan-nasm-installer"
    settings = "os", "arch", "compiler", "build_type"
    build_policy = "missing"
    description="Nasm for windows. Useful as a build_require."

    def configure(self):
        if self.settings.os != "Windows":
            raise Exception("Only windows supported for nasm")

    @property
    def nasm_folder_name(self):
        return "nasm-%s" % self.version

    def build(self):
        def get_version(suffix):
            nasm_zip_name = "%s-%s.zip" % (self.nasm_folder_name, suffix)
            tools.download("http://www.nasm.us/pub/nasm/releasebuilds/"
                           "%s/%s/%s" % (self.version, suffix, nasm_zip_name), nasm_zip_name)
            self.output.warn("Downloading nasm: "
                             "http://www.nasm.us/pub/nasm/releasebuilds"
                             "/%s/%s/%s" % (self.version, suffix, nasm_zip_name))
            tools.unzip(nasm_zip_name)
            os.unlink(nasm_zip_name)

        get_version("win32" if self.settings.arch == "x86" else "win64")

    def package(self):
        self.copy("*", dst="", keep_path=True)
        self.copy("license*", dst="", src=self.nasm_folder_name, keep_path=False, ignore_case=True)

    def package_info(self):
        self.output.info("Using %s version" % self.nasm_folder_name)
        self.env_info.path.append(os.path.join(self.package_folder, self.nasm_folder_name))
