#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os

# Based on recipe rapidjson/1.1.0@bincrafters/stable
class RapidjsonConan(ConanFile):
    name = "rapidjson"
    version = "1.1.0"
    description = "A fast JSON parser/generator for C++ with both SAX/DOM style API"
    homepage = "http://rapidjson.org/"
    url = "https://github.com/bincrafters/conan-rapidjson"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    no_copy_source = True
    _source_subfolder = "source_subfolder"

    def source(self):
        """Retrieve source code."""
        # the 1.1.0 release on github miss the files we used to include.
        commit_sha = "dfbe1db9da455552f7a9ad5d2aea17dd9d832ac1"
        tools.get("https://github.com/Tencent/rapidjson/archive/%s.zip" % commit_sha)
        os.rename("rapidjson-%s" % commit_sha, self._source_subfolder)

    def package(self):
        """Assemble the package."""
        self.copy(pattern="license.txt", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*", dst="include", src=os.path.join(self._source_subfolder, "include"))

    def package_id(self):
        """Header only package hash."""
        self.info.header_only()
