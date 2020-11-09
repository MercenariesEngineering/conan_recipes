from conans import ConanFile
from conans import tools

class wxConan(ConanFile):
    name = "wx"
    version = "guerillaBinaries_2.8.8"
    settings = "os", "compiler", "build_type", "arch"
    description = "Cross-platform GUI Library"
    url = "https://www.wxwidgets.org/"
    license = "None"

    def package(self):
        self.run("rm -Rf include lib")
        self.run("mkdir include lib")

        if self.settings.os == "Windows" :
            src_path = "X:\\Dev\\GuerillaLibs2015\\"

            self.run("mkdir lib\\x64\\%s\\wx" % self.settings.build_type)
            self.run("cp -R %s\\contrib\\wx-2.8.8\\lib\\x64\\%s\\wx\\setup.h lib\\x64\\%s\\wx\\" % (src_path, self.settings.build_type, self.settings.build_type))

            includes = ["\\contrib\\wx-2.8.8\\include\\wx"]
            libs = [
                "lib\\x64\\%s\\wxbase28.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxbase28_net.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxbase28_odbc.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxbase28_xml.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxexpat.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxmsw28_adv.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxmsw28_aui.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxmsw28_core.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxmsw28_dbgrid.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxmsw28_gl.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxmsw28_html.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxmsw28_media.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxmsw28_qa.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxmsw28_richtext.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxmsw28_stc.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxmsw28_xrc.lib" % self.settings.build_type,
                "lib\\x64\\%s\\wxregex.lib" % self.settings.build_type]
        elif self.settings.os == "Linux" :
            src_path = "/usr/local/toolchain/extra/"
            includes = [
                "include/wx"]
            libs = [
                "lib/libwx_baseu_net-2.8.a",
                "lib/libwx_baseu_xml-2.8.a",
                "lib/libwx_baseu-2.8.a",
                "lib/libwx_gtk2u_adv-2.8.a",
                "lib/libwx_gtk2u_aui-2.8.a",
                "lib/libwx_gtk2u_core-2.8.a",
                "lib/libwx_gtk2u_fl-2.8.a",
                "lib/libwx_gtk2u_gizmos-2.8.a",
                "lib/libwx_gtk2u_gl-2.8.a",
                "lib/libwx_gtk2u_html-2.8.a",
                "lib/libwx_gtk2u_ogl-2.8.a",
                "lib/libwx_gtk2u_plot-2.8.a",
                "lib/libwx_gtk2u_qa-2.8.a",
                "lib/libwx_gtk2u_richtext-2.8.a",
                "lib/libwx_gtk2u_stc-2.8.a",
                "lib/libwxregexu-2.8.a"]

        for path in includes:
            self.run("cp -R %s%s include/" % (src_path, path))

        for path in libs:
            self.run("cp -R %s%s lib/" % (src_path, path))

        self.copy("*.h", keep_path=True)
        self.copy("*.lib")
        self.copy("*.a")
        self.copy("*.pdb") # seems ignored on current conan version

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
