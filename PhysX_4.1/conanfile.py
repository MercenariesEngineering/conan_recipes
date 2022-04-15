from conans import ConanFile, CMake, tools
import os

class PhysixConan(ConanFile):
    name = "PhysX"
    version = "4.1"
    license = ""
    url = "https://github.com/NVIDIAGameWorks/PhysX"
    description = ""
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = ""
    exports = ["*.diff"]
    exports_sources = "CMakeLists.txt"
    generators = "cmake"

    def source(self):
        """Retrieve source code."""
        tools.get("%s/archive/refs/heads/%s.zip" % (self.url, self.version))
        if self.settings.os == "Windows":
            tools.patch(patch_file="vs2019.diff")
        else:
            tools.patch(patch_file="linux.diff")

    def build(self):
        """Build the elements to package."""
        with tools.chdir(os.path.join(self.build_folder, "PhysX-4.1", "physx")):
            if self.settings.os == "Windows":
                self.run("generate_projects.bat vc16win64")
                with tools.chdir(os.path.join(self.build_folder, "PhysX-4.1", "physx", "compiler", "vc16win64")):
                    self.run("cmake --build . --config release")
            else:
                self.run("bash generate_projects.sh linux")
                with tools.chdir(os.path.join(self.build_folder, "PhysX-4.1", "physx", "compiler", "linux-release")):
                    self.run("cmake --build .")

    def package(self):
        """Assemble the package."""
        with tools.chdir(os.path.join(self.build_folder, "PhysX-4.1", "physx", "compiler", ("vc16win64" if self.settings.os == "Windows" else "linux-release"))):
            self.run("cmake --install .")
        install_path = "PhysX-4.1/physx/install/" + ("vc15win64" if self.settings.os == "Windows" else "linux")
        self.copy("*.h", dst="include", src=install_path+"/PhysX/include")
        self.copy("*.h", dst="include", src=install_path+"/PxShared/include")
        self.copy("*.lib", dst="lib", src=install_path+"/PhysX/bin", keep_path=False)
        self.copy("*.a", dst="lib", src=install_path+"/PhysX/bin", keep_path=False)
        self.copy("*.dll", dst="bin", src=install_path+"/PhysX/bin", keep_path=False)
        self.copy("*.so", dst="bin", src=install_path+"/PhysX/bin", keep_path=False)

    def package_info(self):
        """Edit package info."""
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
        else:
            self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "bin"))
