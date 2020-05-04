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
    source_subfolder = "source_subfolder"

    def source(self):
        # the 1.1.0 release on github miss the files we used to include.
        sha = "dfbe1db9da455552f7a9ad5d2aea17dd9d832ac1"
        source_url = "https://github.com/Tencent/rapidjson"
        tools.get("{}/archive/{}.zip".format(source_url, sha))
        os.rename("{}-{}".format(self.name, sha), self.source_subfolder)

    def package(self):
        include_folder = os.path.join(self.source_subfolder, "include")
        self.copy(pattern="license.txt", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="*", dst="include", src=include_folder)

    def package_id(self):
        self.info.header_only()
