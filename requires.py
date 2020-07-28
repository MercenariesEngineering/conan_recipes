from conans import ConanFile, tools
import subprocess
import sys
import os

EXPORT_HACK=False
EXPORT_TEMPLATE="""conan export {root}/{name}_{version}/conanfile.py {text}"""
ROOT_DIRECTORY=os.path.dirname(os.path.abspath(__file__))

# Some libraries are required to be shared, either to allow dynamic loading (plugins, system
# dependence, qt loading its dependences programmatically, ...) or because the static version
# does not work/suit our needs.
def shared_packages():
    res = ["cpython", "embree", "freetype", "PortAudio", "PySide2", "qt", "tbb", "USD"]
    if tools.os_info.is_linux:
        res += ["libalsa", "libunwind"]
    return res

class DependenceBuilder(ConanFile):
    settings = "os", "compiler", "build_type"
    default_options = "*:shared=False"

    def req(self, text):
        if not EXPORT_HACK:
            self.requires(text)
        else:
            modified = text.replace("@", "/")
            name, version, _, _ = modified.split('/')
            command = EXPORT_TEMPLATE.format(root=ROOT_DIRECTORY, name=name, version=version, text=text)
            if subprocess.call(command, shell=True) != 0:
                print("failed to export {}".format(text))
                sys.exit(1)

    def requirements(self):
        # header-only libraries
        self.req("GSL/2.1.0@mercseng/version-0")
        self.req("rapidjson/1.1.0@mercseng/version-0")
        self.req("fontstash/1.0.1@mercseng/version-0")
        self.req("pybind11/2.5.0@mercseng/version-0")
        self.req("spdlog-rumba/1.5.0@mercseng/version-0") # spdlog customized for Rumba

        # with dependences
        if self.settings.os == "Linux":
            self.req("catch2/3.0.0@mercseng/version-0")
        self.req("libiconv/1.15@mercseng/version-0")
        self.req("zlib/1.2.11@mercseng/version-0")
        self.req("zstd/1.4.5@mercseng/version-0")
        self.req("bzip2/1.0.8@mercseng/version-0")
        self.req("lzma/5.2.4@mercseng/version-0")
        self.req("icu/64.2@mercseng/version-0")
        self.req("boost/1.73.0@mercseng/version-0")
        self.req("tbb/2020.02@mercseng/version-0")
        self.req("hdf5/1.10.6@mercseng/version-0")
        self.req("OpenEXR/2.5.1@mercseng/version-0")
        self.req("libpng/1.6.37@mercseng/version-0")
        self.req("libjpeg-turbo/1.5.2@mercseng/version-0")
        self.req("libwebp/1.1.0@mercseng/version-0")
        self.req("jbig/20160605@mercseng/version-0")
        self.req("freetype/2.10.2_with_Harfbuzz@mercseng/version-0")
        self.req("libtiff/4.0.9@mercseng/version-0")
        self.req("OpenImageIO/2.1.15.0@mercseng/version-0") #freetype,
        self.req("Alembic/1.7.12@mercseng/version-0")
        self.req("OpenSSL/1.1.1g@mercseng/version-0")
        self.req("libcurl/7.71.0@mercseng/version-0")
        self.req("glu/9.0.1@mercseng/version-0")
        self.req("glew/2.1.0@mercseng/version-0")
        self.req("libsndfile/1.0.29@mercseng/version-0")
        self.req("embree/3.9.0@mercseng/version-0")
        self.req("libxml2/2.9.9@mercseng/version-0")
        self.req("FBX/2020.0.1@mercseng/version-0")
        self.req("materialx/1.37.1@mercseng/version-0")
        self.req("OpenSubdiv/3.4.3@mercseng/version-0")
        if self.settings.os == "Linux":
            self.req("libunwind/1.3.1@mercseng/version-0")
        self.req("expat/2.2.9@mercseng/version-0")
        self.req("libuuid/1.0.3@mercseng/version-0")
        self.req("libffi/3.3@mercseng/version-0")
        self.req("gdbm/1.18.1@mercseng/version-0")
        self.req("sqlite3/3.32.3@mercseng/version-0")
        self.req("pcre2/10.33@mercseng/version-0")
        self.req("ncurses/6.2@mercseng/version-0")
        self.req("readline/8.0@mercseng/version-0")
        self.req("cpython/3.7.7@mercseng/version-0")
        self.req("libalsa/1.2.2@mercseng/version-0")
        self.req("PortAudio/2018-12-24@mercseng/version-0")
        self.req("double-conversion/3.1.5@mercseng/version-0")
        self.req("qt/5.12.6@mercseng/version-0") # freetype, gperf, double-conversion
        self.req("PySide2/5.12.6@mercseng/version-0")
        self.req("OpenColorIO/1.1.1@mercseng/version-0")
        self.req("ptex/2.3.2@mercseng/version-0")
        self.req("USD/20.05@mercseng/version-0")
        self.req("rumba-python/1.0.0@mercseng/version-0")
        self.req("rumba-python-dev/1.0.0@mercseng/version-0")

    def configure(self):
        for name in shared_packages():
            self.options[name].shared = True

        if self.settings.os == "Linux":
            self.options["qt"].with_fontconfig = True
            self.options["boost"].i18n_backend = "icu"
        self.options["boost"].zstd = True
        self.options["boost"].lzma = True
