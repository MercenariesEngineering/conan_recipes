import os
from conans import ConanFile, tools

PYINSTALLER_PATCH_IN = '''
class Qt5LibraryInfo:
    def __init__(self, namespace):
        if namespace not in ['PyQt5', 'PySide2']:
            raise Exception('Invalid namespace: {0}'.format(namespace))
        self.namespace = namespace
        self.is_PyQt5 = namespace == 'PyQt5'

    # Initialize most of this class only when values are first requested from
    # it.
    def __getattr__(self, name):
        if 'version' not in self.__dict__:
            # Get library path information from Qt. See QLibraryInfo_.
            json_str = exec_statement("""
                import sys

                # exec_statement only captures stdout. If there are
                # errors, capture them to stdout so they can be displayed to the
                # user. Do this early, in case PyQt5 imports produce stderr
                # output.
                sys.stderr = sys.stdout

                import json
                try:
                    from %s.QtCore import QLibraryInfo, QCoreApplication
                except:
                    print('False')
                else:
                    # QLibraryInfo isn't always valid until a QCoreApplication is
                    # instantiated.
                    app = QCoreApplication(sys.argv)
                    paths = [x for x in dir(QLibraryInfo) if x.endswith('Path')]
                    location = {x: QLibraryInfo.location(getattr(QLibraryInfo, x))
                                for x in paths}
                    try:
                        version = QLibraryInfo.version().segments()
                    except AttributeError:
                        version = []
                    print(json.dumps({
                        'isDebugBuild': QLibraryInfo.isDebugBuild(),
                        'version': version,
                        'location': location,
                    }))
            """ % self.namespace)
            try:
                qli = json.loads(json_str)
            except Exception as e:
                logger.warning('Cannot read QLibraryInfo output: raised %s when '
                               'decoding:\\n%s', str(e), json_str)
                qli = False

            # If PyQt5/PySide2 can't be imported, record that.
            if not qli:
                self.version = None
            else:
                for k, v in qli.items():
                    setattr(self, k, v)

            return getattr(self, name)
        else:
            raise AttributeError
'''

PYINSTALLER_PATCH_OUT = '''
class Qt5LibraryInfo:
    def __init__(self, namespace):
        if namespace not in ['PyQt5', 'PySide2']:
            raise Exception('Invalid namespace: {{0}}'.format(namespace))
        self.namespace = namespace
        self.is_PyQt5 = namespace == 'PyQt5'
    # Initialize most of this class only when values are first requested from
    # it.
    def __getattr__(self, name):
        if 'version' not in self.__dict__:
            if is_linux:
                qt_root = os.environ.get("QT_PLUGIN_PATH", "/usr/lib/qt/plugins" )
                qt_root = os.path.join(qt_root, "../")
                qli = {'isDebugBuild': False, "version": [5, 12, 6], "location": {
                        'ArchDataPath': qt_root,
                        'BinariesPath': os.path.join(qt_root, "bin"),
                        'DataPath': qt_root,
                        'DocumentationPath': os.path.join(qt_root, "doc"),
                        'ExamplesPath': os.path.join(qt_root, "examples"),
                        'HeadersPath': os.path.join(qt_root, "include"),
                        'ImportsPath': os.path.join(qt_root, "imports"),
                        'LibrariesPath': os.path.join(qt_root, "libexec"),
                        'LibraryExecutablesPath': os.path.join(qt_root, "libexec"),
                        'PluginsPath': os.path.join(qt_root, "plugins"),
                        'PrefixPath': qt_root,
                        'Qml2ImportsPath': os.path.join(qt_root, "qml"),
                        'SettingsPath': qt_root,
                        'TestsPath': os.path.join(qt_root, "tests"),
                        'TranslationsPath': os.path.join(qt_root, "translations")
                    }
                }
            else:
                # Get library path information from Qt. See QLibraryInfo_.
                json_str = exec_statement("""
                    import sys

                    # exec_statement only captures stdout. If there are
                    # errors, capture them to stdout so they can be displayed to the
                    # user. Do this early, in case PyQt5 imports produce stderr
                    # output.
                    sys.stderr = sys.stdout

                    import json
                    try:
                        from %s.QtCore import QLibraryInfo, QCoreApplication
                    except:
                        print('False')
                    else:
                        # QLibraryInfo isn't always valid until a QCoreApplication is
                        # instantiated.
                        app = QCoreApplication(sys.argv)
                        paths = [x for x in dir(QLibraryInfo) if x.endswith('Path')]
                        location = {x: QLibraryInfo.location(getattr(QLibraryInfo, x))
                                    for x in paths}
                        try:
                            version = QLibraryInfo.version().segments()
                        except AttributeError:
                            version = []
                        print(json.dumps({
                            'isDebugBuild': QLibraryInfo.isDebugBuild(),
                            'version': version,
                            'location': location,
                        }))
                """ % self.namespace)
                try:
                    qli = json.loads(json_str)
                except Exception as e:
                    logger.warning('Cannot read QLibraryInfo output: raised %s when '
                                'decoding:\\n%s', str(e), json_str)
                    qli = False

            # If PyQt5/PySide2 can't be imported, record that.
            if not qli:
                self.version = None
            else:
                for k, v in qli.items():
                    setattr(self, k, v)

            return getattr(self, name)
        else:
            raise AttributeError
'''

