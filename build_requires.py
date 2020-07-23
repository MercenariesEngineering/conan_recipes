from conans import ConanFile

class DependenceBuilder(ConanFile):
    settings = "os", "compiler", "build_type"

    def build_requirements(self):
        self.build_requires("cmake/3.17.3@mercseng/version-0")
        self.build_requires("ninja/1.10.0@mercseng/version-0")
        self.build_requires("nasm/2.13.02@mercseng/version-0")
        self.build_requires("ispc/1.13.0@mercseng/version-0")
        self.build_requires("m4/1.4.18@mercseng/version-0")
        self.build_requires("flex/2.6.4@mercseng/version-0")
        self.build_requires("bison/3.5.3@mercseng/version-0")
        self.build_requires("b2/4.2.0@mercseng/version-0")
