from conans.errors import ConanInvalidConfiguration
from conans import ConanFile, CMake, tools
import os

class LlvmConan(ConanFile):
    name = "llvm"
    version = "13.0.1"
    license = ""
    url = "llvm.org"
    description = "A toolkit for the construction of highly optimized compilers, optimizers, and runtime environments"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        'shared': [True, False],
        'fPIC': [True, False],
        'components': 'ANY',
        'targets': 'ANY',
        'exceptions': [True, False],
        'rtti': [True, False],
        'threads': [True, False],
        'lto': ['On', 'Off', 'Full', 'Thin'],
        'static_stdlib': [True, False],
        'unwind_tables': [True, False],
        'expensive_checks': [True, False],
        'use_perf': [True, False],
        'use_sanitizer': [
            'Address',
            'Memory',
            'MemoryWithOrigins',
            'Undefined',
            'Thread',
            'DataFlow',
            'Address;Undefined',
            'None'
        ],
        'with_ffi': [True, False],
        'with_zlib': [True, False],
        'with_xml2': [True, False]
    }
    default_options = {
        'shared': False,
        'fPIC': True,
        'components': 'all',
        'targets': 'X86',
        'exceptions': True,
        'rtti': True,
        'threads': True,
        'lto': 'Off',
        'static_stdlib': False,
        'unwind_tables': True,
        'expensive_checks': False,
        'use_perf': False,
        'use_sanitizer': 'None',
        'with_ffi': False,
        'with_zlib': True,
        'with_xml2': True
    }
    generators = "cmake"
    exports_sources = ['CMakeLists.txt', 'patches/*']
    short_paths = True # LLVM uses long filenames, which are a problem on windows. This helps.
    no_copy_source = True
    _source_subfolder = "source_subfolder"
    recipe_version = "0"

    def _supports_compiler(self):
        compiler = self.settings.compiler.value
        version = tools.Version(self.settings.compiler.version)
        major_rev, minor_rev = int(version.major), int(version.minor)

        unsupported_combinations = [
            [compiler == 'gcc', major_rev == 5, minor_rev < 1],
            [compiler == 'gcc', major_rev < 5],
            [compiler == 'clang', major_rev < 4],
            [compiler == 'apple-clang', major_rev < 9],
            [compiler == 'Visual Studio', major_rev < 15]
        ]
        if any(all(combination) for combination in unsupported_combinations):
            message = 'unsupported compiler: "{}", version "{}"'
            raise ConanInvalidConfiguration(message.format(compiler, version))

    def _patch_sources(self):
        tools.patch(self._source_subfolder, "patches/revert_33ef594c58990d04cc16b3138279b1fb0451ce23.patch")

    def _patch_build(self):
        if os.path.exists('FindIconv.cmake'):
            tools.replace_in_file('FindIconv.cmake', 'iconv charset', 'iconv')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_SHARED_LIBS'] = False
        cmake.definitions['CMAKE_SKIP_RPATH'] = True
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.get_safe('fPIC', default=False) or self.options.shared

        if not self.options.shared:
            cmake.definitions['DISABLE_LLVM_LINK_LLVM_DYLIB'] = True
        # cmake.definitions['LLVM_LINK_DYLIB'] = self.options.shared

        cmake.definitions['LLVM_TARGET_ARCH'] = 'host'
        cmake.definitions['LLVM_TARGETS_TO_BUILD'] = self.options.targets
        cmake.definitions['LLVM_BUILD_LLVM_DYLIB'] = self.options.shared
        cmake.definitions['LLVM_DYLIB_COMPONENTS'] = self.options.components
        cmake.definitions['LLVM_ENABLE_PIC'] = self.options.get_safe('fPIC', default=False)

        if self.settings.compiler == 'Visual Studio':
            build_type = str(self.settings.build_type).upper()
            cmake.definitions['LLVM_USE_CRT_{}'.format(build_type)] = self.settings.compiler.runtime

        cmake.definitions['LLVM_ABI_BREAKING_CHECKS'] = 'WITH_ASSERTS'
        cmake.definitions['LLVM_ENABLE_WARNINGS'] = True
        cmake.definitions['LLVM_ENABLE_PEDANTIC'] = True
        cmake.definitions['LLVM_ENABLE_WERROR'] = False

        cmake.definitions['LLVM_TEMPORARILY_ALLOW_OLD_TOOLCHAIN'] = True
        cmake.definitions['LLVM_USE_RELATIVE_PATHS_IN_DEBUG_INFO'] = False
        cmake.definitions['LLVM_BUILD_INSTRUMENTED_COVERAGE'] = False
        cmake.definitions['LLVM_OPTIMIZED_TABLEGEN'] = True
        cmake.definitions['LLVM_REVERSE_ITERATION'] = False
        cmake.definitions['LLVM_ENABLE_BINDINGS'] = False
        cmake.definitions['LLVM_CCACHE_BUILD'] = False

        cmake.definitions['LLVM_INCLUDE_TOOLS'] = self.options.shared
        cmake.definitions['LLVM_INCLUDE_EXAMPLES'] = False
        cmake.definitions['LLVM_INCLUDE_TESTS'] = False
        cmake.definitions['LLVM_INCLUDE_BENCHMARKS'] = False
        cmake.definitions['LLVM_APPEND_VC_REV'] = False
        cmake.definitions['LLVM_BUILD_DOCS'] = False
        cmake.definitions['LLVM_ENABLE_IDE'] = False
        cmake.definitions['LLVM_ENABLE_TERMINFO'] = False

        cmake.definitions['LLVM_ENABLE_EH'] = self.options.exceptions
        cmake.definitions['LLVM_ENABLE_RTTI'] = self.options.rtti
        cmake.definitions['LLVM_ENABLE_THREADS'] = self.options.threads
        cmake.definitions['LLVM_ENABLE_LTO'] = self.options.lto
        cmake.definitions['LLVM_STATIC_LINK_CXX_STDLIB'] = self.options.static_stdlib
        cmake.definitions['LLVM_ENABLE_UNWIND_TABLES'] = self.options.unwind_tables
        cmake.definitions['LLVM_ENABLE_EXPENSIVE_CHECKS'] = self.options.expensive_checks
        cmake.definitions['LLVM_ENABLE_ASSERTIONS'] = self.settings.build_type == 'Debug'

        cmake.definitions['LLVM_USE_NEWPM'] = False
        cmake.definitions['LLVM_USE_OPROFILE'] = False
        cmake.definitions['LLVM_USE_PERF'] = self.options.use_perf
        if self.options.use_sanitizer == 'None':
            cmake.definitions['LLVM_USE_SANITIZER'] = ''
        else:
            cmake.definitions['LLVM_USE_SANITIZER'] = self.options.use_sanitizer

        cmake.definitions['LLVM_ENABLE_Z3_SOLVER'] = False
        cmake.definitions['LLVM_ENABLE_LIBPFM'] = False
        cmake.definitions['LLVM_ENABLE_LIBEDIT'] = False
        cmake.definitions['LLVM_ENABLE_FFI'] = self.options.with_ffi
        cmake.definitions['LLVM_ENABLE_ZLIB'] = self.options.get_safe('with_zlib', False)
        cmake.definitions['LLVM_ENABLE_LIBXML2'] = self.options.get_safe('with_xml2', False)
        return cmake

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
            del self.options.with_zlib
            del self.options.with_xml2

    def requirements(self):
        if self.options.with_ffi:
            self.requires('libffi/3.3@mercseng/v0')
        if self.options.get_safe('with_zlib', False):
            self.requires('zlib/1.2.11@mercseng/v0')
        if self.options.get_safe('with_xml2', False):
            self.requires('libxml2/2.9.12@mercseng/v0')

    def validate(self):
        if self.options.shared:  # Shared builds disabled just due to the CI
            message = 'Shared builds not currently supported'
            raise ConanInvalidConfiguration(message)
            # del self.options.fPIC
        # if self.settings.os == 'Windows' and self.options.shared:
        #     message = 'Shared builds not supported on Windows'
        #     raise ConanInvalidConfiguration(message)
        if self.options.exceptions and not self.options.rtti:
            message = 'Cannot enable exceptions without rtti support'
            raise ConanInvalidConfiguration(message)
        self._supports_compiler()
        if tools.cross_building(self, skip_x64_x86=True):
            raise ConanInvalidConfiguration('Cross-building not implemented')

    def source(self):
        tools.get("https://github.com/llvm/llvm-project/releases/download/llvmorg-%s/llvm-%s.src.tar.xz" % (self.version, self.version))
        os.rename("llvm-%s.src" % self.version, self._source_subfolder)
        self._patch_sources()

    def build(self):
        self._patch_build()
        cmake = self._configure_cmake()
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy('LICENSE.TXT', dst='licenses', src=self._source_subfolder)
        lib_path = os.path.join(self.package_folder, 'lib')

        cmake = self._configure_cmake()
        cmake.install()

        tools.rmdir(os.path.join(self.package_folder, 'bin'))
        tools.rmdir(os.path.join(self.package_folder, 'lib', 'cmake'))
        tools.rmdir(os.path.join(self.package_folder, 'share'))
    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = tools.collect_libs(self)
        else:
            self.cpp_info.libs = ["LLVMTableGenGlobalISel", "LLVMTableGen", "LLVMFileCheck", "LLVMCoverage", "LLVMDWARFLinker", "LLVMDWP", "LLVMDebugInfoGSYM", "LLVMDlltoolDriver", "LLVMFrontendOpenACC", "LLVMFuzzMutate", "LLVMInterfaceStub", "LLVMInterpreter", "LLVMLTO", "LLVMExtensions", "LLVMLibDriver", "LLVMOption", "LLVMLineEditor", "LLVMMCA", "LLVMMCJIT", "LLVMMIRParser", "LLVMObjectYAML", "LLVMOrcJIT", "LLVMExecutionEngine", "LLVMRuntimeDyld", "LLVMJITLink", "LLVMOrcTargetProcess", "LLVMOrcShared", "LLVMPasses", "LLVMCoroutines", "LLVMipo", "LLVMFrontendOpenMP", "LLVMIRReader", "LLVMAsmParser", "LLVMInstrumentation", "LLVMLinker", "LLVMVectorize", "LLVMObjCARCOpts", "LLVMSymbolize", "LLVMDebugInfoPDB", "LLVMWindowsManifest", "LLVMX86AsmParser", "LLVMX86CodeGen", "LLVMAsmPrinter", "LLVMDebugInfoDWARF", "LLVMDebugInfoMSF", "LLVMCFGuard", "LLVMGlobalISel", "LLVMSelectionDAG", "LLVMCodeGen", "LLVMBitWriter", "LLVMScalarOpts", "LLVMAggressiveInstCombine", "LLVMInstCombine", "LLVMTransformUtils", "LLVMTarget", "LLVMAnalysis", "LLVMProfileData", "LLVMX86Desc", "LLVMX86Disassembler", "LLVMMCDisassembler", "LLVMX86Info", "LLVMXRay", "LLVMObject", "LLVMBitReader", "LLVMCore", "LLVMRemarks", "LLVMBitstreamReader", "LLVMMCParser", "LLVMMC", "LLVMDebugInfoCodeView", "LLVMTextAPI", "LLVMBinaryFormat", "LLVMSupport", "LLVMDemangle"]
        if self.settings.os == 'Linux':
            self.cpp_info.system_libs = ['pthread', 'rt', 'dl', 'm']
        elif self.settings.os == 'Macos':
            self.cpp_info.system_libs = ['m']
            
        #if self.options.get_safe('with_zlib', False):
        #    self.cpp_info.system_libs.append("zlib" if self.settings.os == "Windows" else "z")
        #if self.options.get_safe('with_xml2', False):
        #    self.cpp_info.system_libs.append("xml2")
        #if self.options.with_ffi:
        #    self.cpp_info.system_libs.append("ffi")