class PythonPackages(ConanFile):
    description = "List of python packages used by Rumba."
    name = "rumba-python-dev"
    version = "1.0.0"
    settings = "os", "compiler", "build_type", "arch"
    packages = [
        ("pyinstaller", "3.6"),
        ("pytest", "5.3.4"),
        ("pylint", "2.4.4"),
        ("doxypypy", "0.8.8.6")
    ]
    
    def config_options(self):
        if self.settings.os == "Windows":
            self.settings.remove("build_type")
            self.settings.remove("compiler")

    def build_requirements(self):
        self.build_requires("cpython/3.7.7@mercseng/v0")

    def build(self):
        """Build the elements to package."""
        for package_name, package_version in self.packages:
            command = "python -m pip install {name}=={version} --target={package_folder} --upgrade".format(
                name=package_name,
                version=package_version,
                package_folder=self.package_folder)
            self.run(command)

        # PyInstaller relies on QLibraryInfo to find Qt installation paths. The default behavior of
        # QLibraryInfo is to serve paths compiled into Qt binaries, so those paths are not usable if
        # the package is not where it was produced. QLibraryInfo could also use paths written in a 
        # qt.conf file, however on linux, the only way to use such a file is to have it next to the
        # binary that calls QLibraryInfo. In the present case, the binary is python, meaning we 
        # would have to write a qt.conf file during the build of package cpython, have an unwanted
        # and unrequired dependence on qt in cpython. Also, some bug reports mention that qt.conf is
        # not always correctly used (either on Linux or Windows).
        # The solution proposed here is to not use QLibraryInfo in PyInstaller, and instead use
        # paths that are obtained from the Qt package. There might be a way to do so by adding a 
        # dependence on qt here and overwriting the incriminated file at install on the system.
        if self.settings.os == "Linux":
            tools.replace_in_file(
                os.path.join(self.package_folder, "PyInstaller", "utils", "hooks", "qt.py"),
                PYINSTALLER_PATCH_IN, 
                PYINSTALLER_PATCH_OUT)

    def package(self):
        """Assemble the package."""
        if self.settings.os == "Linux":
            # fix shebangs
            python_shebang = "#!/usr/bin/env python3.7\n"
            bin_directory = os.path.join(self.package_folder, "bin")
            if os.path.exists(bin_directory):
                with tools.chdir(bin_directory):
                    for filename in [entry for entry in os.listdir(".") if os.path.isfile(entry)]:
                        with open(filename, "r") as infile:
                            lines = infile.readlines()
                        
                        if len(lines[0]) > 2 and lines[0].startswith("#!"):
                            lines[0] = python_shebang
                            with open(filename, "w") as outfile:
                                outfile.writelines(lines)
    
    def package_info(self):
        """Edit package info."""
        self.env_info.PYTHONPATH.append(self.package_folder)
        bin_directory = os.path.join(self.package_folder, "bin")
        if os.path.exists(bin_directory):
            self.env_info.PATH.append(bin_directory)

