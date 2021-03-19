#!/usr/bin/env python
from conans import ConanFile, CMake, tools
from conans.tools import Version
import os

class CatchConan(ConanFile):
    name = "catch2"
    description = "A modern, C++-native, framework for unit-tests, TDD and BDD"
    topics = ("conan", "catch2", "unit-test", "tdd", "bdd")
    url = "https://github.com/catchorg/Catch2"
    homepage = url
    license = "BSL-1.0"
    version = "3.0.0-preview3"

    exports = "LICENSE.txt"

    settings = "os", "compiler", "build_type", "arch"

    options = {"with_main": [True, False], "fPIC": [True, False]}
    default_options = {"with_main": True, "fPIC": True}
    _source_subfolder = "source_subfolder"

    def source(self):
        """Retrieve source code."""
        tools.get("https://github.com/catchorg/Catch2/archive/v%s.tar.gz" % self.version)
        os.rename("Catch2-%s" % self.version, self._source_subfolder)

        tools.replace_in_file("%s/CMakeLists.txt" % self._source_subfolder, 
            """include(CTest)""", 
            """include(CTest)
if (UNIX)
  add_compile_options("-fPIE")
endif()""")

        # Remove some features to advanced for msvc2015
        if self.settings.os == "Windows" and \
            self.settings.compiler == "Visual Studio" and \
            Version(self.settings.compiler.version.value) <= "14":
            tools.replace_in_file("%s/src/catch2/internal/catch_stringref.hpp" % self._source_subfolder, 
                """constexpr auto operator[] ( size_type index ) const noexcept -> char {""", 
                """auto operator[] ( size_type index ) const noexcept -> char {""")
            tools.replace_in_file("%s/src/catch2/internal/catch_stringref.hpp" % self._source_subfolder, 
                """constexpr StringRef substr(size_type start, size_type length) const noexcept {""", 
                """StringRef substr(size_type start, size_type length) const noexcept {""")
            
            tools.replace_in_file("%s/src/catch2/internal/catch_clara.cpp" % self._source_subfolder, 
                """for ( auto const& opt : m_options ) {
                parseInfos.push_back( { &opt, 0 } );
            }
            for ( auto const& arg : m_args ) {
                parseInfos.push_back( { &arg, 0 } );
            }""", 
            """for ( auto const& opt : m_options ) {
                ParserInfo I;
                I.parser = &opt;
                parseInfos.push_back( I );
            }
            for ( auto const& arg : m_args ) {
                ParserInfo I;
                I.parser = &arg;
                parseInfos.push_back( I );
            }""")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = "OFF"
        cmake.definitions["CATCH_INSTALL_DOCS"] = "OFF"
        cmake.definitions["CATCH_INSTALL_HELPERS"] = "ON"
        cmake.configure(build_folder="build", source_folder=self._source_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()

    def package_id(self):
        del self.info.options.with_main

    def package_info(self):
        self.cpp_info.libs = ['Catch2Main', 'Catch2'] if self.options.with_main else ['Catch2']
        self.cpp_info.names["cmake_find_package"] = "Catch2"
        self.cpp_info.names["cmake_find_package_multi"] = "Catch2"
