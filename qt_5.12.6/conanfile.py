"""Below is the output of ./configure --help
############################################
Usage:  configure [options] [assignments]

Configure understands variable assignments like VAR=value on the command line.
Each uppercased library name (obtainable with -list-libraries) supports the
suffixes _INCDIR, _LIBDIR, _PREFIX (INCDIR=PREFIX/include, LIBDIR=PREFIX/lib),
_LIBS, and - on Windows and Darwin - _LIBS_DEBUG and _LIBS_RELEASE. E.g.,
ICU_PREFIX=/opt/icu42 ICU_LIBS="-licui18n -licuuc -licudata".

It is also possible to manipulate any QMAKE_* variable, to amend the values
from the mkspec for the build of Qt itself, e.g., QMAKE_CXXFLAGS+=-g3.

Note that the *_LIBS* and QMAKE_* assignments manipulate lists, so items
containing meta characters (spaces in particular) need to be quoted according
to qmake rules. On top of that, the assignments as a whole need to be quoted
according to shell rules. It is recommended to use single quotes for the inner
quoting and double quotes for the outer quoting.

Top-level installation directories:
  -prefix <dir> ...... The deployment directory, as seen on the target device.
                       [/usr/local/Qt-$QT_VERSION; qtbase build directory if
                       -developer-build]
  -extprefix <dir> ... The installation directory, as seen on the host machine.
                       [SYSROOT/PREFIX]
  -hostprefix [dir] .. The installation directory for build tools running on
                       the host machine. If [dir] is not given, the current
                       build directory will be used. [EXTPREFIX]
  -external-hostbindir <path> ... Path to Qt tools built for this machine.
                       Use this when -platform does not match the current
                       system, i.e., to make a Canadian Cross Build.

Fine tuning of installation directory layout. Note that all directories
except -sysconfdir should be located under -prefix/-hostprefix:

  -bindir <dir> ......... Executables [PREFIX/bin]
  -headerdir <dir> ...... Header files [PREFIX/include]
  -libdir <dir> ......... Libraries [PREFIX/lib]
  -archdatadir <dir> .... Arch-dependent data [PREFIX]
  -plugindir <dir> ...... Plugins [ARCHDATADIR/plugins]
  -libexecdir <dir> ..... Helper programs [ARCHDATADIR/bin on Windows,
                          ARCHDATADIR/libexec otherwise]
  -importdir <dir> ...... QML1 imports [ARCHDATADIR/imports]
  -qmldir <dir> ......... QML2 imports [ARCHDATADIR/qml]
  -datadir <dir> ........ Arch-independent data [PREFIX]
  -docdir <dir> ......... Documentation [DATADIR/doc]
  -translationdir <dir> . Translations [DATADIR/translations]
  -sysconfdir <dir> ..... Settings used by Qt programs [PREFIX/etc/xdg]
  -examplesdir <dir> .... Examples [PREFIX/examples]
  -testsdir <dir> ....... Tests [PREFIX/tests]

  -hostbindir <dir> ..... Host executables [HOSTPREFIX/bin]
  -hostlibdir <dir> ..... Host libraries [HOSTPREFIX/lib]
  -hostdatadir <dir> .... Data used by qmake [HOSTPREFIX]

Conventions for the remaining options: When an option's description is
followed by a list of values in brackets, the interpretation is as follows:
'yes' represents the bare option; all other values are possible prefixes to
the option, e.g., -no-gui. Alternatively, the value can be assigned, e.g.,
--gui=yes. Values are listed in the order they are tried if not specified;
'auto' is a shorthand for 'yes/no'. Solitary 'yes' and 'no' represent binary
options without auto-detection.

Configure meta:

  -help, -h ............ Display this help screen
  -verbose, -v ......... Print verbose messages during configuration
  -continue ............ Continue configure despite errors
  -redo ................ Re-configure with previously used options.
                         Additional options may be passed, but will not be
                         saved for later use by -redo.
  -recheck [test,...] .. Discard cached negative configure test results.
                         Use this after installing missing dependencies.
                         Alternatively, if tests are specified, only their
                         results are discarded.
  -recheck-all ......... Discard all cached configure test results.

  -feature-<feature> ... Enable <feature>
  -no-feature-<feature>  Disable <feature> [none]
  -list-features ....... List available features. Note that some features
                         have dedicated command line options as well.

  -list-libraries ...... List possible external dependencies.

Build options:

  -opensource .......... Build the Open-Source Edition of Qt
  -commercial .......... Build the Commercial Edition of Qt
  -confirm-license ..... Automatically acknowledge the license

  -release ............. Build Qt with debugging turned off [yes]
  -debug ............... Build Qt with debugging turned on [no]
  -debug-and-release ... Build two versions of Qt, with and without
                         debugging turned on [yes] (Apple and Windows only)
  -optimize-debug ...... Enable debug-friendly optimizations in debug builds
                         [auto] (Not supported with MSVC or Clang toolchains)
  -optimize-size ....... Optimize release builds for size instead of speed [no]
  -optimized-tools ..... Build optimized host tools even in debug build [no]
  -force-debug-info .... Create symbol files for release builds [no]
  -separate-debug-info . Split off debug information to separate files [no]
  -gdb-index ........... Index the debug info to speed up GDB
                         [no; auto if -developer-build with debug info]
  -strip ............... Strip release binaries of unneeded symbols [yes]
  -gc-binaries ......... Place each function or data item into its own section
                         and enable linker garbage collection of unused
                         sections. [auto for static builds, otherwise no]
  -force-asserts ....... Enable Q_ASSERT even in release builds [no]
  -developer-build ..... Compile and link Qt for developing Qt itself
                         (exports for auto-tests, extra checks, etc.) [no]

  -shared .............. Build shared Qt libraries [yes] (no for UIKit)
  -static .............. Build static Qt libraries [no] (yes for UIKit)
  -framework ........... Build Qt framework bundles [yes] (Apple only)

  -platform <target> ... Select host mkspec [detected]
  -xplatform <target> .. Select target mkspec when cross-compiling [PLATFORM]
  -device <name> ....... Cross-compile for device <name>
  -device-option <key=value> ... Add option for the device mkspec

  -appstore-compliant .. Disable code that is not allowed in platform app stores.
                         This is on by default for platforms which require distribution
                         through an app store by default, in particular Android,
                         iOS, tvOS, watchOS, and Universal Windows Platform. [auto]

  -qtnamespace <name> .. Wrap all Qt library code in 'namespace <name> {...}'.
  -qtlibinfix <infix> .. Rename all libQt5*.so to libQt5*<infix>.so.

  -testcocoon .......... Instrument with the TestCocoon code coverage tool [no]
  -gcov ................ Instrument with the GCov code coverage tool [no]

  -trace [backend] ..... Enable instrumentation with tracepoints.
                         Currently supported backends are 'etw' (Windows) and
                         'lttng' (Linux), or 'yes' for auto-detection. [no]

  -sanitize {address|thread|memory|undefined}
                         Instrument with the specified compiler sanitizer.
                         Note that some sanitizers cannot be combined;
                         for example, -sanitize address cannot be combined with
                         -sanitize thread.

  -c++std <edition> .... Select C++ standard <edition> [c++1z/c++14/c++11]
                         (Not supported with MSVC)

  -sse2 ................ Use SSE2 instructions [auto]
  -sse3/-ssse3/-sse4.1/-sse4.2/-avx/-avx2/-avx512
                         Enable use of particular x86 instructions [auto]
                         Enabled ones are still subject to runtime detection.
  -mips_dsp/-mips_dspr2  Use MIPS DSP/rev2 instructions [auto]

  -qreal <type> ........ typedef qreal to the specified type. [double]
                         Note: this affects binary compatibility.

  -R <string> .......... Add an explicit runtime library path to the Qt
                         libraries. Supports paths relative to LIBDIR.
  -rpath ............... Link Qt libraries and executables using the library
                         install path as a runtime library path. Similar to
                         -R LIBDIR. On Apple platforms, disabling this implies
                         using absolute install names (based in LIBDIR) for
                         dynamic libraries and frameworks. [auto]

  -reduce-exports ...... Reduce amount of exported symbols [auto]
  -reduce-relocations .. Reduce amount of relocations [auto] (Unix only)

  -plugin-manifests .... Embed manifests into plugins [no] (Windows only)
  -static-runtime ...... With -static, use static runtime [no] (Windows only)

  -pch ................. Use precompiled headers [auto]
  -ltcg ................ Use Link Time Code Generation [no]
  -use-gold-linker ..... Use the GNU gold linker [auto]
  -incredibuild-xge .... Use the IncrediBuild XGE [no] (Windows only)
  -ccache .............. Use the ccache compiler cache [no] (Unix only)
  -make-tool <tool> .... Use <tool> to build qmake [nmake] (Windows only)
  -mp .................. Use multiple processors for compilation (MSVC only)

  -warnings-are-errors . Treat warnings as errors [no; yes if -developer-build]
  -silent .............. Reduce the build output so that warnings and errors
                         can be seen more easily

Build environment:

  -sysroot <dir> ....... Set <dir> as the target sysroot
  -gcc-sysroot ......... With -sysroot, pass --sysroot to the compiler [yes]

  -pkg-config .......... Use pkg-config [auto] (Unix only)

  -D <string> .......... Pass additional preprocessor define
  -I <string> .......... Pass additional include path
  -L <string> .......... Pass additional library path
  -F <string> .......... Pass additional framework path (Apple only)

  -sdk <sdk> ........... Build Qt using Apple provided SDK <sdk>. The argument
                         should be one of the available SDKs as listed by
                         'xcodebuild -showsdks'.
                         Note that the argument applies only to Qt libraries
                         and applications built using the target mkspec - not
                         host tools such as qmake, moc, rcc, etc.

  -android-sdk path .... Set Android SDK root path [$ANDROID_SDK_ROOT]
  -android-ndk path .... Set Android NDK root path [$ANDROID_NDK_ROOT]
  -android-ndk-platform  Set Android platform
  -android-ndk-host .... Set Android NDK host (linux-x86, linux-x86_64, etc.)
                         [$ANDROID_NDK_HOST]
  -android-arch ........ Set Android architecture (armeabi, armeabi-v7a,
                         arm64-v8a, x86, x86_64, mips, mips64)
  -android-toolchain-version ... Set Android toolchain version
  -android-style-assets  Automatically extract style assets from the device at
                         run time. This option makes the Android style behave
                         correctly, but also makes the Android platform plugin
                         incompatible with the LGPL2.1. [yes]

Component selection:

  -skip <repo> ......... Exclude an entire repository from the build.
  -make <part> ......... Add <part> to the list of parts to be built.
                         Specifying this option clears the default list first.
                         [libs and examples, also tools if not cross-building,
                         also tests if -developer-build]
  -nomake <part> ....... Exclude <part> from the list of parts to be built.
  -compile-examples .... When unset, install only the sources of examples
                         [no on WebAssembly, otherwise yes]
  -gui ................. Build the Qt GUI module and dependencies [yes]
  -widgets ............. Build the Qt Widgets module and dependencies [yes]
  -no-dbus ............. Do not build the Qt D-Bus module
                         [default on Android and Windows]
  -dbus-linked ......... Build Qt D-Bus and link to libdbus-1 [auto]
  -dbus-runtime ........ Build Qt D-Bus and dynamically load libdbus-1 [no]
  -accessibility ....... Enable accessibility support [yes]
                         Note: Disabling accessibility is not recommended.

Qt comes with bundled copies of some 3rd party libraries. These are used
by default if auto-detection of the respective system library fails.

Core options:

  -doubleconversion .... Select used double conversion library [system/qt/no]
                         No implies use of sscanf_l and snprintf_l (imprecise).
  -glib ................ Enable Glib support [no; auto on Unix]
  -eventfd ............. Enable eventfd support
  -inotify ............. Enable inotify support
  -iconv ............... Enable iconv(3) support [posix/sun/gnu/no] (Unix only)
  -icu ................. Enable ICU support [auto]
  -pcre ................ Select used libpcre2 [system/qt]
  -pps ................. Enable PPS support [auto] (QNX only)
  -zlib ................ Select used zlib [system/qt]

  Logging backends:
    -journald .......... Enable journald support [no] (Unix only)
    -syslog ............ Enable syslog support [no] (Unix only)
    -slog2 ............. Enable slog2 support [auto] (QNX only)

Network options:

  -ssl ................. Enable either SSL support method [auto]
  -no-openssl .......... Do not use OpenSSL [default on Apple and WinRT]
  -openssl-linked ...... Use OpenSSL and link to libssl [no]
  -openssl-runtime ..... Use OpenSSL and dynamically load libssl [auto]
  -securetransport ..... Use SecureTransport [auto] (Apple only)

  -sctp ................ Enable SCTP support [no]

  -libproxy ............ Enable use of libproxy [no]
  -system-proxies ...... Use system network proxies by default [yes]

Gui, printing, widget options:

  -cups ................ Enable CUPS support [auto] (Unix only)

  -fontconfig .......... Enable Fontconfig support [auto] (Unix only)
  -freetype ............ Select used FreeType [system/qt/no]
  -harfbuzz ............ Select used HarfBuzz-NG [system/qt/no]
                         (Not auto-detected on Apple and Windows)

  -gtk ................. Enable GTK platform theme support [auto]

  -lgmon ............... Enable lgmon support [auto] (QNX only)

  -no-opengl ........... Disable OpenGL support
  -opengl <api> ........ Enable OpenGL support. Supported APIs:
                         es2 (default on Windows), desktop (default on Unix),
                         dynamic (Windows only)
  -opengles3 ........... Enable OpenGL ES 3.x support instead of ES 2.x [auto]
  -egl ................. Enable EGL support [auto]
  -angle ............... Use bundled ANGLE to support OpenGL ES 2.0 [auto]
                         (Windows only)
  -combined-angle-lib .. Merge LibEGL and LibGLESv2 into LibANGLE (Windows only)

  -qpa <name> .......... Select default QPA backend(s) (e.g., xcb, cocoa, windows)
                         A prioritized list separated by semi-colons.
  -xcb-xlib............. Enable Xcb-Xlib support [auto]

  Platform backends:
    -direct2d .......... Enable Direct2D support [auto] (Windows only)
    -directfb .......... Enable DirectFB support [no] (Unix only)
    -eglfs ............. Enable EGLFS support [auto; no on Android and Windows]
    -gbm ............... Enable backends for GBM [auto] (Linux only)
    -kms ............... Enable backends for KMS [auto] (Linux only)
    -linuxfb ........... Enable Linux Framebuffer support [auto] (Linux only)
    -mirclient ......... Enable Mir client support [no] (Linux only)
    -xcb ............... Enable X11 support. Select used xcb-* libraries [system/qt/no]
                         (-qt-xcb still uses system version of libxcb itself)

  Input backends:
    -libudev............ Enable udev support [auto]
    -evdev ............. Enable evdev support [auto]
    -imf ............... Enable IMF support [auto] (QNX only)
    -libinput .......... Enable libinput support [auto]
    -mtdev ............. Enable mtdev support [auto]
    -tslib ............. Enable tslib support [auto]
    -xcb-xinput ........ Enable XInput2 support [auto]
    -xkbcommon ......... Enable key mapping support [auto]

  Image formats:
    -gif ............... Enable reading support for GIF [auto]
    -ico ............... Enable support for ICO [yes]
    -libpng ............ Select used libpng [system/qt/no]
    -libjpeg ........... Select used libjpeg [system/qt/no]

Database options:

  -sql-<driver> ........ Enable SQL <driver> plugin. Supported drivers:
                         db2 ibase mysql oci odbc psql sqlite2 sqlite tds
                         [all auto]
  -sqlite .............. Select used sqlite3 [system/qt]

Qt3D options:

  -assimp .............. Select used assimp library [system/qt/no]
  -qt3d-profile-jobs ... Enable jobs profiling [no]
  -qt3d-profile-gl ..... Enable OpenGL profiling [no]
  -qt3d-simd ........... Select level of SIMD support [no/sse2/avx2]
  -qt3d-render ......... Enable the Qt3D Render aspect [yes]
  -qt3d-input .......... Enable the Qt3D Input aspect [yes]
  -qt3d-logic .......... Enable the Qt3D Logic aspect [yes]
  -qt3d-extras ......... Enable the Qt3D Extras aspect [yes]
  -qt3d-animation....... Enable the Qt3D Animation aspect [yes]

Further image format options:

  -jasper .............. Enable JPEG-2000 support using the JasPer library [no]
  -mng ................. Enable MNG support [no]
  -tiff ................ Enable TIFF support [system/qt/no]
  -webp ................ Enable WEBP support [system/qt/no]

Multimedia options:

  -pulseaudio .......... Enable PulseAudio support [auto] (Unix only)
  -alsa ................ Enable ALSA support [auto] (Unix only)
  -no-gstreamer ........ Disable support for GStreamer
  -gstreamer [version] . Enable GStreamer support [auto]
                         With no parameter, 1.0 is tried first, then 0.10.
  -mediaplayer-backend <name> ... Select media player backend (Windows only)
                                  Supported backends: directshow (default), wmf
  -evr ................. Enables EVR in DirectShow and WMF [auto]

WebEngine options:

  -webengine-alsa ................ Enable ALSA support [auto] (Linux only)
  -webengine-pulseaudio .......... Enable PulseAudio support [auto]
                                   (Linux only)
  -webengine-embedded-build ...... Enable Linux embedded build [auto]
                                   (Linux only)
  -webengine-icu ................. Use system ICU libraries [system/qt]
                                   (Linux only)
  -webengine-ffmpeg .............. Use system FFmpeg libraries [system/qt]
                                   (Linux only)
  -webengine-opus ................ Use system Opus libraries [system/qt]
                                   (Linux only)
  -webengine-webp ................ Use system WebP libraries [system/qt]
                                   (Linux only)
  -webengine-pepper-plugins ...... Enable use of Pepper Flash and Widevine
                                   plugins [auto]
  -webengine-printing-and-pdf .... Enable use of printing and output to PDF
                                   [auto]
  -webengine-proprietary-codecs .. Enable support for proprietary codecs [no]
  -webengine-spellchecker ........ Enable support for spellchecker [yes]
  -webengine-native-spellchecker . Enable support for native spellchecker [no]
                                   (macOS only)
  -webengine-webrtc .............. Enable support for WebRTC [auto]"""


