from conans import ConanFile, CMake, tools
import os, shutil

class tbb(ConanFile):
    name = "tbb"
    license = "Apache 2.0"
    description = "Threading Building Blocks"
    url = "https://github.com/01org/tbb"
    version = "2020.02"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=True", "fPIC=True"
    generators = "cmake"

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        # Use the repository of Wenzel Jakob that adds a CMake layer over TBB code.
        url = "https://github.com/wjakob/tbb/archive/860f9dda96a69bc99f79ad0c27450fb19b433457.zip"
        unzipped_folder = "tbb-860f9dda96a69bc99f79ad0c27450fb19b433457"
        zip_name = "tbb.zip"

        tools.download( url, zip_name )
        tools.unzip( zip_name )
        shutil.move( unzipped_folder, self.name )
        os.remove( zip_name )

        tools.replace_in_file("%s/CMakeLists.txt" % self.name,
            """tbb_static""",
            """tbb""")
        tools.replace_in_file("%s/CMakeLists.txt" % self.name,
            """tbbmalloc_static""",
            """tbbmalloc""")

        tools.replace_in_file("%s/CMakeLists.txt" % self.name,
            """  add_definitions (-DUSE_PTHREAD)""",
            """  add_definitions (-DUSE_PTHREAD)
    set(CMAKE_CXX_STANDARD_LIBRARIES "-static-libgcc -static-libstdc++ ${CMAKE_CXX_STANDARD_LIBRARIES}")""")

    def build(self):
        # TBBMALLOC PROXY is not included into this package because:
        # - it prevent crashes when it is linked to, since it should be
        # preloaded only to replace allocators.
        # - it serves a different purpose and could be then included into
        # another package if needed.
        cmake = CMake(self)

        if ("fPIC" in self.options.fields and self.options.fPIC == True):
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = True

        cmake.definitions["CMAKE_BUILD_TYPE"] = self.settings.build_type
        cmake.definitions["TBB_BUILD_SHARED"] = self.options.shared
        cmake.definitions["TBB_BUILD_STATIC"] = not self.options.shared
        cmake.definitions["TBB_BUILD_TBBMALLOC"] = True
        cmake.definitions["TBB_BUILD_TBBMALLOC_PROXY"] = False
        cmake.definitions["TBB_BUILD_TESTS"] = False
        cmake.definitions["TBB_CI_BUILD"] = False

        # Normally not necessary, but it does not cost anything to enforce it.
        if self.settings.os == "Linux" and self.settings.build_type == "Debug":
            cmake.definitions["CMAKE_CXX_FLAGS"] = "-DTBB_USE_DEBUG=2"

        cmake.configure(source_folder = self.name)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy( "*", src = "package/bin"    , dst = "bin" )
        self.copy( "*", src = "package/lib"    , dst = "lib", symlinks = True )
        self.copy( "*", src = "package/include", dst = "include", symlinks = True )
        if self.settings.os == "Linux":
            # There is a dlopen call on libtbbmalloc.so.2 in tbb but this symlink is not built
            # by cmake. The symlink is added to prevent the library loader to use the system one
            # if it exists or to fail if it doesn't.
            os.symlink(
                os.path.join(self.package_folder, "lib", "libtbbmalloc.so"),
                os.path.join(self.package_folder, "lib", "libtbbmalloc.so.2"))

    def package_info(self):
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
        self.cpp_info.libs = tools.collect_libs(self)

        if self.settings.build_type == "Debug":
            self.cpp_info.defines.append( "TBB_USE_DEBUG=1" )
        self.cpp_info.defines.append( "__TBB_NO_IMPLICIT_LINKAGE" )
