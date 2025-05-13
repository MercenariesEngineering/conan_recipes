import os, sys
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.files import get, chdir, rmdir, copy, replace_in_file
from conan.tools.microsoft import msvc_runtime_flag, is_msvc


class PhysxConan(ConanFile):
    name = "physx"
    version = "5.1.3"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Physx here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "release_build_type": ["profile", "release", "checked"],
        "enable_float_point_precise_math": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "release_build_type": "checked",
        "enable_float_point_precise_math": False,
    }

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "physx/*"

    def source(self):
        get(
            self,
            "https://github.com/NVIDIA-Omniverse/PhysX/archive/refs/tags/104.2-blast-5.0.0.zip",
            strip_root=True,
            sha256="7327fc6826f259be89b56e711487e681a7b82e8efed815457e5490a649290c50",
        )

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["PHYSX_ROOT_DIR"] = os.path.join(
            self.source_folder, "physx"
        ).replace("\\", "/")
        tc.cache_variables["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.get_safe("fPIC", True)
        tc.cache_variables["TARGET_BUILD_PLATFORM"] = self._get_target_build_platform()
        tc.cache_variables["PX_BUILDSNIPPETS"] = False
        tc.cache_variables["PX_CMAKE_SUPPRESS_REGENERATION"] = False
        tc.cache_variables["PX_ROOT_LIB_DIR"] = os.path.join(
            self.package_folder, "lib"
        ).replace("\\", "/")
        tc.cache_variables["PX_GENERATE_STATIC_LIBRARIES"] = not self.options.shared

        tc.cache_variables["PX_GENERATE_STATIC_LIBRARIES"] = not self.options.shared
        tc.cache_variables["PX_EXPORT_LOWLEVEL_PDB"] = False
        tc.cache_variables["PX_GENERATE_SOURCE_DISTRO"] = False
        tc.cache_variables["RESOURCE_LIBPATH_SUFFIX"] = "x64"
        tc.cache_variables["WINCRT_NDEBUG"] = "/DNDEBUG"
        
        # if is_msvc(self):
        #     tc.cache_variables["NV_USE_STATIC_WINCRT"] = "MT" in msvc_runtime_flag(self)
        #     tc.cache_variables["NV_USE_DEBUG_WINCRT"] = "d" in msvc_runtime_flag(self)
        # if self.settings.os == "Windows":
        #     tc.cache_variables["PX_COPY_EXTERNAL_DLL"] = False
        #     tc.cache_variables[
        #         "PX_FLOAT_POINT_PRECISE_MATH"
        #     ] = self.options.enable_float_point_precise_math
        #     tc.cache_variables["PX_USE_NVTX"] = False
        #     tc.cache_variables["GPU_DLL_COPIED"] = True
        #     tc.cache_variables["PX_EXE_OUTPUT_DIRECTORY_DEBUG"] = os.path.join(self.package_folder, "bin")
        #     tc.cache_variables["PX_EXE_OUTPUT_DIRECTORY_PROFILE"] = os.path.join(self.package_folder, "bin")
        #     tc.cache_variables["PX_EXE_OUTPUT_DIRECTORY_RELEASE"] = os.path.join(self.package_folder, "bin")
        #     tc.cache_variables["PX_EXE_OUTPUT_DIRECTORY_CHECKED"] = os.path.join(self.package_folder, "bin")

        tc.generate()

    def build(self):
        self._patch_sources()

        modules_dir = os.path.join(self.source_folder, "physx", "modules")
        os.mkdir(modules_dir)
        with open(os.path.join(modules_dir, "NvidiaBuildOptions.cmake"), "w") as f:
            f.write("\n")
        os.environ["PM_CMakeModules_PATH"] = modules_dir

        cmake = CMake(self)
        cmake.configure(build_script_folder="physx/compiler/public")
        cmake.build(build_type=self._get_physx_build_type())

    def _get_target_build_platform(self):
        return {
            "Windows" : "windows",
            "Linux" : "linux",
            "Macos" : "mac",
            "Android" : "android",
            "iOS" : "ios"
        }.get(str(self.settings.os))


    def _get_physx_build_type(self):
        return "checked"
        if self.settings.build_type == "Debug":
            return "debug"
        elif self.settings.build_type == "RelWithDebInfo":
            return "checked"
        elif self.settings.build_type == "Release":
            if self.options.release_build_type == "profile":
                return "profile"
            else:
                return "release"
    
    def _patch_sources(self):
        # There is no reason to force consumer of PhysX public headers to use one of
        # NDEBUG or _DEBUG, since none of them relies on NDEBUG or _DEBUG
        replace_in_file(self, os.path.join(self.source_folder, "physx", "include", "foundation", "PxPreprocessor.h"),
                              "#error Exactly one of NDEBUG and _DEBUG needs to be defined!",
                              "// #error Exactly one of NDEBUG and _DEBUG needs to be defined!")

        physx_source_cmake_dir = os.path.join(self.source_folder, "physx", "source", "compiler", "cmake")

        # Remove global and specifics hard-coded PIC settings
        # (conan's CMake build helper properly sets CMAKE_POSITION_INDEPENDENT_CODE
        # depending on options)
        replace_in_file(self, os.path.join(physx_source_cmake_dir, "CMakeLists.txt"),
                              "SET(CMAKE_POSITION_INDEPENDENT_CODE ON)", "")
        for cmake_file in (
            "FastXml.cmake",
            "LowLevel.cmake",
            "LowLevelAABB.cmake",
            "LowLevelDynamics.cmake",
            "PhysX.cmake",
            "PhysXCharacterKinematic.cmake",
            "PhysXCommon.cmake",
            "PhysXCooking.cmake",
            "PhysXExtensions.cmake",
            "PhysXFoundation.cmake",
            "PhysXPvdSDK.cmake",
            "PhysXTask.cmake",
            "PhysXVehicle.cmake",
            "SceneQuery.cmake",
            "SimulationController.cmake",
        ):
            target, _ = os.path.splitext(os.path.basename(cmake_file))
            replace_in_file(self, os.path.join(physx_source_cmake_dir, cmake_file),
                                  "SET_TARGET_PROPERTIES({} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)".format(target),
                                  "")

        # No error for compiler warnings
        replace_in_file(self, os.path.join(physx_source_cmake_dir, "windows", "CMakeLists.txt"),
                              "/WX", "")
        replace_in_file(self, os.path.join(physx_source_cmake_dir, "linux", "CMakeLists.txt"),
                                "-Werror", "")
        replace_in_file(
            self,
            os.path.join(physx_source_cmake_dir, "windows", "CMakeLists.txt"),
            "FILE(COPY",
            "#FILE(COPY",
        )

    def package(self):
        cmake = CMake(self)
        cmake.install(build_type=self._get_physx_build_type())
        install_dir = os.path.join(self.package_folder, "lib", self._get_physx_build_type())
        copy(
            self,
            pattern="*.a",
            src=install_dir,
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )
        copy(
            self,
            pattern="*.so",
            src=install_dir,
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )
        copy(
            self,
            pattern="*.lib",
            src=install_dir,
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )
        copy(
            self,
            pattern="*.dll",
            src=install_dir,
            dst=os.path.join(self.package_folder, "bin"),
            keep_path=False,
        )
        copy(
            self,
            pattern="*.dylib",
            src=install_dir,
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )
        rmdir(self, install_dir)

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "PhysX")

        # PhysXFoundation
        self.cpp_info.components["physxfoundation"].set_property(
            "cmake_target_name", "PhysX::PhysXFoundation"
        )
        self.cpp_info.components["physxfoundation"].libs = ["PhysXFoundation"]
        if self.settings.os == "Linux":
            self.cpp_info.components["physxfoundation"].system_libs = [
                "m",
                "pthread",
                "rt",
            ]
        elif self.settings.os == "Android":
            self.cpp_info.components["physxfoundation"].system_libs = ["log"]

        # PhysXCommon
        self.cpp_info.components["physxcommon"].set_property(
            "cmake_target_name", "PhysX::PhysXCommon"
        )
        self.cpp_info.components["physxcommon"].libs = ["PhysXCommon"]
        if self.settings.os == "Linux":
            self.cpp_info.components["physxcommon"].system_libs = ["m"]
        self.cpp_info.components["physxcommon"].requires = ["physxfoundation"]

        # PhysXPvdSDK
        self.cpp_info.components["physxpvdsdk"].set_property(
            "cmake_target_name", "PhysX::PhysXPvdSDK"
        )
        self.cpp_info.components["physxpvdsdk"].libs = ["PhysXPvdSDK"]
        self.cpp_info.components["physxpvdsdk"].requires = ["physxfoundation"]

        # PhysX
        self.cpp_info.components["physxmain"].set_property(
            "cmake_target_name", "PhysX::PhysX"
        )
        self.cpp_info.components["physxmain"].libs = ["PhysX"]
        if self.settings.os == "Linux":
            self.cpp_info.components["physxmain"].system_libs = ["m"]
            if self.settings.arch == "x86_64":
                self.cpp_info.components["physxmain"].system_libs.append("dl")
        self.cpp_info.components["physxmain"].requires = [
            "physxpvdsdk",
            "physxcommon",
            "physxfoundation",
        ]

        # PhysXTask
        if self.settings.os == "Windows" and self.options.shared:
            self.cpp_info.components["physxtask"].set_property(
                "cmake_target_name", "PhysX::PhysXTask"
            )
            self.cpp_info.components["physxtask"].libs = ["PhysXTask"]
            self.cpp_info.components["physxmain"].requires.append("physxtask")

        # PhysXCharacterKinematic
        self.cpp_info.components["physxcharacterkinematic"].set_property(
            "cmake_target_name", "PhysX::PhysXCharacterKinematic"
        )
        self.cpp_info.components["physxcharacterkinematic"].libs = [
            "PhysXCharacterKinematic"
        ]
        self.cpp_info.components["physxcharacterkinematic"].requires = [
            "physxfoundation",
            "physxcommon",
            "physxextensions",
        ]

        # PhysXCooking
        self.cpp_info.components["physxcooking"].set_property(
            "cmake_target_name", "PhysX::PhysXCooking"
        )
        self.cpp_info.components["physxcooking"].libs = ["PhysXCooking"]
        if self.settings.os == "Linux":
            self.cpp_info.components["physxcooking"].system_libs = ["m"]
        self.cpp_info.components["physxcooking"].requires = [
            "physxfoundation",
            "physxcommon",
        ]

        # PhysXVehicle
        self.cpp_info.components["physxvehicle"].set_property(
            "cmake_target_name", "PhysX::PhysXVehicle"
        )
        self.cpp_info.components["physxvehicle"].libs = ["PhysXVehicle"]
        self.cpp_info.components["physxvehicle"].requires = [
            "physxfoundation",
            "physxpvdsdk",
            "physxextensions",
        ]

        # PhysXExtensions
        self.cpp_info.components["physxextensions"].set_property(
            "cmake_target_name", "PhysX::PhysXExtensions"
        )
        self.cpp_info.components["physxextensions"].libs = ["PhysXExtensions"]
        self.cpp_info.components["physxextensions"].requires = [
            "physxfoundation",
            "physxpvdsdk",
            "physxmain",
            "physxcommon",
        ]

        # TODO: remove in conan v2 once cmake_find_package* removed
        self.cpp_info.names["cmake_find_package"] = "PhysX"
        self.cpp_info.names["cmake_find_package_multi"] = "PhysX"

        self.cpp_info.components["physxfoundation"].names[
            "cmake_find_package"
        ] = "PhysXFoundation"
        self.cpp_info.components["physxfoundation"].names[
            "cmake_find_package_multi"
        ] = "PhysXFoundation"
        self.cpp_info.components["physxcommon"].names[
            "cmake_find_package"
        ] = "PhysXCommon"
        self.cpp_info.components["physxcommon"].names[
            "cmake_find_package_multi"
        ] = "PhysXCommon"
        self.cpp_info.components["physxpvdsdk"].names[
            "cmake_find_package"
        ] = "PhysXPvdSDK"
        self.cpp_info.components["physxpvdsdk"].names[
            "cmake_find_package_multi"
        ] = "PhysXPvdSDK"
        self.cpp_info.components["physxmain"].names["cmake_find_package"] = "PhysX"
        self.cpp_info.components["physxmain"].names[
            "cmake_find_package_multi"
        ] = "PhysX"
        if self.settings.os == "Windows" and self.options.shared:
            self.cpp_info.components["physxtask"].names[
                "cmake_find_package"
            ] = "PhysXTask"
            self.cpp_info.components["physxtask"].names[
                "cmake_find_package_multi"
            ] = "PhysXTask"
        self.cpp_info.components["physxcharacterkinematic"].names[
            "cmake_find_package"
        ] = "PhysXCharacterKinematic"
        self.cpp_info.components["physxcharacterkinematic"].names[
            "cmake_find_package_multi"
        ] = "PhysXCharacterKinematic"
        self.cpp_info.components["physxcooking"].names[
            "cmake_find_package"
        ] = "PhysXCooking"
        self.cpp_info.components["physxcooking"].names[
            "cmake_find_package_multi"
        ] = "PhysXCooking"
        self.cpp_info.components["physxvehicle"].names[
            "cmake_find_package"
        ] = "PhysXVehicle"
        self.cpp_info.components["physxvehicle"].names[
            "cmake_find_package_multi"
        ] = "PhysXVehicle"
        self.cpp_info.components["physxextensions"].names[
            "cmake_find_package"
        ] = "PhysXExtensions"
        self.cpp_info.components["physxextensions"].names[
            "cmake_find_package_multi"
        ] = "PhysXExtensions"
