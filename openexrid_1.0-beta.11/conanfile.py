from conans import ConanFile, CMake, tools


class OpenexridConan(ConanFile):
    name = "openexrid"
    version = "1.0-beta.11"
    license = "MIT"
    url = ""
    description = "OpenEXR files able to isolate any object of a CG image with a perfect antialiazing "
    requires = "OpenEXR/2.2.0@Mikayex/stable"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False","OpenEXR:shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone http://github.com/MercenariesEngineering/openexrid.git")
#        self.run("cp -R C:/Users/guerilla/Code/openexrid .")
        self.run("cd openexrid")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("openexrid/CMakeLists.txt", "project (openexrid)", '''project (openexrid)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
set(OPENEXR_LOCATION ${CONAN_OPENEXR_ROOT})''')

    def build(self):
        cmake = CMake(self)
        #cmake.configure(source_dir="%s/hello" % self.source_folder)
        #cmake.build()

        # Explicit way:
        self.run('cmake %s/openexrid %s -DCMAKE_INSTALL_PREFIX="%s"' % (self.source_folder, cmake.command_line, self.package_folder))
        self.run("cmake --build . --target install %s" % cmake.build_config)
        
    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = ["openexrid"]
