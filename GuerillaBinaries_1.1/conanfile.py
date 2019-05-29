from conans import ConanFile
from conans import tools

class GuerillabinariesConan(ConanFile):
    name = "GuerillaBinaries"
    version = "1.1"
    settings = "os", "compiler", "build_type", "arch"
    description = "<Description of Guerillabinaries here>"
    url = "None"
    license = "None"
    src_libs_path = "X:\\Dev\\GuerillaLibs2015"

    includes_embree = ["common", "include", "kernels"]
    includes_fumefx = ["FXShadeData.h", "LinuxPorting.h", "SDColor.h", "SDMath.h", "SDPoint3.h", "stdafx.h", "stddefs.h", "vfTypes.h", "VoxelFlowBase.h"]
    includes_llvm1 = ["llvm/", "llvm-c/"]
    includes_llvm2 = ["Config/", "Support/"]
    includes_llvm3 = ["IR\\Intrinsics.gen"]
    includes_ocio1 = ["OpenColorABI.h"]
    includes_ocio2 = ["OpenColorIO.h", "OpenColorTransforms.h", "OpenColorTypes.h"]
    includes_ptex = ["PtexCache.h", "PtexDict.h", "PtexHalf.h", "PtexHashMap.h", "PtexInt.h", "PtexIO.h", "PtexMutex.h", "PtexPlatform.h", "PtexReader.h", "PtexSeparableFilter.h", "PtexSeparableKernel.h", "PtexTriangleFilter.h", "PtexTriangleKernel.h", "Ptexture.h", "PtexUtils.h", "PtexWriter.h"]
    includes_python = ["abstract.h", "asdl.h", "ast.h", "bitset.h", "boolobject.h", "bufferobject.h", "bytearrayobject.h", "bytes_methods.h", "bytesobject.h", "cellobject.h", "ceval.h", "classobject.h", "cobject.h", "code.h", "codecs.h", "compile.h", "complexobject.h", "cStringIO.h", "datetime.h", "descrobject.h", "dictobject.h", "enumobject.h", "errcode.h", "eval.h", "fileobject.h", "floatobject.h", "frameobject.h", "funcobject.h", "genobject.h", "graminit.h", "grammar.h", "import.h", "intobject.h", "intrcheck.h", "iterobject.h", "listobject.h",  "longintrepr.h", "longobject.h", "marshal.h", "metagrammar.h", "methodobject.h", "modsupport.h", "moduleobject.h", "node.h", "object.h", "objimpl.h", "opcode.h", "osdefs.h", "parsetok.h", "patchlevel.h", "pgen.h", "pgenheaders.h", "py_curses.h", "pyarena.h", "pyconfig.h", "pydebug.h", "pyerrors.h", "pyexpat.h", "pyfpe.h", "pygetopt.h", "pymacconfig.h", "pymactoolbox.h", "pymath.h", "pymem.h", "pyport.h", "pystate.h", "pystrcmp.h", "pystrtod.h", "Python.h", "Python-ast.h", "pythonrun.h", "pythread.h", "rangeobject.h", "setobject.h", "sliceobject.h", "stringobject.h", "structmember.h", "structseq.h", "symtable.h", "sysmodule.h", "timefuncs.h", "token.h", "traceback.h", "tupleobject.h", "ucnhash.h", "unicodeobject.h", "warnings.h", "weakrefobject.h"]
    includes_wx1 = ["setup.h"]
    includes_wx2 = ["wx/"]

    libs_embree = ["math.lib", "simd.lib"]
    libs_fumefx = ["FumeFXIO.lib"]
    libs_llvm = ["LLVMAnalysis.lib", "LLVMAsmParser.lib", "LLVMAsmPrinter.lib", "LLVMBitReader.lib", "LLVMBitWriter.lib", "LLVMCodeGen.lib", "LLVMCore.lib", "LLVMDebugInfo.lib", "LLVMExecutionEngine.lib", "LLVMInstCombine.lib", "LLVMInstrumentation.lib", "LLVMInterpreter.lib", "LLVMipa.lib", "LLVMipo.lib", "LLVMIRReader.lib", "LLVMJIT.lib", "LLVMLineEditor.lib", "LLVMLinker.lib", "LLVMLTO.lib", "LLVMMC.lib", "LLVMMCAnalysis.lib", "LLVMMCDisassembler.lib", "LLVMMCJIT.lib", "LLVMMCParser.lib", "LLVMObjCARCOpts.lib", "LLVMObject.lib", "LLVMOption.lib", "LLVMProfileData.lib", "LLVMRuntimeDyld.lib", "LLVMScalarOpts.lib", "LLVMSelectionDAG.lib", "LLVMSupport.lib", "LLVMTableGen.lib", "LLVMTarget.lib", "LLVMTransformUtils.lib", "LLVMVectorize.lib", "LLVMX86AsmParser.lib", "LLVMX86AsmPrinter.lib", "LLVMX86CodeGen.lib", "LLVMX86Desc.lib", "LLVMX86Disassembler.lib", "LLVMX86Info.lib", "LLVMX86Utils.lib"]
    libs_ocio = ["OpenColorIO.lib", "libyaml-cpp.lib", "tinyxml.lib"]
    libs_ptex = ["ptex.lib"]
    libs_wx = ["wxbase28.lib", "wxbase28_net.lib", "wxbase28_odbc.lib", "wxbase28_xml.lib", "wxexpat.lib", "wxmsw28_adv.lib", "wxmsw28_aui.lib", "wxmsw28_core.lib", "wxmsw28_dbgrid.lib", "wxmsw28_gl.lib", "wxmsw28_html.lib", "wxmsw28_media.lib", "wxmsw28_qa.lib", "wxmsw28_richtext.lib", "wxmsw28_stc.lib", "wxmsw28_xrc.lib", "wxregex.lib"]

    def package(self):
        self.run("rm -Rf include lib")
        self.run("mkdir include lib")

        self.run("mkdir include\\embree")
        for path in self.includes_embree:
            self.run("cp -R %s\\contrib\\embree-3.2.0\\%s include\\embree\\" % (self.src_libs_path, path))

        self.run("mkdir include\\fumefx")
        for path in self.includes_fumefx:
            self.run("cp -R %s\\contrib\\FumeFXIO\\include\\%s include\\fumefx\\" % (self.src_libs_path, path))

        for path in self.includes_llvm1:
            self.run("cp -R %s\\contrib\\llvm-3.5.1\\include\\%s include\\" % (self.src_libs_path, path))
        for path in self.includes_llvm2:
            self.run("cp -R %s\\contrib\\llvm-3.5.1\\build\\include\\llvm\\%s include\\llvm\\" % (self.src_libs_path, path))
        for path in self.includes_llvm3:
            self.run("cp -R %s\\contrib\\llvm-3.5.1\\build\\include\\llvm\\%s include\\llvm\\IR\\" % (self.src_libs_path, path))

        self.run("mkdir include\\OpenColorIO")
        for path in self.includes_ocio1:
            self.run("cp -R %s\\contrib\\opencolorio-1.0.8\\build\\export\\%s include\\OpenColorIO" % (self.src_libs_path, path))
        for path in self.includes_ocio2:
            self.run("cp -R %s\\contrib\\opencolorio-1.0.8\\export\\OpenColorIO\\%s include\\OpenColorIO" % (self.src_libs_path, path))

        for path in self.includes_ptex:
            self.run("cp -R %s\\contrib\\ptex-v2.0.30\\src\\ptex\\%s include\\" % (self.src_libs_path, path))

        for path in self.includes_python:
            self.run("cp -R %s\\contrib\\python2.6\\%s include\\" % (self.src_libs_path, path))

        self.run("mkdir lib\\x64\\%s\\wx" % self.settings.build_type)
        for path in self.includes_wx1:
            self.run("cp -R %s\\contrib\\wx-2.8.8\\lib\\x64\\%s\\wx\\%s lib\\x64\\%s\\wx\\" % (self.src_libs_path, self.settings.build_type, path, self.settings.build_type))
        for path in self.includes_wx2:
            self.run("cp -R %s\\contrib\\wx-2.8.8\\include\\%s include\\" % (self.src_libs_path, path))

        ###
        libs = [self.libs_embree, self.libs_llvm, self.libs_ocio, self.libs_ptex, self.libs_wx]
        for lib in libs:
            for path in lib:
                self.run("cp -R %s\\lib\\x64\\%s\\%s lib\\" % (self.src_libs_path, self.settings.build_type, path))

        for path in self.libs_fumefx:
            self.run("cp -R %s\\contrib\\FumeFXIO\\VS_2008SP1\\x64\\%s lib\\" % (self.src_libs_path, path))

        self.copy("*.h")
        self.copy("*.def")
        self.copy("*.gen")

        self.copy("*.lib")
        self.copy("*.pdb") # seems ignored on current conan version


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
