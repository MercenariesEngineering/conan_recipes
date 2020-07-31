from conans import ConanFile, tools

class pythonConan(ConanFile):
    name = "python"
    version = "2.6"
    settings = "os"
    description = "Python is a programming language that lets you work quickly and integrate systems more effectively"
    url = "https://www.python.org/"
    license = "None"
    exports_sources = "dist/*"

    def package(self):
        """Assemble the package."""
        self.copy("*.h", src="dist/include", dst="include")