"""
Build configuration for linux
=============================
Build type: linux-g++ (x86_64, CPU features: mmx sse sse2)
Compiler: gcc 9.3.0
Configuration: use_gold_linker sse2 aesni sse3 ssse3 sse4_1 sse4_2 avx avx2 avx512f avx512bw avx512cd avx512dq avx512er avx512ifma avx512pf avx512vbmi avx512vl compile_examples enable_new_dtags f16c largefile ltcg precompile_header rdrnd shani silent x86SimdAlways shared rpath release c++11 c++14 c++1z concurrent dbus reduce_exports reduce_relocations stl
Build options:
  Mode ................................... release
  Optimize release build for size ........ no
  Building shared libraries .............. yes
  Using C standard ....................... C11
  Using C++ standard ..................... C++1z
  Using ccache ........................... no
  Using gold linker ...................... yes
  Using new DTAGS ........................ yes
  Using precompiled headers .............. yes
  Using LTCG ............................. yes
  Target compiler supports:
    SSE .................................. SSE2 SSE3 SSSE3 SSE4.1 SSE4.2
    AVX .................................. AVX AVX2
    AVX512 ............................... F ER CD PF DQ BW VL IFMA VBMI
    Other x86 ............................ AES F16C RDRAND SHA
    Intrinsics without -mXXX option ...... yes
  Build parts ............................ libs tools
Qt modules and options:
  Qt Concurrent .......................... yes
  Qt D-Bus ............................... yes
  Qt D-Bus directly linked to libdbus .... no
  Qt Gui ................................. yes
  Qt Network ............................. yes
  Qt Sql ................................. yes
  Qt Testlib ............................. yes
  Qt Widgets ............................. yes
  Qt Xml ................................. yes
Support enabled for:
  Using pkg-config ....................... yes
  udev ................................... no
  Using system zlib ...................... yes
Qt Core:
  DoubleConversion ....................... yes
    Using system DoubleConversion ........ yes
  GLib ................................... no
  iconv .................................. no
  ICU .................................... yes
  Tracing backend ........................ <none>
  Logging backends:
    journald ............................. no
    syslog ............................... no
    slog2 ................................ no
  Using system PCRE2 ..................... yes
Qt Network:
  getifaddrs() ........................... yes
  IPv6 ifname ............................ yes
  libproxy ............................... no
  Linux AF_NETLINK ....................... yes
  OpenSSL ................................ yes
    Qt directly linked to OpenSSL ........ yes
  OpenSSL 1.1 ............................ yes
  DTLS ................................... yes
  SCTP ................................... no
  Use system proxies ..................... yes
Qt Gui:
  Accessibility .......................... yes
  FreeType ............................... yes
    Using system FreeType ................ yes
  HarfBuzz ............................... yes
    Using system HarfBuzz ................ yes
  Fontconfig ............................. no
  Image formats:
    GIF .................................. yes
    ICO .................................. yes
    JPEG ................................. yes
      Using system libjpeg ............... yes
    PNG .................................. yes
      Using system libpng ................ yes
  EGL .................................... no
  OpenVG ................................. no
  OpenGL:
    Desktop OpenGL ....................... yes
    OpenGL ES 2.0 ........................ no
    OpenGL ES 3.0 ........................ no
    OpenGL ES 3.1 ........................ no
    OpenGL ES 3.2 ........................ no
  Vulkan ................................. no
  Session Management ..................... yes
Features used by QPA backends:
  evdev .................................. yes
  libinput ............................... no
  INTEGRITY HID .......................... no
  mtdev .................................. no
  tslib .................................. no
  xkbcommon .............................. yes
  X11 specific:
    XLib ................................. yes
    XCB Xlib ............................. yes
    EGL on X11 ........................... no
QPA backends:
  DirectFB ............................... no
  EGLFS .................................. no
  LinuxFB ................................ yes
  VNC .................................... yes
  Mir client ............................. no
  XCB:
    Using system-provided XCB libraries .. no
    XCB XKB .............................. yes
    XCB XInput ........................... yes
    Native painting (experimental) ....... no
    GL integrations:
      GLX Plugin ......................... yes
        XCB GLX .......................... yes
      EGL-X11 Plugin ..................... no
Qt Sql:
  SQL item models ........................ yes
Qt Widgets:
  GTK+ ................................... no
  Styles ................................. Fusion Windows
Qt PrintSupport:
  CUPS ................................... no
Qt Sql Drivers:
  DB2 (IBM) .............................. no
  InterBase .............................. no
  MySql .................................. no
  OCI (Oracle) ........................... no
  ODBC ................................... no
  PostgreSQL ............................. no
  SQLite2 ................................ no
  SQLite ................................. yes
    Using system provided SQLite ......... yes
  TDS (Sybase) ........................... no
Qt Testlib:
  Tester for item models ................. yes
Qt SerialBus:
  Socket CAN ............................. yes
  Socket CAN FD .......................... yes
Further Image Formats:
  JasPer ................................. no
  MNG .................................... no
  TIFF ................................... yes
    Using system libtiff ................. no
  WEBP ................................... yes
    Using system libwebp ................. no
Qt QML:
  QML network support .................... yes
  QML debugging and profiling support .... yes
  QML sequence object .................... yes
  QML list model ......................... yes
  QML XML http request ................... yes
  QML Locale ............................. yes
  QML delegate model ..................... yes
Qt Quick:
  Direct3D 12 ............................ no
  AnimatedImage item ..................... yes
  Canvas item ............................ yes
  Support for Qt Quick Designer .......... yes
  Flipable item .......................... yes
  GridView item .......................... yes
  ListView item .......................... yes
  TableView item ......................... yes
  Path support ........................... yes
  PathView item .......................... yes
  Positioner items ....................... yes
  Repeater item .......................... yes
  ShaderEffect item ...................... yes
  Sprite item ............................ yes
Qt Scxml:
  ECMAScript data model for QtScxml ...... yes
Qt Gamepad:
  SDL2 ................................... no
Qt 3D:
  Assimp ................................. yes
  System Assimp .......................... no
  Output Qt3D Job traces ................. no
  Output Qt3D GL traces .................. no
  Use SSE2 instructions .................. yes
  Use AVX2 instructions .................. no
  Aspects:
    Render aspect ........................ yes
    Input aspect ......................... yes
    Logic aspect ......................... yes
    Animation aspect ..................... yes
    Extras aspect ........................ yes
Qt 3D Renderers:
  OpenGL Renderer ........................ yes
Qt 3D GeometryLoaders:
  Autodesk FBX ........................... no
Qt Wayland Client ........................ no
Qt Wayland Compositor .................... no
Qt Bluetooth:
  BlueZ .................................. no
  BlueZ Low Energy ....................... no
  Linux Crypto API ....................... no
  WinRT Bluetooth API (desktop & UWP) .... no
Qt Sensors:
  sensorfw ............................... no
Qt Quick Controls 2:
  Styles ................................. Default Fusion Imagine Material Universal
Qt Quick Templates 2:
  Hover support .......................... yes
  Multi-touch support .................... yes
Qt Positioning:
  Gypsy GPS Daemon ....................... no
  WinRT Geolocation API .................. no
Qt Location:
  Qt.labs.location experimental QML plugin . yes
  Geoservice plugins:
    OpenStreetMap ........................ yes
    HERE ................................. yes
    Esri ................................. yes
    Mapbox ............................... yes
    MapboxGL ............................. yes
    Itemsoverlay ......................... yes
QtXmlPatterns:
  XML schema support ..................... yes
Qt Multimedia:
  ALSA ................................... yes
  GStreamer 1.0 .......................... no
  GStreamer 0.10 ......................... no
  Video for Linux ........................ yes
  OpenAL ................................. no
  PulseAudio ............................. no
  Resource Policy (libresourceqt5) ....... no
  Windows Audio Services ................. no
  DirectShow ............................. no
  Windows Media Foundation ............... no
Qt Tools:
  QDoc ................................... no
Qt WebEngine:
  Embedded build ......................... no
  Full debug information ................. no
  Pepper Plugins ......................... yes
  Printing and PDF ....................... yes
  Proprietary Codecs ..................... no
  Spellchecker ........................... yes
  Native Spellchecker .................... no
  WebRTC ................................. yes
  Use System Ninja ....................... no
  Geolocation ............................ yes
  WebChannel support ..................... yes
  Use v8 snapshot ........................ yes
  Kerberos Authentication ................ no
  Support qpa-xcb ........................ yes
  Use ALSA ............................... yes
  Use PulseAudio ......................... no
  Optional system libraries used:
    re2 .................................. no
    icu .................................. no
    libwebp, libwebpmux and libwebpdemux . no
    opus ................................. no
    ffmpeg ............................... no
    libvpx ............................... no
    snappy ............................... no
    glib ................................. no
    zlib ................................. yes
    minizip .............................. no
    libevent ............................. no
    jsoncpp .............................. no
    protobuf ............................. no
    libxml2 and libxslt .................. no
    lcms2 ................................ no
    png .................................. yes
    JPEG ................................. yes
    harfbuzz ............................. no
    freetype ............................. yes
  Required system libraries:
    fontconfig ........................... no
    dbus ................................. no
    nss .................................. no
    khr .................................. yes
    glibc ................................ yes
  Required system libraries for qpa-xcb:
    x11 .................................. yes
    libdrm ............................... yes
    xcomposite ........................... yes
    xcursor .............................. yes
    xi ................................... yes
    xtst ................................. yes

Note: Disabling X11 Accessibility Bridge: D-Bus or AT-SPI is missing.

Note: No wayland-egl support detected. Cross-toolkit compatibility disabled.

WARNING: QDoc will not be compiled, probably because libclang could not be located. This means that you cannot build the Qt documentation.
"""

