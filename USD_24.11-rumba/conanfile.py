import os
import shutil
from conans import ConanFile, CMake, tools
from conans.tools import Version

class USDConan(ConanFile):
    name = "USD"
    version = "24.11-rumba"
    url = "https://graphics.pixar.com/usd/docs/index.html"
    description = "Universal scene description"
    license = "Modified Apache 2.0 License"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "with_python": [True, False], "with_qt": [True, False], "debug_symbols": [True, False], "use_imaging": [True, False]}
    default_options = "shared=True", "fPIC=True", "with_python=False", "with_qt=False", "debug_symbols=False", "use_imaging=True", "*:shared=False", "glew:shared=True", "tbb:shared=True", "*:fPIC=True"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    short_paths = True
    recipe_version = "2"
    _source_subfolder = "source_subfolder"
    

    def requirements(self):
        """Define runtime requirements."""
        self.requires("Alembic/1.7.12@mercseng/v1")
        self.requires("hdf5/1.10.6@mercseng/v0")
        self.requires("materialx/1.38.10@mercseng/v0")
        if self.options.use_imaging:
            self.requires("OpenColorIO/1.1.1@mercseng/v0")
            self.requires("OpenImageIO/2.1.15.0@mercseng/v3")
            self.requires("ptex/2.3.2@mercseng/v0")
        self.requires("OpenSubdiv/3.4.3@mercseng/v1")
        self.requires("tbb/2020.02@mercseng/v3")
        self.requires("zlib/1.2.11@mercseng/v0")
        #self.requires("glu/9.0.1@mercseng/v0")
        #self.requires("glew/2.1.0@mercseng/v0")
        if self.options.with_python:
            self.requires("cpython/3.7.7@mercseng/v1")
            self.requires("python-maquina/1.0.0@mercseng/v2")
        if self.options.with_qt:
            self.requires("qt/5.12.6@mercseng/v5")
        if self.options.with_python and self.options.with_qt:
            self.requires("PySide2/5.12.6@mercseng/v6")

    def build_requirements(self):
        self.build_requires("cpython/3.7.7@mercseng/v1")

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        hash_version = "3c49873688d556fab86540de2c97d16372e41fd6"
        tools.get("https://github.com/MercenariesEngineering/USD/archive/{}.zip".format(hash_version))
        os.rename("USD-{}".format(hash_version), self._source_subfolder)

    def _configure_cmake(self):
        """Configure CMake."""
        cmake = CMake(self)

        if self.options.debug_symbols and self.settings.build_type=="Release":
            cmake.build_type = 'RelWithDebInfo'

        definition_dict = {
            "BUILD_SHARED_LIBS": self.options.shared,
            "HDF5_USE_STATIC_LIBRARIES": not self.options["hdf5"].shared,
            "PXR_BUILD_ALEMBIC_PLUGIN": True,
            "PXR_BUILD_DOCUMENTATION": False,
            "PXR_BUILD_DRACO_PLUGIN": False,
            "PXR_BUILD_EMBREE_PLUGIN": False,
            "PXR_BUILD_EXAMPLES": False,
            "PXR_BUILD_IMAGING": self.options.use_imaging,
            "PXR_BUILD_OPENCOLORIO_PLUGIN": (self.options.use_imaging and (Version(self.deps_cpp_info["OpenColorIO"].version) < Version(2.0) or Version(self.deps_cpp_info["OpenColorIO"].version) >= Version(2.2))),       # OpenColorIO v2.0/2.1 is not compatible with this USD version.
            "PXR_BUILD_OPENIMAGEIO_PLUGIN": self.options.use_imaging,
            "PXR_BUILD_PRMAN_PLUGIN": False,
            "PXR_BUILD_PYTHON_DOCUMENTATION": False,
            "PXR_BUILD_TESTS": False,
            "PXR_BUILD_TUTORIALS": False,
            "PXR_BUILD_USD_IMAGING": self.options.use_imaging,
            "PXR_BUILD_USDVIEW": ((self.settings.os == "Linux") and self.options.use_imaging and self.options.with_python and self.options.with_qt),
            "PXR_ENABLE_GL_SUPPORT": True,
            "PXR_ENABLE_HDF5_SUPPORT": True,
            "PXR_ENABLE_MATERIALX_SUPPORT": True,
            "PXR_ENABLE_OPENVDB_SUPPORT": False,
            "PXR_ENABLE_OSL_SUPPORT": False,
            "PXR_ENABLE_PTEX_SUPPORT": True,
            "PXR_ENABLE_PYTHON_SUPPORT": self.options.with_python,
            "PXR_ENABLE_VULKAN_SUPPORT": False,
            "PXR_USE_BOOST_PYTHON": False,
            "PXR_USE_DEBUG_PYTHON": False
        }

        definition_dict["MaterialX_DIR"] = os.path.join(self.deps_cpp_info["materialx"].rootpath, "lib", "cmake", "MaterialX")

        if self.options.use_imaging:
            definition_dict["OIIO_LOCATION"] = self.deps_cpp_info["OpenImageIO"].rootpath

        if self.options.with_python:
            definition_dict["Python3_ROOT_DIR"] = self.deps_cpp_info["cpython"].rootpath
            definition_dict["Python3_FIND_STRATEGY"] = "LOCATION"
            definition_dict["Python3_FIND_REGISTRY"] = "NEVER"
            definition_dict["Python3_FIND_VIRTUALENV"] = "NEVER"

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

    def package_id(self):
        opensubdiv_lib = self.info.requires["OpenSubdiv"]
        # Changes in major and minor versions will change the Package ID but
        # only a OpenSubdiv patch won't. E.g., from 1.2.3 to 1.2.89 won't change.
        opensubdiv_lib.version = opensubdiv_lib.full_version.minor()

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
        
        if self.options.with_python:
            self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "lib", "python"))
        self.env_info.PXR_PLUGINPATH_NAME = os.path.join(self.package_folder, "plugin", "usd")
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
