from conans import ConanFile, CMake, tools
import os

class LlvmConan(ConanFile):
    name = "llvm"
    version = "3.5.1"
    license = ""
    url = "llvm.org"
    description = "The LLVM Compiler Infrastructure"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    generators = "cmake"

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        # http://releases.llvm.org/3.5.1/llvm-3.5.1.src.tar.xz , but xz is not suported
        # https://github.com/llvm/llvm-project/archive/llvmorg-3.5.1.tar.gz
        filename = "llvmorg-%s.tar.gz" % self.version
        tools.download("https://github.com/llvm/llvm-project/archive/%s" % filename, filename)
        tools.untargz(filename)
        os.unlink(filename)

    def build(self):
        cmake = CMake(self)
        if ("fPIC" in self.options.fields and self.options.fPIC == True):
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = True
        cmake.configure(source_dir="llvm-project-llvmorg-%s/llvm/" % self.version)
        cmake.build()

    def package(self):
        self.copy("*.h", src="llvm-project-llvmorg-%s/llvm/include/" % self.version, dst="include")
        self.copy("*.def", src="llvm-project-llvmorg-%s/llvm/include/" % self.version, dst="include")
        self.copy("*.h", src="include/llvm/", dst="include/llvm/")
        self.copy("*.def", src="include/llvm/", dst="include/llvm/")
        self.copy("*.gen", src="include/llvm/", dst="include/llvm/")

        if self.settings.os == "Windows" :
            libs = [
                "LLVMAnalysis.lib",
                "LLVMAsmParser.lib",
                "LLVMAsmPrinter.lib",
                "LLVMBitReader.lib",
                "LLVMBitWriter.lib",
                "LLVMCodeGen.lib",
                "LLVMCore.lib",
                "LLVMDebugInfo.lib",
                "LLVMExecutionEngine.lib",
                "LLVMInstCombine.lib",
                "LLVMInstrumentation.lib",
                "LLVMInterpreter.lib",
                "LLVMipa.lib",
                "LLVMipo.lib",
                "LLVMIRReader.lib",
                "LLVMJIT.lib",
                "LLVMLineEditor.lib",
                "LLVMLinker.lib",
                "LLVMLTO.lib",
                "LLVMMC.lib",
                "LLVMMCAnalysis.lib",
                "LLVMMCDisassembler.lib",
                "LLVMMCJIT.lib",
                "LLVMMCParser.lib",
                "LLVMObjCARCOpts.lib",
                "LLVMObject.lib",
                "LLVMOption.lib",
                "LLVMProfileData.lib",
                "LLVMRuntimeDyld.lib",
                "LLVMScalarOpts.lib",
                "LLVMSelectionDAG.lib",
                "LLVMSupport.lib",
                "LLVMTableGen.lib",
                "LLVMTarget.lib",
                "LLVMTransformUtils.lib",
                "LLVMVectorize.lib",
                "LLVMX86AsmParser.lib",
                "LLVMX86AsmPrinter.lib",
                "LLVMX86CodeGen.lib",
                "LLVMX86Desc.lib",
                "LLVMX86Disassembler.lib",
                "LLVMX86Info.lib",
                "LLVMX86Utils.lib"]
        elif self.settings.os == "Linux" :
            libs = [
                "libLLVMLTO.a",
                "libLLVMObjCARCOpts.a",
                "libLLVMLinker.a",
                "libLLVMipo.a",
                "libLLVMVectorize.a",
                "libLLVMBitWriter.a",
                "libLLVMIRReader.a",
                "libLLVMAsmParser.a",
                "libLLVMR600CodeGen.a",
                "libLLVMR600Desc.a",
                "libLLVMR600Info.a",
                "libLLVMR600AsmPrinter.a",
                "libLLVMSystemZDisassembler.a",
                "libLLVMSystemZCodeGen.a",
                "libLLVMSystemZAsmParser.a",
                "libLLVMSystemZDesc.a",
                "libLLVMSystemZInfo.a",
                "libLLVMSystemZAsmPrinter.a",
                "libLLVMHexagonCodeGen.a",
                "libLLVMHexagonAsmPrinter.a",
                "libLLVMHexagonDesc.a",
                "libLLVMHexagonInfo.a",
                "libLLVMNVPTXCodeGen.a",
                "libLLVMNVPTXDesc.a",
                "libLLVMNVPTXInfo.a",
                "libLLVMNVPTXAsmPrinter.a",
                "libLLVMCppBackendCodeGen.a",
                "libLLVMCppBackendInfo.a",
                "libLLVMMSP430CodeGen.a",
                "libLLVMMSP430Desc.a",
                "libLLVMMSP430Info.a",
                "libLLVMMSP430AsmPrinter.a",
                "libLLVMXCoreDisassembler.a",
                "libLLVMXCoreCodeGen.a",
                "libLLVMXCoreDesc.a",
                "libLLVMXCoreInfo.a",
                "libLLVMXCoreAsmPrinter.a",
                "libLLVMMipsDisassembler.a",
                "libLLVMMipsCodeGen.a",
                "libLLVMMipsAsmParser.a",
                "libLLVMMipsDesc.a",
                "libLLVMMipsInfo.a",
                "libLLVMMipsAsmPrinter.a",
                "libLLVMAArch64Disassembler.a",
                "libLLVMAArch64CodeGen.a",
                "libLLVMAArch64AsmParser.a",
                "libLLVMAArch64Desc.a",
                "libLLVMAArch64Info.a",
                "libLLVMAArch64AsmPrinter.a",
                "libLLVMAArch64Utils.a",
                "libLLVMARMDisassembler.a",
                "libLLVMARMCodeGen.a",
                "libLLVMARMAsmParser.a",
                "libLLVMARMDesc.a",
                "libLLVMARMInfo.a",
                "libLLVMARMAsmPrinter.a",
                "libLLVMPowerPCDisassembler.a",
                "libLLVMPowerPCCodeGen.a",
                "libLLVMPowerPCAsmParser.a",
                "libLLVMPowerPCDesc.a",
                "libLLVMPowerPCInfo.a",
                "libLLVMPowerPCAsmPrinter.a",
                "libLLVMSparcDisassembler.a",
                "libLLVMSparcCodeGen.a",
                "libLLVMSparcAsmParser.a",
                "libLLVMSparcDesc.a",
                "libLLVMSparcInfo.a",
                "libLLVMSparcAsmPrinter.a",
                "libLLVMTableGen.a",
                "libLLVMDebugInfo.a",
                "libLLVMOption.a",
                "libLLVMX86Disassembler.a",
                "libLLVMX86AsmParser.a",
                "libLLVMX86CodeGen.a",
                "libLLVMSelectionDAG.a",
                "libLLVMAsmPrinter.a",
                "libLLVMX86Desc.a",
                "libLLVMX86Info.a",
                "libLLVMX86AsmPrinter.a",
                "libLLVMX86Utils.a",
                "libLLVMJIT.a",
                "libLLVMLineEditor.a",
                "libLLVMMCAnalysis.a",
                "libLLVMMCDisassembler.a",
                "libLLVMInstrumentation.a",
                "libLLVMInterpreter.a",
                "libLLVMCodeGen.a",
                "libLLVMScalarOpts.a",
                "libLLVMInstCombine.a",
                "libLLVMTransformUtils.a",
                "libLLVMipa.a",
                "libLLVMAnalysis.a",
                "libLLVMProfileData.a",
                "libLLVMMCJIT.a",
                "libLLVMTarget.a",
                "libLLVMRuntimeDyld.a",
                "libLLVMObject.a",
                "libLLVMMCParser.a",
                "libLLVMBitReader.a",
                "libLLVMExecutionEngine.a",
                "libLLVMMC.a",
                "libLLVMCore.a",
                "libLLVMSupport.a"]
        else :
            libs = []

        for l in libs:
            self.copy("lib/"+l, dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
