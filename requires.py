from conans import ConanFile

class DependenceBuilder(ConanFile):
    settings = "os", "compiler", "build_type"

    def requirements(self):
        # header-only libraries
        self.requires("GSL/2.1.0@mercseng/version-0")
        self.requires("rapidjson/1.1.0@mercseng/version-0")
        self.requires("fontstash/1.0.1@mercseng/version-0")
        self.requires("pybind11/2.5.0@mercseng/version-0")
        self.requires("spdlog-rumba/1.5.0@mercseng/version-0") # spdlog customized for Rumba

        # with dependences
        self.requires("gperf/3.1@mercseng/version-0")
        self.requires("catch2/3.0.0@mercseng/version-0")
        self.requires("zlib/1.2.11@mercseng/version-0")
        self.requires("zstd/1.4.5@mercseng/version-0")
        self.requires("bzip2/1.0.8@mercseng/version-0")
        self.requires("xz_utils/5.2.4@mercseng/version-0")
        self.requires("lzma/5.2.4@mercseng/version-0")
        self.requires("icu/64.2@mercseng/version-0")
        self.requires("boost/1.73.0@mercseng/version-0")
        self.requires("tbb/2020.02@mercseng/version-0")
        self.requires("hdf5/1.10.6@mercseng/version-0")
        self.requires("OpenEXR/2.5.1@mercseng/version-0")
        self.requires("libpng/1.6.37@mercseng/version-0")
        self.requires("libjpeg-turbo/1.5.2@mercseng/version-0")
        self.requires("libwebp/1.1.0@mercseng/version-0")
        self.requires("jbig/20160605@mercseng/version-0")
        self.requires("freetype/2.10.2_with_Harfbuzz@mercseng/version-0")
        self.requires("libtiff/4.0.9@mercseng/version-0")
        self.requires("OpenImageIO/2.1.15.0@mercseng/version-0") #freetype,
        self.requires("Alembic/1.7.12@mercseng/version-0")
        self.requires("OpenSSL/1.1.1g@mercseng/version-0")
        self.requires("libcurl/7.71.0@mercseng/version-0")
        self.requires("glu/9.0.1@mercseng/version-0")
        self.requires("glew/2.1.0@mercseng/version-0")
        self.requires("libsndfile/1.0.29@mercseng/version-0")
        self.requires("embree/3.9.0@mercseng/version-0")
        self.requires("libxml2/2.9.9@mercseng/version-0")
        self.requires("FBX/2020.0.1@mercseng/version-0")
        self.requires("materialx/1.37.1@mercseng/version-0")
        self.requires("OpenSubdiv/3.4.3@mercseng/version-0")
        self.requires("libunwind/1.3.1@mercseng/version-0")
        self.requires("expat/2.2.9@mercseng/version-0")
        self.requires("libuuid/1.0.3@mercseng/version-0")
        self.requires("libffi/3.3@mercseng/version-0")
        self.requires("gdbm/1.18.1@mercseng/version-0")
        self.requires("sqlite3/3.32.3@mercseng/version-0")
        self.requires("pcre2/10.33@mercseng/version-0")
        self.requires("ncurses/6.2@mercseng/version-0")
        self.requires("readline/8.0@mercseng/version-0")
        self.requires("cpython/3.7.7@mercseng/version-0")
        self.requires("libalsa/1.2.2@mercseng/version-0")
        self.requires("PortAudio/2018-12-24@mercseng/version-0")
        self.requires("double-conversion/3.1.5@mercseng/version-0")
        self.requires("qt/5.12.6@mercseng/version-0") # freetype, gperf, double-conversion
        self.requires("PySide2/5.12.6@mercseng/version-0")
        self.requires("OpenColorIO/1.1.1@mercseng/version-0")
        self.requires("ptex/2.3.2@mercseng/version-0")
        self.requires("USD/20.05@mercseng/version-0")
        self.requires("rumba-python/1.0.0@mercseng/version-0")
        self.requires("rumba-python-dev/1.0.0@mercseng/version-0")

    def configure(self):
        self.options["boost"].i18n_backend = "icu"
        self.options["boost"].zstd = True
        self.options["boost"].lzma = True
