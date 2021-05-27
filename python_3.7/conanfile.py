from conans import ConanFile, tools

class pythonConan(ConanFile):
    name = "python3"
    version = "3.7"
    settings = "os"
    description = "Python is a programming language that lets you work quickly and integrate systems more effectively"
    url = "https://www.python.org/"
    license = "None"
    exports_sources = "dist/*"

    def package(self):
        """Assemble the package."""
        if self.settings.os != "Linux":
            self.copy("*.h", src="dist/windows", dst="include")
        else:
            self.copy("*.h", src="dist/linux", dst="include")
