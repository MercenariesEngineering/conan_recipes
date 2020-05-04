import os
import shutil
from conans import ConanFile, CMake, tools

class USDConan(ConanFile):
	name = "USD"
	version = "20.02"
	license = ""
	url = "https://graphics.pixar.com/usd/docs/index.html"
	description = "Universal scene description"
	license = "Modified Apache 2.0 License"
	settings = "os", "compiler", "build_type", "arch"
	options = {"shared": [True, False], "fPIC": [True, False], "debug_symbols": [True, False]}
	requires = "Alembic/1.7.12@mercseng/stable", "boost/1.64.0@conan/stable", "hdf5/1.10.1@pierousseau/stable", "materialx/1.36.3@pierousseau/stable", "OpenImageIO/1.6.18@mercseng/stable", "OpenColorIO/1.1.1@mercseng/stable", "ptex/2.3.2@pierousseau/stable", "TBB/2019_U6@pierousseau/stable", "zlib/1.2.11@conan/stable"
	default_options = "shared=True", "fPIC=True", "debug_symbols=False", "*:shared=False", "TBB:shared=True", "*:fPIC=True"
	exports_sources = "CMakeLists.txt"
	generators = "cmake"
	short_paths = True
	_source_subfolder = "source_subfolder"

	def configure(self):
		if self.settings.os != "Linux":
			self.options.remove("fPIC")

	def source(self):
		"""Retrieve source code."""
		tools.get("https://github.com/PixarAnimationStudios/USD/archive/v%s.tar.gz" % self.version)
		os.rename("USD-%s" % self.version, self._source_subfolder)

		# point to HDF5
		tools.replace_in_file("%s/CMakeLists.txt" % self._source_subfolder, "project(usd)",
							  """project(usd)
IF (DEFINED HDF5_ROOT)
	MESSAGE(STATUS "Using HDF5_ROOT: ${HDF5_ROOT}")
	# set HDF5_ROOT in the env so FindHDF5.cmake can find it
	SET(ENV{HDF5_ROOT} ${HDF5_ROOT})
ENDIF()
SET(HDF5_USE_STATIC_LIBRARIES ${USE_STATIC_HDF5})
""")

		# Keeping this would mess up dllimport directives in MSVC
		tools.replace_in_file("%s/cmake/defaults/msvcdefaults.cmake" % self._source_subfolder, """_add_define("BOOST_ALL_DYN_LINK")""", "")
		# Nope, openEXR is not necessarily built as a dll. If it actually is, it will be added back by OpenEXR recipe anyway.
		tools.replace_in_file("%s/cmake/defaults/msvcdefaults.cmake" % self._source_subfolder, """_add_define("OPENEXR_DLL")""", "")
		# Alembic plugin needs to link against OpenExr Math library.
		tools.replace_in_file("%s/pxr/usd/plugin/usdAbc/CMakeLists.txt" % self._source_subfolder, """${OPENEXR_Half_LIBRARY}""", "${OPENEXR_Half_LIBRARY} ${OPENEXR_Imath_LIBRARY}")

		# Linux: Add flags -static-libgcc -static-libstdc++
		if self.settings.os == "Linux":
			tools.replace_in_file("%s/CMakeLists.txt" % self._source_subfolder,
			"""set(CMAKE_CXX_FLAGS "${_PXR_CXX_FLAGS} ${CMAKE_CXX_FLAGS}")""", 
"""set(CMAKE_CXX_FLAGS "${_PXR_CXX_FLAGS} ${CMAKE_CXX_FLAGS}")
set(CMAKE_CXX_STANDARD_LIBRARIES "-static-libgcc -static-libstdc++ ${CMAKE_CXX_STANDARD_LIBRARIES}")
""")

		tools.replace_in_file("%s/cmake/modules/FindMaterialX.cmake" % self._source_subfolder, """documents/Libraries""", """libraries/stdlib""")

		os.rename(os.path.join(self._source_subfolder, "CMakeLists.txt"), os.path.join(self._source_subfolder, "CMakeLists_original.txt"))
		shutil.copy("CMakeLists.txt", os.path.join(self._source_subfolder, "CMakeLists.txt"))

	def configure_cmake(self):
		cmake = CMake(self)

		if self.options.debug_symbols and self.settings.build_type=="Release":
			cmake.build_type = 'RelWithDebInfo'

		definition_dict = {
			"BUILD_SHARED_LIBS":self.options.shared,
			"PXR_BUILD_ALEMBIC_PLUGIN":True,
			"PXR_BUILD_DOCUMENTATION": False,
			"PXR_BUILD_DRACO_PLUGIN": False,
			"PXR_BUILD_EMBREE_PLUGIN": False,
			"PXR_BUILD_HOUDINI_PLUGIN": False,
			"PXR_BUILD_IMAGING":False,
			"PXR_BUILD_KATANA_PLUGIN": False,
			"PXR_BUILD_MATERIALX_PLUGIN":True,
			"PXR_BUILD_OPENCOLORIO_PLUGIN": True,
			"PXR_BUILD_OPENIMAGEIO_PLUGIN": True,
			"PXR_BUILD_PRMAN_PLUGIN": False,
			"PXR_BUILD_TESTS": False,
			"PXR_BUILD_USD_IMAGING": False,
			"PXR_BUILD_USDVIEW": False,
			"PXR_ENABLE_GL_SUPPORT": False,
			"PXR_ENABLE_HDF5_SUPPORT":True,
			"PXR_ENABLE_OPENVDB_SUPPORT": True,
			"PXR_ENABLE_OSL_SUPPORT":False,
			"PXR_ENABLE_PTEX_SUPPORT": True,
			"PXR_ENABLE_PYTHON_SUPPORT": False,
			"USE_STATIC_HDF5":True,
		}

		if self.settings.os == "Linux":
			definition_dict["CMAKE_POSITION_INDEPENDENT_CODE"] = ("fPIC" in self.options.fields and self.options.fPIC == True)

		if self.settings.os == "Windows" and self.settings.build_type == "Debug":
			definition_dict["TBB_USE_DEBUG_BUILD"] = True # link against tbb_debug.lib/a

		cmake.configure(defs = definition_dict, source_folder = self._source_subfolder)
		return cmake

	def build(self):
		cmake = self.configure_cmake()
		cmake.build()

	def package(self):
		cmake = self.configure_cmake()
		cmake.install()

	def package_info(self):
		self.cpp_info.libs = tools.collect_libs(self)
		self.cpp_info.bindirs = ["lib", "bin"] # This will put "lib" folder in the path, which we need to find the plugins.
		self.cpp_info.defines = ["NOMINMAX", "YY_NO_UNISTD_H"]
		
		if self.settings.build_type == "Debug":
			self.cpp_info.defines.append("BUILD_OPTLEVEL_DEV")
		
		if self.options.shared == "False":
			self.cpp_info.defines.append("PXR_STATIC=1")
