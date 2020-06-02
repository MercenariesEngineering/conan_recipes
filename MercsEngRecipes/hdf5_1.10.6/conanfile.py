from conans import ConanFile, CMake, tools
import os
import shutil

class Hdf5Conan(ConanFile):
    name = "hdf5"
    version_base = "1.10"
    version_patch = "6"
    version = version_base + "." + version_patch
    license = ""
    url = "https://www.hdfgroup.org/downloads/hdf5/"
    description = "Makes possible the management of extremely large and complex data collections. https://www.hdfgroup.org"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def config_options(self):
        """fPIC is linux only."""
        if self.settings.os != "Linux":
            self.options.remove("fPIC")

    def source(self):
        """Retrieve source code."""
        #https://support.hdfgroup.org/ftp/HDF5/prev-releases/hdf5-1.10/hdf5-1.10.6/src/hdf5-1.10.6.tar.gz
        filename = "hdf5-%s.tar.gz" % self.version
        tools.get("https://support.hdfgroup.org/ftp/HDF5/prev-releases/hdf5-%s/hdf5-%s/src/%s" % (self.version_base, self.version, filename))
        os.rename("hdf5-%s" % self.version, self._source_subfolder)

        cmakelists_file = "%s/src/CMakeLists.txt" % self._source_subfolder
        with open(cmakelists_file, "a") as myfile:
            myfile.write('''
# Hulud : Force threadsafe in static library
if (HDF5_ENABLE_THREADSAFE) 
    set_property (TARGET ${HDF5_LIB_TARGET}
        APPEND PROPERTY COMPILE_DEFINITIONS
            "H5_HAVE_THREADSAFE"
    )
    if (MSVC)
        target_link_libraries (${HDF5_LIB_TARGET} PUBLIC PRIVATE INTERFACE Threads::Threads)
    endif ()
  endif ()
''')
            
        # Add a wrapper CMakeLists.txt file which initializes conan before executing the real CMakeLists.txt
        os.rename(os.path.join(self._source_subfolder, "CMakeLists.txt"), os.path.join(self._source_subfolder, "CMakeLists_original.txt"))
        shutil.copy("CMakeLists.txt", self._source_subfolder)

    def cmake_definitions(self):
        """Setup CMake definitions."""
        definition_dict = {
            "HDF5_ENABLE_THREADSAFE": True,
            "HDF5_BUILD_HL_LIB": True,
            "ALLOW_UNSUPPORTED": True,
            "HDF5_BUILD_CPP_LIB": True,
            "HDF5_BUILD_EXAMPLES": False,
            "HDF5_BUILD_TOOLS": False,
            "BUILD_TESTING": False,
            #"DISABLE_PDB_FILES": True,
        }

        return definition_dict

    def build(self):
        """Build the elements to package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.build()

    def package(self):
        """Assemble the package."""
        cmake = CMake(self)
        cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
        cmake.install()

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
