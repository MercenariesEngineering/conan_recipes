from conans import ConanFile, tools, CMake
import os


class PyBind11Conan(ConanFile):
    name = "pybind11"
    description = "Seamless operability between C++11 and Python"
    topics = "conan", "pybind11", "python", "binding"
    homepage = "https://github.com/pybind/pybind11"
    license = "BSD-3-Clause"
    url = "https://github.com/conan-io/conan-center-index"
    _source_subfolder = "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("{}-{}".format(self.name, self.version), self._source_subfolder)

    def package(self):
        self.copy("LICENSE", src=self._source_subfolder, dst="licenses")
        self.copy("*", src=os.path.join(self.build_folder, self._source_subfolder, "include"), dst="include", keep_path=True)

    def package_id(self):
        self.info.header_only()
