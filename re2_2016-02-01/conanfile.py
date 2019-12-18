from conans import ConanFile, CMake, tools

class Re2Conan(ConanFile):
    name = "re2"
    version = "2016-02-01"
    license = "BSD-3-Clause"
    url = "https://github.com/google/re2"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    build_policy = "missing"
    description = "RE2 is a fast, safe, thread-friendly alternative to backtracking regular expression engines like those used in PCRE, Perl, and Python. It is a C++ library."

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        tools.get("https://github.com/google/re2/archive/2016-02-01.tar.gz")

        tools.replace_in_file("re2-%s/CMakeLists.txt" % self.version,
"""foreach(target ${BENCHMARK_TARGETS})
  add_executable(${target} re2/testing/${target}.cc)
  target_link_libraries(${target} benchmark re2 ${EXTRA_TARGET_LINK_LIBRARIES})
endforeach(target)""",
"""foreach(target ${BENCHMARK_TARGETS})
  add_executable(${target} re2/testing/${target}.cc)
  target_link_libraries(${target} benchmark re2 ${EXTRA_TARGET_LINK_LIBRARIES})
endforeach(target)

set(RE2_HEADERS
    re2/filtered_re2.h
    re2/re2.h
    re2/set.h
    re2/stringpiece.h
    re2/variadic_function.h
    )

install(FILES ${RE2_HEADERS} DESTINATION include/re2)
install(TARGETS re2 EXPORT re2Config ARCHIVE DESTINATION lib LIBRARY DESTINATION lib RUNTIME DESTINATION bin INCLUDES DESTINATION include)
install(EXPORT re2Config DESTINATION lib/cmake/re2 NAMESPACE re2::)""")

        tools.replace_in_file("re2-%s/util/stringprintf.cc" % self.version,
"""#include "util/util.h"
""",
"""#include "util/util.h"
#define va_copy(dest, src) (dest = src)
""")

    def build(self):
        cmake = CMake(self)
        cmake.configure(defs={
                "CMAKE_INSTALL_PREFIX": self.package_folder,
                "BUILD_SHARED_LIBS": "ON" if self.options.shared else "OFF",
                "BUILD_TESTING": "OFF",
                "CMAKE_CXX_FLAGS": "-fPIC" if ("fPIC" in self.options.fields and self.options.fPIC == True) else "",
            }, source_dir="re2-%s" % self.version)
        cmake.build(target="install")

    def package_info(self):
        self.cpp_info.libs = ["re2"]
