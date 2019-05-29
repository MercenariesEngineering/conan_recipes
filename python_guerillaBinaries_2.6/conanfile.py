from conans import ConanFile
from conans import tools

class pythonConan(ConanFile):
    name = "python"
    version = "guerillaBinaries_2.6"
    settings = "os", "compiler", "build_type", "arch"
    description = "Python is a programming language that lets you work quickly and integrate systems more effectively"
    url = "https://www.python.org/"
    license = "None"

    def package(self):
        self.run("rm -Rf include lib")
        self.run("mkdir include lib")

        if self.settings.os == "Windows" :
            src_path = "X:\\Dev\\GuerillaLibs2015\\"
            includes = [
                "contrib\\python2.6\\abstract.h",
                "contrib\\python2.6\\asdl.h",
                "contrib\\python2.6\\ast.h",
                "contrib\\python2.6\\bitset.h",
                "contrib\\python2.6\\boolobject.h",
                "contrib\\python2.6\\bufferobject.h",
                "contrib\\python2.6\\bytearrayobject.h",
                "contrib\\python2.6\\bytes_methods.h",
                "contrib\\python2.6\\bytesobject.h",
                "contrib\\python2.6\\cellobject.h",
                "contrib\\python2.6\\ceval.h",
                "contrib\\python2.6\\classobject.h",
                "contrib\\python2.6\\cobject.h",
                "contrib\\python2.6\\code.h",
                "contrib\\python2.6\\codecs.h",
                "contrib\\python2.6\\compile.h",
                "contrib\\python2.6\\complexobject.h",
                "contrib\\python2.6\\cStringIO.h",
                "contrib\\python2.6\\datetime.h",
                "contrib\\python2.6\\descrobject.h",
                "contrib\\python2.6\\dictobject.h",
                "contrib\\python2.6\\enumobject.h",
                "contrib\\python2.6\\errcode.h",
                "contrib\\python2.6\\eval.h",
                "contrib\\python2.6\\fileobject.h",
                "contrib\\python2.6\\floatobject.h",
                "contrib\\python2.6\\frameobject.h",
                "contrib\\python2.6\\funcobject.h",
                "contrib\\python2.6\\genobject.h",
                "contrib\\python2.6\\graminit.h",
                "contrib\\python2.6\\grammar.h",
                "contrib\\python2.6\\import.h",
                "contrib\\python2.6\\intobject.h",
                "contrib\\python2.6\\intrcheck.h",
                "contrib\\python2.6\\iterobject.h",
                "contrib\\python2.6\\listobject.h",
                "contrib\\python2.6\\longintrepr.h",
                "contrib\\python2.6\\longobject.h",
                "contrib\\python2.6\\marshal.h",
                "contrib\\python2.6\\metagrammar.h",
                "contrib\\python2.6\\methodobject.h",
                "contrib\\python2.6\\modsupport.h",
                "contrib\\python2.6\\moduleobject.h",
                "contrib\\python2.6\\node.h",
                "contrib\\python2.6\\object.h",
                "contrib\\python2.6\\objimpl.h",
                "contrib\\python2.6\\opcode.h",
                "contrib\\python2.6\\osdefs.h",
                "contrib\\python2.6\\parsetok.h",
                "contrib\\python2.6\\patchlevel.h",
                "contrib\\python2.6\\pgen.h",
                "contrib\\python2.6\\pgenheaders.h",
                "contrib\\python2.6\\py_curses.h",
                "contrib\\python2.6\\pyarena.h",
                "contrib\\python2.6\\pyconfig.h",
                "contrib\\python2.6\\pydebug.h",
                "contrib\\python2.6\\pyerrors.h",
                "contrib\\python2.6\\pyexpat.h",
                "contrib\\python2.6\\pyfpe.h",
                "contrib\\python2.6\\pygetopt.h",
                "contrib\\python2.6\\pymacconfig.h",
                "contrib\\python2.6\\pymactoolbox.h",
                "contrib\\python2.6\\pymath.h",
                "contrib\\python2.6\\pymem.h",
                "contrib\\python2.6\\pyport.h",
                "contrib\\python2.6\\pystate.h",
                "contrib\\python2.6\\pystrcmp.h",
                "contrib\\python2.6\\pystrtod.h",
                "contrib\\python2.6\\Python.h",
                "contrib\\python2.6\\Python-ast.h",
                "contrib\\python2.6\\pythonrun.h",
                "contrib\\python2.6\\pythread.h",
                "contrib\\python2.6\\rangeobject.h",
                "contrib\\python2.6\\setobject.h",
                "contrib\\python2.6\\sliceobject.h",
                "contrib\\python2.6\\stringobject.h",
                "contrib\\python2.6\\structmember.h",
                "contrib\\python2.6\\structseq.h",
                "contrib\\python2.6\\symtable.h",
                "contrib\\python2.6\\sysmodule.h",
                "contrib\\python2.6\\timefuncs.h",
                "contrib\\python2.6\\token.h",
                "contrib\\python2.6\\traceback.h",
                "contrib\\python2.6\\tupleobject.h",
                "contrib\\python2.6\\ucnhash.h",
                "contrib\\python2.6\\unicodeobject.h",
                "contrib\\python2.6\\warnings.h",
                "contrib\\python2.6\\weakrefobject.h"]
        elif self.settings.os == "Linux" :
            src_path = "/usr/local/toolchain/gcc-4.9.2/"
            includes = []
            # We don't package python on linux

        for path in includes:
            self.run("cp -R %s%s include\\" % (src_path, path))

        self.copy("*.h")
