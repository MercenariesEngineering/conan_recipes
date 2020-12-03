import os
import shutil
from conans import ConanFile, CMake, tools
from conans.tools import Version

class USDConan(ConanFile):
    name = "USD"
    version = "20.11-rumba"
    url = "https://graphics.pixar.com/usd/docs/index.html"
    description = "Universal scene description"
    license = "Modified Apache 2.0 License"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "debug_symbols": [True, False]}
    default_options = "shared=True", "fPIC=True", "debug_symbols=False", "*:shared=False", "tbb:shared=True", "*:fPIC=True", "boost:i18n_backend=icu", "boost:zstd=True", "boost:lzma=True"
    generators = "cmake"
    short_paths = True
    recipe_version = "1"
    _source_subfolder = "source_subfolder"

    def requirements(self):
        """Define runtime requirements."""
        self.requires("Alembic/1.7.12@mercseng/v1")
        self.requires("boost/1.73.0@mercseng/v2")
        self.requires("hdf5/1.10.6@mercseng/v0")
        self.requires("materialx/1.37.1@mercseng/v0")
        self.requires("OpenColorIO/1.1.1@mercseng/v0")
        self.requires("OpenImageIO/2.1.15.0@mercseng/v2")
        self.requires("ptex/2.3.2@mercseng/v0")
        self.requires("OpenSubdiv/3.4.3@mercseng/v1")
        self.requires("tbb/2020.02@mercseng/v2")
        self.requires("zlib/1.2.11@mercseng/v0")
        self.requires("glu/9.0.1@mercseng/v0")
        self.requires("glew/2.1.0@mercseng/v0")
        self.requires("cpython/3.7.7@mercseng/v0")
        self.requires("qt/5.12.6@mercseng/v0")
        self.requires("PySide2/5.12.6@mercseng/v1")
        self.requires("rumba-python/1.0.0@mercseng/v1")


    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        hash_version = "406d22e3b53649e3975ebf75dc969286aa3e3f12"
        tools.get("https://github.com/tdelame/USD/archive/{}.zip".format(hash_version))
        os.rename("USD-{}".format(hash_version), self._source_subfolder)
 
    def _configure_cmake(self):
        """Configure CMake."""
        cmake = CMake(self)

        if self.options.debug_symbols and self.settings.build_type=="Release":
            cmake.build_type = 'RelWithDebInfo'

        definition_dict = {
            "BUILD_SHARED_LIBS":self.options.shared,
        }

        # Boost default find package is not great... give it a hand.
        #boost_libs = ['atomic', 'chrono', 'container', 'context', 'contract', 'coroutine', 'date_time', 'exception', 'fiber', 'filesystem', 'graph', 'graph_parallel', 'iostreams', 'locale', 'log', 'math', 'mpi', 'program_options', 'python', 'random', 'regex', 'serialization', 'stacktrace', 'system', 'test', 'thread', 'timer', 'type_erasure', 'wave']
        boost_libs = ['program_options']
        for searched_lib in boost_libs:
            for built_lib in self.deps_cpp_info["boost"].libs:
                if built_lib.find(searched_lib) != -1:
                    definition_dict["Boost_%s_FOUND" % searched_lib.upper()] = True
                    definition_dict["Boost_%s_LIBRARY" % searched_lib.upper()] = built_lib

        cmake.configure(defs = definition_dict, source_folder = self._source_subfolder)
        return cmake

    def build(self):
        """Build the elements to package."""
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        """Assemble the package."""
        cmake = self._configure_cmake()
        cmake.install()

        if self.settings.os == "Linux":
            # fix shebangs
            python_shebang = "#!/usr/bin/env python3.7\n"
            bin_directory = os.path.join(self.package_folder, "bin")
            if os.path.exists(bin_directory):
                with tools.chdir(bin_directory):
                    for filename in [entry for entry in os.listdir(".") if os.path.isfile(entry)]:
                        try:
                            with open(filename, "r") as infile:
                                lines = infile.readlines()
                            
                            if len(lines[0]) > 2 and lines[0].startswith("#!"):
                                lines[0] = python_shebang
                                with open(filename, "w") as outfile:
                                    outfile.writelines(lines)
                        except:
                            pass


    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.bindirs = ["lib", "bin"] # This will put "lib" folder in the path, which we need to find the plugins.
        self.cpp_info.defines = ["NOMINMAX", "YY_NO_UNISTD_H"]
        
        if self.settings.build_type == "Debug":
            self.cpp_info.defines.append("BUILD_OPTLEVEL_DEV")
        
        if not self.options.shared:
            self.cpp_info.defines.append("PXR_STATIC=1")
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))    # executables
                self.env_info.PATH.append(os.path.join( self.package_folder, "lib"))    # DLLs
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
        
        self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "lib", "python"))
        self.env_info.PXR_PLUGINPATH_NAME = os.path.join(self.package_folder, "plugin", "usd")
