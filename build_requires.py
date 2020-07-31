from conans import ConanFile
import subprocess
import sys
import os 

EXPORT_HACK=False
EXPORT_TEMPLATE="""conan export {root}/{name}_{version}/conanfile.py {text}"""
ROOT_DIRECTORY=os.path.dirname(os.path.abspath(__file__))


class DependenceBuilder(ConanFile):
    settings = "os", "compiler", "build_type"

    def build_req(self, text):
        if not EXPORT_HACK:
            self.build_requires(text)
        else:
            modified = text.replace("@", "/")
            name, version, _, _ = modified.split('/')
            command = EXPORT_TEMPLATE.format(root=ROOT_DIRECTORY, name=name, version=version, text=text)
            if subprocess.call(command, shell=True) != 0:
                print("failed to export {}".format(text))
                sys.exit(1)

    def build_requirements(self):
        self.build_req("cmake/3.17.3@mercseng/v0")
        self.build_req("ninja/1.10.0@mercseng/v0")
        self.build_req("nasm/2.13.02@mercseng/v0")
        self.build_req("ispc/1.13.0@mercseng/v0")
        self.build_req("m4/1.4.18@mercseng/v0")
        self.build_req("flex/2.6.4@mercseng/v0")
        self.build_req("bison/3.5.3@mercseng/v0")
        self.build_req("b2/4.2.0@mercseng/v0")
