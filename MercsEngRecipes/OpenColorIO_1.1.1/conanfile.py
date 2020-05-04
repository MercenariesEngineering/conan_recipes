from conans import ConanFile, CMake, tools
import os

class OpenColorIOConan(ConanFile):
	name = "OpenColorIO"
	version = "1.1.1"
	license = ""
	url = "https://opencolorio.org/"
	description = "Open Source Color Management"
	settings = "os", "compiler", "build_type", "arch"
	options = {"shared": [True, False], "fPIC": [True, False]}
	default_options = "shared=False", "fPIC=True"
	generators = "cmake"
	_source_subfolder = "source_subfolder"

	def configure(self):
		if self.settings.os != "Linux":
			self.options.remove("fPIC")

	def source(self):
		"""Retrieve source code."""
		#Get a commit from the RB-1.1 branch, incorporating fixes for clang compilation
		commit_sha="6a7c18bec3a2ca8d43d710389ae9cdc2074bff04"
		tools.get("https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/%s.zip" % commit_sha)
		os.rename("OpenColorIO-%s" % commit_sha, self._source_subfolder)

	def cmake_definitions(self):
		"""Setup CMake definitions."""
		definition_dict = {
			"OCIO_BUILD_APPS": False,
			"OCIO_BUILD_DOCS": False,
			"OCIO_BUILD_JNIGLUE": False,
			"OCIO_BUILD_NUKE": False,
			"OCIO_BUILD_PYGLUE": False,
			"OCIO_BUILD_SHARED": self.options.shared,
			"OCIO_BUILD_STATIC": not self.options.shared,
			"OCIO_BUILD_TESTS": False,
			"OCIO_BUILD_TRUELIGHT": False,
		}

		if self.settings.os == "Linux":
			definition_dict["CMAKE_POSITION_INDEPENDENT_CODE"] = ("fPIC" in self.options.fields and self.options.fPIC == True)
			definition_dict["CMAKE_CXX_FLAGS"] = "-Wno-deprecated-declarations"

		return definition_dict

	def build(self):
		cmake = CMake(self)
		cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
		cmake.build()

	def package(self):
		cmake = CMake(self)
		cmake.configure(defs = self.cmake_definitions(), source_folder = self._source_subfolder)
		cmake.install()

		#self.copy("*.h", src="OpenColorIO-%s/export/OpenColorIO/" % self.version, dst="include/OpenColorIO/")
		#self.copy("*.h", src="export/", dst="include/OpenColorIO/")
		#self.copy("*.a", dst="lib", keep_path=False)
		#self.copy("*.lib", dst="lib", keep_path=False)

	def package_info(self):
		self.cpp_info.libs = tools.collect_libs(self)
		if (not self.options.shared):
			self.cpp_info.defines = ["OpenColorIO_STATIC"]
