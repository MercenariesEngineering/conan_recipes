from conans import ConanFile
from conans import tools

class llvmConan(ConanFile):
    name = "llvm"
    version = "guerillaBinaries_3.5.1"
    settings = "os", "compiler", "build_type", "arch"
    description = "The LLVM Compiler Infrastructure"
    url = "https://llvm.org/"
    license = "None"

    def package(self):
        self.run("rm -Rf include lib")
        self.run("mkdir include lib")

        if self.settings.os == "Windows" :
            src_path = "X:\\Dev\\GuerillaLibs2015\\"
            includes = [
                "\\contrib\\llvm-3.5.1\\build\\include\\llvm",
                "\\contrib\\llvm-3.5.1\\include\\llvm",
                "\\contrib\\llvm-3.5.1\\include\\llvm-c"]
            libs = [
                "lib\\x64\\%s\\LLVMAnalysis.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMAsmParser.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMAsmPrinter.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMBitReader.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMBitWriter.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMCodeGen.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMCore.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMDebugInfo.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMExecutionEngine.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMInstCombine.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMInstrumentation.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMInterpreter.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMipa.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMipo.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMIRReader.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMJIT.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMLineEditor.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMLinker.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMLTO.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMMC.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMMCAnalysis.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMMCDisassembler.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMMCJIT.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMMCParser.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMObjCARCOpts.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMObject.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMOption.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMProfileData.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMRuntimeDyld.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMScalarOpts.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMSelectionDAG.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMSupport.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMTableGen.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMTarget.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMTransformUtils.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMVectorize.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMX86AsmParser.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMX86AsmPrinter.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMX86CodeGen.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMX86Desc.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMX86Disassembler.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMX86Info.lib"  % self.settings.build_type,
                "lib\\x64\\%s\\LLVMX86Utils.lib"  % self.settings.build_type]
        elif self.settings.os == "Linux" :
            src_path = "/usr/local/toolchain/gcc-4.9.2/"
            includes = [
                "include/llvm",
                "include/llvm-c"]
            libs = [
                "lib/libLLVMAnalysis.a",
                "lib/libLLVMAsmParser.a",
                "lib/libLLVMAsmPrinter.a",
                "lib/libLLVMBitReader.a",
                "lib/libLLVMBitWriter.a",
                "lib/libLLVMCodeGen.a",
                "lib/libLLVMCore.a",
                "lib/libLLVMDebugInfo.a",
                "lib/libLLVMExecutionEngine.a",
                "lib/libLLVMInstCombine.a",
                "lib/libLLVMInstrumentation.a",
                "lib/libLLVMInterpreter.a",
                "lib/libLLVMipa.a",
                "lib/libLLVMipo.a",
                "lib/libLLVMIRReader.a",
                "lib/libLLVMJIT.a",
                "lib/libLLVMLineEditor.a",
                "lib/libLLVMLinker.a",
                "lib/libLLVMLTO.a",
                "lib/libLLVMMC.a",
                "lib/libLLVMMCAnalysis.a",
                "lib/libLLVMMCDisassembler.a",
                "lib/libLLVMMCJIT.a",
                "lib/libLLVMMCParser.a",
                "lib/libLLVMObjCARCOpts.a",
                "lib/libLLVMObject.a",
                "lib/libLLVMOption.a",
                "lib/libLLVMProfileData.a",
                "lib/libLLVMRuntimeDyld.a",
                "lib/libLLVMScalarOpts.a",
                "lib/libLLVMSelectionDAG.a",
                "lib/libLLVMSupport.a",
                "lib/libLLVMTableGen.a",
                "lib/libLLVMTarget.a",
                "lib/libLLVMTransformUtils.a",
                "lib/libLLVMVectorize.a",
                "lib/libLLVMX86AsmParser.a",
                "lib/libLLVMX86AsmPrinter.a",
                "lib/libLLVMX86CodeGen.a",
                "lib/libLLVMX86Desc.a",
                "lib/libLLVMX86Disassembler.a",
                "lib/libLLVMX86Info.a",
                "lib/libLLVMX86Utils.a"]

        for path in includes:
            self.run("cp -R %s%s include/" % (src_path, path))

        for path in libs:
            self.run("cp -R %s%s lib/" % (src_path, path))

        self.copy("*.h")
        self.copy("*.def")
        self.copy("*.gen")
        self.copy("*.lib")
        self.copy("*.a")
        self.copy("*.pdb") # seems ignored on current conan version

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