import os
import shutil
import itertools

import configparser
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
from conans.model import Generator
from conans.tools import Version


class qt(Generator):
    @property
    def filename(self):
        return "qt.conf"

    @property
    def content(self):
        return "[Paths]\nPrefix = %s\n" % self.conanfile.deps_cpp_info["qt"].rootpath.replace("\\", "/")


def _getsubmodules():
    config = configparser.ConfigParser()
    config.read('qtmodules.conf')
    res = {}
    assert config.sections()
    for s in config.sections():
        section = str(s)
        assert section.startswith("submodule ")
        assert section.count('"') == 2
        modulename = section[section.find('"') + 1: section.rfind('"')]
        status = str(config.get(section, "status"))
        if status != "obsolete" and status != "ignore":
            res[modulename] = {"branch": str(config.get(section, "branch")), "status": status,
                               "path": str(config.get(section, "path")), "depends": []}
            if config.has_option(section, "depends"):
                res[modulename]["depends"] = [str(i) for i in config.get(section, "depends").split()]
    return res


class QtConan(ConanFile):

    _submodules = _getsubmodules()

    generators = "pkg_config"
    name = "qt"
    description = "Qt is a cross-platform framework for graphical user interfaces."
    topics = ("conan", "qt", "ui")
    url = "https://github.com/bincrafters/conan-qt"
    homepage = "https://www.qt.io"
    license = "LGPL-3.0"
    author = "Bincrafters <bincrafters@gmail.com>"
    exports = ["LICENSE.md", "qtmodules.conf", "*.diff"]
    settings = "os", "arch", "compiler", "build_type"

    options = dict({
        "shared": [True, False],
        "commercial": [True, False],

        "opengl": ["no", "es2", "desktop", "dynamic"],
        "openssl": [True, False],
        "with_pcre2": [True, False],
        "with_glib": [True, False],
        "with_doubleconversion": [True, False],
        "with_freetype": [True, False],
        "with_fontconfig": [True, False],
        "with_icu": [True, False],
        "with_harfbuzz": [True, False],
        "with_libjpeg": [True, False],
        "with_libpng": [True, False],
        "with_sqlite3": [True, False],
        "with_mysql": [True, False],
        "with_pq": [True, False],
        "with_odbc": [True, False],
        "with_sdl2": [True, False],
        "with_libalsa": [True, False],
        "with_openal": [True, False],

        "GUI": [True, False],
        "widgets": [True, False],

        "tests": [True, False],
        "examples": [True, False],

        "ltcg": [True, False],
        "device": "ANY",
        "cross_compile": "ANY",
        "sysroot": "ANY",
        "config": "ANY",
        "multiconfiguration": [True, False],
    }, **{module: [True, False] for module in _submodules if module != 'qtbase'}
    )
    no_copy_source = True
    default_options = dict({
        "shared": True,
        "commercial": False,
        "opengl": "desktop",
        "openssl": True,
        "with_pcre2": True,
        "with_glib": False,
        "with_doubleconversion": True,
        "with_freetype": True,
        "with_fontconfig": False,
        "with_icu": True,
        "with_harfbuzz": True,
        "with_libjpeg": True,
        "with_libpng": True,
        "with_sqlite3": True,
        "with_mysql": False,
        "with_pq": False,
        "with_odbc": False,
        "with_sdl2": False,
        "with_libalsa": True,
        "with_openal": True,

        "GUI": True,
        "widgets": True,

        "tests": False,
        "examples": False,

        "ltcg": False, # not really supported everywhere, so turn it off
        "device": None,
        "cross_compile": "/usr/bin/",
        "sysroot": None,
        "config": None,
        "multiconfiguration": False,
    }, **{module: not module in ["qtdoc", "qtwebengine"] for module in _submodules if module != 'qtbase'}
    )
    short_paths = True

    def _system_package_architecture(self):
        if tools.os_info.with_apt:
            if self.settings.arch == "x86":
                return ':i386'
            elif self.settings.arch == "x86_64":
                return ':amd64'
            elif self.settings.arch == "armv6" or self.settings.arch == "armv7":
                return ':armel'
            elif self.settings.arch == "armv7hf":
                return ':armhf'
            elif self.settings.arch == "armv8":
                return ':arm64'

        if tools.os_info.with_yum:
            if self.settings.arch == "x86":
                return '.i686'
            elif self.settings.arch == 'x86_64':
                return '.x86_64'
        return ""

    def build_requirements(self):
        if tools.os_info.is_windows and self.settings.compiler == "Visual Studio":
            self.build_requires("jom_installer/1.1.2@bincrafters/stable")
        if self.settings.os == 'Linux':
            if not tools.which('pkg-config'):
                self.build_requires('pkg-config_installer/0.29.2@bincrafters/stable')
            if self.options.with_libalsa:
                self.build_requires("libalsa/1.2.2@mercseng/version-0")

    def config_options(self):
        if self.settings.os != "Linux":
            self.options.with_icu = False

    def configure(self):
        if self.settings.os != 'Linux':
            self.options.with_glib = False
            self.options.with_fontconfig = False
        if self.settings.compiler == "gcc" and Version(self.settings.compiler.version.value) < "5.3":
            self.options.with_mysql = False
        if self.settings.os == "Windows":
            self.options.with_mysql = False
            if not self.options.shared and self.options.with_icu:
                raise ConanInvalidConfiguration("icu option is not supported on windows in static build. see QTBUG-77120.")

        if self.options.widgets and not self.options.GUI:
            raise ConanInvalidConfiguration("using option qt:widgets without option qt:GUI is not possible. "
                                            "You can either disable qt:widgets or enable qt:GUI")
        if not self.options.GUI:
            self.options.opengl = "no"
            self.options.with_freetype = False
            self.options.with_fontconfig = False
            self.options.with_harfbuzz = False
            self.options.with_libjpeg = False
            self.options.with_libpng = False

        # MercsEng: We use a shared freetype/harfbuzz recipe
        self.options.with_harfbuzz = self.options.with_freetype

        if not self.options.qtgamepad:
            self.options.with_sdl2 = False

        if not self.options.qtmultimedia:
            self.options.with_libalsa = False
            self.options.with_openal = False

        if self.settings.os != "Linux":
            self.options.with_libalsa = False

        if self.settings.os == "Android" and self.options.opengl == "desktop":
            raise ConanInvalidConfiguration("OpenGL desktop is not supported on Android. Consider using OpenGL es2")

        if self.settings.os != "Windows" and self.options.opengl == "dynamic":
            raise ConanInvalidConfiguration("Dynamic OpenGL is supported only on Windows.")

        if self.options.with_fontconfig and not self.options.with_freetype:
            raise ConanInvalidConfiguration("with_fontconfig cannot be enabled if with_freetype is disabled.")

        if self.settings.os == "Macos":
            del self.settings.os.version

        if self.options.multiconfiguration:
            del self.settings.build_type

        if not self.options.with_doubleconversion and str(self.settings.compiler.libcxx) != "libc++":
            raise ConanInvalidConfiguration('Qt without libc++ needs qt:with_doubleconversion. '
                                            'Either enable qt:with_doubleconversion or switch to libc++')

        assert self.version == self._submodules['qtbase']['branch']

        def _enablemodule(mod):
            if mod != 'qtbase':
                setattr(self.options, mod, True)
            for req in self._submodules[mod]["depends"]:
                _enablemodule(req)

        for module in self._submodules:
            if module != 'qtbase' and getattr(self.options, module):
                _enablemodule(module)

        if self.options.with_libalsa and self.settings.os == "Linux":
            self.options["libalsa"].shared = True

    def requirements(self):
        self.requires("zlib/1.2.11@mercseng/version-0")

        if self.options.openssl:
            self.requires("OpenSSL/1.1.1g@mercseng/version-0")

        if self.options.with_pcre2:
            self.requires("pcre2/10.33@mercseng/version-0")

        if self.options.with_freetype and not self.options.multiconfiguration:
            self.requires("freetype/2.10.2_with_Harfbuzz@mercseng/version-0")

        if self.options.with_icu:
            self.requires("icu/64.2@mercseng/version-0")

        if self.options.with_libjpeg and not self.options.multiconfiguration:
            self.requires("libjpeg-turbo/1.5.2@mercseng/version-0")

        if self.options.with_libpng and not self.options.multiconfiguration:
            self.requires("libpng/1.6.37@mercseng/version-0")

        if self.options.with_sqlite3 and not self.options.multiconfiguration:
            self.requires("sqlite3/3.32.3@mercseng/version-0")
            self.options["sqlite3"].enable_column_metadata = True

        if self.options.with_libalsa:
            self.requires("libalsa/1.2.2@mercseng/version-0")


        if self.options.with_glib:
            self.requires("glib/2.58.3@bincrafters/stable")

        if self.options.with_doubleconversion and not self.options.multiconfiguration:
            self.requires("double-conversion/3.1.5@mercseng/version-0")

        # if self.options.qtwebengine:
        #     self.requires("gperf/3.1@mercseng/version-0")

        # if self.options.with_fontconfig:
        #     self.requires("fontconfig/2.13.91@conan/stable")
        
        # if self.options.with_mysql:
        #     self.requires("libmysqlclient/8.0.17")

        # if self.options.with_pq:
        #     self.requires("libpq/11.5")

        # if self.options.with_odbc:
        #     if self.settings.os != "Windows":
        #         self.requires("odbc/2.3.7")

        # if self.options.with_sdl2:
        #     self.requires("sdl2/2.0.9@bincrafters/stable")

        # if self.options.with_openal:
        #     self.requires("openal/1.19.0@bincrafters/stable")

        # if self.options.GUI:
        #     if self.settings.os == "Linux" and not tools.cross_building(self.settings, skip_x64_x86=True):
        #         self.requires("xkbcommon/0.8.4@bincrafters/stable")

    # Dangerous to execute this section of code on linux rollback release 
    # def system_requirements(self):
    #     if self.options.GUI:
    #         pack_names = []
    #         if tools.os_info.is_linux:
    #             if tools.os_info.with_apt:
    #                 pack_names = ["libxcb1-dev", "libx11-dev", "libc6-dev"]
    #                 if self.options.opengl == "desktop":
    #                     pack_names.append("libgl1-mesa-dev")
    #                 elif self.options.opengl == "es2":
    #                     pack_names.append("libgles2-mesa-dev")
    #             else:
    #                 if not tools.os_info.linux_distro.startswith(("opensuse", "sles")):
    #                     pack_names = ["libxcb"]
    #                 if not tools.os_info.with_pacman:
    #                     pack_names += ["libxcb-devel", "libX11-devel", "glibc-devel"]
    #                     if self.options.opengl == "desktop":
    #                         if tools.os_info.linux_distro.startswith(("opensuse", "sles")):
    #                             pack_names.append("Mesa-libGL-devel")
    #                         else:
    #                             pack_names.append("mesa-libGL-devel")

    #         if pack_names:
    #             installer = tools.SystemPackageTool()
    #             for item in pack_names:
    #                 installer.install(item + self._system_package_architecture())

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        shutil.move("qt-everywhere-src-%s" % self.version, "qt5")

        for patch in ["cc04651dea4c4678c626cb31b3ec8394426e2b25.diff", "99e43db7cea1c838993c151d2d40fc2874a94256.diff"]:
            tools.patch("qt5/qtbase", patch)
        for patch in ["a9cc8aa.diff"]:
            tools.patch("qt5/qtmultimedia", patch)

        # Default mkspec might not find clang (e.g. clang-7, clang-9) :
        if self.settings.compiler == "clang":
            tools.replace_in_file("qt5/qtbase/mkspecs/common/clang.conf",
            """
QMAKE_CC                = $${CROSS_COMPILE}clang
QMAKE_CXX               = $${CROSS_COMPILE}clang++""",
            """
QMAKE_CC                = %s
QMAKE_CXX               = %s""" % (self.env["CC"], self.env["CXX"]))

        if self.settings.os == "Linux":
            # if the host has some newer version of XCB available, Qt libraries will have undefined
            # symbols, because they will be configured with the XCB versions of the host instead of
            # the embeeded XCB versions.
            tools.replace_in_file("qt5/qtbase/src/plugins/platforms/xcb/qxcbbackingstore.cpp",
                """#if (XCB_SHM_MAJOR_VERSION == 1 && XCB_SHM_MINOR_VERSION >= 2) || XCB_SHM_MAJOR_VERSION > 1
#define XCB_USE_SHM_FD
#endif""",
                """#undef XCB_USE_SHM_FD""")


    def _xplatform(self):
        if self.settings.os == "Linux":
            if self.settings.compiler == "gcc":
                return {"x86": "linux-g++-32",
                        "armv6": "linux-arm-gnueabi-g++",
                        "armv7": "linux-arm-gnueabi-g++",
                        "armv7hf": "linux-arm-gnueabi-g++",
                        "armv8": "linux-aarch64-gnu-g++"}.get(str(self.settings.arch), "linux-g++")
            elif self.settings.compiler == "clang":
                if self.settings.arch == "x86":
                    return "linux-clang-libc++-32" if self.settings.compiler.libcxx == "libc++" else "linux-clang-32"
                elif self.settings.arch == "x86_64":
                    return "linux-clang-libc++" if self.settings.compiler.libcxx == "libc++" else "linux-clang"

        elif self.settings.os == "Macos":
            return {"clang": "macx-clang",
                    "apple-clang": "macx-clang",
                    "gcc": "macx-g++"}.get(str(self.settings.compiler))

        elif self.settings.os == "iOS":
            if self.settings.compiler == "apple-clang":
                return "macx-ios-clang"

        elif self.settings.os == "watchOS":
            if self.settings.compiler == "apple-clang":
                return "macx-watchos-clang"

        elif self.settings.os == "tvOS":
            if self.settings.compiler == "apple-clang":
                return "macx-tvos-clang"

        elif self.settings.os == "Android":
            return {"clang": "android-clang",
                    "gcc": "android-g++"}.get(str(self.settings.compiler))

        elif self.settings.os == "Windows":
            return {"Visual Studio": "win32-msvc",
                    "gcc": "win32-g++",
                    "clang": "win32-clang-g++"}.get(str(self.settings.compiler))

        elif self.settings.os == "WindowsStore":
            if self.settings.compiler == "Visual Studio":
                return {"14": {"armv7": "winrt-arm-msvc2015",
                               "x86": "winrt-x86-msvc2015",
                               "x86_64": "winrt-x64-msvc2015"},
                        "15": {"armv7": "winrt-arm-msvc2017",
                               "x86": "winrt-x86-msvc2017",
                               "x86_64": "winrt-x64-msvc2017"}
                        }.get(str(self.settings.compiler.version)).get(str(self.settings.arch))

        elif self.settings.os == "FreeBSD":
            return {"clang": "freebsd-clang",
                    "gcc": "freebsd-g++"}.get(str(self.settings.compiler))

        elif self.settings.os == "SunOS":
            if self.settings.compiler == "sun-cc":
                if self.settings.arch == "sparc":
                    return "solaris-cc-stlport" if self.settings.compiler.libcxx == "libstlport" else "solaris-cc"
                elif self.settings.arch == "sparcv9":
                    return "solaris-cc64-stlport" if self.settings.compiler.libcxx == "libstlport" else "solaris-cc64"
            elif self.settings.compiler == "gcc":
                return {"sparc": "solaris-g++",
                        "sparcv9": "solaris-g++-64"}.get(str(self.settings.arch))
        elif self.settings.os == "Neutrino" and self.settings.compiler == "qcc":
            return {"armv8": "qnx-aarch64le-qcc",
                    "armv8.3": "qnx-aarch64le-qcc",
                    "armv7": "qnx-armle-v7-qcc",
                    "armv7hf": "qnx-armle-v7-qcc",
                    "armv7s": "qnx-armle-v7-qcc",
                    "armv7k": "qnx-armle-v7-qcc",
                    "x86": "qnx-x86-qcc",
                    "x86_64": "qnx-x86-64-qcc"}.get(str(self.settings.arch))

        return None

    def build(self):
        args = ["-confirm-license", "-silent", "-prefix %s" % self.package_folder]
        args += ["-make" if self.options.tests else "-nomake", "tests"]
        args += ["-make" if self.options.examples else "-nomake", "examples"]

        if self.options.ltcg:
            args.append("-ltcg")
        if self.options.commercial:
            args.append("-commercial")
        else:
            args.append("-opensource")
        if not self.options.GUI:
            args.append("-no-gui")
        if not self.options.widgets:
            args.append("-no-widgets")
        if not self.options.shared:
            args.insert(0, "-static")
            if self.settings.compiler == "Visual Studio":
                if self.settings.compiler.runtime == "MT" or self.settings.compiler.runtime == "MTd":
                    args.append("-static-runtime")
        else:
            args.insert(0, "-shared")
        if self.options.multiconfiguration:
            args.append("-debug-and-release")
        elif self.settings.build_type == "Debug":
            args.append("-debug")
        elif self.settings.build_type == "Release":
            args.append("-release")
        elif self.settings.build_type == "RelWithDebInfo":
            args.append("-release")
            args.append("-force-debug-info")
        elif self.settings.build_type == "MinSizeRel":
            args.append("-release")
            args.append("-optimize-size")

        for module in self._submodules:
            if module != 'qtbase' and not getattr(self.options, module) \
                    and os.path.isdir(os.path.join(self.source_folder, 'qt5', self._submodules[module]['path'])):
                args.append("-skip " + module)

        args.append("--zlib=system")

        # openGL
        if self.options.opengl == "no":
            args += ["-no-opengl"]
        elif self.options.opengl == "es2":
            args += ["-opengl es2"]
        elif self.options.opengl == "desktop":
            args += ["-opengl desktop"]
        elif self.options.opengl == "dynamic":
            args += ["-opengl dynamic"]

        # openSSL
        if not self.options.openssl:
            args += ["-no-openssl"]
        else:
            if self.options["openssl"].shared:
                args += ["-openssl-runtime"]
            else:
                args += ["-openssl-linked"]

        args.append("--glib=" + ("yes" if self.options.with_glib else "no"))
        args.append("--pcre=" + ("system" if self.options.with_pcre2 else "qt"))
        args.append("--fontconfig=" + ("yes" if self.options.with_fontconfig else "no"))
        args.append("--icu=" + ("yes" if self.options.with_icu else "no"))
        args.append("--sql-mysql=" + ("yes" if self.options.with_mysql else "no"))
        args.append("--sql-psql=" + ("yes" if self.options.with_pq else "no"))
        args.append("--sql-odbc=" + ("yes" if self.options.with_odbc else "no"))

        if self.options.qtmultimedia:
            args.append("--alsa=" + ("yes" if self.options.with_libalsa else "no"))

        for opt, conf_arg in [
                              ("with_doubleconversion", "doubleconversion"),
                              ("with_freetype", "freetype"),
                              ("with_harfbuzz", "harfbuzz"),
                              ("with_libjpeg", "libjpeg"),
                              ("with_libpng", "libpng"),
                              ("with_sqlite3", "sqlite")]:
            if getattr(self.options, opt):
                if self.options.multiconfiguration:
                    args += ["-qt-" + conf_arg]
                else:
                    args += ["-system-" + conf_arg]
            else:
                args += ["-no-" + conf_arg]

        libmap = [("zlib", "ZLIB"),
                  ("OpenSSL", "OPENSSL"),
                  ("pcre2", "PCRE2"),
                  ("glib", "GLIB"),
                  ("double-conversion", "DOUBLECONVERSION"),
                  ("freetype", "FREETYPE"),
                  ("fontconfig", "FONTCONFIG"),
                  ("icu", "ICU"),
                  ("freetype", "HARFBUZZ"),
                  ("libjpeg-turbo", "LIBJPEG"),
                  ("libpng", "LIBPNG"),
                  ("sqlite3", "SQLITE"),
                  ("libmysqlclient", "MYSQL"),
                  ("libpq", "PSQL"),
                  ("odbc", "ODBC"),
                  ("sdl2", "SDL2"),
                  ("openal", "OPENAL"),
                  ("libalsa", "ALSA")]
        libPaths = []
        for package, var in libmap:
            if package in self.deps_cpp_info.deps:
                if package == 'freetype':
                    args.append("\"%s_INCDIR=%s\"" % (var, self.deps_cpp_info[package].include_paths[-1]))
                #else: # MercsEng: no else, we DO want freetype included like other packages.
                args += ["-I " + s for s in self.deps_cpp_info[package].include_paths]
                
                args += ["-D " + s for s in self.deps_cpp_info[package].defines]

                def _remove_duplicate(l):
                    seen = set()
                    seen_add = seen.add
                    for element in itertools.filterfalse(seen.__contains__, l):
                        seen_add(element)
                        yield element

                def _gather_libs(p):
                    libs = ["-l" + i for i in self.deps_cpp_info[p].libs]
                    if p == "freetype" and not self.options["freetype"].shared and self.settings.os == "Linux":
                        libs += ["-lfreetype"]
                    if self.settings.os in ["Macos", "iOS", "watchOS", "tvOS"]:
                        libs += ["-framework " + i for i in self.deps_cpp_info[p].frameworks]
                    libs += self.deps_cpp_info[p].sharedlinkflags
                    for dep in self.deps_cpp_info[p].public_deps:
                        libs += _gather_libs(dep)
                    return libs

                args.append("\"%s_LIBS=%s\"" % (var, " ".join(_gather_libs(package))))

                def _gather_lib_paths(p):
                    lib_paths = self.deps_cpp_info[p].lib_paths
                    for dep in self.deps_cpp_info[p].public_deps:
                        lib_paths += _gather_lib_paths(dep)
                    return _remove_duplicate(lib_paths)
                libPaths += _gather_lib_paths(package)
        args += ["-L " + s for s in _remove_duplicate(libPaths)]
        
        if 'libmysqlclient' in self.deps_cpp_info.deps:
            args.append("-mysql_config " + os.path.join(self.deps_cpp_info['libmysqlclient'].rootpath, "bin", "mysql_config"))
        if 'libpq' in self.deps_cpp_info.deps:
            args.append("-psql_config " + os.path.join(self.deps_cpp_info['libpq'].rootpath, "bin", "pg_config"))
        if self.settings.os == "Linux":
            if self.options.GUI:
                args.append("-qt-xcb")
        elif self.settings.os == "Macos":
            args += ["-no-framework"]
        elif self.settings.os == "Android":
            args += ["-android-ndk-platform android-%s" % self.settings.os.api_level]
            args += ["-android-arch %s" % {"armv6": "armeabi",
                                           "armv7": "armeabi-v7a",
                                           "armv8": "arm64-v8a",
                                           "x86": "x86",
                                           "x86_64": "x86_64",
                                           "mips": "mips",
                                           "mips64": "mips64"}.get(str(self.settings.arch))]
            # args += ["-android-toolchain-version %s" % self.settings.compiler.version]

        if self.options.sysroot:
            args += ["-sysroot %s" % self.options.sysroot]

        if self.options.device:
            args += ["-device %s" % self.options.device]
            if self.options.cross_compile:
                args += ["-device-option CROSS_COMPILE=%s" % self.options.cross_compile]
        else:
            xplatform_val = self._xplatform()
            if xplatform_val:
                if not tools.cross_building(self.settings, skip_x64_x86=True):
                    args += ["-platform %s" % xplatform_val]
                else:
                    args += ["-xplatform %s" % xplatform_val]
            else:
                self.output.warn("host not supported: %s %s %s %s" %
                                 (self.settings.os, self.settings.compiler,
                                  self.settings.compiler.version, self.settings.arch))

        def _getenvpath(var):
            val = os.getenv(var)
            if val and tools.os_info.is_windows:
                val = val.replace("\\", "/")
                os.environ[var] = val
            return val

        value = _getenvpath('CC')
        if value:
            args += ['QMAKE_CC="' + value + '"',
                     'QMAKE_LINK_C="' + value + '"',
                     'QMAKE_LINK_C_SHLIB="' + value + '"']

        value = _getenvpath('CXX')
        if value:
            args += ['QMAKE_CXX="' + value + '"',
                     'QMAKE_LINK="' + value + '"',
                     'QMAKE_LINK_SHLIB="' + value + '"']

        if tools.os_info.is_linux and self.settings.compiler == "clang":
            args += ['QMAKE_CXXFLAGS+="-ftemplate-depth=1024"']
        
        if self.settings.os != "Windows":
            args += ["-no-d3d12"]

        if self.options.config:
            args.append(str(self.options.config))

        for package in ['xkbcommon', 'glib']:
            if package in self.deps_cpp_info.deps:
                lib_path = self.deps_cpp_info[package].rootpath
                for dirpath, _, filenames in os.walk(lib_path):
                    for filename in filenames:
                        if filename.endswith('.pc'):
                            shutil.copyfile(os.path.join(dirpath, filename), filename)
                            tools.replace_prefix_in_pc_file(filename, lib_path)

        with tools.vcvars(self.settings) if self.settings.compiler == "Visual Studio" else tools.no_op():
            with tools.environment_append({"MAKEFLAGS": "j%d" % tools.cpu_count(), "PKG_CONFIG_PATH": os.getcwd()}):
                try:
                    self.run("%s/qt5/configure %s" % (self.source_folder, " ".join(args)))
                finally:
                    self.output.info(open('config.log', errors='backslashreplace').read())

                if self.settings.compiler == "Visual Studio":
                    make = "jom"
                elif tools.os_info.is_windows:
                    make = "mingw32-make"
                else:
                    make = "make"
                self.run(make, run_environment=True)
                self.run("%s install" % make)

        with open('qtbase/bin/qt.conf', 'w') as f:
            f.write('[Paths]\nPrefix = ..')

    def package(self):
        self.copy("bin/qt.conf", src="qtbase")

    def package_id(self):
        # Backwards compatibility for cross_compile to not affect package_id
        # for people who don't use the `device` option
        self.info.options.cross_compile = None
        del self.info.options.sysroot


    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
        self.env_info.QT_PLUGIN_PATH = os.path.join(self.package_folder, "plugins")
        if self.options.shared:
            if self.settings.os == "Windows":
                self.env_info.PATH.append(os.path.join( self.package_folder, "bin"))
            else:
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))

