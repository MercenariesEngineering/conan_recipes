from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy, get, download, collect_libs, export_conandata_patches, apply_conandata_patches, rm, rmdir, replace_in_file
from conan.tools.scm import Version
import os

required_conan_version = ">=2.0"

# Recipe inspired by https://github.com/AlexRamallo/openusd-conan

class USDConan(ConanFile):
    name = "usd"
    user="mercs"
    url = "https://graphics.pixar.com/usd/docs/index.html"
    description = "Universal scene description"
    license = "Modified Apache 2.0 License"
    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_python": [True, False],
        "with_qt": [True, False],
        "debug_symbols": [True, False],
        "use_imaging": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_python": False,
        "with_qt": False,
        "debug_symbols": False,
        "use_imaging": True,
    }

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        self.requires("alembic/1.8.6")
        self.requires("materialx/1.38.10")
        self.requires("imath/3.1.9")
        if self.options.use_imaging:
            self.requires("opencolorio/2.3.1")
            self.requires("openimageio/2.5.18.0")
            self.requires("ptex/2.4.2")
            self.requires("opensubdiv/3.5.0", package_id_mode="minor_mode") # Changes in major and minor versions will change the Package ID but simply a OpenSubdiv patch won't. e.g., from 1.2.3 to 1.2.89 won't change.
        self.requires("onetbb/2020.3.3")

        #self.requires("glu/system")
        if self.settings.os == 'Linux':
            self.requires("opengl/system")
        #self.requires("glew/2.2.0")

        if self.options.with_python:
            self.requires("cpython/3.10.14")
            #self.requires("python-maquina/1.0.0@mercseng/v2")
        if self.options.with_qt:
            self.requires("qt/5.15.16")
        if self.options.with_python and self.options.with_qt:
            self.requires("PySide2/5.15.6")

    def build_requirements(self):
        self.tool_requires("cpython/3.10.14", options={"shared": True})

    def validate(self):
        if self.options.use_imaging:
            if not self.dependencies["opensubdiv"].options.with_tbb:
                raise ConanInvalidConfiguration("openusd requires -o opensubdiv/*:with_tbb=True")
            if not self.dependencies["opensubdiv"].options.with_opengl:
                raise ConanInvalidConfiguration("openusd requires -o opensubdiv/*:with_opengl=True")

    def layout(self):
        cmake_layout(self, src_folder="src")
        
    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def _patch_sources_cmake(self):
        apply_conandata_patches(self)

        # Let's not build usdBakeMtlx, until we need it and solve an openGL linking problem
        replace_in_file(self, os.path.join(self.source_folder, "pxr", "usdImaging", "bin", "CMakeLists.txt"), "add_subdirectory(usdBakeMtlx)", "")

        # OpenUSD uses these cmake files to find third party libraries, but the goal is to provide
        # those libraries via conan, so we delete them and make sure to produce the correct cache
        # variables/target aliases that OpenUSD expects from these modules
        files_to_delete = [
            'FindAlembic.cmake',
            'FindAnimX.cmake',
            'FindDraco.cmake',
            'FindEmbree.cmake',
            'FindJinja2.cmake',
            'FindOpenColorIO.cmake',
            'FindOpenEXR.cmake',
            'FindOpenImageIO.cmake',
            'FindOpenSubdiv.cmake',
            'FindOpenVDB.cmake',
            'FindOSL.cmake',
            'FindPTex.cmake',
            # 'FindPyOpenGL.cmake',
            # 'FindPySide.cmake',
            'FindRenderman.cmake',
            'FindTBB.cmake',
        ]
        for file in files_to_delete:
            os.remove(os.path.join(self.source_folder, "cmake", "modules", file))

    def generate(self):
        tc = CMakeToolchain(self)
        deps = CMakeDeps(self)

        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["PXR_BUILD_ALEMBIC_PLUGIN"] = True
        tc.variables["PXR_BUILD_DOCUMENTATION"] = False
        tc.variables["PXR_BUILD_DRACO_PLUGIN"] = False
        tc.variables["PXR_BUILD_EMBREE_PLUGIN"] = False
        tc.variables["PXR_BUILD_EXAMPLES"] = False
        tc.variables["PXR_BUILD_IMAGING"] = self.options.use_imaging
        if self.options.use_imaging:
            ocio_version = Version(self.dependencies["opencolorio"].ref.version)
            tc.variables["PXR_BUILD_OPENCOLORIO_PLUGIN"] = (ocio_version < Version(2.0) or ocio_version >= Version(2.2)),       # OpenColorIO v2.0/2.1 is not compatible with this USD version
        else:
            tc.variables["PXR_BUILD_OPENCOLORIO_PLUGIN"] = False
        tc.variables["PXR_BUILD_OPENIMAGEIO_PLUGIN"] = self.options.use_imaging
        tc.variables["PXR_BUILD_PRMAN_PLUGIN"] = False
        tc.variables["PXR_BUILD_PYTHON_DOCUMENTATION"] = False
        tc.variables["PXR_BUILD_TESTS"] = False
        tc.variables["PXR_BUILD_TUTORIALS"] = False
        tc.variables["PXR_BUILD_USD_IMAGING"] = self.options.use_imaging
        tc.variables["PXR_BUILD_USDVIEW"] = ((self.settings.os == "Linux") and self.options.use_imaging and self.options.with_python and self.options.with_qt)
        tc.variables["PXR_ENABLE_GL_SUPPORT"] = True
        tc.variables["PXR_ENABLE_MATERIALX_SUPPORT"] = True
        tc.variables["PXR_ENABLE_OPENVDB_SUPPORT"] = False
        tc.variables["PXR_ENABLE_OSL_SUPPORT"] = False
        tc.variables["PXR_ENABLE_PTEX_SUPPORT"] = True
        tc.variables["PXR_ENABLE_PYTHON_SUPPORT"] = self.options.with_python
        tc.variables["PXR_ENABLE_VULKAN_SUPPORT"] = False
        tc.variables["PXR_USE_BOOST_PYTHON"] = False
        tc.variables["PXR_USE_DEBUG_PYTHON"] = False
        
        tc.variables['ALEMBIC_LIBRARIES'] = self.dependencies["alembic"].cpp_info.get_property('cmake_target_name')
        tc.variables['ALEMBIC_FOUND'] = True

        tc.variables['TBB_tbb_LIBRARY'] = "TBB::tbb"

        if self.options.use_imaging:
            tc.variables['PTEX_LIBRARY'] = self.dependencies["ptex"].cpp_info.get_property('cmake_target_name')
            deps.set_property("opencolorio", "cmake_additional_variables_prefixes", ["OCIO"])
            deps.set_property("openimageio", "cmake_additional_variables_prefixes", ["OIIO"])

            deps.set_property("opensubdiv", "cmake_additional_variables_prefixes", ["OPENSUBDIV"]) # capitalize the name
            osd_info = self.dependencies["opensubdiv"].cpp_info
            tc.variables['OPENSUBDIV_OSDCPU_LIBRARY'] = osd_info.components['osdcpu'].get_property('cmake_target_name')
            tc.variables['OPENSUBDIV_OSDGPU_LIBRARY'] = osd_info.components['osdgpu'].get_property('cmake_target_name')

        if self.dependencies["alembic"].options.with_hdf5:
            tc.variables["PXR_ENABLE_HDF5_SUPPORT"] = True
            tc.variables["HDF5_USE_STATIC_LIBRARIES"] = not self.dependencies["hdf5"].options.shared
        else:
            tc.variables["PXR_ENABLE_HDF5_SUPPORT"] = False

        tc.variables['MATERIALX_LIBRARIES'] = self.dependencies["materialx"].cpp_info.get_property('cmake_target_name')
        mtx = self.dependencies["materialx"]
        mtx_comps = {
            'MaterialXCore',
            'MaterialXFormat',
            'MaterialXGenGlsl',
            'MaterialXGenMdl',
            'MaterialXGenMsl',
            'MaterialXGenOsl',
            'MaterialXGenShader',
            'MaterialXRender',
            'MaterialXRenderGlsl',
            'MaterialXRenderHw',
            'MaterialXRenderOsl',
            'MaterialXRenderMsl'
        }
        for comp in mtx_comps:
            if comp in mtx.cpp_info.components.keys():
                info = mtx.cpp_info.components[comp]
                info.set_property('cmake_target_aliases', [comp])

        #tc.variables["ALEMBIC_FOUND"] = True
        #tc.variables["Alembic_DIR"] = self.dependencies["alembic"].package_folder.replace('\\', '\\\\')

        #tc.variables["TBB_DIR"] = self.dependencies["onetbb"].package_folder.replace('\\', '\\\\')
        #tc.variables["MaterialX_DIR"] = self.dependencies["materialx"].package_folder.replace('\\', '\\\\')

        #tc.variables["MaterialX_DIR"] = os.path.join(self.dependencies["materialx"].package_folder, "lib", "cmake", "MaterialX")
        #
        #if self.options.use_imaging:
        #    tc.variables["OIIO_LOCATION"] = self.dependencies["OpenImageIO"].package_folder
        #
        #if self.options.with_python:
        #    tc.variables["Python3_ROOT_DIR"] = self.dependencies["cpython"].package_folder
        #    tc.variables["Python3_FIND_STRATEGY"] = "LOCATION"
        #    tc.variables["Python3_FIND_REGISTRY"] = "NEVER"
        #    tc.variables["Python3_FIND_VIRTUALENV"] = "NEVER"

        tc.generate()

        #deps.set_property("alembic", "cmake_target_name", "ALEMBIC")
        #deps.set_property("materialx", "cmake_target_name", "MATERIALX")
        #deps.set_property("alembic", "cmake_find_mode", "module")
        #deps.set_property("onetbb", "cmake_find_mode", "module")
        deps.generate()

    def build(self):
        self._patch_sources_cmake()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        
    def package(self):
        copy(self, "LICENSE.txt", self.source_folder, os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

        rm(self, "pxrConfig.cmake", self.package_folder)
        rmdir(self, os.path.join(self.package_folder, "cmake"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "USD")
        self.cpp_info.set_property("cmake_target_name", "Mercs::USD")

        self.cpp_info.defines = ["NOMINMAX", "YY_NO_UNISTD_H"]
        if self.settings.build_type == "Debug":
            self.cpp_info.defines.append("BUILD_OPTLEVEL_DEV")
        if not self.options.shared:
            self.cpp_info.defines.append("PXR_STATIC=1")
        
        if self.options.with_python:
            self.runenv_info.append_path("PYTHONPATH", os.path.join(self.package_folder, "lib", "python"))
        self.runenv_info.append_path("PXR_PLUGINPATH_NAME", os.path.join(self.package_folder, "plugin", "usd"))

        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("m")
            self.cpp_info.system_libs.append("pthread")
            self.cpp_info.system_libs.append("dl")

        #self.cpp_info.libs = collect_libs(self)
        self.tbb_libs = ['onetbb::onetbb']
        self.mtlx_prefix = "materialx::"
        if self.options.with_python:
            self.python_libs = ["python", "cpython::cpython"]
        else:
            self.python_libs = []

        #############################
        # AFTER BUILD, SEE FILE $CONAN_HOME\p\b\usdxxxxxx\b\build\pxrTargets.cmake
        # to modify per-component link options below
        #############################

        if self.options.with_python:
            # boost
            self.cpp_info.components["boost"].requires = []
            self.cpp_info.components["boost"].libs = ['usd_arch']
            # arch
            self.cpp_info.components["python"].requires = ['boost', 'cpython::cpython']
            self.cpp_info.components["python"].libs = ['usd_python']

        # arch
        self.cpp_info.components["arch"].requires = []
        self.cpp_info.components["arch"].libs = ['usd_arch']
        if self.settings.os == 'Linux':
            self.cpp_info.components["arch"].system_libs = ['m', 'dl']
        # tf
        self.cpp_info.components["tf"].requires = ['arch'] + self.python_libs + self.tbb_libs
        self.cpp_info.components["tf"].libs = ['usd_tf']
        # gf
        self.cpp_info.components["gf"].requires = ['arch', 'tf']
        self.cpp_info.components["gf"].libs = ['usd_gf']
        # gf
        self.cpp_info.components["pegtl"].requires = ['arch']
        self.cpp_info.components["pegtl"].libs = ['usd_pegtl']
        # js
        self.cpp_info.components["js"].requires = ['tf']
        self.cpp_info.components["js"].libs = ['usd_js']
        # trace
        self.cpp_info.components["trace"].requires = ['arch', 'js', 'tf'] + self.python_libs + self.tbb_libs
        self.cpp_info.components["trace"].libs = ['usd_trace']
        # work
        self.cpp_info.components["work"].requires = ['tf', 'trace'] + self.tbb_libs
        self.cpp_info.components["work"].libs = ['usd_work']
        # plug
        self.cpp_info.components["plug"].requires = ['arch', 'tf', 'js', 'trace', 'work'] + self.python_libs + self.tbb_libs
        self.cpp_info.components["plug"].libs = ['usd_plug']
        # vt
        self.cpp_info.components["vt"].requires = ['arch', 'tf', 'gf', 'trace'] + self.python_libs + self.tbb_libs
        self.cpp_info.components["vt"].libs = ['usd_vt']
        # ts
        # skipped
        self.cpp_info.components["ts"].requires = ['vt', 'gf', 'tf']
        self.cpp_info.components["ts"].libs = ['usd_ts']
        # ar
        self.cpp_info.components["ar"].requires = ['arch', 'js', 'tf', 'plug', 'vt'] + self.python_libs + self.tbb_libs
        self.cpp_info.components["ar"].libs = ['usd_ar']
        # kind
        self.cpp_info.components["kind"].requires = ['tf', 'plug']
        self.cpp_info.components["kind"].libs = ['usd_kind']
        # sdf
        self.cpp_info.components["sdf"].requires = ['arch', 'tf', 'gf', 'pegtl', 'trace', 'ts', 'vt', 'work', 'ar'] + self.python_libs + self.tbb_libs
        self.cpp_info.components["sdf"].libs = ['usd_sdf']
        # ndr
        self.cpp_info.components["ndr"].requires = ['tf', 'plug', 'vt', 'work', 'ar', 'sdf'] + self.python_libs
        self.cpp_info.components["ndr"].libs = ['usd_ndr']
        # sdr
        self.cpp_info.components["sdr"].requires = ['tf', 'vt', 'ar', 'ndr', 'sdf'] + self.python_libs
        self.cpp_info.components["sdr"].libs = ['usd_sdr']
        # pcp
        self.cpp_info.components["pcp"].requires = ['tf', 'trace', 'vt', 'sdf', 'work', 'ar'] + self.python_libs + self.tbb_libs
        self.cpp_info.components["pcp"].libs = ['usd_pcp']
        # usd
        self.cpp_info.components["usd"].requires = ['arch', 'kind', 'pcp', 'sdf', 'ar', 'plug', 'tf', 'trace', 'ts', 'vt', 'work'] + self.python_libs + self.tbb_libs
        self.cpp_info.components["usd"].libs = ['usd_usd']
        # usdGeom
        self.cpp_info.components["usdGeom"].requires = ['js', 'tf', 'plug', 'vt', 'sdf', 'trace', 'usd', 'work'] + self.python_libs + self.tbb_libs
        self.cpp_info.components["usdGeom"].libs = ['usd_usdGeom']
        # usdVol
        self.cpp_info.components["usdVol"].requires = ['tf', 'usd', 'usdGeom']
        self.cpp_info.components["usdVol"].libs = ['usd_usdVol']
        # usdMedia
        self.cpp_info.components["usdMedia"].requires = ['tf', 'vt', 'sdf', 'usd', 'usdGeom']
        self.cpp_info.components["usdMedia"].libs = ['usd_usdMedia']
        # usdShade
        self.cpp_info.components["usdShade"].requires = ['tf', 'vt', 'js', 'sdf', 'ndr', 'sdr', 'usd', 'usdGeom'] + self.python_libs + self.tbb_libs
        self.cpp_info.components["usdShade"].libs = ['usd_usdShade']
        # usdLux
        self.cpp_info.components["usdLux"].requires = ['tf', 'vt', 'ndr', 'sdf', 'usd', 'usdGeom', 'usdShade']
        self.cpp_info.components["usdLux"].libs = ['usd_usdLux']
        # usdProc
        self.cpp_info.components["usdProc"].requires = ['tf', 'usd', 'usdGeom']
        self.cpp_info.components["usdProc"].libs = ['usd_usdProc']
        # usdRender
        self.cpp_info.components["usdRender"].requires = ['gf', 'tf', 'usd', 'usdGeom', 'usdShade']
        self.cpp_info.components["usdRender"].libs = ['usd_usdRender']
        # usdHydra
        self.cpp_info.components["usdHydra"].requires = ['tf', 'usd', 'usdShade']
        self.cpp_info.components["usdHydra"].libs = ['usd_usdHydra']
        # usdRi
        self.cpp_info.components["usdRi"].requires = ['tf', 'vt', 'sdf', 'usd', 'usdShade', 'usdGeom'] + self.python_libs
        self.cpp_info.components["usdRi"].libs = ['usd_usdRi']
        # usdSemantics
        self.cpp_info.components["usdSemantics"].requires = ['tf', 'vt', 'usd']
        self.cpp_info.components["usdSemantics"].libs = ['usd_usdSemantics']
        # usdSkel
        self.cpp_info.components["usdSkel"].requires = ['arch', 'gf', 'tf', 'trace', 'vt', 'work', 'sdf', 'usd', 'usdGeom'] + self.python_libs + self.tbb_libs
        self.cpp_info.components["usdSkel"].libs = ['usd_usdSkel']
        # usdUI
        self.cpp_info.components["usdUI"].requires = ['tf', 'vt', 'sdf', 'usd']
        self.cpp_info.components["usdUI"].libs = ['usd_usdUI']
        # usdUtils
        self.cpp_info.components["usdUtils"].requires = ['arch', 'tf', 'gf', 'sdf', 'usd', 'usdGeom', 'usdShade'] + self.python_libs + self.tbb_libs
        self.cpp_info.components["usdUtils"].libs = ['usd_usdUtils']
        # usdPhysics
        self.cpp_info.components["usdPhysics"].requires = ['tf', 'plug', 'vt', 'sdf', 'trace', 'usd', 'usdGeom', 'usdShade', 'work'] + self.python_libs + self.tbb_libs
        self.cpp_info.components["usdPhysics"].libs = ['usd_usdPhysics']
        # usdMtlx
        #if self.options.materialx:
        self.cpp_info.components["usdMtlx"].requires = ['arch', 'gf', 'ndr', 'sdf', 'sdr', 'tf', 'vt', 'usd', 'usdGeom', 'usdShade', 'usdUI', 'usdUtils'] + [self.mtlx_prefix+'MaterialXCore', self.mtlx_prefix+'MaterialXFormat']
        self.cpp_info.components["usdMtlx"].libs = ['usd_usdMtlx']
        #else:
        #    self.cpp_info.components["usdMtlx"].requires = []
        #    self.cpp_info.components["usdMtlx"].libs = []

        # usdAbc
        self.cpp_info.components["usdAbc"].requires = ['tf', 'work', 'sdf', 'usd', 'usdGeom', 'alembic::alembic', 'imath::imath_lib', 'imath::imath_config']
        self.cpp_info.components["usdAbc"].libs = []

        if self.options.use_imaging:
            # garch
            self.cpp_info.components["garch"].requires = ['arch', 'tf'] + self.python_libs
            self.cpp_info.components["garch"].libs = ['usd_garch']
            if self.settings.os == 'Linux':
                self.cpp_info.components["garch"].requires.append('opengl::opengl')
            # hf
            self.cpp_info.components["hf"].requires = ['plug', 'tf', 'trace']
            self.cpp_info.components["hf"].libs = ['usd_hf']
            # hio
            self.cpp_info.components["hio"].requires = ['arch', 'js', 'plug', 'tf', 'vt', 'trace', 'ar', 'hf']
            self.cpp_info.components["hio"].libs = ['usd_hio']
            # cameraUtil
            self.cpp_info.components["cameraUtil"].requires = ['tf', 'gf'] + self.python_libs
            self.cpp_info.components["cameraUtil"].libs = ['usd_cameraUtil']
            # pxOsd
            self.cpp_info.components["pxOsd"].requires = ['tf', 'gf', 'vt', 'opensubdiv::osdcpu'] + self.python_libs
            self.cpp_info.components["pxOsd"].libs = ['usd_pxOsd']
            # geomUtil
            self.cpp_info.components["geomUtil"].requires = ['arch', 'gf', 'tf', 'vt', 'pxOsd'] + self.python_libs
            self.cpp_info.components["geomUtil"].libs = ['usd_geomUtil']
            # glf
            self.cpp_info.components["glf"].requires = ['ar', 'arch', 'garch', 'gf', 'hf', 'hio', 'plug', 'tf', 'trace', 'sdf'] + self.python_libs
            self.cpp_info.components["glf"].libs = ['usd_glf']
            if self.settings.os == 'Linux':
                self.cpp_info.components["glf"].requires.append('opengl::opengl')
            # hgi
            self.cpp_info.components["hgi"].requires = ['gf', 'plug', 'tf', 'hio']
            self.cpp_info.components["hgi"].libs = ['usd_hgi']
            # hgiGL
            self.cpp_info.components["hgiGL"].requires = ['arch', 'garch', 'hgi', 'tf', 'trace']
            self.cpp_info.components["hgiGL"].libs = ['usd_hgiGL']
            # hgiInterop
            self.cpp_info.components["hgiInterop"].requires = ['gf', 'tf', 'hgi', 'vt', 'garch']
            self.cpp_info.components["hgiInterop"].libs = ['usd_hgiInterop']
            # hd
            self.cpp_info.components["hd"].requires = ['plug', 'tf', 'trace', 'vt', 'work', 'sdf', 'cameraUtil', 'hf', 'pxOsd', 'sdr'] + self.tbb_libs
            self.cpp_info.components["hd"].libs = ['usd_hd']
            # hdar
            self.cpp_info.components["hdar"].requires = ['hd', 'ar']
            self.cpp_info.components["hdar"].libs = ['usd_hdar']
            # hdGp
            self.cpp_info.components["hdGp"].requires = ['hd', 'hf'] + self.tbb_libs
            self.cpp_info.components["hdGp"].libs = ['usd_hdGp']
            # hdsi
            self.cpp_info.components["hdsi"].requires = ['plug', 'tf', 'trace', 'vt', 'work', 'sdf', 'cameraUtil', 'geomUtil', 'hf', 'hd', 'pxOsd']
            self.cpp_info.components["hdsi"].libs = ['usd_hdsi']
            # hdMtlx
            #if self.options.materialx:
            self.cpp_info.components["hdMtlx"].requires = ['gf', 'hd', 'sdf', 'sdr', 'tf', 'trace', 'usdMtlx', 'vt'] + [self.mtlx_prefix+'MaterialXCore', self.mtlx_prefix+'MaterialXFormat']
            self.cpp_info.components["hdMtlx"].libs = ['usd_hdMtlx']
            #else:
            #    self.cpp_info.components["hdMtlx"].requires = []
            #    self.cpp_info.components["hdMtlx"].libs = []
            # hdSt
            self.cpp_info.components["hdSt"].requires = ['hio', 'garch', 'glf', 'hd', 'hdsi', 'hgiGL', 'hgiInterop', 'sdr', 'tf', 'trace', 'hdMtlx', 'opensubdiv::osdcpu', 'opensubdiv::osdgpu']
            #if self.options.materialx:
            self.cpp_info.components["hdSt"].requires += [self.mtlx_prefix+'MaterialXGenShader', self.mtlx_prefix+'MaterialXRender', self.mtlx_prefix+'MaterialXCore', self.mtlx_prefix+'MaterialXFormat', self.mtlx_prefix+'MaterialXGenGlsl', self.mtlx_prefix+'MaterialXGenMsl']
            self.cpp_info.components["hdSt"].requires.append('ptex::ptex')
            self.cpp_info.components["hdSt"].libs = ['usd_hdSt']
            # hdx
            self.cpp_info.components["hdx"].requires = ['plug', 'tf', 'vt', 'gf', 'work', 'garch', 'glf', 'pxOsd', 'hd', 'hdSt', 'hgi', 'hgiInterop', 'cameraUtil', 'sdf', 'opencolorio::opencolorio']
            self.cpp_info.components["hdx"].libs = ['usd_hdx']
            # usdImaging
            self.cpp_info.components["usdImaging"].requires = ['gf', 'tf', 'plug', 'trace', 'vt', 'work', 'geomUtil', 'hd', 'hdar', 'hio', 'pxOsd', 'sdf', 'usd', 'usdGeom', 'usdLux', 'usdRender', 'usdShade', 'usdVol', 'ar'] + self.tbb_libs
            self.cpp_info.components["usdImaging"].libs = ['usd_usdImaging']
            # usdImagingGL
            self.cpp_info.components["usdImagingGL"].requires = ['gf', 'tf', 'plug', 'trace', 'vt', 'work', 'hio', 'garch', 'glf', 'hd', 'hdsi', 'hdx', 'pxOsd', 'sdf', 'sdr', 'usd', 'usdGeom', 'usdHydra', 'usdShade', 'usdImaging', 'ar'] + self.python_libs + self.tbb_libs
            self.cpp_info.components["usdImagingGL"].libs = ['usd_usdImagingGL']
            # usdProcImaging
            self.cpp_info.components["usdProcImaging"].requires = ['usdImaging', 'usdProc']
            self.cpp_info.components["usdProcImaging"].libs = ['usd_usdProcImaging']
            # usdRiPxrImaging
            self.cpp_info.components["usdRiPxrImaging"].requires = ['gf', 'tf', 'plug', 'trace', 'vt', 'work', 'hd', 'pxOsd', 'sdf', 'usd', 'usdGeom', 'usdLux', 'usdShade', 'usdImaging', 'usdVol', 'ar'] + self.tbb_libs
            self.cpp_info.components["usdRiPxrImaging"].libs = ['usd_usdRiPxrImaging']
            # usdSkelImaging
            self.cpp_info.components["usdSkelImaging"].requires = ['hio', 'hd', 'usdImaging', 'usdSkel']
            self.cpp_info.components["usdSkelImaging"].libs = ['usd_usdSkelImaging']
            # usdVolImaging
            self.cpp_info.components["usdVolImaging"].requires = ['usdImaging']
            self.cpp_info.components["usdVolImaging"].libs = ['usd_usdVolImaging']
            # usdAppUtils
            self.cpp_info.components["usdAppUtils"].requires = ['garch', 'gf', 'hio', 'sdf', 'tf', 'usd', 'usdGeom', 'usdImagingGL'] + self.python_libs
            self.cpp_info.components["usdAppUtils"].libs = ['usd_usdAppUtils']
            # usdBakeMtlx
            #self.cpp_info.components["usdBakeMtlx"].requires = ['tf', 'sdr', 'usdMtlx', 'usdShade', 'hd', 'hdMtlx', 'usdImaging'] + self.python_libs + [self.mtlx_prefix+'MaterialXCore', self.mtlx_prefix+'MaterialXFormat', self.mtlx_prefix+'MaterialXRenderGlsl']
            #self.cpp_info.components["usdBakeMtlx"].libs = ['usd_usdBakeMtlx']
            # hioOiio
            self.cpp_info.components["hioOiio"].requires = ['ar', 'arch', 'gf', 'hio', 'tf', 'openimageio::openimageio', 'imath::imath_lib']
            self.cpp_info.components["hioOiio"].libs = []
