from conans import ConanFile, CMake, tools
import os

# mkdir hdf5_1.10.1
# cd hdf5_1.10.1/
# conan new hdf5/1.10.1 --bare
#   write this content to conanfile.py
# conan create hdf5/1.10.1@pierousseau/stable

class OpenimageioConan(ConanFile):
    name = "hdf5"
    version_base = "1.10"
    version_patch = "1"
    version = version_base + "." + version_patch
    license = ""
    url = "https://www.hdfgroup.org/downloads/hdf5/"
    description = "Makes possible the management of extremely large and complex data collections. https://www.hdfgroup.org"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"


    def source(self):
        filename = "hdf5-%s.tar.gz" % self.version
        tools.download("https://support.hdfgroup.org/ftp/HDF5/prev-releases/hdf5-%s/hdf5-%s/src/%s" % (self.version_base, self.version, filename), filename)
        tools.untargz(filename)
        os.unlink(filename)
        #os.rename ("hdf5-%s" % self.version, "hdf5-%s" % self.version)

        tools.replace_in_file("hdf5-%s/CMakeLists.txt" % self.version, "PROJECT (HDF5 C CXX)",
                              """PROJECT (HDF5 C CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
""")

        file = "hdf5-%s/src/CMakeLists.txt" % self.version
        with open(file, "a") as myfile:
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

    def build(self):
        cmake = CMake(self)
        #cmake.configure(source_dir="%s/hdf5-%s" % (self.source_folder, self.version))
        #cmake.build()

        # Explicit way:
        self.run('cmake %s/hdf5-%s %s -DHDF5_ENABLE_THREADSAFE="ON" -DHDF5_BUILD_HL_LIB="OFF" -DHDF5_BUILD_CPP_LIB="OFF" -DHDF5_BUILD_EXAMPLES="OFF" -DHDF5_BUILD_TOOLS="OFF" -DBUILD_TESTING="OFF" -DCMAKE_INSTALL_PREFIX="%s"' % (self.source_folder, self.version, cmake.command_line, self.package_folder))
        self.run("cmake --build . --target install %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.build_type == "Debug" :
            self.cpp_info.libs = ["libhdf5_D"]
        else :
            self.cpp_info.libs = ["libhdf5"]
